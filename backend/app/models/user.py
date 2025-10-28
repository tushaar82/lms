"""
User model for authentication and authorization
"""

from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import enum

from app.models.base import BaseModel


class UserRole(str, enum.Enum):
    """User roles enumeration"""
    SUPER_ADMIN = "super_admin"
    CENTER_ADMIN = "center_admin"
    FACULTY = "faculty"
    ACADEMIC_HEAD = "academic_head"
    STUDENT = "student"


class UserStatus(str, enum.Enum):
    """User status enumeration"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"


class User(BaseModel):
    """
    User model for authentication and basic user information
    """
    __tablename__ = "users"

    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    phone = Column(String(20))
    role = Column(Enum(UserRole), nullable=False)
    center_id = Column(Integer, ForeignKey("centers.id"), nullable=True)
    profile_image = Column(String(255))
    last_login = Column(DateTime)
    status = Column(Enum(UserStatus), default=UserStatus.ACTIVE)

    # Relationships
    center = relationship("Center", back_populates="users")
    student_profile = relationship("Student", back_populates="user", uselist=False)
    faculty_profile = relationship("Faculty", back_populates="user", uselist=False)
    
    # Relationships for entities created by this user
    created_batches = relationship("Batch", foreign_keys="Batch.created_by", back_populates="creator")
    given_feedback = relationship("Feedback", back_populates="student")
    received_feedback = relationship("Feedback", back_populates="faculty")
    notifications = relationship("Notification", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"

    @property
    def full_name(self):
        """Get user's full name"""
        return f"{self.first_name} {self.last_name}"

    def is_active(self):
        """Check if user is active"""
        return self.status == UserStatus.ACTIVE

    def is_admin(self):
        """Check if user has admin privileges"""
        return self.role in [UserRole.SUPER_ADMIN, UserRole.CENTER_ADMIN]

    def is_faculty(self):
        """Check if user is faculty"""
        return self.role == UserRole.FACULTY

    def is_student(self):
        """Check if user is student"""
        return self.role == UserRole.STUDENT

    def can_access_center(self, center_id: int) -> bool:
        """Check if user can access a specific center"""
        if self.role == UserRole.SUPER_ADMIN:
            return True
        return self.center_id == center_id