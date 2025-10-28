"""
BatchSubtopic model for managing subtopic scheduling within batches
"""

from sqlalchemy import Column, Integer, Date, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship
import enum

from app.models.base import BaseModel


class BatchSubtopicStatus(str, enum.Enum):
    """Batch subtopic status enumeration"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    SKIPPED = "skipped"


class BatchSubtopic(BaseModel):
    """
    BatchSubtopic model for managing subtopic scheduling within batches
    """
    __tablename__ = "batch_subtopics"

    batch_id = Column(Integer, ForeignKey("batches.id"), nullable=False)
    subtopic_id = Column(Integer, ForeignKey("subtopics.id"), nullable=False)
    scheduled_date = Column(Date)
    completed_date = Column(Date)
    faculty_id = Column(Integer, ForeignKey("faculty.user_id"), nullable=False)
    status = Column(Enum(BatchSubtopicStatus), default=BatchSubtopicStatus.PENDING)
    notes = Column(Text)

    # Relationships
    batch = relationship("Batch")
    subtopic = relationship("Subtopic", back_populates="batch_subtopics")
    faculty = relationship("Faculty")

    def __repr__(self):
        return f"<BatchSubtopic(id={self.id}, batch_id={self.batch_id}, subtopic_id={self.subtopic_id}, status={self.status})>"

    def is_pending(self):
        """Check if subtopic is pending"""
        return self.status == BatchSubtopicStatus.PENDING

    def is_in_progress(self):
        """Check if subtopic is in progress"""
        return self.status == BatchSubtopicStatus.IN_PROGRESS

    def is_completed(self):
        """Check if subtopic is completed"""
        return self.status == BatchSubtopicStatus.COMPLETED

    def is_skipped(self):
        """Check if subtopic was skipped"""
        return self.status == BatchSubtopicStatus.SKIPPED

    def start_subtopic(self, faculty_id=None):
        """Mark subtopic as in progress"""
        self.status = BatchSubtopicStatus.IN_PROGRESS
        if faculty_id:
            self.faculty_id = faculty_id

    def complete_subtopic(self, notes=None):
        """Mark subtopic as completed"""
        self.status = BatchSubtopicStatus.COMPLETED
        self.completed_date = self.updated_at.date()
        if notes:
            self.notes = notes

    def skip_subtopic(self, notes=None):
        """Skip subtopic"""
        self.status = BatchSubtopicStatus.SKIPPED
        if notes:
            self.notes = notes

    def get_duration_days(self):
        """Get duration taken to complete subtopic"""
        if not self.scheduled_date or not self.completed_date:
            return 0
        return (self.completed_date - self.scheduled_date).days

    def get_duration_hours(self):
        """Get duration in hours (from subtopic definition)"""
        return self.subtopic.duration_hours if self.subtopic else 0

    def is_overdue(self):
        """Check if subtopic is overdue (not completed and past scheduled date)"""
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
        """Check if subtopic can be started"""
        if self.is_completed() or self.is_skipped():
            return False
        
        # Check if prerequisites are completed
        if self.subtopic.prerequisites:
            # This would need to check if prerequisite subtopics are completed
            # For now, return True
            pass
        
        return True

    def get_attendance_records(self):
        """Get attendance records for this subtopic session"""
        return [
            att for att in self.batch.attendance_records 
            if att.topic_covered and self.subtopic.name in att.topic_covered
        ]

    def get_attendance_percentage(self):
        """Get attendance percentage for this subtopic"""
        attendance = self.get_attendance_records()
        if not attendance:
            return 0.0
        
        present_count = len([
            att for att in attendance 
            if att.status == "present"
        ])
        
        return (present_count / len(attendance)) * 100

    def get_student_progress(self, student_id):
        """Get progress for a specific student in this subtopic"""
        # This would need to be implemented based on student-specific progress tracking
        # For now, return basic status
        return {
            "status": self.status,
            "completed_date": self.completed_date,
            "notes": self.notes
        }

    def add_note(self, note):
        """Add a note to the subtopic"""
        if not self.notes:
            self.notes = note
        else:
            self.notes += f"\n\n{note}"

    def get_summary(self):
        """Get summary of batch subtopic"""
        return {
            "subtopic_name": self.subtopic.name if self.subtopic else "Unknown",
            "parent_topic": self.subtopic.parent_topic.name if self.subtopic and self.subtopic.parent_topic else "Unknown",
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
        """Reschedule subtopic to a new date"""
        self.scheduled_date = new_date
        if notes:
            self.add_note(f"Rescheduled: {notes}")
        else:
            self.add_note(f"Rescheduled to {new_date}")

    def assign_faculty(self, faculty_id, notes=None):
        """Assign a different faculty to this subtopic"""
        old_faculty_name = self.faculty.full_name if self.faculty else "Unassigned"
        self.faculty_id = faculty_id
        
        if notes:
            self.add_note(f"Faculty changed from {old_faculty_name}: {notes}")
        else:
            self.add_note(f"Faculty changed from {old_faculty_name}")

    def get_prerequisite_status(self):
        """Get status of prerequisite subtopics"""
        if not self.subtopic or not self.subtopic.prerequisites:
            return {"completed": True, "pending": []}
        
        # This would need to check actual prerequisite completion
        # For now, return as completed
        return {"completed": True, "pending": []}

    def calculate_completion_rate(self):
        """Calculate completion rate for this subtopic across all batches"""
        # This would need to query all batch subtopics for this subtopic
        # For now, return current status
        return 100.0 if self.is_completed() else 0.0

    def get_subtopic_path(self):
        """Get full path including parent topic"""
        if self.subtopic:
            return self.subtopic.get_subtopic_path()
        return "Unknown"

    def get_difficulty_level(self):
        """Get difficulty level from subtopic"""
        if self.subtopic:
            return self.subtopic.get_difficulty_level()
        return "Unknown"

    def get_learning_materials(self):
        """Get learning materials for this subtopic"""
        if self.subtopic:
            return self.subtopic.get_learning_materials_list()
        return []

    def get_prerequisites(self):
        """Get prerequisites for this subtopic"""
        if self.subtopic:
            return self.subtopic.get_prerequisites_list()
        return []

    def can_be_modified_by(self, user_role, user_id):
        """Check if subtopic can be modified by user"""
        # Faculty can modify their own assigned subtopics
        if user_role == "faculty" and self.faculty_id == user_id:
            return True
        
        # Center admin and above can modify any subtopic
        if user_role in ["center_admin", "academic_head", "super_admin"]:
            return True
        
        return False

    def create_notification_for_completion(self):
        """Create notification when subtopic is completed"""
        from app.models.notification import Notification
        
        return Notification(
            user_id=self.batch.faculty_id,
            title="Subtopic Completed",
            message=f"Subtopic '{self.subtopic.name}' has been completed",
            type="success",
            category="progress",
            related_id=self.batch_id
        )

    def get_progress_metrics(self):
        """Get detailed progress metrics for this subtopic"""
        return {
            "subtopic_id": self.subtopic_id if self.subtopic else None,
            "subtopic_name": self.subtopic.name if self.subtopic else "Unknown",
            "status": self.status,
            "scheduled_date": self.scheduled_date,
            "completed_date": self.completed_date,
            "duration_hours": self.get_duration_hours(),
            "attendance_percentage": self.get_attendance_percentage(),
            "faculty_assigned": self.faculty.full_name if self.faculty else None,
            "is_overdue": self.is_overdue(),
            "overdue_days": self.get_overdue_days()
        }

    def validate_batch_subtopic(self):
        """Validate batch subtopic data"""
        errors = []
        
        if not self.batch_id:
            errors.append("Batch ID is required")
        
        if not self.subtopic_id:
            errors.append("Subtopic ID is required")
        
        if not self.faculty_id:
            errors.append("Faculty ID is required")
        
        return errors

    def get_completion_efficiency(self):
        """Get completion efficiency (planned vs actual duration)"""
        if not self.scheduled_date or not self.completed_date:
            return 0.0
        
        planned_hours = self.get_duration_hours()
        actual_days = self.get_duration_days()
        
        if planned_hours == 0:
            return 0.0
        
        # Assuming 8 hours per day for calculation
        actual_hours = actual_days * 8
        return (planned_hours / actual_hours) * 100 if actual_hours > 0 else 0.0