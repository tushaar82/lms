"""
Attendance model for tracking student attendance
"""

from sqlalchemy import Column, Integer, Date, Text, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import enum

from app.models.base import BaseModel


class AttendanceStatus(str, enum.Enum):
    """Attendance status enumeration"""
    PRESENT = "present"
    ABSENT = "absent"
    LATE = "late"
    EXCUSED = "excused"


class Attendance(BaseModel):
    """
    Attendance model for tracking student attendance
    """
    __tablename__ = "attendance"

    student_id = Column(Integer, ForeignKey("students.user_id"), nullable=False)
    batch_id = Column(Integer, ForeignKey("batches.id"), nullable=False)
    faculty_id = Column(Integer, ForeignKey("faculty.user_id"), nullable=False)
    date = Column(Date, nullable=False)
    status = Column(Enum(AttendanceStatus), nullable=False)
    topic_covered = Column(Text)
    remarks = Column(Text)
    marked_at = Column(DateTime)

    # Relationships
    student = relationship("Student", back_populates="attendance_records")
    batch = relationship("Batch", back_populates="attendance_records")
    faculty = relationship("Faculty", back_populates="attendance_records")

    def __repr__(self):
        return f"<Attendance(id={self.id}, student_id={self.student_id}, date={self.date}, status={self.status})>"

    def is_present(self):
        """Check if student was present"""
        return self.status == AttendanceStatus.PRESENT

    def is_absent(self):
        """Check if student was absent"""
        return self.status == AttendanceStatus.ABSENT

    def is_late(self):
        """Check if student was late"""
        return self.status == AttendanceStatus.LATE

    def is_excused(self):
        """Check if absence was excused"""
        return self.status == AttendanceStatus.EXCUSED

    def get_effective_attendance(self):
        """Get effective attendance (present, late, or excused count as attended)"""
        return self.status in [AttendanceStatus.PRESENT, AttendanceStatus.LATE, AttendanceStatus.EXCUSED]

    def get_attendance_score(self):
        """Get attendance score for analytics"""
        if self.status == AttendanceStatus.PRESENT:
            return 100
        elif self.status == AttendanceStatus.LATE:
            return 75
        elif self.status == AttendanceStatus.EXCUSED:
            return 50
        else:  # ABSENT
            return 0

    def can_be_modified(self, user_role, user_id):
        """Check if attendance can be modified by the user"""
        # Faculty can modify their own marked attendance
        if user_role == "faculty" and self.faculty_id == user_id:
            return True
        
        # Center admin and above can modify any attendance
        if user_role in ["center_admin", "super_admin", "academic_head"]:
            return True
        
        return False

    def update_status(self, new_status, faculty_id=None, remarks=None):
        """Update attendance status"""
        self.status = new_status
        if faculty_id:
            self.faculty_id = faculty_id
        if remarks:
            self.remarks = remarks
        self.marked_at = self.updated_at

    def get_topic_list(self):
        """Get list of topics covered in this session"""
        if not self.topic_covered:
            return []
        return [topic.strip() for topic in self.topic_covered.split(",")]

    def add_topic(self, topic_name):
        """Add a topic to the topics covered"""
        if not self.topic_covered:
            self.topic_covered = topic_name
        else:
            topics = self.get_topic_list()
            if topic_name not in topics:
                topics.append(topic_name)
                self.topic_covered = ", ".join(topics)

    def remove_topic(self, topic_name):
        """Remove a topic from the topics covered"""
        if not self.topic_covered:
            return
        
        topics = self.get_topic_list()
        if topic_name in topics:
            topics.remove(topic_name)
            self.topic_covered = ", ".join(topics)

    def get_session_summary(self):
        """Get summary of the attendance session"""
        summary = {
            "date": self.date,
            "status": self.status,
            "topics": self.get_topic_list(),
            "remarks": self.remarks
        }
        return summary

    def was_marked_late(self, hours_threshold=2):
        """Check if attendance was marked late (after class hours)"""
        if not self.marked_at:
            return False
        
        # This would need to be implemented based on batch schedule
        # For now, return False
        return False

    def get_feedback_given(self):
        """Get feedback related to this attendance session"""
        # This would need to be implemented when feedback system is built
        return []

    def create_notification_for_absence(self):
        """Create notification for student absence"""
        if self.status == AttendanceStatus.ABSENT:
            from app.models.notification import Notification
            
            notification = Notification(
                user_id=self.student_id,
                title="Attendance Marked",
                message=f"You were marked absent on {self.date}",
                type="warning",
                category="attendance",
                related_id=self.batch_id
            )
            return notification
        return None

    def get_batch_schedule_conflict(self):
        """Check if this attendance conflicts with batch schedule"""
        # This would need to be implemented based on batch schedule
        # For now, return None
        return None

    def calculate_makeup_required(self):
        """Calculate if makeup class is required"""
        # This would need to be implemented based on institute policy
        # For now, return False
        return False