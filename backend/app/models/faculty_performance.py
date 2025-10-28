"""
FacultyPerformance model for tracking faculty performance metrics
"""

from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class FacultyPerformance(BaseModel):
    """
    FacultyPerformance model for tracking faculty performance metrics
    """
    __tablename__ = "faculty_performance"

    faculty_id = Column(Integer, ForeignKey("faculty.user_id"), nullable=False)
    evaluation_period = Column(String(20), nullable=False)  # e.g., '2023-10', 'Q4-2023'
    total_students_taught = Column(Integer, default=0)
    students_completed = Column(Integer, default=0)
    average_completion_rate = Column(Numeric(5, 2))
    average_feedback_rating = Column(Numeric(3, 2))
    total_classes_taken = Column(Integer, default=0)
    attendance_percentage = Column(Numeric(5, 2))
    punctuality_score = Column(Numeric(5, 2))
    syllabus_coverage_percentage = Column(Numeric(5, 2))
    overall_score = Column(Numeric(5, 2))

    # Relationships
    faculty = relationship("Faculty", back_populates="performance_records")

    def __repr__(self):
        return f"<FacultyPerformance(id={self.id}, faculty_id={self.faculty_id}, period={self.evaluation_period})>"

    def get_completion_rate(self):
        """Get student completion rate"""
        if self.total_students_taught == 0:
            return 0.0
        return (self.students_completed / self.total_students_taught) * 100

    def get_performance_grade(self):
        """Get performance grade based on overall score"""
        if self.overall_score >= 90:
            return "A+"
        elif self.overall_score >= 80:
            return "A"
        elif self.overall_score >= 70:
            return "B"
        elif self.overall_score >= 60:
            return "C"
        elif self.overall_score >= 50:
            return "D"
        else:
            return "F"

    def get_performance_level(self):
        """Get performance level description"""
        score = float(self.overall_score or 0)
        
        if score >= 90:
            return "Outstanding"
        elif score >= 80:
            return "Excellent"
        elif score >= 70:
            return "Good"
        elif score >= 60:
            return "Average"
        elif score >= 50:
            return "Below Average"
        else:
            return "Poor"

    def get_feedback_quality(self):
        """Get feedback quality description"""
        if not self.average_feedback_rating:
            return "No Feedback"
        
        rating = float(self.average_feedback_rating)
        
        if rating >= 4.5:
            return "Exceptional"
        elif rating >= 4.0:
            return "Excellent"
        elif rating >= 3.5:
            return "Good"
        elif rating >= 3.0:
            return "Average"
        else:
            return "Needs Improvement"

    def get_attendance_quality(self):
        """Get attendance quality description"""
        if not self.attendance_percentage:
            return "No Data"
        
        attendance = float(self.attendance_percentage)
        
        if attendance >= 95:
            return "Excellent"
        elif attendance >= 90:
            return "Good"
        elif attendance >= 85:
            return "Average"
        else:
            return "Needs Improvement"

    def get_punctuality_quality(self):
        """Get punctuality quality description"""
        if not self.punctuality_score:
            return "No Data"
        
        score = float(self.punctuality_score)
        
        if score >= 95:
            return "Excellent"
        elif score >= 90:
            return "Good"
        elif score >= 85:
            return "Average"
        else:
            return "Needs Improvement"

    def calculate_overall_score(self):
        """Calculate overall performance score"""
        weights = {
            "completion_rate": 0.25,
            "feedback_rating": 0.25,
            "attendance": 0.20,
            "punctuality": 0.15,
            "syllabus_coverage": 0.15
        }
        
        scores = {
            "completion_rate": float(self.average_completion_rate or 0),
            "feedback_rating": (float(self.average_feedback_rating or 0) / 5) * 100,  # Convert to 100 scale
            "attendance": float(self.attendance_percentage or 0),
            "punctuality": float(self.punctuality_score or 0),
            "syllabus_coverage": float(self.syllabus_coverage_percentage or 0)
        }
        
        overall_score = sum(
            scores[metric] * weights[metric] 
            for metric in weights
        )
        
        self.overall_score = round(overall_score, 2)
        return self.overall_score

    def get_strengths(self):
        """Get faculty strengths based on performance metrics"""
        strengths = []
        
        if float(self.average_completion_rate or 0) >= 80:
            strengths.append("High student completion rate")
        
        if float(self.average_feedback_rating or 0) >= 4.0:
            strengths.append("Excellent student feedback")
        
        if float(self.attendance_percentage or 0) >= 90:
            strengths.append("High student attendance")
        
        if float(self.punctuality_score or 0) >= 90:
            strengths.append("Excellent punctuality")
        
        if float(self.syllabus_coverage_percentage or 0) >= 90:
            strengths.append("Complete syllabus coverage")
        
        return strengths

    def get_improvement_areas(self):
        """Get areas that need improvement"""
        improvements = []
        
        if float(self.average_completion_rate or 0) < 60:
            improvements.append("Student completion rate")
        
        if float(self.average_feedback_rating or 0) < 3.0:
            improvements.append("Student feedback ratings")
        
        if float(self.attendance_percentage or 0) < 85:
            improvements.append("Student attendance")
        
        if float(self.punctuality_score or 0) < 85:
            improvements.append("Punctuality")
        
        if float(self.syllabus_coverage_percentage or 0) < 80:
            improvements.append("Syllabus coverage")
        
        return improvements

    def get_performance_summary(self):
        """Get comprehensive performance summary"""
        return {
            "period": self.evaluation_period,
            "faculty_name": self.faculty.full_name if self.faculty else "Unknown",
            "overall_score": float(self.overall_score or 0),
            "grade": self.get_performance_grade(),
            "level": self.get_performance_level(),
            "metrics": {
                "students_taught": self.total_students_taught,
                "students_completed": self.students_completed,
                "completion_rate": float(self.average_completion_rate or 0),
                "feedback_rating": float(self.average_feedback_rating or 0),
                "feedback_quality": self.get_feedback_quality(),
                "total_classes": self.total_classes_taken,
                "attendance_percentage": float(self.attendance_percentage or 0),
                "attendance_quality": self.get_attendance_quality(),
                "punctuality_score": float(self.punctuality_score or 0),
                "punctuality_quality": self.get_punctuality_quality(),
                "syllabus_coverage": float(self.syllabus_coverage_percentage or 0)
            },
            "strengths": self.get_strengths(),
            "improvement_areas": self.get_improvement_areas()
        }

    def compare_with_period(self, other_performance):
        """Compare performance with another period"""
        if not other_performance:
            return None
        
        comparison = {}
        
        metrics = [
            "overall_score",
            "average_completion_rate",
            "average_feedback_rating",
            "attendance_percentage",
            "punctuality_score",
            "syllabus_coverage_percentage"
        ]
        
        for metric in metrics:
            current = float(getattr(self, metric) or 0)
            previous = float(getattr(other_performance, metric) or 0)
            
            change = current - previous
            change_percent = ((current - previous) / previous * 100) if previous > 0 else 0
            
            comparison[metric] = {
                "current": current,
                "previous": previous,
                "change": change,
                "change_percent": change_percent,
                "trend": "improving" if change > 0 else "declining" if change < 0 else "stable"
            }
        
        return comparison

    def get_ranking_percentile(self, all_performances):
        """Get ranking percentile among all faculty performances"""
        if not all_performances:
            return 0
        
        scores = [
            float(p.overall_score or 0) 
            for p in all_performances 
            if p.overall_score is not None
        ]
        
        if not scores:
            return 0
        
        scores.sort(reverse=True)
        current_score = float(self.overall_score or 0)
        
        try:
            rank = scores.index(current_score) + 1
            percentile = ((len(scores) - rank) / len(scores)) * 100
            return round(percentile, 2)
        except ValueError:
            return 0

    def create_performance_report(self):
        """Create detailed performance report"""
        return {
            "faculty_info": {
                "name": self.faculty.full_name if self.faculty else "Unknown",
                "employee_id": self.faculty.employee_id if self.faculty else "Unknown",
                "specialization": self.faculty.specialization if self.faculty else "Unknown"
            },
            "evaluation_period": self.evaluation_period,
            "performance_metrics": self.get_performance_summary(),
            "recommendations": self.get_recommendations(),
            "goals": self.get_suggested_goals()
        }

    def get_recommendations(self):
        """Get recommendations based on performance"""
        recommendations = []
        
        if float(self.average_completion_rate or 0) < 70:
            recommendations.append("Focus on student engagement and support")
        
        if float(self.average_feedback_rating or 0) < 3.5:
            recommendations.append("Improve teaching methodology and communication")
        
        if float(self.attendance_percentage or 0) < 85:
            recommendations.append("Make classes more interactive and engaging")
        
        if float(self.punctuality_score or 0) < 90:
            recommendations.append("Ensure timely arrival and class management")
        
        if float(self.syllabus_coverage_percentage or 0) < 85:
            recommendations.append("Optimize time management for complete syllabus coverage")
        
        return recommendations

    def get_suggested_goals(self):
        """Get suggested goals for next evaluation period"""
        goals = []
        
        current_completion = float(self.average_completion_rate or 0)
        if current_completion < 80:
            goals.append(f"Achieve {min(current_completion + 10, 90)}% student completion rate")
        
        current_feedback = float(self.average_feedback_rating or 0)
        if current_feedback < 4.0:
            goals.append(f"Maintain {min(current_feedback + 0.5, 4.5)}+ average feedback rating")
        
        current_attendance = float(self.attendance_percentage or 0)
        if current_attendance < 90:
            goals.append(f"Achieve {min(current_attendance + 5, 95)}% student attendance")
        
        return goals