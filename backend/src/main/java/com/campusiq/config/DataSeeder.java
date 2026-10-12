package com.campusiq.config;

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
