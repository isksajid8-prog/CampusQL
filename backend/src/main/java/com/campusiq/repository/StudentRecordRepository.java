package com.campusiq.repository;

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
