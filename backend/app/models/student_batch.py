"""
StudentBatch model for managing student enrollments in batches
"""

from sqlalchemy import Column, Integer, Date, Text, Enum, ForeignKey, Numeric, String
from sqlalchemy.orm import relationship
import enum

from app.models.base import BaseModel


class StudentBatchStatus(str, enum.Enum):
    """Student batch status enumeration"""
    ACTIVE = "active"
    COMPLETED = "completed"
    DROPPED = "dropped"
    TRANSFERRED = "transferred"


class StudentBatch(BaseModel):
    """
    StudentBatch model for managing student enrollments in batches
    """
    __tablename__ = "student_batches"

    student_id = Column(Integer, ForeignKey("students.user_id"), nullable=False)
    batch_id = Column(Integer, ForeignKey("batches.id"), nullable=False)
    enrollment_date = Column(Date, nullable=False)
    completion_date = Column(Date)
    status = Column(Enum(StudentBatchStatus), default=StudentBatchStatus.ACTIVE)
    progress_percentage = Column(Numeric(5, 2), default=0.00)
    final_grade = Column(String(5))
    remarks = Column(Text)

    # Relationships
    student = relationship("Student", back_populates="batches")
    batch = relationship("Batch", back_populates="student_batches")
    transfer_requests = relationship("StudentTransfer", back_populates="student_batch")

    def __repr__(self):
        return f"<StudentBatch(id={self.id}, student_id={self.student_id}, batch_id={self.batch_id})>"

    def is_active(self):
        """Check if student batch enrollment is active"""
        return self.status == StudentBatchStatus.ACTIVE

    def is_completed(self):
        """Check if student has completed the batch"""
        return self.status == StudentBatchStatus.COMPLETED

    def get_attendance_percentage(self):
        """Get attendance percentage for this student in this batch"""
        attendance_records = [
            att for att in self.student.attendance_records 
            if att.batch_id == self.batch_id
        ]
        
        if not attendance_records:
            return 0.0
        
        present_count = len([
            att for att in attendance_records 
            if att.status == "present"
        ])
        
        return (present_count / len(attendance_records)) * 100

    def get_completed_topics_count(self):
        """Get number of completed topics for this student in this batch"""
        batch_topics = [
            bt for bt in self.batch.batch_topics 
            if bt.status == "completed"
        ]
        return len(batch_topics)

    def get_total_topics_count(self):
        """Get total number of topics for this batch"""
        return len(self.batch.batch_topics)

    def calculate_progress(self):
        """Calculate and update progress percentage"""
        total_topics = self.get_total_topics_count()
        if total_topics == 0:
            self.progress_percentage = 0.0
            return self.progress_percentage
        
        completed_topics = self.get_completed_topics_count()
        self.progress_percentage = (completed_topics / total_topics) * 100
        return self.progress_percentage

    def mark_as_completed(self, final_grade=None, remarks=None):
        """Mark student batch as completed"""
        self.status = StudentBatchStatus.COMPLETED
        self.completion_date = self.updated_at.date()
        self.progress_percentage = 100.0
        if final_grade:
            self.final_grade = final_grade
        if remarks:
            self.remarks = remarks

    def mark_as_dropped(self, remarks=None):
        """Mark student as dropped from batch"""
        self.status = StudentBatchStatus.DROPPED
        if remarks:
            self.remarks = remarks

    def get_enrollment_duration_days(self):
        """Get duration of enrollment in days"""
        end_date = self.completion_date or self.updated_at.date()
        return (end_date - self.enrollment_date).days

    def get_feedback_given(self):
        """Get feedback given by student for this batch"""
        return [
            fb for fb in self.student.given_feedback 
            if fb.batch_id == self.batch_id
        ]

    def get_average_feedback_rating(self):
        """Get average feedback rating given by student for this batch"""
        feedback = self.get_feedback_given()
        if not feedback:
            return 0.0
        
        total_rating = sum(fb.rating for fb in feedback)
        return total_rating / len(feedback)

    def can_be_transferred(self):
        """Check if student can be transferred to another batch"""
        return self.status == StudentBatchStatus.ACTIVE

    def transfer_to_batch(self, new_batch_id, remarks=None):
        """Transfer student to a new batch"""
        self.status = StudentBatchStatus.TRANSFERRED
        if remarks:
            self.remarks = remarks
        
        # Create new student batch record
        new_student_batch = StudentBatch(
            student_id=self.student_id,
            batch_id=new_batch_id,
            enrollment_date=self.updated_at.date(),
            status=StudentBatchStatus.ACTIVE
        )
        
        return new_student_batch

    def can_be_transferred(self):
        """Check if student can be transferred"""
        return self.status == StudentBatchStatus.ACTIVE

    def initiate_transfer(self, new_faculty_id, reason=None):
        """Initiate transfer to new faculty"""
        from app.models.student_transfer import StudentTransfer, TransferStatus
        
        transfer = StudentTransfer(
            student_batch_id=self.id,
            from_faculty_id=self.batch.faculty_id,
            to_faculty_id=new_faculty_id,
            reason=reason,
            status=TransferStatus.PENDING
        )
        
        return transfer

    def get_transfer_history(self):
        """Get transfer history for this student batch"""
        return self.transfer_requests

    def has_pending_transfer(self):
        """Check if there's a pending transfer request"""
        return any(
            transfer.is_pending()
            for transfer in self.transfer_requests
        )

    def get_active_transfer(self):
        """Get active transfer request"""
        for transfer in self.transfer_requests:
            if transfer.is_pending():
                return transfer
        return None