# Data Flow Diagrams for Individual-Focused Learning System

## Overview

This document outlines comprehensive data flow diagrams that illustrate how information moves through the individual-focused learning management system. The diagrams cover major workflows including student enrollment, attendance tracking, progress monitoring, and analytics processing.

## System Architecture Data Flow

### High-Level System Data Flow

```mermaid
graph TB
    subgraph "Frontend Layer"
        UI[React.js UI Components]
        State[State Management - Zustand]
        Cache[Local Storage/Cache]
    end
    
    subgraph "API Gateway"
        API[FastAPI Backend]
        Auth[Authentication Service]
        WS[WebSocket Service]
    end
    
    subgraph "Business Logic Layer"
        StudentSvc[Student Service]
        FacultySvc[Faculty Service]
        AttendanceSvc[Attendance Service]
        ProgressSvc[Progress Service]
        CRMSvc[CRM Service]
        AnalyticsSvc[Analytics Service]
        FeedbackSvc[Feedback Service]
    end
    
    subgraph "Data Layer"
        PostgreSQL[(PostgreSQL Database)]
        Redis[(Redis Cache)]
        FileStorage[(File Storage)]
    end
    
    subgraph "External Services"
        Email[Email Service]
        SMS[SMS Service]
        Payment[Payment Gateway]
    end
    
    UI --> State
    State --> API
    API --> Auth
    Auth --> StudentSvc
    Auth --> FacultySvc
    Auth --> AttendanceSvc
    Auth --> ProgressSvc
    Auth --> CRMSvc
    Auth --> AnalyticsSvc
    Auth --> FeedbackSvc
    
    StudentSvc --> PostgreSQL
    FacultySvc --> PostgreSQL
    AttendanceSvc --> PostgreSQL
    ProgressSvc --> PostgreSQL
    CRMSvc --> PostgreSQL
    AnalyticsSvc --> PostgreSQL
    FeedbackSvc --> PostgreSQL
    
    AttendanceSvc --> Redis
    ProgressSvc --> Redis
    AnalyticsSvc --> Redis
    
    CRMSvc --> Email
    CRMSvc --> SMS
    StudentSvc --> Payment
    
    WS --> UI
    AnalyticsSvc --> WS
    AttendanceSvc --> WS
    
    FileStorage --> StudentSvc
    FileStorage --> FacultySvc
```

## Student Enrollment Data Flow

### Student Registration and Onboarding

```mermaid
sequenceDiagram
    participant Student as Student/Parent
    participant UI as Frontend UI
    participant API as FastAPI
    participant Auth as Auth Service
    participant CRM as CRM Service
    participant StudentSvc as Student Service
    participant DB as PostgreSQL
    participant Email as Email Service
    
    Student->>UI: Start Registration
    UI->>API: POST /auth/register
    API->>Auth: Validate user data
    Auth->>API: User validation result
    API->>StudentSvc: Create student record
    StudentSvc->>DB: Insert student data
    DB-->>StudentSvc: Student record created
    StudentSvc-->>API: Student profile
    API->>CRM: Create inquiry record
    CRM->>DB: Insert inquiry data
    DB-->>CRM: Inquiry record
    CRM-->>API: Inquiry created
    API->>Email: Send welcome email
    Email-->>API: Email sent confirmation
    API-->>UI: Registration successful
    UI-->>Student: Show success message
```

### Subject Enrollment and Faculty Assignment

```mermaid
graph TD
    subgraph "Subject Enrollment Process"
        A[Student Selects Subjects] --> B[Check Prerequisites]
        B --> C{Prerequisites Met?}
        C -->|Yes| D[Calculate Fees]
        C -->|No| E[Show Prerequisite Options]
        E --> B
        D --> F[Payment Processing]
        F --> G{Payment Successful?}
        G -->|Yes| H[Enroll in Subjects]
        G -->|No| I[Show Payment Error]
        H --> J[Assign Faculty]
        J --> K[Create Learning Path]
        K --> L[Schedule Initial Sessions]
        L --> M[Send Confirmation]
    end
    
    subgraph "Faculty Assignment Logic"
        J --> N[Check Faculty Availability]
        N --> O[Match Specialization]
        O --> P[Check Workload Balance]
        P --> Q[Assign Best Match]
        Q --> R[Notify Faculty]
        R --> S[Update Faculty Schedule]
    end
```

## Attendance System Data Flow

### Real-Time Attendance Marking

```mermaid
sequenceDiagram
    participant Faculty as Faculty
    participant UI as Attendance UI
    participant API as FastAPI
    participant AttendanceSvc as Attendance Service
    participant ProgressSvc as Progress Service
    participant DB as PostgreSQL
    participant Redis as Redis Cache
    participant WS as WebSocket
    participant Analytics as Analytics Service
    participant Student as Student
    
    Faculty->>UI: Mark attendance for session
    UI->>API: POST /attendance/session/{id}
    API->>AttendanceSvc: Process attendance data
    AttendanceSvc->>DB: Insert attendance records
    DB-->>AttendanceSvc: Attendance saved
    AttendanceSvc->>ProgressSvc: Update student progress
    ProgressSvc->>DB: Update progress records
    DB-->>ProgressSvc: Progress updated
    AttendanceSvc->>Redis: Cache attendance data
    AttendanceSvc->>WS: Broadcast attendance update
    WS->>UI: Real-time update
    AttendanceSvc->>Analytics: Trigger analytics update
    Analytics->>DB: Update analytics tables
    AttendanceSvc-->>API: Attendance marked successfully
    API-->>UI: Success response
    UI-->>Faculty: Show confirmation
    
    Note over WS: Student receives notification
    WS->>Student: Attendance marked notification
```

### Topic Coverage and Competency Tracking

```mermaid
graph LR
    subgraph "Attendance Marking"
        A[Session Start] --> B[Mark Attendance]
        B --> C[Select Topics Covered]
        C --> D[Rate Understanding Level]
        D --> E[Add Session Notes]
        E --> F[Save Attendance]
    end
    
    subgraph "Progress Update"
        F --> G[Update Topic Progress]
        G --> H[Calculate Competency Level]
        H --> I[Update Subject Progress]
        I --> J[Calculate Learning Velocity]
        J --> K[Predict Completion Date]
    end
    
    subgraph "Analytics Processing"
        K --> L[Update Student Analytics]
        L --> M[Update Faculty Performance]
        M --> N[Update Institute Metrics]
        N --> O[Generate Reports]
    end
    
    subgraph "Notifications"
        O --> P[Send Progress Updates]
        P --> Q[Trigger Alerts if Needed]
        Q --> R[Schedule Follow-ups]
    end
```

## Student Progress Analytics Data Flow

### Real-Time Progress Calculation

```mermaid
graph TB
    subgraph "Data Collection"
        A[Attendance Records] --> D[Progress Engine]
        B[Topic Completions] --> D
        C[Assessment Scores] --> D
        E[Faculty Feedback] --> D
        F[Student Activities] --> D
    end
    
    subgraph "Progress Calculation"
        D --> G[Calculate Topic Mastery]
        G --> H[Update Subject Progress]
        H --> I[Calculate Learning Velocity]
        I --> J[Predict Completion Timeline]
        J --> K[Identify Learning Patterns]
        K --> L[Generate Insights]
    end
    
    subgraph "Analytics Processing"
        L --> M[Student Performance Analytics]
        L --> N[Faculty Effectiveness Analytics]
        L --> O[Curriculum Effectiveness Analytics]
        L --> P[Institute Performance Analytics]
    end
    
    subgraph "Output Generation"
        M --> Q[Student Dashboards]
        N --> R[Faculty Reports]
        O --> S[Curriculum Updates]
        P --> T[Management Reports]
    end
```

### Predictive Analytics Pipeline

```mermaid
sequenceDiagram
    participant Scheduler as Analytics Scheduler
    participant Analytics as Analytics Service
    participant ML as ML Models
    participant DB as PostgreSQL
    participant Cache as Redis
    participant API as FastAPI
    participant UI as Frontend
    
    Scheduler->>Analytics: Trigger analytics job
    Analytics->>DB: Extract student progress data
    Analytics->>DB: Extract attendance data
    Analytics->>DB: Extract assessment data
    Analytics->>ML: Process data for predictions
    ML->>ML: Calculate completion probabilities
    ML->>ML: Identify at-risk students
    ML->>ML: Generate learning recommendations
    ML-->>Analytics: Prediction results
    Analytics->>Cache: Store predictions
    Analytics->>DB: Update analytics tables
    Analytics->>API: Notify of new insights
    API->>UI: Push real-time updates
    UI-->>Scheduler: Display updated analytics
```

## CRM System Data Flow

### Lead Management and Conversion

```mermaid
graph TD
    subgraph "Lead Generation"
        A[Website Form] --> E[CRM System]
        B[Phone Inquiry] --> E
        C[Walk-in Visit] --> E
        D[Referral] --> E
    end
    
    subgraph "Lead Processing"
        E --> F[Lead Scoring Algorithm]
        F --> G[Assign to Counselor]
        G --> H[Schedule Initial Contact]
        H --> I[Follow-up Sequence]
    end
    
    subgraph "Conversion Process"
        I --> J{Qualified Lead?}
        J -->|Yes| K[Course Counseling]
        J -->|No| L[Nurture Campaign]
        K --> M[Enrollment Process]
        L --> I
        M --> N[Payment Processing]
        N --> O[Student Onboarding]
    end
    
    subgraph "Analytics & Reporting"
        O --> P[Conversion Analytics]
        P --> Q[Counselor Performance]
        Q --> R[Pipeline Health]
        R --> S[Revenue Tracking]
    end
```

### Follow-up Automation Flow

```mermaid
sequenceDiagram
    participant CRM as CRM Service
    participant Scheduler as Task Scheduler
    participant Email as Email Service
    participant SMS as SMS Service
    participant Counselor as Counselor
    participant Student as Student
    participant DB as PostgreSQL
    
    CRM->>Scheduler: Schedule follow-up
    Scheduler->>CRM: Trigger follow-up task
    CRM->>DB: Update follow-up status
    CRM->>Email: Send follow-up email
    CRM->>SMS: Send SMS reminder
    Email-->>Student: Email delivered
    SMS-->>Student: SMS delivered
    Student->>CRM: Response/Action
    CRM->>Counselor: Notify counselor
    Counselor->>CRM: Update interaction
    CRM->>DB: Log interaction
    CRM->>Scheduler: Schedule next follow-up
```

## Feedback System Data Flow

### Multi-Channel Feedback Collection

```mermaid
graph LR
    subgraph "Feedback Collection"
        A[Session Feedback] --> F[Feedback Processor]
        B[Faculty Evaluation] --> F
        C[Subject Feedback] --> F
        D[Institute Feedback] --> F
        E[Real-time Feedback] --> F
    end
    
    subgraph "Feedback Processing"
        F --> G[Sentiment Analysis]
        G --> H[Theme Extraction]
        H --> I[Urgency Classification]
        I --> J[Action Item Generation]
    end
    
    subgraph "Response System"
        J --> K[Assign Responsibility]
        K --> L[Create Action Plan]
        L --> M[Schedule Resolution]
        M --> N[Track Progress]
        N --> O[Close Loop]
    end
    
    subgraph "Analytics"
        O --> P[Feedback Analytics]
        P --> Q[Trend Analysis]
        Q --> R[Improvement Insights]
        R --> S[Strategic Planning]
    end
```

## Faculty Management Data Flow

### Performance Tracking and Analytics

```mermaid
graph TB
    subgraph "Data Sources"
        A[Session Records] --> G[Faculty Analytics Engine]
        B[Student Progress] --> G
        C[Attendance Data] --> G
        D[Student Feedback] --> G
        E[Time Tracking] --> G
        F[Self-Assessments] --> G
    end
    
    subgraph "Analytics Processing"
        G --> H[Calculate Performance Metrics]
        H --> I[Identify Strengths/Weaknesses]
        I --> J[Generate Performance Score]
        J --> K[Compare with Benchmarks]
        K --> L[Create Development Plan]
    end
    
    subgraph "Output & Actions"
        L --> M[Performance Reports]
        L --> N[Training Recommendations]
        L --> O[Workload Adjustments]
        L --> P[Incentive Calculations]
    end
```

## Real-Time Data Synchronization

### WebSocket Communication Flow

```mermaid
graph TD
    subgraph "Real-Time Events"
        A[Attendance Marked] --> WS[WebSocket Manager]
        B[Progress Updated] --> WS
        C[Feedback Submitted] --> WS
        D[Alert Triggered] --> WS
        E[System Notification] --> WS
    end
    
    subgraph "Event Processing"
        WS --> F[Event Validation]
        F --> G[User Authorization]
        G --> H[Target User Identification]
        H --> I[Message Formatting]
        I --> J[Delivery Queue]
    end
    
    subgraph "Client Delivery"
        J --> K[Connected Clients]
        K --> L[Student Dashboard]
        K --> M[Faculty Interface]
        K --> N[Admin Panel]
        K --> O[Counselor Dashboard]
    end
```

## Data Integration and ETL

### Batch Processing Pipeline

```mermaid
graph LR
    subgraph "Data Extraction"
        A[Operational DB] --> E[ETL Pipeline]
        B[Transaction Logs] --> E
        C[External APIs] --> E
        D[File Storage] --> E
    end
    
    subgraph "Data Transformation"
        E --> F[Data Cleaning]
        F --> G[Validation]
        G --> H[Aggregation]
        H --> I[Enrichment]
    end
    
    subgraph "Data Loading"
        I --> J[Analytics Database]
        I --> K[Data Warehouse]
        I --> L[Cache Layer]
        I --> M[Search Index]
    end
    
    subgraph "Consumption"
        J --> N[Reporting Tools]
        K --> O[BI Dashboards]
        L --> P[Real-time APIs]
        M --> Q[Search Functionality]
    end
```

## Data Security and Privacy Flow

### Data Access Control

```mermaid
graph TD
    subgraph "Authentication"
        A[User Login] --> B[JWT Token Generation]
        B --> C[Role Assignment]
        C --> D[Permission Mapping]
    end
    
    subgraph "Authorization"
        D --> E[API Request]
        E --> F[Token Validation]
        F --> G[Permission Check]
        G --> H{Authorized?}
        H -->|Yes| I[Process Request]
        H -->|No| J[Access Denied]
    end
    
    subgraph "Data Access"
        I --> K[Data Filtering]
        K --> L[PII Masking]
        L --> M[Audit Logging]
        M --> N[Return Data]
    end
```

These data flow diagrams provide a comprehensive view of how information moves through the individual-focused learning management system, ensuring clear understanding of system interactions and data processing pipelines.