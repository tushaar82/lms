# Student Academics Management System

A comprehensive Student Academics Management System designed for computer institutes with multiple centers. The system focuses on tracking student learning progress, faculty time management, and providing detailed insights through analytics and reporting.

## Features

- **Multi-Center Support**: Manage multiple institute locations with isolated data
- **User Management**: Role-based access control for Super Admin, Center Admin, Faculty, Academic Head, and Students
- **Student Management**: Complete student lifecycle management with enrollment, progress tracking, and performance analytics
- **Faculty Management**: Faculty profiles, workload management, availability tracking, and performance evaluation
- **Batch Management**: Flexible batch creation, scheduling, and enrollment management
- **Attendance System**: Mobile-friendly attendance marking with analytics and alerts
- **Progress Tracking**: Topic-wise progress monitoring with completion analytics
- **Feedback System**: Student-to-faculty feedback with analytics and insights
- **Analytics & Reporting**: Comprehensive dashboards with Gantt charts and Kanban boards
- **Notifications**: Real-time notifications for attendance, progress, and system updates

## Technology Stack

### Backend
- **FastAPI**: Python web framework for building APIs
- **PostgreSQL**: Primary database for storing application data
- **Redis**: Caching and session management
- **SQLAlchemy**: ORM for database operations
- **Alembic**: Database migration management

### Frontend (Planned)
- **React.js**: JavaScript library for building user interfaces
- **Volt React Dashboard**: Dashboard template for UI components
- **Google Charts**: For Gantt charts and data visualization

### Deployment
- **Docker**: Containerization for deployment
- **Nginx**: Reverse proxy and load balancing

## Project Structure

```
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI application entry point
│   │   ├── config.py             # Application configuration
│   │   ├── database.py           # Database connection and session management
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── security.py       # Authentication and authorization utilities
│   │   │   ├── exceptions.py     # Custom exception classes
│   │   │   └── utils.py         # Utility functions
│   │   ├── models/              # Database models
│   │   │   ├── __init__.py
│   │   │   ├── base.py          # Base model class
│   │   │   ├── user.py          # User model
│   │   │   ├── center.py        # Center model
│   │   │   ├── student.py       # Student model
│   │   │   ├── faculty.py       # Faculty model
│   │   │   ├── subject.py       # Subject model
│   │   │   ├── topic.py         # Topic model
│   │   │   ├── batch.py         # Batch model
│   │   │   ├── student_batch.py # Student-Batch relationship
│   │   │   ├── attendance.py    # Attendance model
│   │   │   ├── batch_topic.py   # Batch-Topic relationship
│   │   │   ├── feedback.py      # Feedback model
│   │   │   ├── notification.py  # Notification model
│   │   │   ├── batch_extension.py # Batch extension model
│   │   │   ├── faculty_availability.py # Faculty availability
│   │   │   └── faculty_performance.py # Faculty performance
│   │   └── api/                # API routes (to be created)
│   ├── alembic/                 # Database migrations
│   ├── requirements.txt           # Python dependencies
│   └── Dockerfile              # Docker configuration
├── docker-compose.yml           # Docker compose configuration
├── .env.example               # Environment variables template
└── README.md                 # This file
```

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development)
- PostgreSQL 15+ (for local development)
- Redis 7+ (for local development)

### Using Docker Compose (Recommended)

1. Clone the repository:
```bash
git clone <repository-url>
cd lms
```

2. Copy environment file:
```bash
cp .env.example .env
```

3. Update environment variables in `.env` file as needed.

4. Start the services:
```bash
docker-compose up -d
```

5. The API will be available at `http://localhost:8000`
6. API documentation will be available at `http://localhost:8000/docs`

### Local Development Setup

1. Install Python dependencies:
```bash
cd backend
pip install -r requirements.txt
```

2. Set up PostgreSQL and Redis services.

3. Copy and configure environment variables:
```bash
cp .env.example .env
# Edit .env with your database and Redis credentials
```

4. Run database migrations:
```bash
alembic upgrade head
```

5. Start the development server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

Once the server is running, you can access:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`

## Database Migrations

### Create new migration
```bash
alembic revision --autogenerate -m "Description of changes"
```

### Apply migrations
```bash
alembic upgrade head
```

### Rollback migration
```bash
alembic downgrade -1
```

## Development Phases

The project is being developed in phases:

1. **Phase 1**: Backend Foundation Setup ✅
2. **Phase 2**: Authentication & User Management
3. **Phase 3**: Core Entity Management APIs
4. **Phase 4**: Batch & Enrollment System
5. **Phase 5**: Attendance Management System
6. **Phase 6**: Progress Tracking & Analytics
7. **Phase 7**: Frontend Foundation
8. **Phase 8**: Frontend Authentication & User Management
9. **Phase 9**: Frontend Entity Management Interfaces
10. **Phase 10**: Frontend Attendance & Progress Tracking
11. **Phase 11**: Analytics & Reporting Dashboard
12. **Phase 12**: Testing & Quality Assurance
13. **Phase 13**: Deployment & Documentation

## Configuration

### Environment Variables

Key environment variables (see `.env.example` for complete list):

- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `SECRET_KEY`: JWT secret key
- `ENVIRONMENT`: Development/Production environment
- `DEBUG`: Enable debug mode

### Database Configuration

The system uses PostgreSQL as the primary database. The schema is designed to support:

- Multi-center data isolation
- Complex relationships between entities
- Audit trails with timestamps
- Performance-optimized queries

### Security Features

- JWT-based authentication with refresh tokens
- Role-based access control (RBAC)
- Password hashing with bcrypt
- Input validation and sanitization
- CORS protection
- Rate limiting (planned)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions, please open an issue in the repository.