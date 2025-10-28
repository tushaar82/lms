"""
Notification model for system notifications
"""

from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
import enum

from app.models.base import BaseModel


class NotificationType(str, enum.Enum):
    """Notification type enumeration"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    SUCCESS = "success"


class NotificationCategory(str, enum.Enum):
    """Notification category enumeration"""
    ATTENDANCE = "attendance"
    PROGRESS = "progress"
    BATCH = "batch"
    FEEDBACK = "feedback"
    SYSTEM = "system"


class Notification(BaseModel):
    """
    Notification model for system notifications
    """
    __tablename__ = "notifications"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    type = Column(Enum(NotificationType), nullable=False)
    category = Column(Enum(NotificationCategory), nullable=False)
    related_id = Column(Integer)  # Can reference batch_id, student_id, etc.
    is_read = Column(Boolean, default=False)
    read_at = Column(DateTime)

    # Relationships
    user = relationship("User", back_populates="notifications")

    def __repr__(self):
        return f"<Notification(id={self.id}, user_id={self.user_id}, title={self.title}, type={self.type})>"

    def is_info(self):
        """Check if notification is info type"""
        return self.type == NotificationType.INFO

    def is_warning(self):
        """Check if notification is warning type"""
        return self.type == NotificationType.WARNING

    def is_error(self):
        """Check if notification is error type"""
        return self.type == NotificationType.ERROR

    def is_success(self):
        """Check if notification is success type"""
        return self.type == NotificationType.SUCCESS

    def is_attendance_related(self):
        """Check if notification is attendance related"""
        return self.category == NotificationCategory.ATTENDANCE

    def is_progress_related(self):
        """Check if notification is progress related"""
        return self.category == NotificationCategory.PROGRESS

    def is_batch_related(self):
        """Check if notification is batch related"""
        return self.category == NotificationCategory.BATCH

    def is_feedback_related(self):
        """Check if notification is feedback related"""
        return self.category == NotificationCategory.FEEDBACK

    def is_system_related(self):
        """Check if notification is system related"""
        return self.category == NotificationCategory.SYSTEM

    def mark_as_read(self):
        """Mark notification as read"""
        self.is_read = True
        self.read_at = self.updated_at

    def mark_as_unread(self):
        """Mark notification as unread"""
        self.is_read = False
        self.read_at = None

    def get_priority(self):
        """Get priority level based on type"""
        priority_map = {
            NotificationType.ERROR: "high",
            NotificationType.WARNING: "medium",
            NotificationType.SUCCESS: "low",
            NotificationType.INFO: "low"
        }
        return priority_map.get(self.type, "low")

    def get_icon_class(self):
        """Get CSS icon class based on type and category"""
        icon_map = {
            NotificationType.ERROR: "fas fa-exclamation-circle text-danger",
            NotificationType.WARNING: "fas fa-exclamation-triangle text-warning",
            NotificationType.SUCCESS: "fas fa-check-circle text-success",
            NotificationType.INFO: "fas fa-info-circle text-info"
        }
        return icon_map.get(self.type, "fas fa-bell")

    def get_action_url(self):
        """Get action URL based on category and related_id"""
        if not self.related_id:
            return None
        
        url_map = {
            NotificationCategory.ATTENDANCE: f"/attendance?batch_id={self.related_id}",
            NotificationCategory.PROGRESS: f"/students/progress?student_id={self.related_id}",
            NotificationCategory.BATCH: f"/batches/{self.related_id}",
            NotificationCategory.FEEDBACK: f"/feedback?batch_id={self.related_id}",
            NotificationCategory.SYSTEM: "/settings"
        }
        return url_map.get(self.category)

    def get_summary(self):
        """Get notification summary"""
        return {
            "id": self.id,
            "title": self.title,
            "message": self.message,
            "type": self.type,
            "category": self.category,
            "priority": self.get_priority(),
            "icon_class": self.get_icon_class(),
            "action_url": self.get_action_url(),
            "is_read": self.is_read,
            "read_at": self.read_at,
            "created_at": self.created_at,
            "time_ago": self.get_time_ago()
        }

    def get_time_ago(self):
        """Get human-readable time ago"""
        from datetime import datetime
        
        now = datetime.utcnow()
        diff = now - self.created_at.replace(tzinfo=None)
        
        days = diff.days
        hours, remainder = divmod(diff.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        
        if days > 0:
            return f"{days} day{'s' if days > 1 else ''} ago"
        elif hours > 0:
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif minutes > 0:
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        else:
            return "Just now"

    def can_be_deleted_by(self, user_role, user_id):
        """Check if notification can be deleted by user"""
        # Users can delete their own notifications
        if self.user_id == user_id:
            return True
        
        # Admin can delete any notification
        if user_role in ["center_admin", "academic_head", "super_admin"]:
            return True
        
        return False

    def create_email_notification(self):
        """Create email notification content"""
        return {
            "to": self.user.email,
            "subject": f"[{self.type.upper()}] {self.title}",
            "body": f"""
            <html>
            <body>
                <h2>{self.title}</h2>
                <p>{self.message}</p>
                <p><small>Sent at: {self.created_at}</small></p>
                {f'<p><a href="{self.get_action_url()}">View Details</a></p>' if self.get_action_url() else ''}
            </body>
            </html>
            """
        }

    def create_sms_notification(self):
        """Create SMS notification content"""
        return f"[{self.type.upper()}] {self.title}: {self.message[:100]}"

    def is_actionable(self):
        """Check if notification requires action"""
        return self.get_action_url() is not None

    def get_related_entity(self):
        """Get related entity based on category"""
        if not self.related_id:
            return None
        
        # This would need to query the appropriate entity based on category
        # For now, return None
        return None

    @staticmethod
    def create_attendance_notification(user_id, batch_id, message, notification_type="info"):
        """Create attendance-related notification"""
        return Notification(
            user_id=user_id,
            title="Attendance Update",
            message=message,
            type=NotificationType(notification_type),
            category=NotificationCategory.ATTENDANCE,
            related_id=batch_id
        )

    @staticmethod
    def create_progress_notification(user_id, student_id, message, notification_type="info"):
        """Create progress-related notification"""
        return Notification(
            user_id=user_id,
            title="Progress Update",
            message=message,
            type=NotificationType(notification_type),
            category=NotificationCategory.PROGRESS,
            related_id=student_id
        )

    @staticmethod
    def create_batch_notification(user_id, batch_id, message, notification_type="info"):
        """Create batch-related notification"""
        return Notification(
            user_id=user_id,
            title="Batch Update",
            message=message,
            type=NotificationType(notification_type),
            category=NotificationCategory.BATCH,
            related_id=batch_id
        )

    @staticmethod
    def create_feedback_notification(user_id, batch_id, message, notification_type="info"):
        """Create feedback-related notification"""
        return Notification(
            user_id=user_id,
            title="Feedback Update",
            message=message,
            type=NotificationType(notification_type),
            category=NotificationCategory.FEEDBACK,
            related_id=batch_id
        )

    @staticmethod
    def create_system_notification(user_id, message, notification_type="info"):
        """Create system notification"""
        return Notification(
            user_id=user_id,
            title="System Notification",
            message=message,
            type=NotificationType(notification_type),
            category=NotificationCategory.SYSTEM
        )