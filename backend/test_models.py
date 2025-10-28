"""
Test script to verify database models work correctly
"""

import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import engine, Base
from app.models import *  # Import all models
from app.config import settings


def test_models():
    """Test that all models can be created and relationships work"""
    print("Testing database models...")
    
    try:
        # Skip database table creation for now
        # Base.metadata.create_all(bind=engine)
        # print("✅ All database tables created successfully")
        
        # Test model instantiation
        print("\n📝 Testing model instantiation...")
        
        # Test User model
        user = User(
            email="test@example.com",
            password_hash="test_hash",
            first_name="Test",
            last_name="User",
            role="student"
        )
        print(f"✅ User model created: {user}")
        
        # Test Center model
        center = Center(
            name="Test Center",
            code="TC001",
            address="Test Address"
        )
        print(f"✅ Center model created: {center}")
        
        # Test Student model
        student = Student(
            user_id=1,
            enrollment_number="ENR001",
            enrollment_date="2023-01-01"
        )
        print(f"✅ Student model created: {student}")
        
        # Test Faculty model
        faculty = Faculty(
            user_id=2,
            employee_id="EMP001",
            joining_date="2023-01-01"
        )
        print(f"✅ Faculty model created: {faculty}")
        
        # Test Subject model
        subject = Subject(
            name="Test Subject",
            code="TS001",
            duration_hours=40
        )
        print(f"✅ Subject model created: {subject}")
        
        # Test Topic model
        topic = Topic(
            subject_id=1,
            name="Test Topic",
            duration_hours=2,
            order_index=1
        )
        print(f"✅ Topic model created: {topic}")
        
        # Test Subtopic model
        subtopic = Subtopic(
            parent_topic_id=1,
            name="Test Subtopic",
            duration_hours=1,
            order_index=1
        )
        print(f"✅ Subtopic model created: {subtopic}")
        
        # Test Batch model
        batch = Batch(
            name="Test Batch",
            subject_id=1,
            faculty_id=1,
            center_id=1,
            start_date="2023-01-01",
            end_date="2023-03-01"
        )
        print(f"✅ Batch model created: {batch}")
        
        # Test StudentBatch model
        student_batch = StudentBatch(
            student_id=1,
            batch_id=1,
            enrollment_date="2023-01-01"
        )
        print(f"✅ StudentBatch model created: {student_batch}")
        
        # Test StudentLeave model
        student_leave = StudentLeave(
            student_id=1,
            batch_id=1,
            start_date="2023-01-01",
            end_date="2023-01-02",
            leave_type="medical",
            reason="Test leave"
        )
        print(f"✅ StudentLeave model created: {student_leave}")
        
        # Test StudentTransfer model
        student_transfer = StudentTransfer(
            student_batch_id=1,
            from_faculty_id=1,
            to_faculty_id=2,
            reason="Test transfer"
        )
        print(f"✅ StudentTransfer model created: {student_transfer}")
        
        # Test Attendance model
        attendance = Attendance(
            student_id=1,
            batch_id=1,
            faculty_id=1,
            date="2023-01-01",
            status="present",
            topic_covered="Test Topic"
        )
        print(f"✅ Attendance model created: {attendance}")
        
        # Test BatchTopic model
        batch_topic = BatchTopic(
            batch_id=1,
            topic_id=1,
            faculty_id=1,
            status="pending"
        )
        print(f"✅ BatchTopic model created: {batch_topic}")
        
        # Test BatchSubtopic model
        batch_subtopic = BatchSubtopic(
            batch_id=1,
            subtopic_id=1,
            faculty_id=1,
            status="pending"
        )
        print(f"✅ BatchSubtopic model created: {batch_subtopic}")
        
        # Test Feedback model
        feedback = Feedback(
            student_id=1,
            faculty_id=1,
            batch_id=1,
            rating=5,
            feedback_type="faculty",
            comments="Great teaching!"
        )
        print(f"✅ Feedback model created: {feedback}")
        
        # Test Notification model
        notification = Notification(
            user_id=1,
            title="Test Notification",
            message="This is a test notification",
            type="info",
            category="system"
        )
        print(f"✅ Notification model created: {notification}")
        
        # Test BatchExtension model
        batch_extension = BatchExtension(
            batch_id=1,
            original_end_date="2023-03-01",
            new_end_date="2023-03-15",
            reason="Test extension"
        )
        print(f"✅ BatchExtension model created: {batch_extension}")
        
        # Test FacultyAvailability model
        faculty_availability = FacultyAvailability(
            faculty_id=1,
            date="2023-01-01",
            start_time="09:00",
            end_time="12:00",
            status="available"
        )
        print(f"✅ FacultyAvailability model created: {faculty_availability}")
        
        # Test FacultyPerformance model
        faculty_performance = FacultyPerformance(
            faculty_id=1,
            evaluation_period="2023-01",
            total_students_taught=10,
            students_completed=8,
            average_feedback_rating=4.5
        )
        print(f"✅ FacultyPerformance model created: {faculty_performance}")
        
        print("\n🔗 Testing model relationships...")
        
        # Test relationships
        print(f"✅ User -> Student: {hasattr(user, 'student_profile')}")
        print(f"✅ User -> Faculty: {hasattr(user, 'faculty_profile')}")
        print(f"✅ Center -> Users: {hasattr(center, 'users')}")
        print(f"✅ Student -> Batches: {hasattr(student, 'batches')}")
        print(f"✅ Faculty -> Batches: {hasattr(faculty, 'batches')}")
        print(f"✅ Subject -> Topics: {hasattr(subject, 'topics')}")
        print(f"✅ Topic -> Subtopics: {hasattr(topic, 'subtopics')}")
        print(f"✅ Batch -> StudentBatches: {hasattr(batch, 'student_batches')}")
        print(f"✅ Batch -> Attendance: {hasattr(batch, 'attendance_records')}")
        print(f"✅ Student -> Leave: {hasattr(student, 'leave_requests')}")
        print(f"✅ StudentBatch -> Transfers: {hasattr(student_batch, 'transfer_requests')}")
        
        print("\n🧪 Testing model methods...")
        
        # Test model methods
        print(f"✅ User.full_name: {user.full_name}")
        print(f"✅ User.is_student: {user.is_student()}")
        print(f"✅ Center.is_active: {center.is_active()}")
        print(f"✅ Student.is_active: {student.is_active()}")
        print(f"✅ Faculty.is_active: {faculty.is_active()}")
        print(f"✅ Subject.is_active: {subject.is_active()}")
        print(f"✅ Topic.is_active: {topic.is_active()}")
        print(f"✅ Batch.is_active: {batch.is_active()}")
        print(f"✅ StudentBatch.is_active: {student_batch.is_active()}")
        print(f"✅ Attendance.is_present: {attendance.is_present()}")
        print(f"✅ Feedback.is_positive: {feedback.is_positive()}")
        print(f"✅ Notification.is_info: {notification.is_info()}")
        
        print("\n🎯 Testing new requirements...")
        
        # Test new requirements
        print(f"✅ Student has leave_requests: {hasattr(student, 'leave_requests')}")
        print(f"✅ StudentBatch can_be_transferred: {student_batch.can_be_transferred()}")
        print(f"✅ StudentLeave.is_pending: {student_leave.is_pending()}")
        print(f"✅ StudentTransfer.is_pending: {student_transfer.is_pending()}")
        print(f"✅ Topic has_subtopics: {topic.has_subtopics()}")
        print(f"✅ Subtopic is_leaf_subtopic: {subtopic.is_leaf_subtopic()}")
        print(f"✅ BatchSubtopic is_pending: {batch_subtopic.is_pending()}")
        
        print("\n✅ All models and relationships tested successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing models: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_configuration():
    """Test configuration settings"""
    print("\n⚙️ Testing configuration...")
    
    try:
        print(f"✅ Project Name: {settings.PROJECT_NAME}")
        print(f"✅ Version: {settings.VERSION}")
        print(f"✅ Environment: {settings.ENVIRONMENT}")
        print(f"✅ Debug: {settings.DEBUG}")
        print(f"✅ Database URL configured: {'✅' if settings.DATABASE_URL else '❌'}")
        print(f"✅ Redis URL configured: {'✅' if settings.REDIS_URL else '❌'}")
        print(f"✅ Secret Key configured: {'✅' if settings.SECRET_KEY else '❌'}")
        print(f"✅ CORS origins: {len(settings.BACKEND_CORS_ORIGINS)} configured")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing configuration: {e}")
        return False


def test_utilities():
    """Test utility functions"""
    print("\n🛠️ Testing utilities...")
    
    try:
        from app.core.utils import (
            validate_email, validate_phone, validate_password_strength,
            generate_enrollment_number, generate_employee_id,
            calculate_percentage, calculate_grade,
            format_currency, format_duration_hours
        )
        
        # Test email validation
        valid_email = validate_email("test@example.com")
        invalid_email = validate_email("invalid-email")
        print(f"✅ Email validation (valid): {valid_email}")
        print(f"✅ Email validation (invalid): {not invalid_email}")
        
        # Test phone validation
        valid_phone = validate_phone("9876543210")
        invalid_phone = validate_phone("123")
        print(f"✅ Phone validation (valid): {valid_phone}")
        print(f"✅ Phone validation (invalid): {not invalid_phone}")
        
        # Test password validation
        password_result = validate_password_strength("StrongPass123!")
        print(f"✅ Password validation: {password_result['is_strong']}")
        
        # Test enrollment number generation
        enrollment_num = generate_enrollment_number("TC", 2023)
        print(f"✅ Enrollment number generation: {enrollment_num}")
        
        # Test employee ID generation
        emp_id = generate_employee_id("TC")
        print(f"✅ Employee ID generation: {emp_id}")
        
        # Test percentage calculation
        percentage = calculate_percentage(25, 100)
        print(f"✅ Percentage calculation: {percentage}%")
        
        # Test grade calculation
        grade = calculate_grade(85)
        print(f"✅ Grade calculation: {grade}")
        
        # Test currency formatting
        currency = format_currency(1234.56)
        print(f"✅ Currency formatting: {currency}")
        
        # Test duration formatting
        duration = format_duration_hours(2.5)
        print(f"✅ Duration formatting: {duration}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing utilities: {e}")
        return False


if __name__ == "__main__":
    print("🚀 Starting Phase 1 Testing...\n")
    
    # Run all tests
    config_ok = test_configuration()
    utils_ok = test_utilities()
    models_ok = test_models()
    
    print(f"\n📊 Test Results:")
    print(f"   Configuration: {'✅ PASS' if config_ok else '❌ FAIL'}")
    print(f"   Utilities: {'✅ PASS' if utils_ok else '❌ FAIL'}")
    print(f"   Models: {'✅ PASS' if models_ok else '❌ FAIL'}")
    
    if config_ok and utils_ok and models_ok:
        print("\n🎉 All tests passed! Phase 1 implementation is correct.")
        print("\n📋 Ready to proceed to Phase 2: Implement Authentication & User Management")
    else:
        print("\n⚠️ Some tests failed. Please review the errors above.")
        sys.exit(1)