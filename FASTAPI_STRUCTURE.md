# FastAPI Backend Architecture Design

## Overview

This document outlines the comprehensive FastAPI backend architecture that will power the student academics management system. The design emphasizes modularity, scalability, and performance while supporting individual-focused learning with real-time analytics.

## Technology Stack

### Core Technologies
- **Backend Framework**: FastAPI 0.104+
- **Database**: PostgreSQL 15+ with SQLAlchemy 2.0
- **Authentication**: JWT with OAuth2 with password flow
- **Caching**: Redis 7+ for session and data caching
- **Task Queue**: Celery with Redis broker
- **File Storage**: MinIO (S3-compatible) or AWS S3
- **Real-time**: WebSocket connections for live updates
- **API Documentation**: Automatic OpenAPI/Swagger generation

### Supporting Technologies
- **Data Validation**: Pydantic v2
- **Database Migrations**: Alembic
- **Testing**: Pytest with async support
- **Logging**: Structlog with JSON formatting
- **Monitoring**: Prometheus metrics + Grafana
- **Containerization**: Docker with Docker Compose

## Project Structure

```
app/
├── __init__.py
├── main.py                     # FastAPI application entry point
├── config/
│   ├── __init__.py
│   ├── settings.py              # Application settings
│   ├── database.py              # Database configuration
│   └── redis.py                # Redis configuration
├── core/
│   ├── __init__.py
│   ├── auth.py                  # Authentication utilities
│   ├── security.py              # Security functions
│   ├── permissions.py           # Role-based permissions
│   └── exceptions.py            # Custom exceptions
├── models/
│   ├── __init__.py
│   ├── base.py                  # Base model classes
│   ├── user.py                  # User models
│   ├── student.py               # Student models
│   ├── faculty.py               # Faculty models
│   ├── subject.py               # Subject models
│   ├── session.py               # Learning session models
│   ├── attendance.py            # Attendance models
│   ├── progress.py              # Progress tracking models
│   ├── crm.py                   # CRM models
│   ├── feedback.py              # Feedback models
│   └── analytics.py             # Analytics models
├── schemas/
│   ├── __init__.py
│   ├── user.py                  # User schemas
│   ├── student.py               # Student schemas
│   ├── faculty.py               # Faculty schemas
│   ├── subject.py               # Subject schemas
│   ├── session.py               # Session schemas
│   ├── attendance.py            # Attendance schemas
│   ├── progress.py              # Progress schemas
│   ├── crm.py                   # CRM schemas
│   ├── feedback.py              # Feedback schemas
│   └── analytics.py             # Analytics schemas
├── api/
│   ├── __init__.py
│   ├── deps.py                  # Dependencies
│   ├── v1/
│   │   ├── __init__.py
│   │   ├── auth.py              # Authentication endpoints
│   │   ├── users.py             # User management
│   │   ├── students.py          # Student endpoints
│   │   ├── faculties.py         # Faculty endpoints
│   │   ├── subjects.py          # Subject endpoints
│   │   ├── sessions.py          # Learning session endpoints
│   │   ├── attendance.py         # Attendance endpoints
│   │   ├── progress.py           # Progress tracking
│   │   ├── crm.py               # CRM endpoints
│   │   ├── feedback.py          # Feedback endpoints
│   │   ├── analytics.py         # Analytics endpoints
│   │   └── reports.py           # Report generation
│   └── websocket/
│       ├── __init__.py
│       ├── attendance.py        # Real-time attendance
│       ├── notifications.py     # Live notifications
│       └── progress.py          # Progress updates
├── services/
│   ├── __init__.py
│   ├── auth.py                  # Authentication service
│   ├── student.py               # Student business logic
│   ├── faculty.py               # Faculty business logic
│   ├── attendance.py            # Attendance service
│   ├── progress.py              # Progress tracking service
│   ├── analytics.py             # Analytics service
│   ├── crm.py                   # CRM service
│   ├── feedback.py              # Feedback service
│   ├── notification.py          # Notification service
│   └── report.py                # Report generation
├── repositories/
│   ├── __init__.py
│   ├── base.py                  # Base repository
│   ├── user.py                  # User repository
│   ├── student.py               # Student repository
│   ├── faculty.py               # Faculty repository
│   ├── subject.py               # Subject repository
│   ├── session.py               # Session repository
│   ├── attendance.py            # Attendance repository
│   ├── progress.py              # Progress repository
│   ├── crm.py                   # CRM repository
│   ├── feedback.py              # Feedback repository
│   └── analytics.py             # Analytics repository
├── utils/
│   ├── __init__.py
│   ├── email.py                 # Email utilities
│   ├── sms.py                   # SMS utilities
│   ├── file_handler.py          # File handling
│   ├── validators.py            # Custom validators
│   ├── helpers.py               # Helper functions
│   └── constants.py             # Application constants
├── tasks/
│   ├── __init__.py
│   ├── celery_app.py            # Celery configuration
│   ├── attendance_tasks.py      # Attendance related tasks
│   ├── notification_tasks.py    # Notification tasks
│   ├── report_tasks.py          # Report generation tasks
│   └── analytics_tasks.py       # Analytics processing tasks
└── tests/
    ├── __init__.py
    ├── conftest.py              # Test configuration
    ├── test_auth.py             # Authentication tests
    ├── test_students.py         # Student tests
    ├── test_faculties.py        # Faculty tests
    ├── test_attendance.py       # Attendance tests
    └── test_analytics.py        # Analytics tests
```

## Core API Endpoints

### 1. Authentication Module

#### Authentication Endpoints
```python
# api/v1/auth.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from schemas.auth import Token, UserCreate, UserResponse
from services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends()
):
    """Authenticate user and return access token"""
    return await auth_service.authenticate(
        username=form_data.username,
        password=form_data.password
    )

@router.post("/register", response_model=UserResponse)
async def register(
    user_data: UserCreate,
    auth_service: AuthService = Depends()
):
    """Register new user"""
    return await auth_service.register(user_data)

@router.post("/refresh", response_model=Token)
async def refresh_token(
    current_user: User = Depends(get_current_user),
    auth_service: AuthService = Depends()
):
    """Refresh access token"""
    return await auth_service.refresh_token(current_user)

@router.post("/logout")
async def logout(
    current_user: User = Depends(get_current_user),
    auth_service: AuthService = Depends()
):
    """Logout user and invalidate token"""
    await auth_service.logout(current_user)
    return {"message": "Successfully logged out"}
```

### 2. Student Management Module

#### Student Endpoints
```python
# api/v1/students.py
from fastapi import APIRouter, Depends, Query
from schemas.student import StudentCreate, StudentUpdate, StudentResponse
from services.student import StudentService

router = APIRouter(prefix="/students", tags=["students"])

@router.post("/", response_model=StudentResponse)
async def create_student(
    student_data: StudentCreate,
    student_service: StudentService = Depends(),
    current_user: User = Depends(get_current_active_user)
):
    """Create new student"""
    return await student_service.create_student(student_data)

@router.get("/", response_model=List[StudentResponse])
async def list_students(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[str] = Query(None),
    student_service: StudentService = Depends(),
    current_user: User = Depends(get_current_active_user)
):
    """List students with pagination and filtering"""
    return await student_service.list_students(
        skip=skip, limit=limit, status=status
    )

@router.get("/{student_id}", response_model=StudentResponse)
async def get_student(
    student_id: int,
    student_service: StudentService = Depends(),
    current_user: User = Depends(get_current_active_user)
):
    """Get student by ID"""
    return await student_service.get_student(student_id)

@router.put("/{student_id}", response_model=StudentResponse)
async def update_student(
    student_id: int,
    student_data: StudentUpdate,
    student_service: StudentService = Depends(),
    current_user: User = Depends(get_current_active_user)
):
    """Update student information"""
    return await student_service.update_student(student_id, student_data)

@router.get("/{student_id}/progress")
async def get_student_progress(
    student_id: int,
    subject_id: Optional[int] = Query(None),
    student_service: StudentService = Depends(),
    current_user: User = Depends(get_current_active_user)
):
    """Get student progress details"""
    return await student_service.get_student_progress(
        student_id, subject_id
    )

@router.get("/{student_id}/attendance")
async def get_student_attendance(
    student_id: int,
    start_date: date = Query(...),
    end_date: date = Query(...),
    student_service: StudentService = Depends(),
    current_user: User = Depends(get_current_active_user)
):
    """Get student attendance records"""
    return await student_service.get_student_attendance(
        student_id, start_date, end_date
    )
```

### 3. Attendance System Module

#### Attendance Endpoints
```python
# api/v1/attendance.py
from fastapi import APIRouter, Depends, BackgroundTasks
from schemas.attendance import AttendanceCreate, AttendanceResponse, BulkAttendance
from services.attendance import AttendanceService

router = APIRouter(prefix="/attendance", tags=["attendance"])

@router.post("/session/{session_id}", response_model=AttendanceResponse)
async def mark_attendance(
    session_id: int,
    attendance_data: AttendanceCreate,
    background_tasks: BackgroundTasks,
    attendance_service: AttendanceService = Depends(),
    current_user: User = Depends(get_current_faculty_user)
):
    """Mark attendance for a student in a session"""
    attendance = await attendance_service.mark_attendance(
        session_id, attendance_data
    )
    
    # Schedule background tasks
    background_tasks.add_task(
        attendance_service.process_attendance_update,
        attendance.id
    )
    
    return attendance

@router.post("/bulk", response_model=List[AttendanceResponse])
async def mark_bulk_attendance(
    bulk_data: BulkAttendance,
    background_tasks: BackgroundTasks,
    attendance_service: AttendanceService = Depends(),
    current_user: User = Depends(get_current_faculty_user)
):
    """Mark attendance for multiple students"""
    attendances = await attendance_service.mark_bulk_attendance(bulk_data)
    
    # Process bulk attendance in background
    background_tasks.add_task(
        attendance_service.process_bulk_attendance,
        [a.id for a in attendances]
    )
    
    return attendances

@router.get("/student/{student_id}")
async def get_student_attendance_summary(
    student_id: int,
    start_date: date = Query(...),
    end_date: date = Query(...),
    attendance_service: AttendanceService = Depends(),
    current_user: User = Depends(get_current_active_user)
):
    """Get attendance summary for student"""
    return await attendance_service.get_attendance_summary(
        student_id, start_date, end_date
    )

@router.get("/faculty/{faculty_id}/today")
async def get_today_attendance(
    faculty_id: int,
    attendance_service: AttendanceService = Depends(),
    current_user: User = Depends(get_current_active_user)
):
    """Get today's attendance for faculty"""
    return await attendance_service.get_today_attendance(faculty_id)

@router.get("/analytics/absenteeism")
async def get_absenteeism_report(
    start_date: date = Query(...),
    end_date: date = Query(...),
    threshold_days: int = Query(5),
    attendance_service: AttendanceService = Depends(),
    current_user: User = Depends(get_current_admin_user)
):
    """Get absenteeism report for irregular students"""
    return await attendance_service.get_absenteeism_report(
        start_date, end_date, threshold_days
    )
```

### 4. Analytics Module

#### Analytics Endpoints
```python
# api/v1/analytics.py
from fastapi import APIRouter, Depends, Query
from schemas.analytics import (
    StudentProgressAnalytics,
    FacultyPerformanceAnalytics,
    InstituteAnalytics
)
from services.analytics import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/student/{student_id}/progress")
async def get_student_progress_analytics(
    student_id: int,
    time_period: str = Query("month", regex="^(week|month|quarter|year)$"),
    analytics_service: AnalyticsService = Depends(),
    current_user: User = Depends(get_current_active_user)
):
    """Get detailed progress analytics for student"""
    return await analytics_service.get_student_progress_analytics(
        student_id, time_period
    )

@router.get("/faculty/{faculty_id}/performance")
async def get_faculty_performance_analytics(
    faculty_id: int,
    time_period: str = Query("month", regex="^(week|month|quarter|year)$"),
    analytics_service: AnalyticsService = Depends(),
    current_user: User = Depends(get_current_active_user)
):
    """Get performance analytics for faculty"""
    return await analytics_service.get_faculty_performance_analytics(
        faculty_id, time_period
    )

@router.get("/institute/overview")
async def get_institute_analytics(
    time_period: str = Query("month", regex="^(week|month|quarter|year)$"),
    analytics_service: AnalyticsService = Depends(),
    current_user: User = Depends(get_current_admin_user)
):
    """Get institute-level analytics"""
    return await analytics_service.get_institute_analytics(time_period)

@router.get("/predictions/completion")
async def get_completion_predictions(
    student_ids: List[int] = Query(...),
    analytics_service: AnalyticsService = Depends(),
    current_user: User = Depends(get_current_active_user)
):
    """Get completion predictions for students"""
    return await analytics_service.predict_completion_dates(student_ids)

@router.get("/trends/learning-velocity")
async def get_learning_velocity_trends(
    subject_id: Optional[int] = Query(None),
    time_period: str = Query("quarter", regex="^(month|quarter|year)$"),
    analytics_service: AnalyticsService = Depends(),
    current_user: User = Depends(get_current_active_user)
):
    """Get learning velocity trends"""
    return await analytics_service.get_learning_velocity_trends(
        subject_id, time_period
    )
```

### 5. CRM Module

#### CRM Endpoints
```python
# api/v1/crm.py
from fastapi import APIRouter, Depends, BackgroundTasks
from schemas.crm import (
    InquiryCreate, InquiryUpdate, InquiryResponse,
    FollowUpCreate, FollowUpResponse
)
from services.crm import CRMService

router = APIRouter(prefix="/crm", tags=["crm"])

@router.post("/inquiries", response_model=InquiryResponse)
async def create_inquiry(
    inquiry_data: InquiryCreate,
    background_tasks: BackgroundTasks,
    crm_service: CRMService = Depends(),
    current_user: User = Depends(get_current_counselor_user)
):
    """Create new inquiry"""
    inquiry = await crm_service.create_inquiry(inquiry_data)
    
    # Schedule follow-up reminders
    background_tasks.add_task(
        crm_service.schedule_initial_follow_up,
        inquiry.id
    )
    
    return inquiry

@router.get("/inquiries", response_model=List[InquiryResponse])
async def list_inquiries(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[str] = Query(None),
    counselor_id: Optional[int] = Query(None),
    crm_service: CRMService = Depends(),
    current_user: User = Depends(get_current_counselor_user)
):
    """List inquiries with filtering"""
    return await crm_service.list_inquiries(
        skip, limit, status, counselor_id
    )

@router.post("/inquiries/{inquiry_id}/follow-ups", response_model=FollowUpResponse)
async def create_follow_up(
    inquiry_id: int,
    follow_up_data: FollowUpCreate,
    background_tasks: BackgroundTasks,
    crm_service: CRMService = Depends(),
    current_user: User = Depends(get_current_counselor_user)
):
    """Create follow-up for inquiry"""
    follow_up = await crm_service.create_follow_up(inquiry_id, follow_up_data)
    
    # Schedule notification
    background_tasks.add_task(
        crm_service.schedule_follow_up_reminder,
        follow_up.id
    )
    
    return follow_up

@router.get("/analytics/conversion")
async def get_conversion_analytics(
    time_period: str = Query("month", regex="^(week|month|quarter|year)$"),
    crm_service: CRMService = Depends(),
    current_user: User = Depends(get_current_counselor_user)
):
    """Get conversion analytics"""
    return await crm_service.get_conversion_analytics(time_period)

@router.get("/pipeline/health")
async def get_pipeline_health(
    crm_service: CRMService = Depends(),
    current_user: User = Depends(get_current_counselor_user)
):
    """Get CRM pipeline health metrics"""
    return await crm_service.get_pipeline_health()
```

## WebSocket Endpoints

### Real-time Attendance Updates
```python
# api/websocket/attendance.py
from fastapi import WebSocket, WebSocketDisconnect, Depends
from services.websocket_manager import WebSocketManager
from core.auth import get_current_user_websocket

manager = WebSocketManager()

@router.websocket("/attendance/{session_id}")
async def attendance_websocket(
    websocket: WebSocket,
    session_id: int,
    token: str = None
):
    """WebSocket for real-time attendance updates"""
    user = await get_current_user_websocket(token)
    await manager.connect(websocket, session_id, user)
    
    try:
        while True:
            data = await websocket.receive_json()
            
            # Process attendance update
            if data["type"] == "attendance_marked":
                await manager.broadcast_to_session(
                    session_id,
                    {
                        "type": "attendance_update",
                        "student_id": data["student_id"],
                        "status": data["status"],
                        "timestamp": datetime.utcnow().isoformat()
                    }
                )
            
            # Handle other real-time events
            elif data["type"] == "topic_completed":
                await manager.broadcast_to_session(
                    session_id,
                    {
                        "type": "progress_update",
                        "student_id": data["student_id"],
                        "topic_id": data["topic_id"],
                        "progress": data["progress"]
                    }
                )
                
    except WebSocketDisconnect:
        manager.disconnect(websocket, session_id)
```

## Service Layer Architecture

### Base Service Pattern
```python
# services/base.py
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Type, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")

class BaseService(Generic[ModelType, CreateSchemaType, UpdateSchemaType], ABC):
    def __init__(
        self,
        model: Type[ModelType],
        db_session: AsyncSession
    ):
        self.model = model
        self.db_session = db_session
    
    async def get(self, id: int) -> Optional[ModelType]:
        """Get single record by ID"""
        result = await self.db_session.get(self.model, id)
        return result
    
    async def get_multi(
        self,
        skip: int = 0,
        limit: int = 100
    ) -> List[ModelType]:
        """Get multiple records with pagination"""
        statement = select(self.model).offset(skip).limit(limit)
        result = await self.db_session.execute(statement)
        return result.scalars().all()
    
    async def create(
        self,
        obj_in: CreateSchemaType
    ) -> ModelType:
        """Create new record"""
        obj_data = obj_in.dict()
        db_obj = self.model(**obj_data)
        self.db_session.add(db_obj)
        await self.db_session.commit()
        await self.db_session.refresh(db_obj)
        return db_obj
    
    async def update(
        self,
        db_obj: ModelType,
        obj_in: UpdateSchemaType
    ) -> ModelType:
        """Update existing record"""
        obj_data = obj_in.dict(exclude_unset=True)
        for field, value in obj_data.items():
            setattr(db_obj, field, value)
        
        self.db_session.add(db_obj)
        await self.db_session.commit()
        await self.db_session.refresh(db_obj)
        return db_obj
    
    async def delete(self, id: int) -> ModelType:
        """Delete record by ID"""
        obj = await self.get(id)
        await self.db_session.delete(obj)
        await self.db_session.commit()
        return obj
```

## Database Configuration

### SQLAlchemy Setup
```python
# config/database.py
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from config.settings import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_recycle=300,
)

AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db() -> AsyncSession:
    """Dependency to get database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
```

## Authentication & Authorization

### JWT Configuration
```python
# core/auth.py
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from config.settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None
) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt

def verify_token(token: str) -> Optional[str]:
    """Verify JWT token and return username"""
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            return None
        return username
    except JWTError:
        return None
```

## Error Handling

### Custom Exceptions
```python
# core/exceptions.py
from fastapi import HTTPException

class CustomException(Exception):
    """Base custom exception"""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class NotFoundException(CustomException):
    """Resource not found exception"""
    def __init__(self, resource: str):
        super().__init__(
            f"{resource} not found",
            status_code=404
        )

class UnauthorizedException(CustomException):
    """Unauthorized access exception"""
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(
            message,
            status_code=401
        )

class ForbiddenException(CustomException):
    """Forbidden access exception"""
    def __init__(self, message: str = "Forbidden"):
        super().__init__(
            message,
            status_code=403
        )

class ValidationException(CustomException):
    """Validation error exception"""
    def __init__(self, message: str):
        super().__init__(
            f"Validation error: {message}",
            status_code=422
        )
```

## Performance Optimizations

### Caching Strategy
```python
# utils/cache.py
from functools import wraps
import json
import redis.asyncio as redis
from config.settings import settings

redis_client = redis.from_url(settings.REDIS_URL)

def cache_result(expire: int = 3600):
    """Decorator to cache function results"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"
            
            # Try to get from cache
            cached_result = await redis_client.get(cache_key)
            if cached_result:
                return json.loads(cached_result)
            
            # Execute function and cache result
            result = await func(*args, **kwargs)
            await redis_client.setex(
                cache_key,
                expire,
                json.dumps(result, default=str)
            )
            
            return result
        return wrapper
    return decorator
```

This FastAPI architecture provides a robust, scalable foundation for the student academics management system with comprehensive API coverage for all major functionalities.