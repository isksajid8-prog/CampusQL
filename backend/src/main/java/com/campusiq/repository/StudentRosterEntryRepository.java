package com.campusiq.repository;

import com.campusiq.model.StudentRosterEntry;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface StudentRosterEntryRepository extends JpaRepository<StudentRosterEntry, Long> {
    Optional<StudentRosterEntry> findByStudentId(String studentId);
    Optional<StudentRosterEntry> findByEmail(String email);
}
