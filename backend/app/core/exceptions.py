"""
Custom exceptions for the Student Academics Management System
"""

from typing import Any, Dict, Optional


class CustomException(Exception):
    """
    Base custom exception class
    """
    
    def __init__(
        self,
        message: str,
        status_code: int = 500,
        error_code: str = "INTERNAL_ERROR",
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)


class AuthenticationError(CustomException):
    """Authentication related errors"""
    
    def __init__(self, message: str = "Authentication failed", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=401,
            error_code="AUTHENTICATION_ERROR",
            details=details
        )


class AuthorizationError(CustomException):
    """Authorization related errors"""
    
    def __init__(self, message: str = "Access denied", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=403,
            error_code="AUTHORIZATION_ERROR",
            details=details
        )


class ValidationError(CustomException):
    """Validation related errors"""
    
    def __init__(self, message: str = "Validation failed", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=422,
            error_code="VALIDATION_ERROR",
            details=details
        )


class NotFoundError(CustomException):
    """Resource not found errors"""
    
    def __init__(self, message: str = "Resource not found", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=404,
            error_code="NOT_FOUND_ERROR",
            details=details
        )


class ConflictError(CustomException):
    """Conflict errors (e.g., duplicate resources)"""
    
    def __init__(self, message: str = "Resource conflict", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=409,
            error_code="CONFLICT_ERROR",
            details=details
        )


class BusinessLogicError(CustomException):
    """Business logic validation errors"""
    
    def __init__(self, message: str = "Business rule violation", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=400,
            error_code="BUSINESS_LOGIC_ERROR",
            details=details
        )


class DatabaseError(CustomException):
    """Database related errors"""
    
    def __init__(self, message: str = "Database operation failed", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=500,
            error_code="DATABASE_ERROR",
            details=details
        )


class ExternalServiceError(CustomException):
    """External service integration errors"""
    
    def __init__(self, message: str = "External service error", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=502,
            error_code="EXTERNAL_SERVICE_ERROR",
            details=details
        )


class RateLimitError(CustomException):
    """Rate limiting errors"""
    
    def __init__(self, message: str = "Rate limit exceeded", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=429,
            error_code="RATE_LIMIT_ERROR",
            details=details
        )


class FileUploadError(CustomException):
    """File upload related errors"""
    
    def __init__(self, message: str = "File upload failed", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=400,
            error_code="FILE_UPLOAD_ERROR",
            details=details
        )


class EmailError(CustomException):
    """Email sending errors"""
    
    def __init__(self, message: str = "Email sending failed", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=500,
            error_code="EMAIL_ERROR",
            details=details
        )


class SMSError(CustomException):
    """SMS sending errors"""
    
    def __init__(self, message: str = "SMS sending failed", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=500,
            error_code="SMS_ERROR",
            details=details
        )


class CacheError(CustomException):
    """Cache related errors"""
    
    def __init__(self, message: str = "Cache operation failed", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=500,
            error_code="CACHE_ERROR",
            details=details
        )


class ConfigurationError(CustomException):
    """Configuration related errors"""
    
    def __init__(self, message: str = "Configuration error", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=500,
            error_code="CONFIGURATION_ERROR",
            details=details
        )


# Specific business logic exceptions
class StudentNotFoundError(NotFoundError):
    """Student not found"""
    
    def __init__(self, student_id: int):
        super().__init__(
            message=f"Student with ID {student_id} not found",
            details={"student_id": student_id}
        )


class FacultyNotFoundError(NotFoundError):
    """Faculty not found"""
    
    def __init__(self, faculty_id: int):
        super().__init__(
            message=f"Faculty with ID {faculty_id} not found",
            details={"faculty_id": faculty_id}
        )


class BatchNotFoundError(NotFoundError):
    """Batch not found"""
    
    def __init__(self, batch_id: int):
        super().__init__(
            message=f"Batch with ID {batch_id} not found",
            details={"batch_id": batch_id}
        )


class SubjectNotFoundError(NotFoundError):
    """Subject not found"""
    
    def __init__(self, subject_id: int):
        super().__init__(
            message=f"Subject with ID {subject_id} not found",
            details={"subject_id": subject_id}
        )


class CenterNotFoundError(NotFoundError):
    """Center not found"""
    
    def __init__(self, center_id: int):
        super().__init__(
            message=f"Center with ID {center_id} not found",
            details={"center_id": center_id}
        )


class BatchFullError(BusinessLogicError):
    """Batch is full"""
    
    def __init__(self, batch_id: int, max_students: int):
        super().__init__(
            message=f"Batch {batch_id} is full (max {max_students} students)",
            details={"batch_id": batch_id, "max_students": max_students}
        )


class InvalidEnrollmentError(BusinessLogicError):
    """Invalid enrollment attempt"""
    
    def __init__(self, reason: str):
        super().__init__(
            message=f"Invalid enrollment: {reason}",
            details={"reason": reason}
        )


class DuplicateEnrollmentError(ConflictError):
    """Duplicate enrollment attempt"""
    
    def __init__(self, student_id: int, batch_id: int):
        super().__init__(
            message=f"Student {student_id} is already enrolled in batch {batch_id}",
            details={"student_id": student_id, "batch_id": batch_id}
        )


class AttendanceAlreadyMarkedError(ConflictError):
    """Attendance already marked"""
    
    def __init__(self, student_id: int, date: str):
        super().__init__(
            message=f"Attendance for student {student_id} on {date} is already marked",
            details={"student_id": student_id, "date": date}
        )


class InvalidAttendanceDateError(BusinessLogicError):
    """Invalid attendance date"""
    
    def __init__(self, date: str, reason: str):
        super().__init__(
            message=f"Invalid attendance date {date}: {reason}",
            details={"date": date, "reason": reason}
        )


class InsufficientPermissionsError(AuthorizationError):
    """Insufficient permissions"""
    
    def __init__(self, required_permission: str):
        super().__init__(
            message=f"Insufficient permissions. Required: {required_permission}",
            details={"required_permission": required_permission}
        )


class CenterAccessDeniedError(AuthorizationError):
    """Access denied for center"""
    
    def __init__(self, center_id: int):
        super().__init__(
            message=f"Access denied for center {center_id}",
            details={"center_id": center_id}
        )


class InvalidRoleError(BusinessLogicError):
    """Invalid user role"""
    
    def __init__(self, role: str):
        super().__init__(
            message=f"Invalid role: {role}",
            details={"role": role}
        )


class PasswordMismatchError(AuthenticationError):
    """Password mismatch"""
    
    def __init__(self):
        super().__init__(
            message="Current password does not match",
            details={"field": "current_password"}
        )


class WeakPasswordError(ValidationError):
    """Weak password"""
    
    def __init__(self, requirements: list):
        super().__init__(
            message="Password does not meet requirements",
            details={"requirements": requirements}
        )


class EmailAlreadyExistsError(ConflictError):
    """Email already exists"""
    
    def __init__(self, email: str):
        super().__init__(
            message=f"Email {email} already exists",
            details={"email": email}
        )


class InvalidTokenError(AuthenticationError):
    """Invalid token"""
    
    def __init__(self, token_type: str = "access"):
        super().__init__(
            message=f"Invalid {token_type} token",
            details={"token_type": token_type}
        )


class TokenExpiredError(AuthenticationError):
    """Token expired"""
    
    def __init__(self, token_type: str = "access"):
        super().__init__(
            message=f"{token_type.capitalize()} token has expired",
            details={"token_type": token_type}
        )