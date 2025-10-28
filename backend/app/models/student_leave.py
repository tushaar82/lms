"""
StudentLeave model for managing student leave requests
"""

from sqlalchemy import Column, Integer, Date, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship
import enum

from app.models.base import BaseModel


class LeaveStatus(str, enum.Enum):
    """Leave status enumeration"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"


class LeaveType(str, enum.Enum):
    """Leave type enumeration"""
    MEDICAL = "medical"
    PERSONAL = "personal"
    ACADEMIC = "academic"
    EMERGENCY = "emergency"


class StudentLeave(BaseModel):
    """
    StudentLeave model for managing student leave requests
    """
    __tablename__ = "student_leaves"

    student_id = Column(Integer, ForeignKey("students.user_id"), nullable=False)
    batch_id = Column(Integer, ForeignKey("batches.id"), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    leave_type = Column(Enum(LeaveType), nullable=False)
    reason = Column(Text)
    status = Column(Enum(LeaveStatus), default=LeaveStatus.PENDING)
    approved_by = Column(Integer, ForeignKey("faculty.user_id"))
    approval_remarks = Column(Text)

    # Relationships
    student = relationship("Student", back_populates="leave_requests")
    batch = relationship("Batch")
    approver = relationship("Faculty", foreign_keys=[approved_by])

    def __repr__(self):
        return f"<StudentLeave(id={self.id}, student_id={self.student_id}, status={self.status})>"

    def is_pending(self):
        """Check if leave is pending"""
        return self.status == LeaveStatus.PENDING

    def is_approved(self):
        """Check if leave is approved"""
        return self.status == LeaveStatus.APPROVED

    def is_rejected(self):
        """Check if leave is rejected"""
        return self.status == LeaveStatus.REJECTED

    def is_cancelled(self):
        """Check if leave is cancelled"""
        return self.status == LeaveStatus.CANCELLED

    def get_duration_days(self):
        """Get duration of leave in days"""
        return (self.end_date - self.start_date).days + 1

    def get_duration_weeks(self):
        """Get duration of leave in weeks"""
        return self.get_duration_days() / 7

    def can_be_approved_by(self, user_role, user_id):
        """Check if user can approve this leave"""
        # Faculty can approve leave for their batch students
        if user_role == "faculty" and self.batch.faculty_id == user_id:
            return True
        
        # Center admin and above can approve any leave
        if user_role in ["center_admin", "academic_head", "super_admin"]:
            return True
        
        return False

    def approve(self, approved_by, remarks=None):
        """Approve the leave request"""
        self.status = LeaveStatus.APPROVED
        self.approved_by = approved_by
        if remarks:
            self.approval_remarks = remarks

    def reject(self, approved_by, remarks=None):
        """Reject the leave request"""
        self.status = LeaveStatus.REJECTED
        self.approved_by = approved_by
        if remarks:
            self.approval_remarks = remarks

    def cancel(self):
        """Cancel the leave request"""
        self.status = LeaveStatus.CANCELLED

    def overlaps_with_attendance(self):
        """Check if leave overlaps with attendance records"""
        # This would need to check attendance records for the student
        # For now, return False
        return False

    def affects_batch_progress(self):
        """Check if leave affects batch progress significantly"""
        duration = self.get_duration_days()
        
        # If leave is more than 3 days, it might affect progress
        return duration > 3

    def get_leave_summary(self):
        """Get summary of leave request"""
        return {
            "id": self.id,
            "student_name": self.student.full_name if self.student else "Unknown",
            "batch_name": self.batch.name if self.batch else "Unknown",
            "start_date": self.start_date,
            "end_date": self.end_date,
            "duration_days": self.get_duration_days(),
            "leave_type": self.leave_type,
            "reason": self.reason,
            "status": self.status,
            "approved_by": self.approver.full_name if self.approver else None,
            "approval_remarks": self.approval_remarks,
            "created_at": self.created_at
        }

    def create_notification_for_approval(self):
        """Create notification for faculty about leave request"""
        from app.models.notification import Notification
        
        return Notification(
            user_id=self.batch.faculty_id,
            title="Leave Request",
            message=f"{self.student.full_name} has requested leave from {self.start_date} to {self.end_date}",
            type="info",
            category="attendance",
            related_id=self.batch_id
        )

    def create_notification_for_student(self, status_change):
        """Create notification for student about status change"""
        from app.models.notification import Notification
        
        if status_change == "approved":
            title = "Leave Approved"
            message = f"Your leave request from {self.start_date} to {self.end_date} has been approved"
            notification_type = "success"
        elif status_change == "rejected":
            title = "Leave Rejected"
            message = f"Your leave request from {self.start_date} to {self.end_date} has been rejected"
            notification_type = "error"
        else:
            return None
        
        return Notification(
            user_id=self.student_id,
            title=title,
            message=message,
            type=notification_type,
            category="attendance",
            related_id=self.batch_id
        )

    def is_medical_leave(self):
        """Check if this is medical leave"""
        return self.leave_type == LeaveType.MEDICAL

    def is_emergency_leave(self):
        """Check if this is emergency leave"""
        return self.leave_type == LeaveType.EMERGENCY

    def requires_documentation(self):
        """Check if leave requires documentation"""
        return self.leave_type in [LeaveType.MEDICAL, LeaveType.EMERGENCY]

    def can_be_cancelled_by(self, user_role, user_id):
        """Check if leave can be cancelled"""
        # Student can cancel their own pending leave
        if user_role == "student" and self.student_id == user_id and self.is_pending():
            return True
        
        # Faculty can cancel leave for their batch students
        if user_role == "faculty" and self.batch.faculty_id == user_id:
            return True
        
        # Admin can cancel any leave
        if user_role in ["center_admin", "academic_head", "super_admin"]:
            return True
        
        return False

    def get_impact_on_attendance(self):
        """Get impact of leave on attendance percentage"""
        if not self.batch:
            return 0
        
        # Calculate total batch duration
        batch_duration = (self.batch.end_date - self.batch.start_date).days + 1
        if batch_duration == 0:
            return 0
        
        # Calculate attendance impact
        leave_duration = self.get_duration_days()
        return (leave_duration / batch_duration) * 100

    def is_long_leave(self):
        """Check if this is a long leave request"""
        return self.get_duration_days() > 7

    def get_approval_deadline(self):
        """Get deadline for approval (2 days before start date)"""
        from datetime import timedelta
        
        return self.start_date - timedelta(days=2)

    def is_overdue_for_approval(self):
        """Check if approval is overdue"""
        from datetime import date
        
        return date.today() > self.get_approval_deadline() and self.is_pending()