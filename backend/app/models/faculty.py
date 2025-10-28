"""
Faculty model for faculty-specific information and management
"""

from sqlalchemy import Column, Integer, String, Date, Text, Enum, ForeignKey, Numeric
from sqlalchemy.orm import relationship
import enum

from app.models.base import BaseModel


class FacultyStatus(str, enum.Enum):
    """Faculty status enumeration"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    ON_LEAVE = "on_leave"


class Faculty(BaseModel):
    """
    Faculty model for faculty-specific information
    """
    __tablename__ = "faculty"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    employee_id = Column(String(20), unique=True, nullable=False, index=True)
    specialization = Column(Text)
    qualification = Column(Text)
    experience_years = Column(Numeric(3, 1))
    previous_company = Column(Text)
    joining_date = Column(Date, nullable=False)
    salary = Column(Numeric(10, 2))
    bank_details = Column(Text)
    status = Column(Enum(FacultyStatus), default=FacultyStatus.ACTIVE)

    # Relationships
    user = relationship("User", back_populates="faculty_profile")
    center = relationship("Center", back_populates="faculty")
    batches = relationship("Batch", back_populates="faculty")
    attendance_records = relationship("Attendance", back_populates="faculty")
    batch_topics = relationship("BatchTopic", back_populates="faculty")
    received_feedback = relationship("Feedback", back_populates="faculty")
    availability = relationship("FacultyAvailability", back_populates="faculty")
    performance_records = relationship("FacultyPerformance", back_populates="faculty")

    def __repr__(self):
        return f"<Faculty(id={self.user_id}, employee_id={self.employee_id})>"

    @property
    def full_name(self):
        """Get faculty's full name"""
        return self.user.full_name if self.user else ""

    @property
    def email(self):
        """Get faculty's email"""
        return self.user.email if self.user else ""

    @property
    def phone(self):
        """Get faculty's phone"""
        return self.user.phone if self.user else ""

    def is_active(self):
        """Check if faculty is active"""
        return self.status == FacultyStatus.ACTIVE

    def get_active_batches(self):
        """Get faculty's active batches"""
        return [batch for batch in self.batches if batch.is_active()]

    def get_completed_batches(self):
        """Get faculty's completed batches"""
        return [batch for batch in self.batches if batch.status == "completed"]

    def get_total_students_taught(self):
        """Get total number of students taught by this faculty"""
        total_students = 0
        for batch in self.batches:
            total_students += len(batch.students)
        return total_students

    def get_completed_students_count(self):
        """Get number of students who completed batches with this faculty"""
        completed_students = 0
        for batch in self.get_completed_batches():
            completed_students += len([
                sb for sb in batch.student_batches 
                if sb.status == "completed"
            ])
        return completed_students

    def get_average_feedback_rating(self):
        """Get average feedback rating received by faculty"""
        feedback_received = self.received_feedback
        if not feedback_received:
            return 0.0
        
        total_rating = sum(fb.rating for fb in feedback_received)
        return total_rating / len(feedback_received)

    def get_completion_rate(self):
        """Get student completion rate for this faculty"""
        total_students = self.get_total_students_taught()
        if total_students == 0:
            return 0.0
        
        completed_students = self.get_completed_students_count()
        return (completed_students / total_students) * 100

    def get_workload_percentage(self):
        """Get current workload as percentage of maximum capacity"""
        active_batches = self.get_active_batches()
        # Assuming maximum of 5 batches per faculty
        max_batches = 5
        return (len(active_batches) / max_batches) * 100

    def get_specialization_list(self):
        """Get list of specializations"""
        if not self.specialization:
            return []
        return [spec.strip() for spec in self.specialization.split(",")]

    def is_available_on_date(self, date):
        """Check if faculty is available on a specific date"""
        availability = self.availability
        for avail in availability:
            if avail.date == date and avail.status == "available":
                return True
        return False

    def get_total_classes_taken(self):
        """Get total number of classes taken by this faculty"""
        return len(self.attendance_records)