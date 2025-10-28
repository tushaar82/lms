"""
BatchExtension model for managing batch extensions
"""

from sqlalchemy import Column, Integer, Date, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship
import enum

from app.models.base import BaseModel


class ExtensionStatus(str, enum.Enum):
    """Extension status enumeration"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class BatchExtension(BaseModel):
    """
    BatchExtension model for managing batch extensions
    """
    __tablename__ = "batch_extensions"

    batch_id = Column(Integer, ForeignKey("batches.id"), nullable=False)
    original_end_date = Column(Date, nullable=False)
    new_end_date = Column(Date, nullable=False)
    reason = Column(Text)
    requested_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    approved_by = Column(Integer, ForeignKey("users.id"))
    status = Column(Enum(ExtensionStatus), default=ExtensionStatus.PENDING)

    # Relationships
    batch = relationship("Batch", back_populates="extensions")
    requester = relationship("User", foreign_keys=[requested_by])
    approver = relationship("User", foreign_keys=[approved_by])

    def __repr__(self):
        return f"<BatchExtension(id={self.id}, batch_id={self.batch_id}, status={self.status})>"

    def is_pending(self):
        """Check if extension is pending"""
        return self.status == ExtensionStatus.PENDING

    def is_approved(self):
        """Check if extension is approved"""
        return self.status == ExtensionStatus.APPROVED

    def is_rejected(self):
        """Check if extension is rejected"""
        return self.status == ExtensionStatus.REJECTED

    def approve(self, approved_by, notes=None):
        """Approve the extension"""
        self.status = ExtensionStatus.APPROVED
        self.approved_by = approved_by
        
        # Update batch end date
        if self.batch:
            self.batch.end_date = self.new_end_date
        
        if notes:
            self.reason = f"{self.reason}\n\nApproval notes: {notes}"

    def reject(self, approved_by, notes=None):
        """Reject the extension"""
        self.status = ExtensionStatus.REJECTED
        self.approved_by = approved_by
        
        if notes:
            self.reason = f"{self.reason}\n\nRejection notes: {notes}"

    def get_extension_days(self):
        """Get number of days extended"""
        return (self.new_end_date - self.original_end_date).days

    def get_extension_weeks(self):
        """Get number of weeks extended"""
        return self.get_extension_days() / 7

    def get_extension_months(self):
        """Get number of months extended"""
        return self.get_extension_days() / 30.44  # Average days in month

    def can_be_approved_by(self, user_role, user_id):
        """Check if user can approve this extension"""
        # Center admin and above can approve
        if user_role in ["center_admin", "academic_head", "super_admin"]:
            return True
        
        # Faculty cannot approve their own requested extensions
        if user_role == "faculty" and self.requested_by == user_id:
            return False
        
        return False

    def get_requester_name(self):
        """Get name of requester"""
        return self.requester.full_name if self.requester else "Unknown"

    def get_approver_name(self):
        """Get name of approver"""
        return self.approver.full_name if self.approver else "Not yet approved"

    def get_batch_name(self):
        """Get batch name"""
        return self.batch.name if self.batch else "Unknown"

    def get_summary(self):
        """Get summary of extension"""
        return {
            "id": self.id,
            "batch_name": self.get_batch_name(),
            "original_end_date": self.original_end_date,
            "new_end_date": self.new_end_date,
            "extension_days": self.get_extension_days(),
            "reason": self.reason,
            "requested_by": self.get_requester_name(),
            "approved_by": self.get_approver_name(),
            "status": self.status,
            "created_at": self.created_at
        }

    def is_overdue(self):
        """Check if extension request is overdue (pending for too long)"""
        if not self.is_pending():
            return False
        
        from datetime import datetime, timedelta
        
        # Consider overdue if pending for more than 7 days
        overdue_date = self.created_at + timedelta(days=7)
        return datetime.utcnow() > overdue_date

    def get_overdue_days(self):
        """Get number of days overdue"""
        if not self.is_overdue():
            return 0
        
        from datetime import datetime
        
        overdue_date = self.created_at + timedelta(days=7)
        return (datetime.utcnow() - overdue_date).days

    def create_notification_for_requester(self):
        """Create notification for requester about status change"""
        from app.models.notification import Notification
        
        if self.is_approved():
            title = "Extension Approved"
            message = f"Extension for {self.get_batch_name()} has been approved"
            notification_type = "success"
        elif self.is_rejected():
            title = "Extension Rejected"
            message = f"Extension for {self.get_batch_name()} has been rejected"
            notification_type = "error"
        else:
            return None
        
        return Notification(
            user_id=self.requested_by,
            title=title,
            message=message,
            type=notification_type,
            category="batch",
            related_id=self.batch_id
        )

    def create_notification_for_admin(self):
        """Create notification for admin about new extension request"""
        from app.models.notification import Notification
        
        return Notification(
            user_id=self.batch.center.users[0].id,  # Center admin
            title="Extension Request",
            message=f"Extension requested for {self.get_batch_name()}",
            type="info",
            category="batch",
            related_id=self.batch_id
        )

    def get_impact_analysis(self):
        """Get impact analysis of extension"""
        if not self.batch:
            return {}
        
        return {
            "students_affected": len(self.batch.get_active_students()),
            "faculty_affected": self.batch.faculty.full_name if self.batch.faculty else "Unknown",
            "additional_cost": self.calculate_additional_cost(),
            "schedule_impact": self.get_extension_days()
        }

    def calculate_additional_cost(self):
        """Calculate additional cost of extension"""
        # This would need to be implemented based on institute's cost structure
        # For now, return 0
        return 0

    def get_extension_history(self):
        """Get history of extensions for this batch"""
        # This would need to query other extensions for the same batch
        # For now, return empty list
        return []

    def can_be_cancelled(self, user_role, user_id):
        """Check if extension can be cancelled"""
        # Only pending extensions can be cancelled
        if not self.is_pending():
            return False
        
        # Requester can cancel their own request
        if self.requested_by == user_id:
            return True
        
        # Admin can cancel any pending extension
        if user_role in ["center_admin", "academic_head", "super_admin"]:
            return True
        
        return False

    def cancel(self, cancelled_by, notes=None):
        """Cancel the extension request"""
        self.status = ExtensionStatus.REJECTED
        self.approved_by = cancelled_by
        
        if notes:
            self.reason = f"{self.reason}\n\nCancelled: {notes}"
        else:
            self.reason = f"{self.reason}\n\nCancelled by {cancelled_by}"