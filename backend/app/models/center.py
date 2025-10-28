"""
Center model for multi-center management
"""

from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
import enum

from app.models.base import BaseModel


class CenterStatus(str, enum.Enum):
    """Center status enumeration"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"


class Center(BaseModel):
    """
    Center model for managing multiple institute locations
    """
    __tablename__ = "centers"

    name = Column(String(100), nullable=False)
    code = Column(String(20), unique=True, nullable=False, index=True)
    address = Column(String(255))
    city = Column(String(50))
    state = Column(String(50))
    country = Column(String(50), default="India")
    phone = Column(String(20))
    email = Column(String(100))
    status = Column(Enum(CenterStatus), default=CenterStatus.ACTIVE)

    # Relationships
    users = relationship("User", back_populates="center")
    batches = relationship("Batch", back_populates="center")
    students = relationship("Student", secondary="student_batches", back_populates="centers")
    faculty = relationship("Faculty", back_populates="center")

    def __repr__(self):
        return f"<Center(id={self.id}, name={self.name}, code={self.code})>"

    @property
    def full_address(self):
        """Get complete address"""
        address_parts = []
        if self.address:
            address_parts.append(self.address)
        if self.city:
            address_parts.append(self.city)
        if self.state:
            address_parts.append(self.state)
        if self.country:
            address_parts.append(self.country)
        return ", ".join(address_parts)

    def is_active(self):
        """Check if center is active"""
        return self.status == CenterStatus.ACTIVE

    def get_active_users_count(self):
        """Get count of active users in this center"""
        return len([user for user in self.users if user.is_active()])

    def get_active_batches_count(self):
        """Get count of active batches in this center"""
        return len([batch for batch in self.batches if batch.is_active()])

    def get_total_students_count(self):
        """Get total number of students enrolled in this center"""
        return len(self.students)

    def get_total_faculty_count(self):
        """Get total number of faculty in this center"""
        return len(self.faculty)