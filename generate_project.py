from pathlib import Path

root = Path(r'C:\Users\isksa\OneDrive\Documents\GitHub\CampusQL\backend')
files = {
    'pom.xml': '''<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.3.4</version>
        <relativePath/>
    </parent>

    <groupId>com.campusiq</groupId>
    <artifactId>campusiq-backend</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    <name>campusiq-backend</name>
    <description>CampusIQ secure portal</description>

    <properties>
        <java.version>17</java.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-security</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-jpa</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-validation</artifactId>
        </dependency>
        <dependency>
            <groupId>com.h2database</groupId>
            <artifactId>h2</artifactId>
            <scope>runtime</scope>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>
</project>
''',
    'src/main/java/com/campusiq/CampusiqApplication.java': '''package com.campusiq;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class CampusiqApplication {
    public static void main(String[] args) {
        SpringApplication.run(CampusiqApplication.class, args);
    }
}
''',
    'src/main/java/com/campusiq/model/Role.java': '''package com.campusiq.model;

public enum Role {
    STUDENT,
    FACULTY,
    ADMIN
}
''',
    'src/main/java/com/campusiq/model/AccountStatus.java': '''package com.campusiq.model;

public enum AccountStatus {
    PENDING,
    ACTIVE,
    DISABLED
}
''',
    'src/main/java/com/campusiq/model/UserAccount.java': '''package com.campusiq.model;

import jakarta.persistence.*;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;

import java.util.Collection;
import java.util.List;

@Entity
@Table(name = "user_account", uniqueConstraints = {
        @UniqueConstraint(columnNames = "email"),
        @UniqueConstraint(columnNames = "student_id")
})
public class UserAccount implements UserDetails {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true)
    private String email;

    @Column(nullable = false)
    private String password;

    @Column(nullable = false)
    private String fullName;

    @Column(name = "student_id", nullable = false, unique = true)
    private String studentId;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private Role role = Role.STUDENT;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private AccountStatus status = AccountStatus.PENDING;

    @Column(nullable = false)
    private String department;

    @Column(nullable = false)
    private Integer academicYear;

    @Column(nullable = false)
    private Integer semester;

    private String phone;
    private String profileImage;

    public UserAccount() {
    }

    public UserAccount(String email, String password, String fullName, String studentId, Role role, AccountStatus status,
                       String department, Integer academicYear, Integer semester, String phone, String profileImage) {
        this.email = email;
        this.password = password;
        this.fullName = fullName;
        this.studentId = studentId;
        this.role = role;
        this.status = status;
        this.department = department;
        this.academicYear = academicYear;
        this.semester = semester;
        this.phone = phone;
        this.profileImage = profileImage;
    }

    @Override
    public Collection<? extends GrantedAuthority> getAuthorities() {
        return List.of(new SimpleGrantedAuthority("ROLE_" + this.role.name()));
    }

    @Override
    public String getPassword() {
        return password;
    }

    @Override
    public String getUsername() {
        return email;
    }

    @Override
    public boolean isAccountNonExpired() {
        return true;
    }

    @Override
    public boolean isAccountNonLocked() {
        return status != AccountStatus.DISABLED;
    }

    @Override
    public boolean isCredentialsNonExpired() {
        return true;
    }

    @Override
    public boolean isEnabled() {
        return true;
    }

    public Long getId() {
        return id;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public String getFullName() {
        return fullName;
    }

    public void setFullName(String fullName) {
        this.fullName = fullName;
    }

    public String getStudentId() {
        return studentId;
    }

    public void setStudentId(String studentId) {
        this.studentId = studentId;
    }

    public Role getRole() {
        return role;
    }

    public void setRole(Role role) {
        this.role = role;
    }

    public AccountStatus getStatus() {
        return status;
    }

    public void setStatus(AccountStatus status) {
        this.status = status;
    }

    public String getDepartment() {
        return department;
    }

    public void setDepartment(String department) {
        this.department = department;
    }

    public Integer getAcademicYear() {
        return academicYear;
    }

    public void setAcademicYear(Integer academicYear) {
        this.academicYear = academicYear;
    }

    public Integer getSemester() {
        return semester;
    }

    public void setSemester(Integer semester) {
        this.semester = semester;
    }

    public String getPhone() {
        return phone;
    }

    public void setPhone(String phone) {
        this.phone = phone;
    }

    public String getProfileImage() {
        return profileImage;
    }

    public void setProfileImage(String profileImage) {
        this.profileImage = profileImage;
    }
}
''',
    'src/main/java/com/campusiq/model/StudentRosterEntry.java': '''package com.campusiq.model;

import jakarta.persistence.*;

@Entity
@Table(name = "student_roster_entry", uniqueConstraints = {
        @UniqueConstraint(columnNames = "student_id"),
        @UniqueConstraint(columnNames = "email")
})
public class StudentRosterEntry {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "student_id", nullable = false, unique = true)
    private String studentId;

    @Column(nullable = false)
    private String fullName;

    @Column(nullable = false, unique = true)
    private String email;

    @Column(nullable = false)
    private String department;

    @Column(nullable = false)
    private Integer academicYear;

    @Column(nullable = false)
    private Integer semester;

    public StudentRosterEntry() {
    }

    public StudentRosterEntry(String studentId, String fullName, String email, String department, Integer academicYear, Integer semester) {
        this.studentId = studentId;
        this.fullName = fullName;
        this.email = email;
        this.department = department;
        this.academicYear = academicYear;
        this.semester = semester;
    }

    public Long getId() {
        return id;
    }

    public String getStudentId() {
        return studentId;
    }

    public String getFullName() {
        return fullName;
    }

    public void setFullName(String fullName) {
        this.fullName = fullName;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getDepartment() {
        return department;
    }

    public void setDepartment(String department) {
        this.department = department;
    }

    public Integer getAcademicYear() {
        return academicYear;
    }

    public void setAcademicYear(Integer academicYear) {
        this.academicYear = academicYear;
    }

    public Integer getSemester() {
        return semester;
    }

    public void setSemester(Integer semester) {
        this.semester = semester;
    }
}
''',
    'src/main/java/com/campusiq/model/StudentRecord.java': '''package com.campusiq.model;

import jakarta.persistence.*;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Entity
@Table(name = "student_record", uniqueConstraints = {
        @UniqueConstraint(columnNames = "student_id")
})
public class StudentRecord {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "student_id", nullable = false, unique = true)
    private String studentId;

    @Column(nullable = false)
    private String fullName;

    @Column(nullable = false)
    private String email;

    @Column(nullable = false)
    private String department;

    @Column(nullable = false)
    private Integer academicYear;

    @Column(nullable = false)
    private Integer semester;

    @Column(nullable = false)
    private Double attendancePercentage;

    @Column(nullable = false)
    private Double cgpa;

    @Column(nullable = false)
    private Integer backlogCount;

    @Column(nullable = false)
    private Double studentSuccessScore;

    @Column(nullable = false)
    private String placementReadiness;

    @ElementCollection(fetch = FetchType.EAGER)
    @CollectionTable(name = "student_subject_marks", joinColumns = @JoinColumn(name = "student_id"))
    @MapKeyColumn(name = "subject_name")
    @Column(name = "mark")
    private Map<String, Integer> subjectMarks = new HashMap<>();

    @ElementCollection(fetch = FetchType.EAGER)
    @CollectionTable(name = "student_attendance_by_subject", joinColumns = @JoinColumn(name = "student_id"))
    @MapKeyColumn(name = "subject_name")
    @Column(name = "attendance")
    private Map<String, Integer> subjectAttendance = new HashMap<>();

    @ElementCollection(fetch = FetchType.EAGER)
    @CollectionTable(name = "student_internal_marks", joinColumns = @JoinColumn(name = "student_id"))
    @MapKeyColumn(name = "assessment_name")
    @Column(name = "mark")
    private Map<String, Integer> internalAssessment = new HashMap<>();

    @ElementCollection(fetch = FetchType.EAGER)
    @CollectionTable(name = "student_exam_results", joinColumns = @JoinColumn(name = "student_id"))
    @MapKeyColumn(name = "exam_name")
    @Column(name = "score")
    private Map<String, Integer> examResults = new HashMap<>();

    @ElementCollection(fetch = FetchType.EAGER)
    @CollectionTable(name = "student_backlogs", joinColumns = @JoinColumn(name = "student_id"))
    @Column(name = "backlog")
    private List<String> backlogs = new ArrayList<>();

    @ElementCollection(fetch = FetchType.EAGER)
    @CollectionTable(name = "student_risk_indicators", joinColumns = @JoinColumn(name = "student_id"))
    @Column(name = "indicator")
    private List<String> riskIndicators = new ArrayList<>();

    @ElementCollection(fetch = FetchType.EAGER)
    @CollectionTable(name = "student_improvement_suggestions", joinColumns = @JoinColumn(name = "student_id"))
    @Column(name = "suggestion")
    private List<String> improvementSuggestions = new ArrayList<>();

    public StudentRecord() {
    }

    public StudentRecord(String studentId, String fullName, String email, String department,
                        Integer academicYear, Integer semester, Double attendancePercentage, Double cgpa,
                        Integer backlogCount, Double studentSuccessScore, String placementReadiness) {
        this.studentId = studentId;
        this.fullName = fullName;
        this.email = email;
        this.department = department;
        this.academicYear = academicYear;
        this.semester = semester;
        this.attendancePercentage = attendancePercentage;
        this.cgpa = cgpa;
        this.backlogCount = backlogCount;
        this.studentSuccessScore = studentSuccessScore;
        this.placementReadiness = placementReadiness;
    }

    public Long getId() {
        return id;
    }

    public String getStudentId() {
        return studentId;
    }

    public void setStudentId(String studentId) {
        this.studentId = studentId;
    }

    public String getFullName() {
        return fullName;
    }

    public void setFullName(String fullName) {
        this.fullName = fullName;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getDepartment() {
        return department;
    }

    public void setDepartment(String department) {
        this.department = department;
    }

    public Integer getAcademicYear() {
        return academicYear;
    }

    public void setAcademicYear(Integer academicYear) {
        this.academicYear = academicYear;
    }

    public Integer getSemester() {
        return semester;
    }

    public void setSemester(Integer semester) {
        this.semester = semester;
    }

    public Double getAttendancePercentage() {
        return attendancePercentage;
    }

    public void setAttendancePercentage(Double attendancePercentage) {
        this.attendancePercentage = attendancePercentage;
    }

    public Double getCgpa() {
        return cgpa;
    }

    public void setCgpa(Double cgpa) {
        this.cgpa = cgpa;
    }

    public Integer getBacklogCount() {
        return backlogCount;
    }

    public void setBacklogCount(Integer backlogCount) {
        this.backlogCount = backlogCount;
    }

    public Double getStudentSuccessScore() {
        return studentSuccessScore;
    }

    public void setStudentSuccessScore(Double studentSuccessScore) {
        this.studentSuccessScore = studentSuccessScore;
    }

    public String getPlacementReadiness() {
        return placementReadiness;
    }

    public void setPlacementReadiness(String placementReadiness) {
        this.placementReadiness = placementReadiness;
    }

    public Map<String, Integer> getSubjectMarks() {
        return subjectMarks;
    }

    public void setSubjectMarks(Map<String, Integer> subjectMarks) {
        this.subjectMarks = subjectMarks;
    }

    public Map<String, Integer> getSubjectAttendance() {
        return subjectAttendance;
    }

    public void setSubjectAttendance(Map<String, Integer> subjectAttendance) {
        this.subjectAttendance = subjectAttendance;
    }

    public Map<String, Integer> getInternalAssessment() {
        return internalAssessment;
    }

    public void setInternalAssessment(Map<String, Integer> internalAssessment) {
        this.internalAssessment = internalAssessment;
    }

    public Map<String, Integer> getExamResults() {
        return examResults;
    }

    public void setExamResults(Map<String, Integer> examResults) {
        this.examResults = examResults;
    }

    public List<String> getBacklogs() {
        return backlogs;
    }

    public void setBacklogs(List<String> backlogs) {
        this.backlogs = backlogs;
    }

    public List<String> getRiskIndicators() {
        return riskIndicators;
    }

    public void setRiskIndicators(List<String> riskIndicators) {
        this.riskIndicators = riskIndicators;
    }

    public List<String> getImprovementSuggestions() {
        return improvementSuggestions;
    }

    public void setImprovementSuggestions(List<String> improvementSuggestions) {
        this.improvementSuggestions = improvementSuggestions;
    }
}
''',
    'src/main/java/com/campusiq/model/FacultyAssignment.java': '''package com.campusiq.model;

import jakarta.persistence.*;

@Entity
@Table(name = "faculty_assignment", uniqueConstraints = {
        @UniqueConstraint(columnNames = {"faculty_email", "student_id"})
})
public class FacultyAssignment {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "faculty_email", nullable = false)
    private String facultyEmail;

    @Column(name = "student_id", nullable = false)
    private String studentId;

    public FacultyAssignment() {
    }

    public FacultyAssignment(String facultyEmail, String studentId) {
        this.facultyEmail = facultyEmail;
        this.studentId = studentId;
    }

    public Long getId() {
        return id;
    }

    public String getFacultyEmail() {
        return facultyEmail;
    }

    public String getStudentId() {
        return studentId;
    }
}
''',
    'src/main/java/com/campusiq/model/AuditLog.java': '''package com.campusiq.model;

import jakarta.persistence.*;

import java.time.LocalDateTime;

@Entity
@Table(name = "audit_log")
public class AuditLog {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String actorEmail;

    @Column(nullable = false)
    private String targetStudentId;

    @Column(nullable = false)
    private String action;

    @Column(nullable = false)
    private String details;

    @Column(nullable = false)
    private LocalDateTime createdAt = LocalDateTime.now();

    public AuditLog() {
    }

    public AuditLog(String actorEmail, String targetStudentId, String action, String details) {
        this.actorEmail = actorEmail;
        this.targetStudentId = targetStudentId;
        this.action = action;
        this.details = details;
    }

    public Long getId() {
        return id;
    }

    public String getActorEmail() {
        return actorEmail;
    }

    public String getTargetStudentId() {
        return targetStudentId;
    }

    public String getAction() {
        return action;
    }

    public String getDetails() {
        return details;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }
}
''',
    'src/main/java/com/campusiq/repository/UserAccountRepository.java': '''package com.campusiq.repository;

import com.campusiq.model.UserAccount;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface UserAccountRepository extends JpaRepository<UserAccount, Long> {
    Optional<UserAccount> findByEmail(String email);
    boolean existsByEmail(String email);
    boolean existsByStudentId(String studentId);
}
''',
    'src/main/java/com/campusiq/repository/StudentRosterEntryRepository.java': '''package com.campusiq.repository;

import com.campusiq.model.StudentRosterEntry;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface StudentRosterEntryRepository extends JpaRepository<StudentRosterEntry, Long> {
    Optional<StudentRosterEntry> findByStudentId(String studentId);
    Optional<StudentRosterEntry> findByEmail(String email);
}
''',
    'src/main/java/com/campusiq/repository/StudentRecordRepository.java': '''package com.campusiq.repository;

import com.campusiq.model.StudentRecord;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.Optional;

public interface StudentRecordRepository extends JpaRepository<StudentRecord, Long> {
    Optional<StudentRecord> findByStudentId(String studentId);
    List<StudentRecord> findByDepartment(String department);
    List<StudentRecord> findAllByOrderByStudentSuccessScoreDesc();
    List<StudentRecord> findByStudentIdIn(List<String> studentIds);
}
''',
    'src/main/java/com/campusiq/repository/FacultyAssignmentRepository.java': '''package com.campusiq.repository;

import com.campusiq.model.FacultyAssignment;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface FacultyAssignmentRepository extends JpaRepository<FacultyAssignment, Long> {
    List<FacultyAssignment> findByFacultyEmail(String facultyEmail);
    boolean existsByFacultyEmailAndStudentId(String facultyEmail, String studentId);
}
''',
    'src/main/java/com/campusiq/repository/AuditLogRepository.java': '''package com.campusiq.repository;

import com.campusiq.model.AuditLog;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface AuditLogRepository extends JpaRepository<AuditLog, Long> {
    List<AuditLog> findAllByOrderByCreatedAtDesc();
    List<AuditLog> findByTargetStudentIdOrderByCreatedAtDesc(String targetStudentId);
}
''',
    'src/main/java/com/campusiq/service/CustomUserDetailsService.java': '''package com.campusiq.service;

import com.campusiq.model.UserAccount;
import com.campusiq.repository.UserAccountRepository;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

@Service
public class CustomUserDetailsService implements UserDetailsService {
    private final UserAccountRepository userAccountRepository;

    public CustomUserDetailsService(UserAccountRepository userAccountRepository) {
        this.userAccountRepository = userAccountRepository;
    }

    @Override
    public UserDetails loadUserByUsername(String email) throws UsernameNotFoundException {
        UserAccount account = userAccountRepository.findByEmail(email)
                .orElseThrow(() -> new UsernameNotFoundException("User not found"));
        return account;
    }
}
''',
    'src/main/java/com/campusiq/config/SecurityConfig.java': '''package com.campusiq.config;

import com.campusiq.service.CustomUserDetailsService;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpMethod;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.dao.DaoAuthenticationProvider;
import org.springframework.security.config.Customizer;
import org.springframework.security.config.annotation.authentication.configuration.AuthenticationConfiguration;
import org.springframework.security.config.annotation.method.configuration.EnableMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configurers.AbstractHttpConfigurer;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.csrf.CookieCsrfTokenRepository;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.CorsConfigurationSource;
import org.springframework.web.cors.UrlBasedCorsConfigurationSource;

import java.util.List;

@Configuration
@EnableMethodSecurity
public class SecurityConfig {

    private final CustomUserDetailsService userDetailsService;

    public SecurityConfig(CustomUserDetailsService userDetailsService) {
        this.userDetailsService = userDetailsService;
    }

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http
            .csrf(csrf -> csrf.csrfTokenRepository(CookieCsrfTokenRepository.withHttpOnlyFalse()))
            .cors(Customizer.withDefaults())
            .sessionManagement(session -> session.sessionCreationPolicy(SessionCreationPolicy.IF_REQUIRED))
            .authorizeHttpRequests(auth -> auth
                .requestMatchers(HttpMethod.OPTIONS, "/**").permitAll()
                .requestMatchers("/", "/index.html", "/styles.css", "/app.js", "/favicon.ico", "/api/health", "/api/auth/register", "/api/auth/login").permitAll()
                .requestMatchers("/api/admin/**").hasRole("ADMIN")
                .requestMatchers("/api/faculty/**").hasRole("FACULTY")
                .requestMatchers("/api/student/**").hasAnyRole("STUDENT", "FACULTY", "ADMIN")
                .requestMatchers("/api/**").authenticated()
                .anyRequest().permitAll()
            )
            .formLogin(AbstractHttpConfigurer::disable)
            .httpBasic(AbstractHttpConfigurer::disable)
            .logout(logout -> logout
                .logoutUrl("/api/auth/logout")
                .invalidateHttpSession(true)
                .deleteCookies("JSESSIONID")
            );

        return http.build();
    }

    @Bean
    public DaoAuthenticationProvider authenticationProvider(PasswordEncoder passwordEncoder) {
        DaoAuthenticationProvider provider = new DaoAuthenticationProvider();
        provider.setUserDetailsService(userDetailsService);
        provider.setPasswordEncoder(passwordEncoder);
        return provider;
    }

    @Bean
    public AuthenticationManager authenticationManager(AuthenticationConfiguration configuration) throws Exception {
        return configuration.getAuthenticationManager();
    }

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }

    @Bean
    CorsConfigurationSource corsConfigurationSource() {
        CorsConfiguration configuration = new CorsConfiguration();
        configuration.setAllowedOrigins(List.of("http://localhost:8080", "http://127.0.0.1:8080", "http://localhost:3000"));
        configuration.setAllowedMethods(List.of("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"));
        configuration.setAllowedHeaders(List.of("Authorization", "Content-Type", "X-XSRF-TOKEN", "X-CSRF-TOKEN"));
        configuration.setAllowCredentials(true);
        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/**", configuration);
        return source;
    }
}
''',
    'src/main/java/com/campusiq/config/DataSeeder.java': '''package com.campusiq.config;

import com.campusiq.model.*;
import com.campusiq.repository.*;
import org.springframework.boot.CommandLineRunner;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;

import java.util.List;
import java.util.Map;

@Component
public class DataSeeder implements CommandLineRunner {

    private final UserAccountRepository userAccountRepository;
    private final StudentRosterEntryRepository rosterEntryRepository;
    private final StudentRecordRepository studentRecordRepository;
    private final FacultyAssignmentRepository facultyAssignmentRepository;
    private final AuditLogRepository auditLogRepository;
    private final PasswordEncoder passwordEncoder;

    public DataSeeder(UserAccountRepository userAccountRepository,
                      StudentRosterEntryRepository rosterEntryRepository,
                      StudentRecordRepository studentRecordRepository,
                      FacultyAssignmentRepository facultyAssignmentRepository,
                      AuditLogRepository auditLogRepository,
                      PasswordEncoder passwordEncoder) {
        this.userAccountRepository = userAccountRepository;
        this.rosterEntryRepository = rosterEntryRepository;
        this.studentRecordRepository = studentRecordRepository;
        this.facultyAssignmentRepository = facultyAssignmentRepository;
        this.auditLogRepository = auditLogRepository;
        this.passwordEncoder = passwordEncoder;
    }

    @Override
    public void run(String... args) {
        if (userAccountRepository.count() == 0) {
            UserAccount admin = new UserAccount(
                "admin@campus.edu",
                passwordEncoder.encode("Campus@123"),
                "Dr. Asha Mehta",
                "ADMIN-001",
                Role.ADMIN,
                AccountStatus.ACTIVE,
                "Academic Office",
                2024,
                1,
                "+91-90000-0001",
                null
            );
            userAccountRepository.save(admin);

            UserAccount faculty = new UserAccount(
                "faculty@campus.edu",
                passwordEncoder.encode("Campus@123"),
                "Prof. Ram Bhatia",
                "FAC-001",
                Role.FACULTY,
                AccountStatus.ACTIVE,
                "Computer Science",
                2024,
                1,
                "+91-90000-0002",
                null
            );
            userAccountRepository.save(faculty);
        }

        if (rosterEntryRepository.count() == 0) {
            rosterEntryRepository.saveAll(List.of(
                new StudentRosterEntry("2024001", "Aisha Khan", "aisha.khan@campus.edu", "Computer Science", 2024, 6),
                new StudentRosterEntry("2024002", "Rahul Verma", "rahul.verma@campus.edu", "Computer Science", 2024, 6),
                new StudentRosterEntry("2024003", "Neha Singh", "neha.singh@campus.edu", "Electronics", 2024, 5)
            ));
        }

        if (studentRecordRepository.count() == 0) {
            StudentRecord record1 = new StudentRecord("2024001", "Aisha Khan", "aisha.khan@campus.edu", "Computer Science", 2024, 6, 92.5, 8.7, 0, 88.4, "High");
            record1.setSubjectMarks(Map.of("Data Structures", 92, "Operating Systems", 88, "DBMS", 94));
            record1.setSubjectAttendance(Map.of("Data Structures", 96, "Operating Systems", 90, "DBMS", 94));
            record1.setInternalAssessment(Map.of("Midterm", 82, "Quiz-2", 90));
            record1.setExamResults(Map.of("Semester-5", 88, "Internals", 92));
            record1.setBacklogs(List.of());
            record1.setRiskIndicators(List.of("Low risk", "Strong programming trend"));
            record1.setImprovementSuggestions(List.of("Continue leadership mentoring", "Assess internship readiness"));

            StudentRecord record2 = new StudentRecord("2024002", "Rahul Verma", "rahul.verma@campus.edu", "Computer Science", 2024, 6, 76.8, 7.1, 1, 68.9, "Moderate");
            record2.setSubjectMarks(Map.of("Data Structures", 72, "Operating Systems", 69, "DBMS", 78));
            record2.setSubjectAttendance(Map.of("Data Structures", 78, "Operating Systems", 71, "DBMS", 81));
            record2.setInternalAssessment(Map.of("Midterm", 70, "Quiz-2", 73));
            record2.setExamResults(Map.of("Semester-5", 74, "Internals", 71));
            record2.setBacklogs(List.of("Data Structures"));
            record2.setRiskIndicators(List.of("Attendance dip", "Needs mentoring"));
            record2.setImprovementSuggestions(List.of("Attend remedial classes", "Review DBMS lab practice"));

            StudentRecord record3 = new StudentRecord("2024003", "Neha Singh", "neha.singh@campus.edu", "Electronics", 2024, 5, 84.2, 8.1, 0, 80.5, "Medium");
            record3.setSubjectMarks(Map.of("Signals", 85, "Microcontrollers", 81, "VLSI", 88));
            record3.setSubjectAttendance(Map.of("Signals", 88, "Microcontrollers", 82, "VLSI", 86));
            record3.setInternalAssessment(Map.of("Midterm", 79, "Quiz-2", 84));
            record3.setExamResults(Map.of("Semester-4", 82, "Internals", 83));
            record3.setBacklogs(List.of());
            record3.setRiskIndicators(List.of("Needs lab confidence"));
            record3.setImprovementSuggestions(List.of("Focus on hardware projects", "Increase lab participation"));

            studentRecordRepository.saveAll(List.of(record1, record2, record3));
        }

        if (facultyAssignmentRepository.count() == 0) {
            facultyAssignmentRepository.saveAll(List.of(
                new FacultyAssignment("faculty@campus.edu", "2024001"),
                new FacultyAssignment("faculty@campus.edu", "2024002")
            ));
        }

        if (auditLogRepository.count() == 0) {
            auditLogRepository.saveAll(List.of(
                new AuditLog("admin@campus.edu", "2024001", "STUDENT_APPROVAL", "Initial verification passed"),
                new AuditLog("faculty@campus.edu", "2024002", "INTERVENTION_NOTE", "Assigned remedial support plan")
            ));
        }
    }
}
''',
    'src/main/java/com/campusiq/dto/RegisterRequest.java': '''package com.campusiq.dto;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;

public class RegisterRequest {
    @NotBlank(message = "Student ID is required")
    private String studentId;

    @NotBlank(message = "Full name is required")
    private String fullName;

    @NotBlank(message = "College email is required")
    @Email(message = "Email format is invalid")
    private String email;

    @NotBlank(message = "Department is required")
    private String department;

    @NotBlank(message = "Academic year is required")
    private String academicYear;

    @NotBlank(message = "Semester is required")
    private String semester;

    @NotBlank(message = "Password is required")
    @Size(min = 8, message = "Password must be at least 8 characters")
    @Pattern(regexp = "^(?=.*[A-Z])(?=.*[0-9]).+$", message = "Password must contain at least one uppercase letter and one number")
    private String password;

    @NotBlank(message = "Confirm password is required")
    private String confirmPassword;

    private String phone;
    private String profileImage;

    @NotBlank(message = "You must accept the terms and conditions")
    private String termsAccepted;

    public String getStudentId() {
        return studentId;
    }

    public void setStudentId(String studentId) {
        this.studentId = studentId;
    }

    public String getFullName() {
        return fullName;
    }

    public void setFullName(String fullName) {
        this.fullName = fullName;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getDepartment() {
        return department;
    }

    public void setDepartment(String department) {
        this.department = department;
    }

    public String getAcademicYear() {
        return academicYear;
    }

    public void setAcademicYear(String academicYear) {
        this.academicYear = academicYear;
    }

    public String getSemester() {
        return semester;
    }

    public void setSemester(String semester) {
        this.semester = semester;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public String getConfirmPassword() {
        return confirmPassword;
    }

    public void setConfirmPassword(String confirmPassword) {
        this.confirmPassword = confirmPassword;
    }

    public String getPhone() {
        return phone;
    }

    public void setPhone(String phone) {
        this.phone = phone;
    }

    public String getProfileImage() {
        return profileImage;
    }

    public void setProfileImage(String profileImage) {
        this.profileImage = profileImage;
    }

    public String getTermsAccepted() {
        return termsAccepted;
    }

    public void setTermsAccepted(String termsAccepted) {
        this.termsAccepted = termsAccepted;
    }
}
''',
    'src/main/java/com/campusiq/dto/LoginRequest.java': '''package com.campusiq.dto;

import jakarta.validation.constraints.NotBlank;

public class LoginRequest {
    @NotBlank(message = "Email is required")
    private String email;

    @NotBlank(message = "Password is required")
    private String password;

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }
}
''',
    'src/main/java/com/campusiq/controller/AuthController.java': '''package com.campusiq.controller;

import com.campusiq.dto.LoginRequest;
import com.campusiq.dto.RegisterRequest;
import com.campusiq.model.*;
import com.campusiq.repository.*;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
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
}
''',
    'src/main/java/com/campusiq/controller/DashboardController.java': '''package com.campusiq.controller;

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
''',
    'src/main/resources/application.properties': '''server.port=8080
spring.application.name=campusiq
server.servlet.session.cookie.http-only=true
server.servlet.session.cookie.same-site=Lax
server.servlet.session.cookie.secure=false

spring.datasource.url=jdbc:h2:mem:campusiq;MODE=LEGACY;DB_CLOSE_DELAY=-1;DB_CLOSE_ON_EXIT=FALSE
spring.datasource.driver-class-name=org.h2.Driver
spring.datasource.username=sa
spring.datasource.password=
spring.h2.console.enabled=true
spring.h2.console.path=/h2-console

spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=false
spring.jpa.properties.hibernate.format_sql=true
spring.jpa.defer-datasource-initialization=true
''',
    'src/main/resources/static/styles.css': '''body {
    font-family: Arial, sans-serif;
    background: #f4f7fb;
    margin: 0;
    color: #1d2939;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 24px;
}

.topbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #0f172a;
    color: white;
    padding: 18px 30px;
}

.hero {
    display: grid;
    grid-template-columns: 1.2fr 0.8fr;
    gap: 24px;
    padding: 32px 0;
}

.card, .panel {
    background: white;
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 6px 18px rgba(15, 23, 42, 0.08);
}

button, input, select {
    border-radius: 10px;
    border: 1px solid #d0d7de;
    padding: 12px 14px;
    font-size: 1rem;
}

button {
    background: #2563eb;
    color: white;
    border: none;
    cursor: pointer;
    font-weight: 600;
}

button.secondary {
    background: #e2e8f0;
    color: #0f172a;
}

button.danger {
    background: #dc2626;
}

.form-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(220px, 1fr));
    gap: 16px;
}

.form-field {
    display: flex;
    flex-direction: column;
    gap: 6px;
}

.inline {
    display: flex;
    gap: 12px;
    align-items: center;
}

.table {
    width: 100%;
    border-collapse: collapse;
}

.table th, .table td {
    border-bottom: 1px solid #e2e8f0;
    padding: 10px 12px;
    text-align: left;
}

.muted {
    color: #475569;
}

.badge {
    display: inline-block;
    padding: 6px 12px;
    border-radius: 999px;
    font-size: 0.8rem;
    font-weight: 700;
    background: #dcfce7;
    color: #166534;
}

.hidden { display: none; }

.alert { padding: 12px 16px; border-radius: 10px; margin: 12px 0; }
.alert.success { background: #dcfce7; color: #166534; }
.alert.error { background: #fee2e2; color: #991b1b; }
.alert.info { background: #dbeafe; color: #1d4ed8; }

.metric-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 16px;
    margin-top: 20px;
}

.metric {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 16px;
}

@media (max-width: 800px) {
    .hero, .form-grid { grid-template-columns: 1fr; }
}
''',
    'src/main/resources/static/app.js': '''const app = document.getElementById('app');
const state = { user: null, dashboard: null };

async function request(path, options = {}) {
    const defaultOptions = {
        headers: { 'Content-Type': 'application/json' },
        credentials: 'same-origin',
    };

    const merged = {
        ...defaultOptions,
        ...options,
        headers: {
            ...defaultOptions.headers,
            ...(options.headers || {})
        }
    };

    const csrfToken = document.cookie.split('; ').find(row => row.startsWith('XSRF-TOKEN='));
    if (csrfToken && !merged.headers['X-XSRF-TOKEN']) {
        merged.headers['X-XSRF-TOKEN'] = decodeURIComponent(csrfToken.split('=')[1]);
    }

    const response = await fetch(path, merged);
    const contentType = response.headers.get('content-type') || '';
    const payload = contentType.includes('application/json') ? await response.json() : await response.text();

    if (!response.ok) {
        throw new Error(payload.message || 'Request failed');
    }

    return payload;
}

function setAlert(message, kind = 'info') {
    const alertBox = document.getElementById('alertBox');
    alertBox.className = `alert ${kind}`;
    alertBox.textContent = message;
}

function renderAuth() {
    app.innerHTML = `
      <div class="topbar">
        <div><strong>CampusIQ</strong> Secure Student Portal</div>
        <span class="badge">Synthetic roster enabled</span>
      </div>
      <div class="container">
        <div class="hero">
          <div class="card">
            <h1>Smart campus analytics for secure academic visibility</h1>
            <p class="muted">Students, faculty, and administrators work from a verified identity model that protects private academic records.</p>
            <div class="metric-grid">
              <div class="metric"><strong>92.5%</strong><div>Average attendance</div></div>
              <div class="metric"><strong>8.7</strong><div>CGPA trend</div></div>
              <div class="metric"><strong>3</strong><div>Verified students</div></div>
            </div>
          </div>
          <div class="card">
            <div class="inline" style="margin-bottom:18px;">
              <button class="secondary" data-auth-tab="login">Login</button>
              <button class="secondary" data-auth-tab="register">Register</button>
            </div>
            <div id="alertBox" class="alert info">Use the demo accounts below to explore the system.</div>
            <div id="loginPanel">
              <h3>Login</h3>
              <div class="form-grid">
                <div class="form-field">
                  <label>Email</label>
                  <input id="loginEmail" type="email" placeholder="college email">
                </div>
                <div class="form-field">
                  <label>Password</label>
                  <input id="loginPassword" type="password" placeholder="password">
                </div>
              </div>
              <div style="margin-top:16px;">
                <button id="loginButton">Login</button>
              </div>
              <p class="muted">Demo accounts: admin@campus.edu / Campus@123, faculty@campus.edu / Campus@123</p>
            </div>
            <div id="registerPanel" class="hidden">
              <h3>Student Registration</h3>
              <div class="form-grid">
                <div class="form-field"><label>Student ID</label><input id="studentId" value="2024001"></div>
                <div class="form-field"><label>Full name</label><input id="fullName" value="Aisha Khan"></div>
                <div class="form-field"><label>College email</label><input id="email" type="email" value="aisha.khan@campus.edu"></div>
                <div class="form-field"><label>Department</label><input id="department" value="Computer Science"></div>
                <div class="form-field"><label>Academic year</label><input id="academicYear" value="2024"></div>
                <div class="form-field"><label>Current semester</label><input id="semester" value="6"></div>
                <div class="form-field"><label>Password</label><input id="password" type="password" value="Campus@123"></div>
                <div class="form-field"><label>Confirm password</label><input id="confirmPassword" type="password" value="Campus@123"></div>
                <div class="form-field"><label>Phone</label><input id="phone" value="+91-90000-1001"></div>
                <div class="form-field"><label>Profile image</label><input id="profileImage" value=""></div>
              </div>
              <label style="display:block; margin-top:12px;">
                <input id="termsAccepted" type="checkbox" checked> I accept the terms and conditions.
              </label>
              <div style="margin-top:16px;">
                <button id="registerButton">Submit Registration</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    `;

    document.querySelectorAll('[data-auth-tab]').forEach(btn => {
        btn.onclick = () => {
            const tab = btn.dataset.authTab;
            document.getElementById('loginPanel').classList.toggle('hidden', tab !== 'login');
            document.getElementById('registerPanel').classList.toggle('hidden', tab !== 'register');
        };
    });

    document.getElementById('loginButton').onclick = async () => {
        const email = document.getElementById('loginEmail').value;
        const password = document.getElementById('loginPassword').value;
        try {
            const result = await request('/api/auth/login', {
                method: 'POST',
                body: JSON.stringify({ email, password })
            });
            loadUser();
            setAlert(result.message, 'success');
        } catch (err) {
            setAlert(err.message, 'error');
        }
    };

    document.getElementById('registerButton').onclick = async () => {
        const payload = {
            studentId: document.getElementById('studentId').value,
            fullName: document.getElementById('fullName').value,
            email: document.getElementById('email').value,
            department: document.getElementById('department').value,
            academicYear: document.getElementById('academicYear').value,
            semester: document.getElementById('semester').value,
            password: document.getElementById('password').value,
            confirmPassword: document.getElementById('confirmPassword').value,
            phone: document.getElementById('phone').value,
            profileImage: document.getElementById('profileImage').value,
            termsAccepted: document.getElementById('termsAccepted').checked ? 'true' : 'false'
        };

        try {
            const result = await request('/api/auth/register', {
                method: 'POST',
                body: JSON.stringify(payload)
            });
            setAlert(result.message, 'success');
        } catch (err) {
            setAlert(err.message, 'error');
        }
    };
}

async function loadUser() {
    try {
        const profile = await request('/api/auth/me');
        state.user = profile;
        renderDashboard();
    } catch (error) {
        state.user = null;
        renderAuth();
    }
}

function renderDashboard() {
    const role = state.user.role;
    const userName = state.user.name;
    app.innerHTML = `
      <div class="topbar">
        <div><strong>CampusIQ</strong> ${userName}</div>
        <div class="inline">
          <span class="badge">${role}</span>
          <button class="danger" id="logoutButton">Logout</button>
        </div>
      </div>
      <div class="container">
        <div class="card" style="margin-top:24px;">
          <h2>Welcome, ${userName}</h2>
          <p class="muted">${role} access • ${state.user.department || 'Institutional'} • ${state.user.studentId || ''}</p>
          <div id="dashboardContent"></div>
        </div>
      </div>
    `;

    document.getElementById('logoutButton').onclick = async () => {
        await request('/api/auth/logout', { method: 'POST' });
        state.user = null;
        renderAuth();
    };

    if (role === 'STUDENT') {
        fetchStudentDashboard();
    } else if (role === 'FACULTY') {
        fetchFacultyDashboard();
    } else {
        fetchAdminDashboard();
    }
}

async function fetchStudentDashboard() {
    try {
        const data = await request('/api/student/dashboard');
        state.dashboard = data;
        const subjectRows = Object.entries(data.subjectMarks || {}).map(([subject, score]) => `
          <tr><td>${subject}</td><td>${score}</td><td>${data.subjectAttendance?.[subject] ?? 0}%</td></tr>
        `).join('');

        document.getElementById('dashboardContent').innerHTML = `
          <div class="metric-grid">
            <div class="metric"><strong>${data.attendancePercentage}%</strong><div>Attendance</div></div>
            <div class="metric"><strong>${data.cgpa}</strong><div>CGPA</div></div>
            <div class="metric"><strong>${data.studentSuccessScore}</strong><div>Success score</div></div>
            <div class="metric"><strong>${data.placementReadiness}</strong><div>Placement readiness</div></div>
          </div>
          <h3 style="margin-top:24px;">Academic performance</h3>
          <table class="table">
            <thead><tr><th>Subject</th><th>Marks</th><th>Attendance</th></tr></thead>
            <tbody>${subjectRows}</tbody>
          </table>
          <h3 style="margin-top:24px;">Risk indicators & suggestions</h3>
          <ul>${(data.riskIndicators || []).map(item => `<li>${item}</li>`).join('')}</ul>
          <ul>${(data.improvementSuggestions || []).map(item => `<li>${item}</li>`).join('')}</ul>
        `;
    } catch (error) {
        setAlert(error.message, 'error');
    }
}

async function fetchFacultyDashboard() {
    try {
        const data = await request('/api/faculty/overview');
        const rows = (data.assignedStudents || []).map(student => `
            <tr>
              <td>${student.fullName}</td>
              <td>${student.studentId}</td>
              <td>${student.studentSuccessScore}</td>
              <td>${student.riskIndicators[0] || 'No major risk'}</td>
            </tr>
        `).join('');

        document.getElementById('dashboardContent').innerHTML = `
          <h3>Assigned student cohort</h3>
          <table class="table"><thead><tr><th>Student</th><th>ID</th><th>Success Score</th><th>Risk</th></tr></thead><tbody>${rows}</tbody></table>
        `;
    } catch (error) {
        setAlert(error.message, 'error');
    }
}

async function fetchAdminDashboard() {
    try {
        const data = await request('/api/admin/overview');
        const rows = (data.studentRecords || []).map(student => `
            <tr>
              <td>${student.fullName}</td>
              <td>${student.studentId}</td>
              <td>${student.department}</td>
              <td>${student.studentSuccessScore}</td>
            </tr>
        `).join('');

        document.getElementById('dashboardContent').innerHTML = `
          <div class="metric-grid">
            <div class="metric"><strong>${data.institutionalSummary.totalStudents}</strong><div>Total students</div></div>
            <div class="metric"><strong>${data.institutionalSummary.avgSuccessScore.toFixed(1)}</strong><div>Average score</div></div>
            <div class="metric"><strong>${data.institutionalSummary.pendingRegistrations}</strong><div>Pending registrations</div></div>
          </div>
          <h3 style="margin-top:24px;">All student records</h3>
          <table class="table"><thead><tr><th>Name</th><th>ID</th><th>Department</th><th>Success Score</th></tr></thead><tbody>${rows}</tbody></table>
        `;
    } catch (error) {
        setAlert(error.message, 'error');
    }
}

renderAuth();
''',
    'src/main/resources/static/index.html': '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CampusIQ</title>
    <link rel="stylesheet" href="/styles.css">
</head>
<body>
    <div id="app"></div>
    <script src="/app.js"></script>
</body>
</html>
''',
}

for relative_path, content in files.items():
    path = root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')
print('Created project files under', root)
