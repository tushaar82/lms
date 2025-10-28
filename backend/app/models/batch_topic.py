"""
BatchTopic model for managing topic scheduling within batches
"""

from sqlalchemy import Column, Integer, Date, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship
import enum

from app.models.base import BaseModel


class BatchTopicStatus(str, enum.Enum):
    """Batch topic status enumeration"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    SKIPPED = "skipped"


class BatchTopic(BaseModel):
    """
    BatchTopic model for managing topic scheduling within batches
    """
    __tablename__ = "batch_topics"

    batch_id = Column(Integer, ForeignKey("batches.id"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    scheduled_date = Column(Date)
    completed_date = Column(Date)
    faculty_id = Column(Integer, ForeignKey("faculty.user_id"), nullable=False)
    status = Column(Enum(BatchTopicStatus), default=BatchTopicStatus.PENDING)
    notes = Column(Text)

    # Relationships
    batch = relationship("Batch", back_populates="batch_topics")
    topic = relationship("Topic", back_populates="batch_topics")
    faculty = relationship("Faculty", back_populates="batch_topics")

    def __repr__(self):
        return f"<BatchTopic(id={self.id}, batch_id={self.batch_id}, topic_id={self.topic_id}, status={self.status})>"

    def is_pending(self):
        """Check if topic is pending"""
        return self.status == BatchTopicStatus.PENDING

    def is_in_progress(self):
        """Check if topic is in progress"""
        return self.status == BatchTopicStatus.IN_PROGRESS

    def is_completed(self):
        """Check if topic is completed"""
        return self.status == BatchTopicStatus.COMPLETED

    def is_skipped(self):
        """Check if topic was skipped"""
        return self.status == BatchTopicStatus.SKIPPED

    def start_topic(self, faculty_id=None):
        """Mark topic as in progress"""
        self.status = BatchTopicStatus.IN_PROGRESS
        if faculty_id:
            self.faculty_id = faculty_id

    def complete_topic(self, notes=None):
        """Mark topic as completed"""
        self.status = BatchTopicStatus.COMPLETED
        self.completed_date = self.updated_at.date()
        if notes:
            self.notes = notes

    def skip_topic(self, notes=None):
        """Skip topic"""
        self.status = BatchTopicStatus.SKIPPED
        if notes:
            self.notes = notes

    def get_duration_days(self):
        """Get duration taken to complete the topic"""
        if not self.scheduled_date or not self.completed_date:
            return 0
        return (self.completed_date - self.scheduled_date).days

    def get_duration_hours(self):
        """Get duration in hours (from topic definition)"""
        return self.topic.duration_hours if self.topic else 0

    def is_overdue(self):
        """Check if topic is overdue (not completed and past scheduled date)"""
        if self.is_completed() or self.is_skipped():
            return False
        
        if not self.scheduled_date:
            return False
        
        from datetime import date
        return self.scheduled_date < date.today()

    def get_overdue_days(self):
        """Get number of days overdue"""
        if not self.is_overdue():
            return 0
        
        from datetime import date
        return (date.today() - self.scheduled_date).days

    def can_be_started(self):
        """Check if topic can be started"""
        if self.is_completed() or self.is_skipped():
            return False
        
        # Check if prerequisites are completed
        if self.topic.prerequisites:
            # This would need to check if prerequisite topics are completed
            # For now, return True
            pass
        
        return True

    def get_attendance_records(self):
        """Get attendance records for this topic session"""
        return [
            att for att in self.batch.attendance_records 
            if att.topic_covered and self.topic.name in att.topic_covered
        ]

    def get_attendance_percentage(self):
        """Get attendance percentage for this topic"""
        attendance = self.get_attendance_records()
        if not attendance:
            return 0.0
        
        present_count = len([
            att for att in attendance 
            if att.status == "present"
        ])
        
        return (present_count / len(attendance)) * 100

    def get_student_progress(self, student_id):
        """Get progress for a specific student in this topic"""
        # This would need to be implemented based on student-specific progress tracking
        # For now, return basic status
        return {
            "status": self.status,
            "completed_date": self.completed_date,
            "notes": self.notes
        }

    def add_note(self, note):
        """Add a note to the topic"""
        if not self.notes:
            self.notes = note
        else:
            self.notes += f"\n\n{note}"

    def get_summary(self):
        """Get summary of the batch topic"""
        return {
            "topic_name": self.topic.name if self.topic else "Unknown",
            "scheduled_date": self.scheduled_date,
            "completed_date": self.completed_date,
            "status": self.status,
            "faculty_name": self.faculty.full_name if self.faculty else "Unknown",
            "duration_hours": self.get_duration_hours(),
            "duration_days": self.get_duration_days(),
            "attendance_percentage": self.get_attendance_percentage(),
            "notes": self.notes
        }

    def reschedule(self, new_date, notes=None):
        """Reschedule the topic to a new date"""
        self.scheduled_date = new_date
        if notes:
            self.add_note(f"Rescheduled: {notes}")
        else:
            self.add_note(f"Rescheduled to {new_date}")

    def assign_faculty(self, faculty_id, notes=None):
        """Assign a different faculty to this topic"""
        old_faculty_name = self.faculty.full_name if self.faculty else "Unassigned"
        self.faculty_id = faculty_id
        
        if notes:
            self.add_note(f"Faculty changed from {old_faculty_name}: {notes}")
        else:
            self.add_note(f"Faculty changed from {old_faculty_name}")

    def get_prerequisite_status(self):
        """Get status of prerequisite topics"""
        if not self.topic or not self.topic.prerequisites:
            return {"completed": True, "pending": []}
        
        # This would need to check actual prerequisite completion
        # For now, return as completed
        return {"completed": True, "pending": []}

    def calculate_completion_rate(self):
        """Calculate completion rate for this topic across all batches"""
        # This would need to query all batch topics for this topic
        # For now, return current status
        return 100.0 if self.is_completed() else 0.0