"""
Batch model for managing student batches and schedules
"""

from sqlalchemy import Column, Integer, String, Date, Text, Enum, ForeignKey, JSON, Numeric
from sqlalchemy.orm import relationship
import enum

from app.models.base import BaseModel


class BatchStatus(str, enum.Enum):
    """Batch status enumeration"""
    PLANNED = "planned"
    ACTIVE = "active"
    COMPLETED = "completed"
    SUSPENDED = "suspended"
    CANCELLED = "cancelled"


class Batch(BaseModel):
    """
    Batch model for managing student batches
    """
    __tablename__ = "batches"

    name = Column(String(100), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    faculty_id = Column(Integer, ForeignKey("faculty.user_id"), nullable=False)
    center_id = Column(Integer, ForeignKey("centers.id"), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    schedule = Column(JSON)  # Store complex schedule as JSON
    max_students = Column(Integer, default=30, nullable=False)
    current_students = Column(Integer, default=0)
    status = Column(Enum(BatchStatus), default=BatchStatus.PLANNED)
    created_by = Column(Integer, ForeignKey("users.id"))

    # Relationships
    subject = relationship("Subject", back_populates="batches")
    faculty = relationship("Faculty", back_populates="batches")
    center = relationship("Center", back_populates="batches")
    creator = relationship("User", foreign_keys=[created_by], back_populates="created_batches")
    student_batches = relationship("StudentBatch", back_populates="batch", cascade="all, delete-orphan")
    attendance_records = relationship("Attendance", back_populates="batch")
    batch_topics = relationship("BatchTopic", back_populates="batch", cascade="all, delete-orphan")
    extensions = relationship("BatchExtension", back_populates="batch")

    def __repr__(self):
        return f"<Batch(id={self.id}, name={self.name}, status={self.status})>"

    def is_active(self):
        """Check if batch is active"""
        return self.status == BatchStatus.ACTIVE

    def is_completed(self):
        """Check if batch is completed"""
        return self.status == BatchStatus.COMPLETED

    def get_active_students(self):
        """Get active students in this batch"""
        return [sb for sb in self.student_batches if sb.is_active()]

    def get_completed_students(self):
        """Get completed students in this batch"""
        return [sb for sb in self.student_batches if sb.status == "completed"]

    def get_dropped_students(self):
        """Get dropped students from this batch"""
        return [sb for sb in self.student_batches if sb.status == "dropped"]

    def is_full(self):
        """Check if batch is at maximum capacity"""
        return self.current_students >= self.max_students

    def get_available_slots(self):
        """Get number of available slots in batch"""
        return max(0, self.max_students - self.current_students)

    def get_enrollment_rate(self):
        """Get enrollment rate as percentage"""
        if self.max_students == 0:
            return 0.0
        return (self.current_students / self.max_students) * 100

    def get_completion_rate(self):
        """Get student completion rate for this batch"""
        total_students = len(self.student_batches)
        if total_students == 0:
            return 0.0
        
        completed_students = len(self.get_completed_students())
        return (completed_students / total_students) * 100

    def get_average_progress(self):
        """Get average progress of all students in batch"""
        active_students = self.get_active_students()
        if not active_students:
            return 0.0
        
        total_progress = sum(sb.progress_percentage or 0 for sb in active_students)
        return total_progress / len(active_students)

    def get_attendance_percentage(self, date_range=None):
        """Get attendance percentage for the batch"""
        attendance = self.attendance_records
        if date_range:
            # Filter by date range if provided
            attendance = [
                att for att in attendance 
                if date_range[0] <= att.date <= date_range[1]
            ]
        
        if not attendance:
            return 0.0
        
        present_count = len([
            att for att in attendance 
            if att.status == "present"
        ])
        
        return (present_count / len(attendance)) * 100

    def get_completed_topics(self):
        """Get completed topics for this batch"""
        return [bt for bt in self.batch_topics if bt.status == "completed"]

    def get_pending_topics(self):
        """Get pending topics for this batch"""
        return [bt for bt in self.batch_topics if bt.status == "pending"]

    def get_in_progress_topics(self):
        """Get topics currently in progress"""
        return [bt for bt in self.batch_topics if bt.status == "in_progress"]

    def get_syllabus_completion_percentage(self):
        """Get syllabus completion percentage"""
        if not self.batch_topics:
            return 0.0
        
        completed_topics = len(self.get_completed_topics())
        return (completed_topics / len(self.batch_topics)) * 100

    def get_duration_days(self):
        """Get batch duration in days"""
        if not self.end_date:
            return 0
        return (self.end_date - self.start_date).days

    def get_schedule_summary(self):
        """Get human-readable schedule summary"""
        if not self.schedule:
            return "No schedule set"
        
        # Parse JSON schedule and return summary
        days = self.schedule.get("days", [])
        times = self.schedule.get("times", [])
        
        if not days and not times:
            return "No schedule set"
        
        schedule_parts = []
        if days:
            schedule_parts.append(f"Days: {', '.join(days)}")
        if times:
            schedule_parts.append(f"Time: {', '.join(times)}")
        
        return " | ".join(schedule_parts)

    def can_be_extended(self):
        """Check if batch can be extended"""
        return self.status in [BatchStatus.ACTIVE, BatchStatus.SUSPENDED]

    def has_active_extensions(self):
        """Check if batch has active extension requests"""
        return any(
            ext.status == "pending" 
            for ext in self.extensions
        )

    def get_average_feedback_rating(self):
        """Get average feedback rating for this batch"""
        feedback = [
            fb for fb in self.attendance_records 
            if hasattr(fb, 'feedback') and fb.feedback
        ]
        
        if not feedback:
            return 0.0
        
        total_rating = sum(fb.feedback.rating for fb in feedback)
        return total_rating / len(feedback)

    def get_upcoming_classes(self, days=7):
        """Get upcoming classes within specified days"""
        from datetime import date, timedelta
        
        upcoming_date = date.today() + timedelta(days=days)
        
        # This would need to be implemented based on schedule logic
        # For now, return empty list
        return []

    def get_recent_attendance(self, days=7):
        """Get recent attendance records"""
        from datetime import date, timedelta
        
        recent_date = date.today() - timedelta(days=days)
        
        return [
            att for att in self.attendance_records 
            if att.date >= recent_date
        ]