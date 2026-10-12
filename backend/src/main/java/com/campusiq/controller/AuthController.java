package com.campusiq.controller;

import com.campusiq.dto.LoginRequest;
import com.campusiq.dto.RegisterRequest;
import com.campusiq.model.*;
import com.campusiq.repository.*;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpSession;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;
import java.util.Optional;

@RestController
@RequestMapping("/api")
public class AuthController {

    private final AuthenticationManager authenticationManager;
    private final UserAccountRepository userAccountRepository;
    private final StudentRosterEntryRepository rosterEntryRepository;
    private final PasswordEncoder passwordEncoder;

    public AuthController(AuthenticationManager authenticationManager,
                         UserAccountRepository userAccountRepository,
                         StudentRosterEntryRepository rosterEntryRepository,
                         PasswordEncoder passwordEncoder) {
        this.authenticationManager = authenticationManager;
        this.userAccountRepository = userAccountRepository;
        this.rosterEntryRepository = rosterEntryRepository;
        this.passwordEncoder = passwordEncoder;
    }

    @GetMapping("/health")
    public Map<String, String> health() {
        return Map.of("status", "UP");
    }

    @PostMapping("/auth/register")
    public ResponseEntity<?> register(@Valid @RequestBody RegisterRequest request) {
        if (!request.getPassword().equals(request.getConfirmPassword())) {
            return ResponseEntity.badRequest().body(Map.of("message", "Passwords do not match."));
        }

        if (!"true".equalsIgnoreCase(request.getTermsAccepted())) {
            return ResponseEntity.badRequest().body(Map.of("message", "You must accept the terms and conditions."));
        }

        Optional<StudentRosterEntry> rosterEntry = rosterEntryRepository.findByStudentId(request.getStudentId());
        if (rosterEntry.isEmpty()) {
            return ResponseEntity.badRequest().body(Map.of("message", "Student ID is not present in the institutional roster."));
        }

        if (!rosterEntry.get().getEmail().equalsIgnoreCase(request.getEmail())) {
            return ResponseEntity.badRequest().body(Map.of("message", "College email does not match the verified roster."));
        }

        if (userAccountRepository.existsByStudentId(request.getStudentId())) {
            return ResponseEntity.status(HttpStatus.CONFLICT).body(Map.of("message", "This student identity is already linked to an account."));
        }

        if (userAccountRepository.existsByEmail(request.getEmail())) {
            return ResponseEntity.status(HttpStatus.CONFLICT).body(Map.of("message", "This email is already in use."));
        }

        StudentRosterEntry verifiedEntry = rosterEntry.get();
        UserAccount user = new UserAccount();
        user.setEmail(request.getEmail().trim());
        user.setPassword(passwordEncoder.encode(request.getPassword()));
        user.setFullName(request.getFullName().trim());
        user.setStudentId(request.getStudentId());
        user.setRole(Role.STUDENT);
        user.setStatus(AccountStatus.PENDING);
        user.setDepartment(verifiedEntry.getDepartment());
        user.setAcademicYear(verifiedEntry.getAcademicYear());
        user.setSemester(verifiedEntry.getSemester());
        user.setPhone(request.getPhone());
        user.setProfileImage(request.getProfileImage());

        userAccountRepository.save(user);

        return ResponseEntity.ok(Map.of(
            "message", "Registration submitted successfully. Your account is pending administrator approval.",
            "status", "PENDING",
            "role", "STUDENT"
        ));
    }

    @PostMapping("/auth/login")
    public ResponseEntity<?> login(@Valid @RequestBody LoginRequest request, HttpServletRequest httpRequest) {
        try {
            Authentication authentication = authenticationManager.authenticate(
                new UsernamePasswordAuthenticationToken(request.getEmail().trim(), request.getPassword())
            );
            SecurityContextHolder.getContext().setAuthentication(authentication);
            HttpSession session = httpRequest.getSession(true);
            session.setAttribute("SPRING_SECURITY_CONTEXT", SecurityContextHolder.getContext());

            UserAccount account = userAccountRepository.findByEmail(request.getEmail().trim())
                    .orElse(null);
            if (account == null) {
                return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(Map.of("message", "Invalid email or password."));
            }

            if (AccountStatus.PENDING.equals(account.getStatus())) {
                SecurityContextHolder.clearContext();
                return ResponseEntity.status(HttpStatus.LOCKED)
                    .body(Map.of("message", "Your account is pending administrator approval."));
            }

            if (AccountStatus.DISABLED.equals(account.getStatus())) {
                SecurityContextHolder.clearContext();
                return ResponseEntity.status(HttpStatus.FORBIDDEN)
                    .body(Map.of("message", "This account has been disabled."));
            }

            Map<String, Object> response = new HashMap<>();
            response.put("message", "Login successful");
            response.put("email", account.getEmail());
            response.put("role", account.getRole().name());
            response.put("name", account.getFullName());
            response.put("status", account.getStatus().name());
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(Map.of("message", "Invalid email or password."));
        }
    }

    @PostMapping("/auth/logout")
    public ResponseEntity<?> logout(HttpServletRequest request, HttpServletResponse response) {
        SecurityContextHolder.clearContext();
        if (request.getSession(false) != null) {
            request.getSession(false).invalidate();
        }
        return ResponseEntity.ok(Map.of("message", "Logged out successfully."));
    }

    @GetMapping("/auth/me")
    public ResponseEntity<?> currentUser() {
        Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
        if (authentication == null || !authentication.isAuthenticated() || "anonymousUser".equals(authentication.getPrincipal())) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(Map.of("message", "Authentication required."));
        }

        String email = authentication.getName();
        UserAccount account = userAccountRepository.findByEmail(email)
                .orElseThrow(() -> new IllegalStateException("Current user not found."));

        return ResponseEntity.ok(Map.of(
            "email", account.getEmail(),
            "name", account.getFullName(),
            "role", account.getRole().name(),
            "status", account.getStatus().name(),
            "studentId", account.getStudentId(),
            "department", account.getDepartment(),
            "semester", account.getSemester()
        ));
    }

    @GetMapping("/auth/csrf")
    public ResponseEntity<?> csrf() {
        return ResponseEntity.ok(Map.of("message", "CSRF ready"));
    }
}
