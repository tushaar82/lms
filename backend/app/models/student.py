"""
Student model for student-specific information and management
"""

from sqlalchemy import Column, Integer, String, Date, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship
import enum

from app.models.base import BaseModel


class StudentStatus(str, enum.Enum):
    """Student status enumeration"""
    ACTIVE = "active"
    COMPLETED = "completed"
    DROPPED = "dropped"
    SUSPENDED = "suspended"


class Gender(str, enum.Enum):
    """Gender enumeration"""
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class Student(BaseModel):
    """
    Student model for student-specific information
    """
    __tablename__ = "students"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    enrollment_number = Column(String(20), unique=True, nullable=False, index=True)
    date_of_birth = Column(Date)
    gender = Column(Enum(Gender))
    address = Column(Text)
    emergency_contact_name = Column(String(100))
    emergency_contact_phone = Column(String(20))
    education_background = Column(Text)
    previous_experience = Column(Text)
    enrollment_date = Column(Date, nullable=False)
    status = Column(Enum(StudentStatus), default=StudentStatus.ACTIVE)

    # Relationships
    user = relationship("User", back_populates="student_profile")
    batches = relationship("StudentBatch", back_populates="student")
    attendance_records = relationship("Attendance", back_populates="student")
    given_feedback = relationship("Feedback", back_populates="student")
    centers = relationship("Center", secondary="student_batches", back_populates="students")
    leave_requests = relationship("StudentLeave", back_populates="student")

    def __repr__(self):
        return f"<Student(id={self.user_id}, enrollment_number={self.enrollment_number})>"

    @property
    def full_name(self):
        """Get student's full name"""
        return self.user.full_name if self.user else ""

    @property
    def email(self):
        """Get student's email"""
        return self.user.email if self.user else ""

    @property
    def phone(self):
        """Get student's phone"""
        return self.user.phone if self.user else ""

    def is_active(self):
        """Check if student is active"""
        return self.status == StudentStatus.ACTIVE

    def get_active_batches(self):
        """Get student's active batches"""
        return [sb for sb in self.batches if sb.is_active()]

    def get_completed_batches(self):
        """Get student's completed batches"""
        return [sb for sb in self.batches if sb.status == "completed"]

    def get_current_progress(self):
        """Get overall progress across all active batches"""
        active_batches = self.get_active_batches()
        if not active_batches:
            return 0.0
        total_progress = sum(sb.progress_percentage or 0 for sb in active_batches)
        return total_progress / len(active_batches)

    def get_attendance_percentage(self, batch_id=None):
        """Get attendance percentage for a specific batch or overall"""
        if batch_id:
            batch_attendance = [
                att for att in self.attendance_records 
                if att.batch_id == batch_id
            ]
        else:
            batch_attendance = self.attendance_records

        if not batch_attendance:
            return 0.0

        present_count = len([
            att for att in batch_attendance 
            if att.status == "present"
        ])
        return (present_count / len(batch_attendance)) * 100

    def get_average_feedback_rating(self):
        """Get average feedback rating given by student"""
        feedback_given = self.given_feedback
        if not feedback_given:
            return 0.0
        
        total_rating = sum(fb.rating for fb in feedback_given)
        return total_rating / len(feedback_given)