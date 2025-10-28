"""
Dependencies for API endpoints
"""

from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.security import settings
from app.database import get_db
from app.models.user import User
from app.core.exceptions import AuthenticationError, AuthorizationError

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="api/v1/auth/login",
    auto_error=False
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Get current user from JWT token
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception
    
    if not user.is_active():
        raise AuthenticationError("Account is inactive")
    
    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Get current active user (additional check for active status)
    """
    if not current_user.is_active():
        raise AuthenticationError("Account is inactive")
    return current_user


def get_current_user_with_role(required_role: str):
    """
    Get current user with required role check
    """
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role != required_role:
            raise AuthorizationError(f"Requires {required_role} role")
        return current_user
    
    return role_checker


def get_current_admin_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Get current admin user (super_admin or center_admin)
    """
    if current_user.role not in [UserRole.SUPER_ADMIN, UserRole.CENTER_ADMIN]:
        raise AuthorizationError("Requires admin role")
    return current_user


def get_current_super_admin(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Get current super admin user
    """
    if current_user.role != UserRole.SUPER_ADMIN:
        raise AuthorizationError("Requires super admin role")
    return current_user