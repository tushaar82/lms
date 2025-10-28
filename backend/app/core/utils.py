"""
Utility functions for the Student Academics Management System
"""

import re
import secrets
from datetime import datetime, date, timedelta
from typing import Any, Dict, List, Optional, Union
from passlib.context import CryptContext
import hashlib
import base64

from app.config import settings


# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_password_reset_token(email: str) -> str:
    """Generate a secure password reset token"""
    timestamp = str(int(datetime.utcnow().timestamp()))
    token_data = f"{email}:{timestamp}:{secrets.token_urlsafe(32)}"
    token_hash = hashlib.sha256(token_data.encode()).hexdigest()
    return base64.urlsafe_b64encode(f"{token_data}:{token_hash}".encode()).decode()


def verify_password_reset_token(token: str, max_age_hours: int = 24) -> Optional[str]:
    """Verify password reset token and return email if valid"""
    try:
        decoded = base64.urlsafe_b64decode(token.encode()).decode()
        token_data, token_hash = decoded.rsplit(":", 1)
        
        # Verify hash
        expected_hash = hashlib.sha256(token_data.encode()).hexdigest()
        if token_hash != expected_hash:
            return None
        
        # Extract email and timestamp
        email, timestamp, _ = token_data.split(":", 2)
        
        # Check age
        token_time = datetime.fromtimestamp(float(timestamp))
        if datetime.utcnow() - token_time > timedelta(hours=max_age_hours):
            return None
        
        return email
    except (ValueError, TypeError):
        return None


def generate_enrollment_number(center_code: str, year: int = None) -> str:
    """Generate unique enrollment number"""
    if year is None:
        year = date.today().year
    
    # Generate random 4-digit number
    random_part = secrets.randbelow(10000)
    return f"{center_code}{year}{random_part:04d}"


def generate_employee_id(center_code: str) -> str:
    """Generate unique employee ID"""
    random_part = secrets.randbelow(10000)
    return f"EMP{center_code.upper()}{random_part:04d}"


def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_phone(phone: str) -> bool:
    """Validate phone number format (Indian format)"""
    # Remove spaces, dashes, parentheses
    cleaned = re.sub(r'[\s\-\(\)]', '', phone)
    
    # Check if it's a valid Indian phone number
    pattern = r'^(\+91|91|0)?[6-9]\d{9}$'
    return re.match(pattern, cleaned) is not None


def validate_password_strength(password: str) -> Dict[str, Any]:
    """Validate password strength and return requirements"""
    requirements = {
        "min_length": len(password) >= 8,
        "uppercase": bool(re.search(r'[A-Z]', password)),
        "lowercase": bool(re.search(r'[a-z]', password)),
        "digit": bool(re.search(r'\d', password)),
        "special": bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password)),
        "no_spaces": ' ' not in password
    }
    
    is_strong = all(requirements.values())
    
    return {
        "is_strong": is_strong,
        "requirements": requirements,
        "missing_requirements": [
            req for req, met in requirements.items() if not met
        ]
    }


def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return pwd_context.verify(plain_password, hashed_password)


def generate_random_string(length: int = 32) -> str:
    """Generate cryptographically secure random string"""
    return secrets.token_urlsafe(length)


def calculate_age(birth_date: date) -> int:
    """Calculate age from birth date"""
    today = date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age


def calculate_percentage(part: Union[int, float], total: Union[int, float]) -> float:
    """Calculate percentage safely"""
    if total == 0:
        return 0.0
    return round((part / total) * 100, 2)


def calculate_grade(score: float) -> str:
    """Calculate grade from score"""
    if score >= 90:
        return "A+"
    elif score >= 85:
        return "A"
    elif score >= 80:
        return "A-"
    elif score >= 75:
        return "B+"
    elif score >= 70:
        return "B"
    elif score >= 65:
        return "B-"
    elif score >= 60:
        return "C+"
    elif score >= 55:
        return "C"
    elif score >= 50:
        return "C-"
    elif score >= 45:
        return "D"
    else:
        return "F"


def format_currency(amount: Union[int, float]) -> str:
    """Format currency amount"""
    return f"₹{amount:,.2f}"


def format_duration_hours(hours: Union[int, float]) -> str:
    """Format duration in hours to human readable format"""
    if hours < 1:
        minutes = int(hours * 60)
        return f"{minutes} minutes"
    elif hours == 1:
        return "1 hour"
    elif hours < 24:
        return f"{hours} hours"
    else:
        days = int(hours // 24)
        remaining_hours = int(hours % 24)
        if remaining_hours == 0:
            return f"{days} days"
        else:
            return f"{days} days {remaining_hours} hours"


def get_date_range(period: str) -> tuple[date, date]:
    """Get date range for a given period"""
    today = date.today()
    
    if period == "today":
        return today, today
    elif period == "yesterday":
        yesterday = today - timedelta(days=1)
        return yesterday, yesterday
    elif period == "this_week":
        start = today - timedelta(days=today.weekday())
        return start, today
    elif period == "last_week":
        start = today - timedelta(days=today.weekday() + 7)
        end = start + timedelta(days=6)
        return start, end
    elif period == "this_month":
        start = today.replace(day=1)
        return start, today
    elif period == "last_month":
        if today.month == 1:
            start = today.replace(year=today.year - 1, month=12, day=1)
            end = today.replace(year=today.year - 1, month=12, day=31)
        else:
            start = today.replace(month=today.month - 1, day=1)
            end = today.replace(day=1) - timedelta(days=1)
        return start, end
    elif period == "this_year":
        start = today.replace(month=1, day=1)
        return start, today
    elif period == "last_year":
        start = today.replace(year=today.year - 1, month=1, day=1)
        end = today.replace(year=today.year - 1, month=12, day=31)
        return start, end
    else:
        # Default to last 30 days
        start = today - timedelta(days=30)
        return start, today


def sanitize_string(text: str) -> str:
    """Sanitize string by removing potentially harmful characters"""
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate text to specified length"""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def generate_slug(text: str) -> str:
    """Generate URL-friendly slug from text"""
    # Convert to lowercase and replace spaces with hyphens
    slug = text.lower().replace(' ', '-')
    # Remove special characters except hyphens
    slug = re.sub(r'[^a-z0-9-]', '', slug)
    # Remove multiple consecutive hyphens
    slug = re.sub(r'-+', '-', slug)
    # Remove leading/trailing hyphens
    slug = slug.strip('-')
    return slug


def parse_schedule(schedule_str: str) -> Dict[str, Any]:
    """Parse schedule string into structured format"""
    # This is a basic parser - can be enhanced based on requirements
    if not schedule_str:
        return {}
    
    # Example format: "Mon,Wed,Fri 10:00-12:00"
    parts = schedule_str.split(' ')
    if len(parts) != 2:
        return {}
    
    days_part, time_part = parts
    days = [day.strip() for day in days_part.split(',')]
    time_range = time_part.split('-')
    
    if len(time_range) != 2:
        return {}
    
    return {
        "days": days,
        "start_time": time_range[0].strip(),
        "end_time": time_range[1].strip()
    }


def format_schedule(schedule: Dict[str, Any]) -> str:
    """Format schedule dictionary into string"""
    if not schedule or not schedule.get("days") or not schedule.get("start_time"):
        return ""
    
    days = ", ".join(schedule["days"])
    if schedule.get("end_time"):
        return f"{days} {schedule['start_time']}-{schedule['end_time']}"
    else:
        return f"{days} {schedule['start_time']}"


def is_valid_date(date_string: str, date_format: str = "%Y-%m-%d") -> bool:
    """Check if date string is valid"""
    try:
        datetime.strptime(date_string, date_format)
        return True
    except ValueError:
        return False


def get_file_extension(filename: str) -> str:
    """Get file extension from filename"""
    return filename.rsplit('.', 1)[1].lower() if '.' in filename else ""


def is_allowed_file(filename: str) -> bool:
    """Check if file extension is allowed"""
    extension = get_file_extension(filename)
    return extension in settings.ALLOWED_EXTENSIONS


def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"


def generate_api_key() -> str:
    """Generate API key"""
    return f"lms_{secrets.token_urlsafe(32)}"


def verify_api_key(api_key: str) -> bool:
    """Verify API key format"""
    return api_key.startswith("lms_") and len(api_key) == 36


def create_pagination_params(
    page: int = 1, 
    page_size: int = None
) -> Dict[str, Any]:
    """Create pagination parameters"""
    if page_size is None:
        page_size = settings.DEFAULT_PAGE_SIZE
    
    page_size = min(page_size, settings.MAX_PAGE_SIZE)
    offset = (page - 1) * page_size
    
    return {
        "limit": page_size,
        "offset": offset,
        "page": page,
        "page_size": page_size
    }


def create_pagination_response(
    items: List[Any],
    total: int,
    page: int,
    page_size: int
) -> Dict[str, Any]:
    """Create paginated response"""
    total_pages = (total + page_size - 1) // page_size
    
    return {
        "items": items,
        "pagination": {
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_prev": page > 1
        }
    }


def mask_email(email: str) -> str:
    """Mask email for privacy"""
    if '@' not in email:
        return email
    
    local, domain = email.split('@', 1)
    if len(local) <= 2:
        masked_local = '*' * len(local)
    else:
        masked_local = local[0] + '*' * (len(local) - 2) + local[-1]
    
    return f"{masked_local}@{domain}"


def mask_phone(phone: str) -> str:
    """Mask phone number for privacy"""
    # Remove non-digit characters
    digits = re.sub(r'\D', '', phone)
    
    if len(digits) <= 4:
        return '*' * len(digits)
    
    # Show last 4 digits
    return '*' * (len(digits) - 4) + digits[-4:]


def calculate_gst(amount: Union[int, float], gst_rate: float = 18.0) -> Dict[str, float]:
    """Calculate GST amounts"""
    gst_amount = round(amount * (gst_rate / 100), 2)
    total_amount = round(amount + gst_amount, 2)
    
    return {
        "base_amount": round(amount, 2),
        "gst_rate": gst_rate,
        "gst_amount": gst_amount,
        "total_amount": total_amount
    }