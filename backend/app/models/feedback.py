"""
Feedback model for student feedback system
"""

from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey, Boolean
from sqlalchemy.orm import relationship
import enum

from app.models.base import BaseModel


class FeedbackType(str, enum.Enum):
    """Feedback type enumeration"""
    FACULTY = "faculty"
    COURSE = "course"
    BATCH = "batch"
    OVERALL = "overall"


class FeedbackStatus(str, enum.Enum):
    """Feedback status enumeration"""
    PENDING = "pending"
    REVIEWED = "reviewed"
    RESOLVED = "resolved"


class Feedback(BaseModel):
    """
    Feedback model for student feedback system
    """
    __tablename__ = "feedback"

    student_id = Column(Integer, ForeignKey("students.user_id"), nullable=False)
    faculty_id = Column(Integer, ForeignKey("faculty.user_id"), nullable=False)
    batch_id = Column(Integer, ForeignKey("batches.id"), nullable=False)
    rating = Column(Integer, nullable=False)  # 1-5 rating
    comments = Column(Text)
    feedback_type = Column(Enum(FeedbackType), nullable=False)
    is_anonymous = Column(Boolean, default=False)
    status = Column(Enum(FeedbackStatus), default=FeedbackStatus.PENDING)

    # Relationships
    student = relationship("Student", back_populates="given_feedback")
    faculty = relationship("Faculty", back_populates="received_feedback")
    batch = relationship("Batch")

    def __repr__(self):
        return f"<Feedback(id={self.id}, student_id={self.student_id}, faculty_id={self.faculty_id}, rating={self.rating})>"

    def is_positive(self):
        """Check if feedback is positive (rating >= 4)"""
        return self.rating >= 4

    def is_neutral(self):
        """Check if feedback is neutral (rating == 3)"""
        return self.rating == 3

    def is_negative(self):
        """Check if feedback is negative (rating <= 2)"""
        return self.rating <= 2

    def get_rating_text(self):
        """Get text representation of rating"""
        rating_texts = {
            1: "Very Poor",
            2: "Poor", 
            3: "Average",
            4: "Good",
            5: "Excellent"
        }
        return rating_texts.get(self.rating, "Unknown")

    def get_sentiment(self):
        """Get sentiment of feedback"""
        if self.is_positive():
            return "positive"
        elif self.is_negative():
            return "negative"
        else:
            return "neutral"

    def can_be_viewed_by(self, user_role, user_id):
        """Check if feedback can be viewed by the user"""
        # Students can view their own feedback
        if user_role == "student" and self.student_id == user_id:
            return True
        
        # Faculty can view feedback about themselves
        if user_role == "faculty" and self.faculty_id == user_id:
            return True
        
        # Center admin and above can view all feedback in their center
        if user_role in ["center_admin", "academic_head", "super_admin"]:
            return True
        
        return False

    def mark_as_reviewed(self, reviewed_by=None):
        """Mark feedback as reviewed"""
        self.status = FeedbackStatus.REVIEWED
        # This would need to add a reviewed_by field and timestamp

    def mark_as_resolved(self, resolved_by=None):
        """Mark feedback as resolved"""
        self.status = FeedbackStatus.RESOLVED
        # This would need to add a resolved_by field and timestamp

    def get_student_name(self):
        """Get student name (or anonymous if anonymous)"""
        if self.is_anonymous:
            return "Anonymous"
        return self.student.full_name if self.student else "Unknown"

    def get_faculty_name(self):
        """Get faculty name"""
        return self.faculty.full_name if self.faculty else "Unknown"

    def get_batch_name(self):
        """Get batch name"""
        return self.batch.name if self.batch else "Unknown"

    def get_feedback_summary(self):
        """Get summary of feedback"""
        return {
            "id": self.id,
            "student_name": self.get_student_name(),
            "faculty_name": self.get_faculty_name(),
            "batch_name": self.get_batch_name(),
            "rating": self.rating,
            "rating_text": self.get_rating_text(),
            "sentiment": self.get_sentiment(),
            "feedback_type": self.feedback_type,
            "comments": self.comments,
            "is_anonymous": self.is_anonymous,
            "status": self.status,
            "created_at": self.created_at
        }

    def get_action_items(self):
        """Get action items based on feedback"""
        action_items = []
        
        if self.is_negative():
            if self.feedback_type == FeedbackType.FACULTY:
                action_items.append("Review faculty performance")
                action_items.append("Provide faculty training if needed")
            elif self.feedback_type == FeedbackType.COURSE:
                action_items.append("Review course content")
                action_items.append("Update curriculum if needed")
            elif self.feedback_type == FeedbackType.BATCH:
                action_items.append("Review batch management")
                action_items.append("Address batch-specific issues")
        
        return action_items

    def create_notification_for_faculty(self):
        """Create notification for faculty about new feedback"""
        from app.models.notification import Notification
        
        notification = Notification(
            user_id=self.faculty_id,
            title="New Feedback Received",
            message=f"You received {self.get_rating_text()} feedback",
            type="info",
            category="feedback",
            related_id=self.batch_id
        )
        return notification

    def create_notification_for_admin(self):
        """Create notification for admin about negative feedback"""
        if self.is_negative():
            from app.models.notification import Notification
            
            notification = Notification(
                user_id=self.batch.center.users[0].id,  # Center admin
                title="Negative Feedback Alert",
                message=f"Negative feedback received for {self.get_batch_name()}",
                type="warning",
                category="feedback",
                related_id=self.batch_id
            )
            return notification
        return None

    def get_trend_analysis(self):
        """Get trend analysis for this feedback"""
        # This would need to compare with historical feedback
        # For now, return basic analysis
        return {
            "current_rating": self.rating,
            "sentiment": self.get_sentiment(),
            "trend": "stable"  # Would calculate actual trend
        }

    def get_improvement_suggestions(self):
        """Get improvement suggestions based on feedback"""
        suggestions = []
        
        if self.rating <= 2:
            if self.feedback_type == FeedbackType.FACULTY:
                suggestions.extend([
                    "Improve teaching methodology",
                    "Enhance communication skills",
                    "Provide better subject knowledge"
                ])
            elif self.feedback_type == FeedbackType.COURSE:
                suggestions.extend([
                    "Update course materials",
                    "Improve practical examples",
                    "Enhance course structure"
                ])
        
        return suggestions

    def is_actionable(self):
        """Check if feedback requires action"""
        return self.is_negative() and self.status != FeedbackStatus.RESOLVED

    def get_priority_level(self):
        """Get priority level for addressing feedback"""
        if self.rating == 1:
            return "high"
        elif self.rating == 2:
            return "medium"
        else:
            return "low"