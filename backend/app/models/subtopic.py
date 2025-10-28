"""
Subtopic model for managing subtopics within topics
"""

from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship
import enum

from app.models.base import BaseModel


class SubtopicStatus(str, enum.Enum):
    """Subtopic status enumeration"""
    ACTIVE = "active"
    INACTIVE = "inactive"


class Subtopic(BaseModel):
    """
    Subtopic model for managing subtopics within topics
    """
    __tablename__ = "subtopics"

    parent_topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    duration_hours = Column(Integer, nullable=False, default=1)
    order_index = Column(Integer, nullable=False)
    prerequisites = Column(Text)
    learning_materials = Column(Text)
    status = Column(Enum(SubtopicStatus), default=SubtopicStatus.ACTIVE)

    # Relationships
    parent_topic = relationship("Topic", back_populates="subtopics")
    batch_subtopics = relationship("BatchSubtopic", back_populates="subtopic", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Subtopic(id={self.id}, name={self.name}, parent_topic_id={self.parent_topic_id})>"

    def is_active(self):
        """Check if subtopic is active"""
        return self.status == SubtopicStatus.ACTIVE

    def is_completed(self):
        """Check if subtopic is completed in all batches"""
        if not self.batch_subtopics:
            return False
        
        return all(
            bs.status == "completed" 
            for bs in self.batch_subtopics
        )

    def get_completion_rate(self):
        """Get completion rate across all batches"""
        if not self.batch_subtopics:
            return 0.0
        
        completed_count = len([
            bs for bs in self.batch_subtopics 
            if bs.status == "completed"
        ])
        
        return (completed_count / len(self.batch_subtopics)) * 100

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
        """Get batches where this subtopic is scheduled"""
        return [bs.batch for bs in self.batch_subtopics if bs.batch]

    def get_batches_completed(self):
        """Get batches where this subtopic is completed"""
        return [
            bs.batch for bs in self.batch_subtopics 
            if bs.status == "completed" and bs.batch
        ]

    def get_batches_in_progress(self):
        """Get batches where this subtopic is in progress"""
        return [
            bs.batch for bs in self.batch_subtopics 
            if bs.status == "in_progress" and bs.batch
        ]

    def get_average_completion_time(self):
        """Get average time taken to complete this subtopic across batches"""
        completed_batches = [
            bs for bs in self.batch_subtopics 
            if bs.status == "completed" and bs.completed_date and bs.scheduled_date
        ]
        
        if not completed_batches:
            return 0
        
        total_days = sum(
            (bs.completed_date - bs.scheduled_date).days 
            for bs in completed_batches
        )
        
        return total_days / len(completed_batches)

    def get_faculty_assigned(self):
        """Get list of faculty assigned to teach this subtopic"""
        faculty_list = []
        for bs in self.batch_subtopics:
            if bs.faculty and bs.faculty not in faculty_list:
                faculty_list.append(bs.faculty)
        return faculty_list

    def get_next_subtopic(self):
        """Get the next subtopic in the parent topic"""
        return (
            self.session.query(Subtopic)
            .filter(
                Subtopic.parent_topic_id == self.parent_topic_id,
                Subtopic.order_index == self.order_index + 1,
                Subtopic.status == SubtopicStatus.ACTIVE
            )
            .first()
        )

    def get_previous_subtopic(self):
        """Get the previous subtopic in the parent topic"""
        return (
            self.session.query(Subtopic)
            .filter(
                Subtopic.parent_topic_id == self.parent_topic_id,
                Subtopic.order_index == self.order_index - 1,
                Subtopic.status == SubtopicStatus.ACTIVE
            )
            .first()
        )

    def can_be_started(self, completed_subtopics=None):
        """Check if this subtopic can be started based on prerequisites"""
        if not self.prerequisites:
            return True
        
        if completed_subtopics is None:
            completed_subtopics = []
        
        prerequisites = self.get_prerequisites_list()
        return all(prereq in completed_subtopics for prereq in prerequisites)

    def get_subtopic_summary(self):
        """Get summary of subtopic"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "duration_hours": self.duration_hours,
            "order_index": self.order_index,
            "status": self.status,
            "parent_topic": self.parent_topic.name if self.parent_topic else "Unknown",
            "prerequisites": self.get_prerequisites_list(),
            "learning_materials": self.get_learning_materials_list(),
            "completion_rate": self.get_completion_rate(),
            "batches_scheduled": len(self.get_batches_scheduled()),
            "batches_completed": len(self.get_batches_completed())
        }

    def add_prerequisite(self, prerequisite):
        """Add a prerequisite to this subtopic"""
        if not self.prerequisites:
            self.prerequisites = prerequisite
        else:
            prereqs = self.get_prerequisites_list()
            if prerequisite not in prereqs:
                prereqs.append(prerequisite)
                self.prerequisites = ", ".join(prereqs)

    def remove_prerequisite(self, prerequisite):
        """Remove a prerequisite from this subtopic"""
        if not self.prerequisites:
            return
        
        prereqs = self.get_prerequisites_list()
        if prerequisite in prereqs:
            prereqs.remove(prerequisite)
            self.prerequisites = ", ".join(prereqs)

    def add_learning_material(self, material):
        """Add a learning material to this subtopic"""
        if not self.learning_materials:
            self.learning_materials = material
        else:
            materials = self.get_learning_materials_list()
            if material not in materials:
                materials.append(material)
                self.learning_materials = ", ".join(materials)

    def remove_learning_material(self, material):
        """Remove a learning material from this subtopic"""
        if not self.learning_materials:
            return
        
        materials = self.get_learning_materials_list()
        if material in materials:
            materials.remove(material)
            self.learning_materials = ", ".join(materials)

    def get_subtopic_path(self):
        """Get full path of subtopic (including parent topic)"""
        if self.parent_topic:
            return f"{self.parent_topic.name} > {self.name}"
        return self.name

    def get_depth_level(self):
        """Get depth level (1 for direct subtopic, 2+ for nested)"""
        # For now, return 1 as we only support one level of subtopics
        return 1

    def is_leaf_subtopic(self):
        """Check if this is a leaf subtopic (no further subdivisions)"""
        # For now, all subtopics are leaf nodes
        return True

    def get_progress_metrics(self):
        """Get detailed progress metrics for this subtopic"""
        total_batches = len(self.batch_subtopics)
        if total_batches == 0:
            return {
                "total_batches": 0,
                "completed_batches": 0,
                "in_progress_batches": 0,
                "completion_rate": 0.0,
                "average_completion_time": 0
            }
        
        completed_batches = len([
            bs for bs in self.batch_subtopics 
            if bs.status == "completed"
        ])
        
        in_progress_batches = len([
            bs for bs in self.batch_subtopics 
            if bs.status == "in_progress"
        ])
        
        return {
            "total_batches": total_batches,
            "completed_batches": completed_batches,
            "in_progress_batches": in_progress_batches,
            "completion_rate": self.get_completion_rate(),
            "average_completion_time": self.get_average_completion_time()
        }

    def validate_subtopic(self):
        """Validate subtopic data"""
        errors = []
        
        if not self.name or len(self.name.strip()) == 0:
            errors.append("Subtopic name is required")
        
        if self.duration_hours <= 0:
            errors.append("Duration must be greater than 0")
        
        if self.order_index < 1:
            errors.append("Order index must be greater than 0")
        
        return errors

    def clone_for_topic(self, new_parent_topic_id):
        """Clone this subtopic for a different parent topic"""
        return Subtopic(
            parent_topic_id=new_parent_topic_id,
            name=self.name,
            description=self.description,
            duration_hours=self.duration_hours,
            prerequisites=self.prerequisites,
            learning_materials=self.learning_materials,
            status=self.status
        )

    def get_difficulty_level(self):
        """Estimate difficulty level based on duration and prerequisites"""
        difficulty = "Easy"
        
        if self.duration_hours > 3:
            difficulty = "Medium"
        
        if self.duration_hours > 6:
            difficulty = "Hard"
        
        if self.prerequisites and len(self.get_prerequisites_list()) > 2:
            difficulty = "Very Hard"
        
        return difficulty

    def get_estimated_completion_date(self, start_date):
        """Get estimated completion date based on duration"""
        from datetime import timedelta
        
        return start_date + timedelta(hours=self.duration_hours)