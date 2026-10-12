package com.campusiq.model;

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
