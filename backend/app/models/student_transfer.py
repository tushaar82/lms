"""
StudentTransfer model for managing student transfers between faculties
"""

from sqlalchemy import Column, Integer, Text, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import enum

from app.models.base import BaseModel


class TransferStatus(str, enum.Enum):
    """Transfer status enumeration"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


class TransferReason(str, enum.Enum):
    """Transfer reason enumeration"""
    FACULTY_UNAVAILABLE = "faculty_unavailable"
    SCHEDULE_CONFLICT = "schedule_conflict"
    PERFORMANCE_ISSUES = "performance_issues"
    PERSONAL_REQUEST = "personal_request"
    ADMIN_DECISION = "admin_decision"


class StudentTransfer(BaseModel):
    """
    StudentTransfer model for managing student transfers between faculties
    """
    __tablename__ = "student_transfers"

    student_batch_id = Column(Integer, ForeignKey("student_batches.id"), nullable=False)
    from_faculty_id = Column(Integer, ForeignKey("faculty.user_id"), nullable=False)
    to_faculty_id = Column(Integer, ForeignKey("faculty.user_id"), nullable=False)
    reason = Column(Text)
    transfer_reason_type = Column(Enum(TransferReason))
    status = Column(Enum(TransferStatus), default=TransferStatus.PENDING)
    requested_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    approved_by = Column(Integer, ForeignKey("users.id"))
    approval_remarks = Column(Text)
    completed_at = Column(DateTime)
    effective_date = Column(DateTime)

    # Relationships
    student_batch = relationship("StudentBatch", back_populates="transfer_requests")
    from_faculty = relationship("Faculty", foreign_keys=[from_faculty_id])
    to_faculty = relationship("Faculty", foreign_keys=[to_faculty_id])
    requester = relationship("User", foreign_keys=[requested_by])
    approver = relationship("User", foreign_keys=[approved_by])

    def __repr__(self):
        return f"<StudentTransfer(id={self.id}, student_batch_id={self.student_batch_id}, status={self.status})>"

    def is_pending(self):
        """Check if transfer is pending"""
        return self.status == TransferStatus.PENDING

    def is_approved(self):
        """Check if transfer is approved"""
        return self.status == TransferStatus.APPROVED

    def is_rejected(self):
        """Check if transfer is rejected"""
        return self.status == TransferStatus.REJECTED

    def is_cancelled(self):
        """Check if transfer is cancelled"""
        return self.status == TransferStatus.CANCELLED

    def is_completed(self):
        """Check if transfer is completed"""
        return self.status == TransferStatus.COMPLETED

    def can_be_approved_by(self, user_role, user_id):
        """Check if user can approve this transfer"""
        # Center admin and above can approve transfers
        if user_role in ["center_admin", "academic_head", "super_admin"]:
            return True
        
        # From faculty can approve transfers from their batch
        if user_role == "faculty" and self.from_faculty_id == user_id:
            return True
        
        return False

    def approve(self, approved_by, remarks=None, effective_date=None):
        """Approve transfer request"""
        self.status = TransferStatus.APPROVED
        self.approved_by = approved_by
        if remarks:
            self.approval_remarks = remarks
        
        # Set effective date
        from datetime import datetime
        self.effective_date = effective_date or datetime.utcnow()

    def reject(self, approved_by, remarks=None):
        """Reject transfer request"""
        self.status = TransferStatus.REJECTED
        self.approved_by = approved_by
        if remarks:
            self.approval_remarks = remarks

    def cancel(self):
        """Cancel transfer request"""
        self.status = TransferStatus.CANCELLED

    def complete(self):
        """Complete the transfer"""
        if not self.is_approved():
            return False
        
        self.status = TransferStatus.COMPLETED
        from datetime import datetime
        self.completed_at = datetime.utcnow()
        
        # Update the batch faculty
        if self.student_batch and self.student_batch.batch:
            self.student_batch.batch.faculty_id = self.to_faculty_id

    def get_student_name(self):
        """Get student name"""
        if self.student_batch and self.student_batch.student:
            return self.student_batch.student.full_name
        return "Unknown"

    def get_from_faculty_name(self):
        """Get from faculty name"""
        if self.from_faculty:
            return self.from_faculty.full_name
        return "Unknown"

    def get_to_faculty_name(self):
        """Get to faculty name"""
        if self.to_faculty:
            return self.to_faculty.full_name
        return "Unknown"

    def get_batch_name(self):
        """Get batch name"""
        if self.student_batch and self.student_batch.batch:
            return self.student_batch.batch.name
        return "Unknown"

    def get_transfer_summary(self):
        """Get summary of transfer request"""
        return {
            "id": self.id,
            "student_name": self.get_student_name(),
            "batch_name": self.get_batch_name(),
            "from_faculty": self.get_from_faculty_name(),
            "to_faculty": self.get_to_faculty_name(),
            "reason": self.reason,
            "transfer_reason_type": self.transfer_reason_type,
            "status": self.status,
            "requested_by": self.requester.full_name if self.requester else "Unknown",
            "approved_by": self.approver.full_name if self.approver else None,
            "approval_remarks": self.approval_remarks,
            "effective_date": self.effective_date,
            "completed_at": self.completed_at,
            "created_at": self.created_at
        }

    def create_notification_for_from_faculty(self):
        """Create notification for from faculty about transfer request"""
        from app.models.notification import Notification
        
        return Notification(
            user_id=self.from_faculty_id,
            title="Transfer Request",
            message=f"Transfer request for {self.get_student_name()} from {self.get_batch_name()}",
            type="info",
            category="batch",
            related_id=self.student_batch.batch_id if self.student_batch else None
        )

    def create_notification_for_to_faculty(self):
        """Create notification for to faculty about transfer request"""
        from app.models.notification import Notification
        
        return Notification(
            user_id=self.to_faculty_id,
            title="Incoming Transfer",
            message=f"{self.get_student_name()} may be transferred to your batch",
            type="info",
            category="batch",
            related_id=self.student_batch.batch_id if self.student_batch else None
        )

    def create_notification_for_approval(self, status):
        """Create notification about transfer approval/rejection"""
        from app.models.notification import Notification
        
        if status == "approved":
            title = "Transfer Approved"
            message = f"Transfer request for {self.get_student_name()} has been approved"
            notification_type = "success"
            recipients = [self.from_faculty_id, self.to_faculty_id]
        elif status == "rejected":
            title = "Transfer Rejected"
            message = f"Transfer request for {self.get_student_name()} has been rejected"
            notification_type = "error"
            recipients = [self.from_faculty_id, self.to_faculty_id]
        else:
            return None
        
        notifications = []
        for user_id in recipients:
            notifications.append(Notification(
                user_id=user_id,
                title=title,
                message=message,
                type=notification_type,
                category="batch",
                related_id=self.student_batch.batch_id if self.student_batch else None
            ))
        
        return notifications

    def is_emergency_transfer(self):
        """Check if this is an emergency transfer"""
        return self.transfer_reason_type == TransferReason.PERSONAL_REQUEST

    def requires_immediate_action(self):
        """Check if transfer requires immediate action"""
        return self.transfer_reason_type in [
            TransferReason.FACULTY_UNAVAILABLE,
            TransferReason.PERFORMANCE_ISSUES
        ]

    def get_processing_days(self):
        """Get number of days transfer has been processing"""
        from datetime import datetime
        
        if self.completed_at:
            return (self.completed_at - self.created_at).days
        return (datetime.utcnow() - self.created_at).days

    def is_overdue_for_approval(self):
        """Check if transfer approval is overdue"""
        from datetime import datetime, timedelta
        
        # Consider overdue if pending for more than 3 days
        overdue_date = self.created_at + timedelta(days=3)
        return datetime.utcnow() > overdue_date and self.is_pending()

    def can_be_cancelled_by(self, user_role, user_id):
        """Check if transfer can be cancelled"""
        # Student can cancel their own pending transfer
        if (user_role == "student" and 
            self.student_batch and 
            self.student_batch.student_id == user_id and 
            self.is_pending()):
            return True
        
        # From faculty can cancel transfer from their batch
        if user_role == "faculty" and self.from_faculty_id == user_id:
            return True
        
        # Admin can cancel any pending transfer
        if user_role in ["center_admin", "academic_head", "super_admin"]:
            return True
        
        return False

    def get_impact_analysis(self):
        """Get impact analysis of this transfer"""
        return {
            "student_impact": "Medium" if not self.is_emergency_transfer() else "High",
            "from_faculty_workload": "Reduced",
            "to_faculty_workload": "Increased",
            "batch_continuity": "Disrupted" if not self.is_emergency_transfer() else "Maintained"
        }

    def validate_transfer(self):
        """Validate transfer request"""
        errors = []
        
        # Check if to faculty is different from from faculty
        if self.from_faculty_id == self.to_faculty_id:
            errors.append("Cannot transfer to same faculty")
        
        # Check if student batch is active
        if self.student_batch and not self.student_batch.is_active():
            errors.append("Cannot transfer from inactive batch")
        
        # Check if to faculty has capacity
        if self.to_faculty:
            active_batches = len(self.to_faculty.get_active_batches())
            if active_batches >= 5:  # Assuming max 5 batches per faculty
                errors.append("Target faculty has reached maximum batch capacity")
        
        return errors