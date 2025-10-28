"""
Main API router for v1 endpoints
"""

from fastapi import APIRouter

from app.api.v1.endpoints import auth, users, centers, students, faculty, subjects, batches, attendance, feedback, notifications

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(centers.router, prefix="/centers", tags=["centers"])
api_router.include_router(students.router, prefix="/students", tags=["students"])
api_router.include_router(faculty.router, prefix="/faculty", tags=["faculty"])
api_router.include_router(subjects.router, prefix="/subjects", tags=["subjects"])
api_router.include_router(batches.router, prefix="/batches", tags=["batches"])
api_router.include_router(attendance.router, prefix="/attendance", tags=["attendance"])
api_router.include_router(feedback.router, prefix="/feedback", tags=["feedback"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["notifications"])