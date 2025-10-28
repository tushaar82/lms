# Project Structure and Docker Setup

## Project Directory Structure

```
student-academics-management/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI application entry point
│   │   ├── config.py               # Configuration settings
│   │   ├── database.py             # Database connection setup
│   │   ├── dependencies.py         # Dependency injection
│   │   ├── middleware.py           # Custom middleware
│   │   ├── exceptions.py           # Custom exception handlers
│   │   ├── models/                 # SQLAlchemy models
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── user.py
│   │   │   ├── center.py
│   │   │   ├── student.py
│   │   │   ├── faculty.py
│   │   │   ├── subject.py
│   │   │   ├── batch.py
│   │   │   ├── attendance.py
│   │   │   ├── feedback.py
│   │   │   └── notification.py
│   │   ├── schemas/                # Pydantic schemas
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── center.py
│   │   │   ├── student.py
│   │   │   ├── faculty.py
│   │   │   ├── subject.py
│   │   │   ├── batch.py
│   │   │   ├── attendance.py
│   │   │   ├── feedback.py
│   │   │   └── notification.py
│   │   ├── api/                    # API routes
│   │   │   ├── __init__.py
│   │   │   ├── deps.py
│   │   │   ├── v1/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── auth.py
│   │   │   │   ├── users.py
│   │   │   │   ├── centers.py
│   │   │   │   ├── students.py
│   │   │   │   ├── faculty.py
│   │   │   │   ├── subjects.py
│   │   │   │   ├── batches.py
│   │   │   │   ├── attendance.py
│   │   │   │   ├── feedback.py
│   │   │   │   ├── notifications.py
│   │   │   │   └── analytics.py
│   │   ├── core/                   # Core functionality
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── security.py
│   │   │   ├── permissions.py
│   │   │   └── utils.py
│   │   ├── services/               # Business logic services
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py
│   │   │   ├── student_service.py
│   │   │   ├── faculty_service.py
│   │   │   ├── batch_service.py
│   │   │   ├── attendance_service.py
│   │   │   ├── analytics_service.py
│   │   │   └── notification_service.py
│   │   └── utils/                  # Utility functions
│   │       ├── __init__.py
│   │       ├── email.py
│   │       ├── sms.py
│   │       ├── file_handler.py
│   │       └── validators.py
│   ├── tests/                       # Test files
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── test_auth.py
│   │   ├── test_students.py
│   │   ├── test_faculty.py
│   │   ├── test_batches.py
│   │   └── test_attendance.py
│   ├── alembic/                     # Database migrations
│   │   ├── versions/
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── alembic.ini
│   ├── requirements.txt             # Python dependencies
│   ├── Dockerfile                   # Docker configuration
│   └── .env.example                 # Environment variables example
├── frontend/
│   ├── public/
│   │   ├── index.html
│   │   ├── favicon.ico
│   │   └── manifest.json
│   ├── src/
│   │   ├── components/              # Reusable components
│   │   │   ├── common/
│   │   │   │   ├── Header.jsx
│   │   │   │   ├── Sidebar.jsx
│   │   │   │   ├── Footer.jsx
│   │   │   │   ├── Loading.jsx
│   │   │   │   └── ErrorBoundary.jsx
│   │   │   ├── auth/
│   │   │   │   ├── LoginForm.jsx
│   │   │   │   ├── ProtectedRoute.jsx
│   │   │   │   └── RoleBasedAccess.jsx
│   │   │   ├── students/
│   │   │   │   ├── StudentList.jsx
│   │   │   │   ├── StudentForm.jsx
│   │   │   │   ├── StudentDetails.jsx
│   │   │   │   ├── StudentProgress.jsx
│   │   │   │   └── StudentAttendance.jsx
│   │   │   ├── faculty/
│   │   │   │   ├── FacultyList.jsx
│   │   │   │   ├── FacultyForm.jsx
│   │   │   │   ├── FacultyDetails.jsx
│   │   │   │   ├── FacultySchedule.jsx
│   │   │   │   └── FacultyPerformance.jsx
│   │   │   ├── batches/
│   │   │   │   ├── BatchList.jsx
│   │   │   │   ├── BatchForm.jsx
│   │   │   │   ├── BatchDetails.jsx
│   │   │   │   ├── BatchStudents.jsx
│   │   │   │   └── BatchSchedule.jsx
│   │   │   ├── attendance/
│   │   │   │   ├── AttendanceMarker.jsx
│   │   │   │   ├── AttendanceHistory.jsx
│   │   │   │   ├── AttendanceAnalytics.jsx
│   │   │   │   └── AttendanceHeatmap.jsx
│   │   │   ├── analytics/
│   │   │   │   ├── Dashboard.jsx
│   │   │   │   ├── GanttChart.jsx
│   │   │   │   ├── KanbanBoard.jsx
│   │   │   │   ├── PerformanceCharts.jsx
│   │   │   │   └── Reports.jsx
│   │   │   ├── feedback/
│   │   │   │   ├── FeedbackForm.jsx
│   │   │   │   ├── FeedbackList.jsx
│   │   │   │   └── FeedbackAnalytics.jsx
│   │   │   └── notifications/
│   │   │       ├── NotificationCenter.jsx
│   │   │       ├── NotificationItem.jsx
│   │   │       └── NotificationSettings.jsx
│   │   ├── pages/                   # Page components
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Login.jsx
│   │   │   ├── Students.jsx
│   │   │   ├── Faculty.jsx
│   │   │   ├── Batches.jsx
│   │   │   ├── Attendance.jsx
│   │   │   ├── Analytics.jsx
│   │   │   ├── Feedback.jsx
│   │   │   ├── Settings.jsx
│   │   │   └── Profile.jsx
│   │   ├── services/                # API services
│   │   │   ├── api.js
│   │   │   ├── auth.js
│   │   │   ├── students.js
│   │   │   ├── faculty.js
│   │   │   ├── batches.js
│   │   │   ├── attendance.js
│   │   │   ├── analytics.js
│   │   │   └── notifications.js
│   │   ├── hooks/                   # Custom hooks
│   │   │   ├── useAuth.js
│   │   │   ├── useApi.js
│   │   │   ├── useLocalStorage.js
│   │   │   ├── useWebSocket.js
│   │   │   └── useNotifications.js
│   │   ├── context/                 # React context
│   │   │   ├── AuthContext.js
│   │   │   ├── NotificationContext.js
│   │   │   └── ThemeContext.js
│   │   ├── utils/                   # Utility functions
│   │   │   ├── constants.js
│   │   │   ├── helpers.js
│   │   │   ├── validators.js
│   │   │   └── formatters.js
│   │   ├── styles/                  # CSS/SCSS files
│   │   │   ├── globals.css
│   │   │   ├── variables.css
│   │   │   └── components.css
│   │   ├── assets/                  # Static assets
│   │   │   ├── images/
│   │   │   ├── icons/
│   │   │   └── fonts/
│   │   ├── App.jsx
│   │   ├── index.js
│   │   └── setupTests.js
│   ├── package.json
│   ├── package-lock.json
│   ├── Dockerfile
│   └── .env.example
├── nginx/                           # Nginx configuration
│   ├── nginx.conf
│   └── Dockerfile
├── docker-compose.yml               # Main Docker compose file
├── docker-compose.dev.yml           # Development environment
├── docker-compose.prod.yml          # Production environment
├── .env.example                     # Environment variables template
├── .gitignore
├── README.md
└── docs/                           # Documentation
    ├── api.md
    ├── deployment.md
    └── user_guide.md
```

## Docker Configuration Files

### 1. Main Docker Compose File (docker-compose.yml)

```yaml
version: '3.8'

services:
  # PostgreSQL Database
  postgres:
    image: postgres:14-alpine
    container_name: lms_postgres
    environment:
      POSTGRES_DB: ${DB_NAME}
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./backend/init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"
    networks:
      - lms_network
    restart: unless-stopped

  # Redis Cache
  redis:
    image: redis:7-alpine
    container_name: lms_redis
    command: redis-server --appendonly yes --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis_data:/data
    ports:
      - "6379:6379"
    networks:
      - lms_network
    restart: unless-stopped

  # FastAPI Backend
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: lms_backend
    environment:
      - DATABASE_URL=postgresql://${DB_USER}:${DB_PASSWORD}@postgres:5432/${DB_NAME}
      - REDIS_URL=redis://:${REDIS_PASSWORD}@redis:6379/0
      - SECRET_KEY=${SECRET_KEY}
      - ALGORITHM=${ALGORITHM}
      - ACCESS_TOKEN_EXPIRE_MINUTES=${ACCESS_TOKEN_EXPIRE_MINUTES}
      - ENVIRONMENT=${ENVIRONMENT}
    volumes:
      - ./backend:/app
      - uploads:/app/uploads
    ports:
      - "8000:8000"
    depends_on:
      - postgres
      - redis
    networks:
      - lms_network
    restart: unless-stopped

  # React Frontend
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: lms_frontend
    environment:
      - REACT_APP_API_URL=${REACT_APP_API_URL}
      - REACT_APP_WS_URL=${REACT_APP_WS_URL}
    volumes:
      - ./frontend:/app
      - /app/node_modules
    ports:
      - "3000:3000"
    depends_on:
      - backend
    networks:
      - lms_network
    restart: unless-stopped

  # Nginx Reverse Proxy
  nginx:
    build:
      context: ./nginx
      dockerfile: Dockerfile
    container_name: lms_nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/ssl:/etc/nginx/ssl
      - static_files:/var/www/static
    depends_on:
      - backend
      - frontend
    networks:
      - lms_network
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
  uploads:
  static_files:

networks:
  lms_network:
    driver: bridge
```

### 2. Development Docker Compose (docker-compose.dev.yml)

```yaml
version: '3.8'

services:
  postgres:
    ports:
      - "5432:5432"
    environment:
      POSTGRES_DB: lms_dev
      POSTGRES_USER: dev_user
      POSTGRES_PASSWORD: dev_password

  redis:
    ports:
      - "6379:6379"
    command: redis-server --appendonly yes

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.dev
    environment:
      - DATABASE_URL=postgresql://dev_user:dev_password@postgres:5432/lms_dev
      - REDIS_URL=redis://redis:6379/0
      - SECRET_KEY=dev-secret-key-change-in-production
      - ENVIRONMENT=development
    volumes:
      - ./backend:/app
    ports:
      - "8000:8000"
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.dev
    environment:
      - REACT_APP_API_URL=http://localhost:8000
      - REACT_APP_WS_URL=ws://localhost:8000
    volumes:
      - ./frontend:/app
      - /app/node_modules
    ports:
      - "3000:3000"
    command: npm start
```

### 3. Production Docker Compose (docker-compose.prod.yml)

```yaml
version: '3.8'

services:
  postgres:
    environment:
      POSTGRES_DB: ${DB_NAME}
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: always

  redis:
    command: redis-server --appendonly yes --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis_data:/data
    restart: always

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    environment:
      - DATABASE_URL=postgresql://${DB_USER}:${DB_PASSWORD}@postgres:5432/${DB_NAME}
      - REDIS_URL=redis://:${REDIS_PASSWORD}@redis:6379/0
      - SECRET_KEY=${SECRET_KEY}
      - ENVIRONMENT=production
    volumes:
      - uploads:/app/uploads
    restart: always

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    environment:
      - REACT_APP_API_URL=${REACT_APP_API_URL}
      - REACT_APP_WS_URL=${REACT_APP_WS_URL}
    restart: always

  nginx:
    build:
      context: ./nginx
      dockerfile: Dockerfile
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/ssl:/etc/nginx/ssl
      - static_files:/var/www/static
    restart: always
```

### 4. Backend Dockerfile

```dockerfile
# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create uploads directory
RUN mkdir -p uploads

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 5. Backend Development Dockerfile

```dockerfile
# backend/Dockerfile.dev
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install development dependencies
COPY requirements.dev.txt .
RUN pip install --no-cache-dir -r requirements.dev.txt

# Copy application code
COPY . .

# Create uploads directory
RUN mkdir -p uploads

# Expose port
EXPOSE 8000

# Run the application in development mode
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

### 6. Frontend Dockerfile

```dockerfile
# frontend/Dockerfile
# Build stage
FROM node:18-alpine as build

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy source code
COPY . .

# Build the application
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy built application
COPY --from=build /app/build /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
```

### 7. Frontend Development Dockerfile

```dockerfile
# frontend/Dockerfile.dev
FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Expose port
EXPOSE 3000

# Start the development server
CMD ["npm", "start"]
```

### 8. Nginx Dockerfile

```dockerfile
# nginx/Dockerfile
FROM nginx:alpine

# Remove default configuration
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Create directories for SSL and static files
RUN mkdir -p /etc/nginx/ssl /var/www/static

# Expose ports
EXPOSE 80 443

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
```

### 9. Nginx Configuration

```nginx
# nginx/nginx.conf
events {
    worker_connections 1024;
}

http {
    upstream backend {
        server backend:8000;
    }

    upstream frontend {
        server frontend:3000;
    }

    server {
        listen 80;
        server_name localhost;

        # Frontend routes
        location / {
            proxy_pass http://frontend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Backend API routes
        location /api/ {
            proxy_pass http://backend/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # WebSocket support
        location /ws/ {
            proxy_pass http://backend/ws/;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Static files
        location /static/ {
            alias /var/www/static/;
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }

    # HTTPS configuration (for production)
    server {
        listen 443 ssl http2;
        server_name localhost;

        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;

        # Frontend routes
        location / {
            proxy_pass http://frontend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Backend API routes
        location /api/ {
            proxy_pass http://backend/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # WebSocket support
        location /ws/ {
            proxy_pass http://backend/ws/;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Static files
        location /static/ {
            alias /var/www/static/;
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }
}
```

### 10. Environment Variables Template (.env.example)

```bash
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=lms
DB_USER=lms_user
DB_PASSWORD=your_secure_password

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=your_redis_password

# JWT Configuration
SECRET_KEY=your_super_secret_key_change_this_in_production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application Configuration
ENVIRONMENT=development
DEBUG=true
API_V1_STR=/api/v1
PROJECT_NAME=Student Academics Management System

# Frontend Configuration
REACT_APP_API_URL=http://localhost:8000
REACT_APP_WS_URL=ws://localhost:8000

# Email Configuration (for notifications)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_email_password

# SMS Configuration (for attendance alerts)
SMS_API_KEY=your_sms_api_key
SMS_API_SECRET=your_sms_api_secret

# File Upload Configuration
MAX_FILE_SIZE=10485760  # 10MB
UPLOAD_DIR=uploads

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
```

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd student-academics-management
```

### 2. Environment Setup
```bash
# Copy environment template
cp .env.example .env

# Edit environment variables
nano .env
```

### 3. Development Setup
```bash
# Start development environment
docker-compose -f docker-compose.dev.yml up -d

# Run database migrations
docker-compose -f docker-compose.dev.yml exec backend alembic upgrade head

# Create initial data
docker-compose -f docker-compose.dev.yml exec backend python -m app.initial_data
```

### 4. Production Setup
```bash
# Build and start production environment
docker-compose -f docker-compose.prod.yml up -d --build

# Run database migrations
docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head

# Create initial data
docker-compose -f docker-compose.prod.yml exec backend python -m app.initial_data
```

### 5. Common Commands
```bash
# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Stop services
docker-compose down

# Rebuild specific service
docker-compose build --no-cache backend

# Access backend container
docker-compose exec backend bash

# Access database
docker-compose exec postgres psql -U lms_user -d lms