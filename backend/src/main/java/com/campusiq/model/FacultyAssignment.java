package com.campusiq.model;

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
