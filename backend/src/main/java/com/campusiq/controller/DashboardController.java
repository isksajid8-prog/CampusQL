package com.campusiq.controller;

import com.campusiq.model.*;
import com.campusiq.repository.*;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;

import java.util.*;

@RestController
@RequestMapping("/api")
public class DashboardController {

    private final UserAccountRepository userAccountRepository;
    private final StudentRecordRepository studentRecordRepository;
    private final FacultyAssignmentRepository facultyAssignmentRepository;
    private final AuditLogRepository auditLogRepository;

    public DashboardController(UserAccountRepository userAccountRepository,
                              StudentRecordRepository studentRecordRepository,
                              FacultyAssignmentRepository facultyAssignmentRepository,
                              AuditLogRepository auditLogRepository) {
        this.userAccountRepository = userAccountRepository;
        this.studentRecordRepository = studentRecordRepository;
        this.facultyAssignmentRepository = facultyAssignmentRepository;
        this.auditLogRepository = auditLogRepository;
    }

    @GetMapping("/student/dashboard")
    public ResponseEntity<?> studentDashboard(@AuthenticationPrincipal UserAccount principal) {
        if (principal == null || principal.getRole() != Role.STUDENT) {
            return ResponseEntity.status(403).body(Map.of("message", "Student access only."));
        }

        StudentRecord record = studentRecordRepository.findByStudentId(principal.getStudentId())
                .orElseThrow(() -> new IllegalStateException("Student record missing."));

        Map<String, Object> response = new LinkedHashMap<>();
        response.put("studentId", principal.getStudentId());
        response.put("name", principal.getFullName());
        response.put("department", principal.getDepartment());
        response.put("semester", principal.getSemester());
        response.put("attendancePercentage", record.getAttendancePercentage());
        response.put("cgpa", record.getCgpa());
        response.put("studentSuccessScore", record.getStudentSuccessScore());
        response.put("placementReadiness", record.getPlacementReadiness());
        response.put("backlogCount", record.getBacklogCount());
        response.put("backlogs", record.getBacklogs());
        response.put("subjectMarks", record.getSubjectMarks());
        response.put("subjectAttendance", record.getSubjectAttendance());
        response.put("internalAssessment", record.getInternalAssessment());
        response.put("examResults", record.getExamResults());
        response.put("riskIndicators", record.getRiskIndicators());
        response.put("improvementSuggestions", record.getImprovementSuggestions());
        return ResponseEntity.ok(response);
    }

    @GetMapping("/faculty/overview")
    public ResponseEntity<?> facultyOverview(@AuthenticationPrincipal UserAccount principal) {
        if (principal == null || principal.getRole() != Role.FACULTY) {
            return ResponseEntity.status(403).body(Map.of("message", "Faculty access only."));
        }

        List<String> studentIds = facultyAssignmentRepository.findByFacultyEmail(principal.getEmail())
                .stream().map(FacultyAssignment::getStudentId).toList();

        List<StudentRecord> records = studentRecordRepository.findByStudentIdIn(studentIds);
        return ResponseEntity.ok(Map.of(
            "faculty", principal.getFullName(),
            "assignedStudents", records,
            "auditLog", auditLogRepository.findAllByOrderByCreatedAtDesc().stream().limit(10).toList()
        ));
    }

    @GetMapping("/faculty/students")
    public ResponseEntity<?> facultyStudents(@AuthenticationPrincipal UserAccount principal) {
        if (principal == null || principal.getRole() != Role.FACULTY) {
            return ResponseEntity.status(403).body(Map.of("message", "Faculty access only."));
        }

        List<String> studentIds = facultyAssignmentRepository.findByFacultyEmail(principal.getEmail())
                .stream().map(FacultyAssignment::getStudentId).toList();
        return ResponseEntity.ok(studentRecordRepository.findByStudentIdIn(studentIds));
    }

    @GetMapping("/admin/overview")
    public ResponseEntity<?> adminOverview(@AuthenticationPrincipal UserAccount principal) {
        if (principal == null || principal.getRole() != Role.ADMIN) {
            return ResponseEntity.status(403).body(Map.of("message", "Admin access only."));
        }

        List<StudentRecord> allStudents = studentRecordRepository.findAllByOrderByStudentSuccessScoreDesc();
        List<UserAccount> pendingAccounts = userAccountRepository.findAll().stream()
                .filter(user -> user.getRole() == Role.STUDENT && user.getStatus() == AccountStatus.PENDING)
                .toList();

        return ResponseEntity.ok(Map.of(
            "institutionalSummary", Map.of(
                "totalStudents", allStudents.size(),
                "avgSuccessScore", allStudents.stream().mapToDouble(StudentRecord::getStudentSuccessScore).average().orElse(0.0),
                "pendingRegistrations", pendingAccounts.size()
            ),
            "studentRecords", allStudents,
            "pendingAccounts", pendingAccounts,
            "auditLog", auditLogRepository.findAllByOrderByCreatedAtDesc()
        ));
    }

    @PostMapping("/admin/approve/{studentId}")
    public ResponseEntity<?> approveStudent(@AuthenticationPrincipal UserAccount principal, @PathVariable String studentId) {
        if (principal == null || principal.getRole() != Role.ADMIN) {
            return ResponseEntity.status(403).body(Map.of("message", "Admin access only."));
        }

        UserAccount toApprove = userAccountRepository.findAll().stream()
                .filter(user -> user.getStudentId().equals(studentId))
                .findFirst()
                .orElse(null);

        if (toApprove == null) {
            return ResponseEntity.badRequest().body(Map.of("message", "Student account not found."));
        }

        toApprove.setStatus(AccountStatus.ACTIVE);
        userAccountRepository.save(toApprove);
        auditLogRepository.save(new AuditLog(principal.getEmail(), studentId, "APPROVE_ACCOUNT", "Admin approved account"));
        return ResponseEntity.ok(Map.of("message", "Student account approved.", "studentId", studentId));
    }

    @GetMapping("/dashboard")
    public ResponseEntity<?> dashboard(@AuthenticationPrincipal UserAccount principal) {
        if (principal == null) {
            return ResponseEntity.status(401).body(Map.of("message", "Authentication required."));
        }

        switch (principal.getRole()) {
            case STUDENT -> {
                return studentDashboard(principal);
            }
            case FACULTY -> {
                return facultyOverview(principal);
            }
            case ADMIN -> {
                return adminOverview(principal);
            }
            default -> {
                return ResponseEntity.ok(Map.of("message", "Profile loaded."));
            }
        }
    }
}
