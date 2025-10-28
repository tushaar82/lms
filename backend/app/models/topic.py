"""
Topic model for subject topics and learning materials
"""

from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship
import enum

from app.models.base import BaseModel


class TopicStatus(str, enum.Enum):
    """Topic status enumeration"""
    ACTIVE = "active"
    INACTIVE = "inactive"


class Topic(BaseModel):
    """
    Topic model for subject topics
    """
    __tablename__ = "topics"

    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    duration_hours = Column(Integer, nullable=False)
    order_index = Column(Integer, nullable=False)
    prerequisites = Column(Text)
    learning_materials = Column(Text)
    status = Column(Enum(TopicStatus), default=TopicStatus.ACTIVE)

    # Relationships
    subject = relationship("Subject", back_populates="topics")
    batch_topics = relationship("BatchTopic", back_populates="topic")
    subtopics = relationship("Subtopic", back_populates="parent_topic", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Topic(id={self.id}, name={self.name}, subject_id={self.subject_id})>"

    def is_active(self):
        """Check if topic is active"""
        return self.status == TopicStatus.ACTIVE

    def is_completed(self):
        """Check if topic is completed in all batches"""
        if not self.batch_topics:
            return False
        
        return all(
            bt.status == "completed" 
            for bt in self.batch_topics
        )

    def get_completion_rate(self):
        """Get completion rate across all batches"""
        if not self.batch_topics:
            return 0.0
        
        completed_count = len([
            bt for bt in self.batch_topics 
            if bt.status == "completed"
        ])
        
        return (completed_count / len(self.batch_topics)) * 100

    def get_prerequisites_list(self):
        """Get list of prerequisites"""
        if not self.prerequisites:
            return []
        return [prereq.strip() for prereq in self.prerequisites.split(",")]

    def get_learning_materials_list(self):
        """Get list of learning materials"""
        if not self.learning_materials:
            return []
        return [material.strip() for material in self.learning_materials.split(",")]

    def get_batches_scheduled(self):
        """Get batches where this topic is scheduled"""
        return [bt.batch for bt in self.batch_topics if bt.batch]

    def get_batches_completed(self):
        """Get batches where this topic is completed"""
        return [
            bt.batch for bt in self.batch_topics 
            if bt.status == "completed" and bt.batch
        ]

    def get_batches_in_progress(self):
        """Get batches where this topic is in progress"""
        return [
            bt.batch for bt in self.batch_topics 
            if bt.status == "in_progress" and bt.batch
        ]

    def get_average_completion_time(self):
        """Get average time taken to complete this topic across batches"""
        completed_batches = [
            bt for bt in self.batch_topics 
            if bt.status == "completed" and bt.completed_date and bt.scheduled_date
        ]
        
        if not completed_batches:
            return 0
        
        total_days = sum(
            (bt.completed_date - bt.scheduled_date).days 
            for bt in completed_batches
        )
        
        return total_days / len(completed_batches)

    def get_faculty_assigned(self):
        """Get list of faculty assigned to teach this topic"""
        faculty_list = []
        for bt in self.batch_topics:
            if bt.faculty and bt.faculty not in faculty_list:
                faculty_list.append(bt.faculty)
        return faculty_list

    def get_next_topic(self):
        """Get the next topic in the subject sequence"""
        return (
            self.session.query(Topic)
            .filter(
                Topic.subject_id == self.subject_id,
                Topic.order_index == self.order_index + 1,
                Topic.status == TopicStatus.ACTIVE
            )
            .first()
        )

    def get_previous_topic(self):
        """Get the previous topic in the subject sequence"""
        return (
            self.session.query(Topic)
            .filter(
                Topic.subject_id == self.subject_id,
                Topic.order_index == self.order_index - 1,
                Topic.status == TopicStatus.ACTIVE
            )
            .first()
        )

    def can_be_started(self, completed_topics=None):
        """Check if this topic can be started based on prerequisites"""
        if not self.prerequisites:
            return True
        
        if completed_topics is None:
            completed_topics = []
        
        prerequisites = self.get_prerequisites_list()
        return all(prereq in completed_topics for prereq in prerequisites)

    def get_subtopics(self):
        """Get all subtopics for this topic"""
        return self.subtopics

    def get_active_subtopics(self):
        """Get active subtopics for this topic"""
        return [sub for sub in self.subtopics if sub.is_active()]

    def get_completed_subtopics(self):
        """Get completed subtopics for this topic"""
        return [sub for sub in self.subtopics if sub.is_completed()]

    def get_subtopic_completion_percentage(self):
        """Get completion percentage of subtopics"""
        active_subtopics = self.get_active_subtopics()
        if not active_subtopics:
            return 0.0
        
        completed_count = len(self.get_completed_subtopics())
        return (completed_count / len(active_subtopics)) * 100

    def add_subtopic(self, name, description=None, duration_hours=1, order_index=None):
        """Add a new subtopic to this topic"""
        from app.models.subtopic import Subtopic
        
        if order_index is None:
            # Get next order index
            max_order = max([sub.order_index for sub in self.subtopics], default=0)
            order_index = max_order + 1
        
        subtopic = Subtopic(
            parent_topic_id=self.id,
            name=name,
            description=description,
            duration_hours=duration_hours,
            order_index=order_index
        )
        
        return subtopic

    def has_subtopics(self):
        """Check if topic has subtopics"""
        return len(self.subtopics) > 0

    def get_total_duration_with_subtopics(self):
        """Get total duration including subtopics"""
        total_duration = self.duration_hours
        
        # Add subtopic durations
        for subtopic in self.get_active_subtopics():
            total_duration += subtopic.duration_hours
        
        return total_duration

    def is_leaf_topic(self):
        """Check if this is a leaf topic (no subtopics)"""
        return not self.has_subtopics()

    def get_topic_hierarchy(self):
        """Get hierarchical structure of topic and subtopics"""
        hierarchy = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "duration_hours": self.duration_hours,
            "order_index": self.order_index,
            "status": self.status,
            "subtopics": []
        }
        
        for subtopic in sorted(self.subtopics, key=lambda x: x.order_index):
            hierarchy["subtopics"].append(subtopic.get_subtopic_hierarchy())
        
        return hierarchy

    def reorder_subtopics(self, new_order):
        """Reorder subtopics based on new order list"""
        subtopic_map = {sub.id: sub for sub in self.subtopics}
        
        for index, subtopic_id in enumerate(new_order, 1):
            if subtopic_id in subtopic_map:
                subtopic_map[subtopic_id].order_index = index

    def can_add_subtopic(self):
        """Check if subtopic can be added to this topic"""
        # Can add subtopic if topic is active
        return self.is_active()

    def get_progress_summary(self):
        """Get progress summary including subtopics"""
        return {
            "topic_id": self.id,
            "topic_name": self.name,
            "topic_status": self.status,
            "topic_completed": self.is_completed(),
            "has_subtopics": self.has_subtopics(),
            "total_subtopics": len(self.get_active_subtopics()),
            "completed_subtopics": len(self.get_completed_subtopics()),
            "subtopic_completion_percentage": self.get_subtopic_completion_percentage(),
            "total_duration": self.get_total_duration_with_subtopics()
        }