"""
Authentication endpoints for user login, registration, and token management
"""

from datetime import datetime, timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.v1.endpoints.deps import get_db, get_current_user
from app.core.security import (
    create_access_token,
    create_refresh_token,
    verify_token,
    get_password_hash,
    verify_password
)
from app.core.exceptions import (
    AuthenticationError,
    ValidationError,
    EmailAlreadyExistsError,
    InvalidTokenError,
    TokenExpiredError
)
from app.models.user import User, UserRole
from app.schemas.auth import Token, TokenRefresh, UserCreate, UserResponse
from app.core.utils import validate_email, validate_password_strength

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
) -> Any:
    """
    Register a new user
    """
    # Validate email
    if not validate_email(user_data.email):
        raise ValidationError("Invalid email format")
    
    # Validate password strength
    password_validation = validate_password_strength(user_data.password)
    if not password_validation["is_valid"]:
        raise ValidationError(f"Weak password: {', '.join(password_validation['errors'])}")
    
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise EmailAlreadyExistsError(user_data.email)
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        email=user_data.email,
        password_hash=hashed_password,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        phone=user_data.phone,
        role=user_data.role,
        center_id=user_data.center_id
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return UserResponse.from_orm(db_user)


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
) -> Any:
    """
    Authenticate user and return access token
    """
    # Authenticate user
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise AuthenticationError("Incorrect email or password")
    
    if not user.is_active():
        raise AuthenticationError("Account is inactive")
    
    # Create tokens
    access_token_expires = timedelta(minutes=30)
    refresh_token_expires = timedelta(days=7)
    
    access_token = create_access_token(
        data={"sub": str(user.id), "role": user.role},
        expires_delta=access_token_expires
    )
    
    refresh_token = create_refresh_token(
        data={"sub": str(user.id)},
        expires_delta=refresh_token_expires
    )
    
    # Update last login
    user.last_login = datetime.utcnow()
    db.commit()
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": 1800,  # 30 minutes in seconds
        "user": UserResponse.from_orm(user)
    }


@router.post("/refresh", response_model=TokenRefresh)
def refresh_token(
    refresh_token: str,
    db: Session = Depends(get_db)
) -> Any:
    """
    Refresh access token using refresh token
    """
    try:
        # Verify refresh token
        user_id = verify_token(refresh_token, "refresh")
        
        # Get user
        user = db.query(User).filter(User.id == int(user_id)).first()
        if not user or not user.is_active():
            raise AuthenticationError("Invalid or expired refresh token")
        
        # Create new access token
        access_token_expires = timedelta(minutes=30)
        new_access_token = create_access_token(
            data={"sub": str(user.id), "role": user.role},
            expires_delta=access_token_expires
        )
        
        return {
            "access_token": new_access_token,
            "token_type": "bearer",
            "expires_in": 1800  # 30 minutes in seconds
        }
        
    except (InvalidTokenError, TokenExpiredError):
        raise AuthenticationError("Invalid or expired refresh token")


@router.post("/logout")
def logout(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Logout user (invalidate tokens)
    """
    # In a real implementation, you would:
    # 1. Add the token to a blacklist in Redis
    # 2. Or use JWT token revocation
    # For now, we'll just return success
    
    return {"message": "Successfully logged out"}


@router.post("/reset-password-request")
def reset_password_request(
    email: str,
    db: Session = Depends(get_db)
) -> Any:
    """
    Request password reset
    """
    # Validate email
    if not validate_email(email):
        raise ValidationError("Invalid email format")
    
    # Check if user exists
    user = db.query(User).filter(User.email == email).first()
    if not user:
        # Don't reveal if email exists or not
        return {"message": "If the email exists, a reset link has been sent"}
    
    # Generate reset token
    reset_token = create_password_reset_token(email)
    
    # In a real implementation, send email with reset token
    # send_password_reset_email(email, reset_token)
    
    return {"message": "If the email exists, a reset link has been sent"}


@router.post("/reset-password")
def reset_password(
    token: str,
    new_password: str,
    db: Session = Depends(get_db)
) -> Any:
    """
    Reset password using token
    """
    try:
        # Verify reset token
        email = verify_password_reset_token(token)
        
        # Validate new password
        password_validation = validate_password_strength(new_password)
        if not password_validation["is_valid"]:
            raise ValidationError(f"Weak password: {', '.join(password_validation['errors'])}")
        
        # Get user
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise AuthenticationError("Invalid or expired reset token")
        
        # Update password
        user.password_hash = get_password_hash(new_password)
        db.commit()
        
        return {"message": "Password reset successfully"}
        
    except (InvalidTokenError, TokenExpiredError):
        raise AuthenticationError("Invalid or expired reset token")


@router.get("/me", response_model=UserResponse)
def get_current_user_info(
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get current user information
    """
    return UserResponse.from_orm(current_user)