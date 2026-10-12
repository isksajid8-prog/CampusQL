package com.campusiq.repository;

import com.campusiq.model.FacultyAssignment;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface FacultyAssignmentRepository extends JpaRepository<FacultyAssignment, Long> {
    List<FacultyAssignment> findByFacultyEmail(String facultyEmail);
    boolean existsByFacultyEmailAndStudentId(String facultyEmail, String studentId);
}
