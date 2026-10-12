package com.campusiq.repository;

import com.campusiq.model.AuditLog;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface AuditLogRepository extends JpaRepository<AuditLog, Long> {
    List<AuditLog> findAllByOrderByCreatedAtDesc();
    List<AuditLog> findByTargetStudentIdOrderByCreatedAtDesc(String targetStudentId);
}
