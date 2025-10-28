"""
Subject model for course subjects and topics
"""

from sqlalchemy import Column, Integer, String, Text, Enum
from sqlalchemy.orm import relationship
import enum

from app.models.base import BaseModel


class SubjectStatus(str, enum.Enum):
    """Subject status enumeration"""
    ACTIVE = "active"
    INACTIVE = "inactive"


class Subject(BaseModel):
    """
    Subject model for course subjects
    """
    __tablename__ = "subjects"

    name = Column(String(100), nullable=False)
    code = Column(String(20), unique=True, nullable=False, index=True)
    description = Column(Text)
    duration_hours = Column(Integer, nullable=False)
    syllabus = Column(Text)
    prerequisites = Column(Text)
    learning_outcomes = Column(Text)
    status = Column(Enum(SubjectStatus), default=SubjectStatus.ACTIVE)

    # Relationships
    batches = relationship("Batch", back_populates="subject")
    topics = relationship("Topic", back_populates="subject", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Subject(id={self.id}, name={self.name}, code={self.code})>"

    def is_active(self):
        """Check if subject is active"""
        return self.status == SubjectStatus.ACTIVE

    def get_active_batches(self):
        """Get active batches for this subject"""
        return [batch for batch in self.batches if batch.is_active()]

    def get_completed_batches(self):
        """Get completed batches for this subject"""
        return [batch for batch in self.batches if batch.status == "completed"]

    def get_total_students_enrolled(self):
        """Get total number of students enrolled in this subject"""
        total_students = 0
        for batch in self.batches:
            total_students += len(batch.students)
        return total_students

    def get_total_students_completed(self):
        """Get total number of students who completed this subject"""
        completed_students = 0
        for batch in self.get_completed_batches():
            completed_students += len([
                sb for sb in batch.student_batches 
                if sb.status == "completed"
            ])
        return completed_students

    def get_completion_rate(self):
        """Get completion rate for this subject"""
        total_students = self.get_total_students_enrolled()
        if total_students == 0:
            return 0.0
        
        completed_students = self.get_total_students_completed()
        return (completed_students / total_students) * 100

    def get_active_topics(self):
        """Get active topics for this subject"""
        return [topic for topic in self.topics if topic.is_active()]

    def get_total_duration_hours(self):
        """Get total duration hours from all topics"""
        return sum(topic.duration_hours for topic in self.get_active_topics())

    def get_prerequisites_list(self):
        """Get list of prerequisites"""
        if not self.prerequisites:
            return []
        return [prereq.strip() for prereq in self.prerequisites.split(",")]

    def get_learning_outcomes_list(self):
        """Get list of learning outcomes"""
        if not self.learning_outcomes:
            return []
        return [outcome.strip() for outcome in self.learning_outcomes.split(";")]

    def get_average_batch_size(self):
        """Get average batch size for this subject"""
        batches = self.get_active_batches()
        if not batches:
            return 0
        
        total_students = sum(len(batch.students) for batch in batches)
        return total_students / len(batches)

    def get_faculty_assigned(self):
        """Get list of faculty assigned to this subject"""
        faculty_list = []
        for batch in self.batches:
            if batch.faculty and batch.faculty not in faculty_list:
                faculty_list.append(batch.faculty)
        return faculty_list

    def get_completion_percentage(self):
        """Get overall completion percentage for this subject"""
        active_topics = self.get_active_topics()
        if not active_topics:
            return 0.0
        
        completed_topics = len([
            topic for topic in active_topics 
            if topic.is_completed()
        ])
        
        return (completed_topics / len(active_topics)) * 100