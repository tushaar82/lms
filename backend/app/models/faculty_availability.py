"""
FacultyAvailability model for managing faculty availability
"""

from sqlalchemy import Column, Integer, Date, Time, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship
import enum

from app.models.base import BaseModel


class AvailabilityStatus(str, enum.Enum):
    """Availability status enumeration"""
    AVAILABLE = "available"
    BUSY = "busy"
    ON_LEAVE = "on_leave"


class FacultyAvailability(BaseModel):
    """
    FacultyAvailability model for managing faculty availability
    """
    __tablename__ = "faculty_availability"

    faculty_id = Column(Integer, ForeignKey("faculty.user_id"), nullable=False)
    date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    status = Column(Enum(AvailabilityStatus), nullable=False)
    remarks = Column(Text)

    # Relationships
    faculty = relationship("Faculty", back_populates="availability")

    def __repr__(self):
        return f"<FacultyAvailability(id={self.id}, faculty_id={self.faculty_id}, date={self.date}, status={self.status})>"

    def is_available(self):
        """Check if faculty is available"""
        return self.status == AvailabilityStatus.AVAILABLE

    def is_busy(self):
        """Check if faculty is busy"""
        return self.status == AvailabilityStatus.BUSY

    def is_on_leave(self):
        """Check if faculty is on leave"""
        return self.status == AvailabilityStatus.ON_LEAVE

    def get_duration_hours(self):
        """Get duration in hours"""
        from datetime import datetime
        
        # Convert time strings to datetime objects for calculation
        start_datetime = datetime.combine(self.date, self.start_time)
        end_datetime = datetime.combine(self.date, self.end_time)
        
        duration = end_datetime - start_datetime
        return duration.total_seconds() / 3600  # Convert to hours

    def get_duration_minutes(self):
        """Get duration in minutes"""
        return self.get_duration_hours() * 60

    def overlaps_with(self, other_availability):
        """Check if this availability overlaps with another"""
        if self.date != other_availability.date:
            return False
        
        # Check time overlap
        return (
            (self.start_time <= other_availability.start_time < self.end_time) or
            (other_availability.start_time <= self.start_time < other_availability.end_time)
        )

    def can_schedule_batch(self, batch_start_time, batch_end_time, batch_date):
        """Check if a batch can be scheduled during this availability"""
        if self.date != batch_date:
            return False
        
        if not self.is_available():
            return False
        
        # Check if batch time fits within availability
        return (
            self.start_time <= batch_start_time and
            batch_end_time <= self.end_time
        )

    def get_time_slot_summary(self):
        """Get human-readable time slot summary"""
        return f"{self.start_time.strftime('%I:%M %p')} - {self.end_time.strftime('%I:%M %p')}"

    def get_full_summary(self):
        """Get full summary of availability"""
        return {
            "date": self.date,
            "time_slot": self.get_time_slot_summary(),
            "duration_hours": self.get_duration_hours(),
            "status": self.status,
            "remarks": self.remarks
        }

    def mark_as_busy(self, remarks=None):
        """Mark availability as busy"""
        self.status = AvailabilityStatus.BUSY
        if remarks:
            self.remarks = remarks

    def mark_as_available(self, remarks=None):
        """Mark availability as available"""
        self.status = AvailabilityStatus.AVAILABLE
        if remarks:
            self.remarks = remarks

    def mark_as_on_leave(self, remarks=None):
        """Mark availability as on leave"""
        self.status = AvailabilityStatus.ON_LEAVE
        if remarks:
            self.remarks = remarks

    def get_conflicting_batches(self):
        """Get batches that conflict with this availability"""
        # This would need to query batches that overlap with this time slot
        # For now, return empty list
        return []

    def can_be_modified_by(self, user_role, user_id):
        """Check if availability can be modified by user"""
        # Faculty can modify their own availability
        if user_role == "faculty" and self.faculty_id == user_id:
            return True
        
        # Center admin and above can modify any availability
        if user_role in ["center_admin", "academic_head", "super_admin"]:
            return True
        
        return False

    def create_notification_for_conflict(self, conflicting_batch):
        """Create notification for scheduling conflict"""
        from app.models.notification import Notification
        
        return Notification(
            user_id=self.faculty_id,
            title="Scheduling Conflict",
            message=f"Batch {conflicting_batch.name} conflicts with your availability",
            type="warning",
            category="batch",
            related_id=conflicting_batch.id
        )

    def get_weekday(self):
        """Get weekday name"""
        import calendar
        return calendar.day_name[self.date.weekday()]

    def is_weekend(self):
        """Check if date is weekend"""
        return self.date.weekday() >= 5  # Saturday=5, Sunday=6

    def is_working_hours(self, start_hour=9, end_hour=18):
        """Check if time slot is within working hours"""
        return (
            self.start_time.hour >= start_hour and
            self.end_time.hour <= end_hour
        )

    def get_optimal_batch_duration(self):
        """Get optimal batch duration for this time slot"""
        # Standard batch duration is 2-3 hours
        max_duration = self.get_duration_hours()
        
        if max_duration >= 3:
            return 3
        elif max_duration >= 2:
            return 2
        else:
            return max_duration

    def can_accommodate_batch(self, required_hours):
        """Check if availability can accommodate a batch of required hours"""
        return self.get_duration_hours() >= required_hours

    def get_break_suggestions(self):
        """Get suggestions for breaks during long availability"""
        duration = self.get_duration_hours()
        
        if duration > 4:
            return [
                "Consider adding a 15-minute break every 2 hours",
                "Split into multiple sessions if possible"
            ]
        elif duration > 2:
            return [
                "Consider a 10-minute break midway"
            ]
        else:
            return []

    def get_utilization_rate(self):
        """Get utilization rate of this availability slot"""
        conflicting_batches = self.get_conflicting_batches()
        
        if not conflicting_batches:
            return 0.0
        
        # Calculate total time used by batches
        total_batch_time = sum(
            batch.get_duration_hours() for batch in conflicting_batches
        )
        
        return (total_batch_time / self.get_duration_hours()) * 100

    def get_efficiency_score(self):
        """Get efficiency score for this availability"""
        utilization = self.get_utilization_rate()
        
        if utilization >= 80:
            return "excellent"
        elif utilization >= 60:
            return "good"
        elif utilization >= 40:
            return "average"
        else:
            return "poor"

    @staticmethod
    def create_recurring_availability(faculty_id, start_date, end_date, 
                                   start_time, end_time, weekdays, status="available"):
        """Create recurring availability for specified weekdays"""
        from datetime import datetime, timedelta
        
        availabilities = []
        current_date = start_date
        
        while current_date <= end_date:
            if current_date.weekday() in weekdays:
                availability = FacultyAvailability(
                    faculty_id=faculty_id,
                    date=current_date,
                    start_time=start_time,
                    end_time=end_time,
                    status=AvailabilityStatus(status)
                )
                availabilities.append(availability)
            
            current_date += timedelta(days=1)
        
        return availabilities

    def get_recurring_pattern(self):
        """Get recurring pattern if this is part of a recurring schedule"""
        # This would need to check for patterns in faculty's availability
        # For now, return None
        return None