# Enhanced Database Schema for Individual Student Tracking

## Overview

This database schema is designed to support individual-focused learning with flexible batch support, emphasizing detailed student progress tracking and topic-level attendance management.

## Core Tables

### Users
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    uuid UUID UNIQUE NOT NULL DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    avatar_url VARCHAR(500),
    role VARCHAR(50) NOT NULL CHECK (role IN ('super_admin', 'counselor', 'faculty', 'student', 'admin')),
    status VARCHAR(20) NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'suspended')),
    email_verified_at TIMESTAMP,
    last_login_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Students
```sql
CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    enrollment_no VARCHAR(50) UNIQUE NOT NULL,
    date_of_birth DATE,
    address TEXT,
    emergency_contact_name VARCHAR(100),
    emergency_contact_phone VARCHAR(20),
    admission_date DATE NOT NULL,
    counselor_id INTEGER REFERENCES users(id),
    learning_style VARCHAR(50) CHECK (learning_style IN ('visual', 'auditory', 'kinesthetic', 'reading')),
    preferred_schedule JSONB, -- {preferred_days: [], preferred_times: []}
    status VARCHAR(20) NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'completed', 'dropped', 'hold', 'graduated')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Faculties
```sql
CREATE TABLE faculties (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    employee_id VARCHAR(50) UNIQUE NOT NULL,
    specialization TEXT[], -- Array of specializations
    qualification TEXT,
    experience_years DECIMAL(3,1),
    hourly_rate DECIMAL(10,2),
    max_hours_per_day INTEGER DEFAULT 8,
    max_students_per_day INTEGER DEFAULT 10,
    available_time_slots JSONB, -- {days: [{day: 'monday', slots: [{start: '09:00', end: '17:00'}]}]}
    performance_rating DECIMAL(3,2) CHECK (performance_rating >= 0 AND performance_rating <= 5),
    status VARCHAR(20) NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'on_leave')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Subjects
```sql
CREATE TABLE subjects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    code VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    duration_hours INTEGER NOT NULL,
    category VARCHAR(100),
    difficulty_level VARCHAR(20) CHECK (difficulty_level IN ('beginner', 'intermediate', 'advanced')),
    prerequisites INTEGER[] REFERENCES subjects(id),
    status VARCHAR(20) NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'inactive')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Topics
```sql
CREATE TABLE topics (
    id SERIAL PRIMARY KEY,
    subject_id INTEGER NOT NULL REFERENCES subjects(id) ON DELETE CASCADE,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    order_index INTEGER NOT NULL,
    estimated_duration_minutes INTEGER NOT NULL,
    difficulty_level VARCHAR(20) CHECK (difficulty_level IN ('easy', 'medium', 'hard')),
    prerequisites INTEGER[] REFERENCES topics(id),
    learning_objectives TEXT[],
    resources JSONB, -- {videos: [], documents: [], links: []}
    status VARCHAR(20) NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'inactive')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Student_Subject_Enrollments
```sql
CREATE TABLE student_subject_enrollments (
    id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    subject_id INTEGER NOT NULL REFERENCES subjects(id) ON DELETE CASCADE,
    faculty_id INTEGER NOT NULL REFERENCES faculties(id),
    enrollment_date DATE NOT NULL,
    expected_completion_date DATE,
    actual_completion_date DATE,
    completion_percentage DECIMAL(5,2) DEFAULT 0,
    status VARCHAR(20) NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'completed', 'paused', 'dropped')),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(student_id, subject_id)
);
```

### Learning_Sessions
```sql
CREATE TABLE learning_sessions (
    id SERIAL PRIMARY KEY,
    uuid UUID UNIQUE NOT NULL DEFAULT gen_random_uuid(),
    student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    faculty_id INTEGER NOT NULL REFERENCES faculties(id) ON DELETE CASCADE,
    subject_id INTEGER NOT NULL REFERENCES subjects(id) ON DELETE CASCADE,
    session_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    duration_minutes INTEGER NOT NULL,
    session_type VARCHAR(20) NOT NULL DEFAULT 'individual' CHECK (session_type IN ('individual', 'group', 'workshop')),
    location VARCHAR(100),
    status VARCHAR(20) NOT NULL DEFAULT 'scheduled' CHECK (status IN ('scheduled', 'completed', 'cancelled', 'no_show')),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Session_Attendance
```sql
CREATE TABLE session_attendance (
    id SERIAL PRIMARY KEY,
    session_id INTEGER NOT NULL REFERENCES learning_sessions(id) ON DELETE CASCADE,
    student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    attendance_status VARCHAR(20) NOT NULL CHECK (attendance_status IN ('present', 'absent', 'late')),
    check_in_time TIME,
    check_out_time TIME,
    topics_covered INTEGER[] REFERENCES topics(id), -- Array of topic IDs covered in this session
    topic_competency JSONB, -- {topic_id: {understanding_level: 1-5, notes: 'text'}}
    faculty_notes TEXT,
    student_feedback TEXT,
    next_session_prep JSONB, -- {topics_to_review: [], new_topics: []}
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(session_id, student_id)
);
```

### Student_Topic_Progress
```sql
CREATE TABLE student_topic_progress (
    id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    topic_id INTEGER NOT NULL REFERENCES topics(id) ON DELETE CASCADE,
    competency_level INTEGER DEFAULT 0 CHECK (competency_level >= 0 AND competency_level <= 5),
    status VARCHAR(20) NOT NULL DEFAULT 'not_started' CHECK (status IN ('not_started', 'in_progress', 'completed', 'mastered', 'needs_review')),
    first_introduced_date DATE,
    completion_date DATE,
    time_spent_minutes INTEGER DEFAULT 0,
    session_count INTEGER DEFAULT 0,
    assessment_scores JSONB, -- {quiz1: 85, practical: 90}
    notes TEXT,
    last_updated_by INTEGER REFERENCES faculties(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(student_id, topic_id)
);
```

### Flexible_Batches
```sql
CREATE TABLE flexible_batches (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    subject_id INTEGER NOT NULL REFERENCES subjects(id) ON DELETE CASCADE,
    faculty_id INTEGER NOT NULL REFERENCES faculties(id) ON DELETE CASCADE,
    batch_type VARCHAR(20) NOT NULL CHECK (batch_type IN ('temporary', 'workshop', 'project', 'peer_learning')),
    start_date DATE NOT NULL,
    end_date DATE,
    schedule JSONB, -- Flexible scheduling information
    max_students INTEGER,
    status VARCHAR(20) NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'completed', 'cancelled')),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Batch_Session_Attendance
```sql
CREATE TABLE batch_session_attendance (
    id SERIAL PRIMARY KEY,
    batch_id INTEGER NOT NULL REFERENCES flexible_batches(id) ON DELETE CASCADE,
    session_date DATE NOT NULL,
    student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    attendance_status VARCHAR(20) NOT NULL CHECK (attendance_status IN ('present', 'absent', 'late')),
    topics_covered INTEGER[] REFERENCES topics(id),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(batch_id, session_date, student_id)
);
```

### Assessments
```sql
CREATE TABLE assessments (
    id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    topic_id INTEGER REFERENCES topics(id) ON DELETE CASCADE,
    subject_id INTEGER NOT NULL REFERENCES subjects(id) ON DELETE CASCADE,
    assessment_type VARCHAR(30) NOT NULL CHECK (assessment_type IN ('quiz', 'assignment', 'project', 'exam', 'practical')),
    title VARCHAR(200) NOT NULL,
    description TEXT,
    total_marks DECIMAL(5,2) NOT NULL,
    marks_obtained DECIMAL(5,2),
    percentage DECIMAL(5,2),
    grade VARCHAR(10),
    assessment_date DATE NOT NULL,
    faculty_id INTEGER NOT NULL REFERENCES faculties(id),
    feedback TEXT,
    status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'completed', 'graded')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### CRM_Inquiries
```sql
CREATE TABLE crm_inquiries (
    id SERIAL PRIMARY KEY,
    uuid UUID UNIQUE NOT NULL DEFAULT gen_random_uuid(),
    counselor_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    student_name VARCHAR(200) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(255),
    interested_subjects INTEGER[] REFERENCES subjects(id),
    source VARCHAR(30) CHECK (source IN ('website', 'referral', 'walk_in', 'social_media', 'campaign')),
    status VARCHAR(20) NOT NULL DEFAULT 'new' CHECK (status IN ('new', 'contacted', 'follow_up_scheduled', 'enrolled', 'lost')),
    priority VARCHAR(10) DEFAULT 'medium' CHECK (priority IN ('low', 'medium', 'high')),
    next_follow_up_date TIMESTAMP,
    notes TEXT,
    tags TEXT[],
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Follow_Ups
```sql
CREATE TABLE follow_ups (
    id SERIAL PRIMARY KEY,
    inquiry_id INTEGER NOT NULL REFERENCES crm_inquiries(id) ON DELETE CASCADE,
    counselor_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    follow_up_date TIMESTAMP NOT NULL,
    follow_up_type VARCHAR(20) NOT NULL CHECK (follow_up_type IN ('call', 'email', 'visit', 'sms', 'whatsapp')),
    notes TEXT,
    next_follow_up_date TIMESTAMP,
    status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (status IN ('completed', 'pending', 'missed')),
    outcome TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Rewards_Penalties
```sql
CREATE TABLE rewards_penalties (
    id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    faculty_id INTEGER REFERENCES faculties(id),
    type VARCHAR(10) NOT NULL CHECK (type IN ('reward', 'penalty')),
    category VARCHAR(30) NOT NULL CHECK (category IN ('attendance', 'performance', 'behavior', 'assignment', 'other')),
    reason TEXT NOT NULL,
    points INTEGER NOT NULL,
    date DATE NOT NULL,
    created_by INTEGER NOT NULL REFERENCES users(id),
    status VARCHAR(20) NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'appealed', 'resolved')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Feedback
```sql
CREATE TABLE feedback (
    id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    faculty_id INTEGER REFERENCES faculties(id),
    session_id INTEGER REFERENCES learning_sessions(id) ON DELETE CASCADE,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    comments TEXT,
    feedback_type VARCHAR(20) NOT NULL CHECK (feedback_type IN ('faculty', 'session', 'subject', 'institute', 'facility')),
    sentiment VARCHAR(10) CHECK (sentiment IN ('positive', 'neutral', 'negative')),
    status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'reviewed', 'resolved')),
    reviewed_by INTEGER REFERENCES users(id),
    reviewed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Student_Reports
```sql
CREATE TABLE student_reports (
    id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    report_type VARCHAR(30) NOT NULL CHECK (report_type IN ('progress', 'attendance', 'performance', 'final')),
    report_period_start DATE NOT NULL,
    report_period_end DATE NOT NULL,
    data JSONB NOT NULL, -- Report data in JSON format
    generated_by INTEGER NOT NULL REFERENCES users(id),
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) NOT NULL DEFAULT 'generated' CHECK (status IN ('generated', 'sent', 'viewed'))
);
```

### Faculty_Reports
```sql
CREATE TABLE faculty_reports (
    id SERIAL PRIMARY KEY,
    faculty_id INTEGER NOT NULL REFERENCES faculties(id) ON DELETE CASCADE,
    report_type VARCHAR(30) NOT NULL CHECK (report_type IN ('performance', 'utilization', 'student_progress', 'time_management')),
    report_period_start DATE NOT NULL,
    report_period_end DATE NOT NULL,
    data JSONB NOT NULL,
    generated_by INTEGER NOT NULL REFERENCES users(id),
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) NOT NULL DEFAULT 'generated' CHECK (status IN ('generated', 'sent', 'viewed'))
);
```

## Indexes for Performance

```sql
-- User and role-based queries
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_status ON users(status);

-- Student-related queries
CREATE INDEX idx_students_counselor ON students(counselor_id);
CREATE INDEX idx_students_status ON students(status);
CREATE INDEX idx_students_admission_date ON students(admission_date);

-- Faculty-related queries
CREATE INDEX idx_faculties_status ON faculties(status);
CREATE INDEX idx_faculties_specialization ON faculties USING GIN(specialization);

-- Subject and topic queries
CREATE INDEX idx_topics_subject ON topics(subject_id);
CREATE INDEX idx_topics_order ON topics(subject_id, order_index);

-- Enrollment and progress queries
CREATE INDEX idx_enrollments_student ON student_subject_enrollments(student_id);
CREATE INDEX idx_enrollments_faculty ON student_subject_enrollments(faculty_id);
CREATE INDEX idx_enrollments_status ON student_subject_enrollments(status);

-- Session and attendance queries
CREATE INDEX idx_sessions_student ON learning_sessions(student_id);
CREATE INDEX idx_sessions_faculty ON learning_sessions(faculty_id);
CREATE INDEX idx_sessions_date ON learning_sessions(session_date);
CREATE INDEX idx_attendance_session ON session_attendance(session_id);
CREATE INDEX idx_attendance_student ON session_attendance(student_id);

-- Progress tracking
CREATE INDEX idx_topic_progress_student ON student_topic_progress(student_id);
CREATE INDEX idx_topic_progress_topic ON student_topic_progress(topic_id);
CREATE INDEX idx_topic_progress_status ON student_topic_progress(status);

-- CRM queries
CREATE INDEX idx_inquiries_counselor ON crm_inquiries(counselor_id);
CREATE INDEX idx_inquiries_status ON crm_inquiries(status);
CREATE INDEX idx_followups_inquiry ON follow_ups(inquiry_id);
CREATE INDEX idx_followups_date ON follow_ups(follow_up_date);

-- Report queries
CREATE INDEX idx_student_reports_student ON student_reports(student_id);
CREATE INDEX idx_student_reports_type ON student_reports(report_type);
CREATE INDEX idx_faculty_reports_faculty ON faculty_reports(faculty_id);
CREATE INDEX idx_faculty_reports_type ON faculty_reports(report_type);
```

## Views for Common Queries

```sql
-- Student Progress View
CREATE VIEW student_progress_view AS
SELECT 
    s.id as student_id,
    s.enrollment_no,
    u.first_name || ' ' || u.last_name as student_name,
    sub.name as subject_name,
    sub.code as subject_code,
    sse.completion_percentage,
    sse.status as enrollment_status,
    COUNT(stp.id) as total_topics,
    COUNT(CASE WHEN stp.status = 'completed' THEN 1 END) as completed_topics,
    AVG(stp.competency_level) as avg_competency,
    f.user_id as faculty_id,
    fu.first_name || ' ' || fu.last_name as faculty_name
FROM students s
JOIN users u ON s.user_id = u.id
JOIN student_subject_enrollments sse ON s.id = sse.student_id
JOIN subjects sub ON sse.subject_id = sub.id
JOIN faculties f ON sse.faculty_id = f.id
JOIN users fu ON f.user_id = fu.id
LEFT JOIN topics t ON sub.id = t.subject_id
LEFT JOIN student_topic_progress stp ON s.id = stp.student_id AND t.id = stp.topic_id
GROUP BY s.id, s.enrollment_no, u.first_name, u.last_name, sub.name, sub.code, 
         sse.completion_percentage, sse.status, f.user_id, fu.first_name, fu.last_name;

-- Faculty Utilization View
CREATE VIEW faculty_utilization_view AS
SELECT 
    f.id as faculty_id,
    f.employee_id,
    u.first_name || ' ' || u.last_name as faculty_name,
    COUNT(ls.id) as total_sessions,
    SUM(ls.duration_minutes) as total_minutes,
    COUNT(DISTINCT ls.student_id) as unique_students,
    AVG(ls.duration_minutes) as avg_session_duration,
    COUNT(CASE WHEN ls.status = 'completed' THEN 1 END) as completed_sessions,
    COUNT(CASE WHEN ls.status = 'cancelled' THEN 1 END) as cancelled_sessions
FROM faculties f
JOIN users u ON f.user_id = u.id
LEFT JOIN learning_sessions ls ON f.id = ls.faculty_id
GROUP BY f.id, f.employee_id, u.first_name, u.last_name;

-- Attendance Analytics View
CREATE VIEW attendance_analytics_view AS
SELECT 
    s.id as student_id,
    s.enrollment_no,
    u.first_name || ' ' || u.last_name as student_name,
    COUNT(sa.id) as total_sessions,
    COUNT(CASE WHEN sa.attendance_status = 'present' THEN 1 END) as present_count,
    COUNT(CASE WHEN sa.attendance_status = 'absent' THEN 1 END) as absent_count,
    COUNT(CASE WHEN sa.attendance_status = 'late' THEN 1 END) as late_count,
    ROUND(COUNT(CASE WHEN sa.attendance_status = 'present' THEN 1 END) * 100.0 / COUNT(sa.id), 2) as attendance_percentage,
    MAX(CASE WHEN sa.attendance_status = 'absent' THEN sa.created_at END) as last_absent_date
FROM students s
JOIN users u ON s.user_id = u.id
LEFT JOIN session_attendance sa ON s.id = sa.student_id
GROUP BY s.id, s.enrollment_no, u.first_name, u.last_name;
```

This enhanced database schema provides a robust foundation for individual-focused learning with detailed progress tracking, flexible batch support, and comprehensive analytics capabilities.