"""
JWT Authentication Utilities for VisualVerse
Provides JWT token generation and verification.
"""

import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status

# Security configuration
SECRET_KEY = os.getenv("VISUALVERSE_JWT_SECRET", "your-secret-key-change-in-production")
ALGORITHM = os.getenv("VISUALVERSE_JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("VISUALVERSE_JWT_EXPIRE_MINUTES", "60*24"))  # 24 hours default

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.
    
    Args:
        plain_password: The plain text password to verify
        hashed_password: The hashed password to compare against
        
    Returns:
        True if passwords match, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a password for storage.
    
    Args:
        password: The plain text password to hash
        
    Returns:
        The hashed password
    """
    return pwd_context.hash(password)


def create_access_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a JWT access token.
    
    Args:
        data: The payload data to encode in the token
        expires_delta: Optional custom expiration time
        
    Returns:
        Encoded JWT token string
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Dict[str, Any]:
    """
    Decode and validate a JWT access token.
    
    Args:
        token: The JWT token to decode
        
    Returns:
        Decoded token payload
        
    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


def create_refresh_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a JWT refresh token with longer expiration.
    
    Args:
        data: The payload data to encode in the token
        expires_delta: Optional custom expiration time (default: 7 days)
        
    Returns:
        Encoded JWT refresh token string
    """
    if expires_delta is None:
        expires_delta = timedelta(days=7)
    
    to_encode = data.copy()
    to_encode.update({"type": "refresh", "exp": datetime.utcnow() + expires_delta})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_refresh_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Verify a refresh token and return its payload if valid.
    
    Args:
        token: The refresh token to verify
        
    Returns:
        Decoded token payload if valid, None otherwise
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "refresh":
            return None
        return payload
    except JWTError:
        return None


def get_current_user(token: str) -> Dict[str, Any]:
    """
    Get current user from JWT token for dependency injection.
    
    Args:
        token: The JWT access token
        
    Returns:
        User information extracted from token
        
    Raises:
        HTTPException: If token is invalid or expired
    """
    payload = decode_access_token(token)
    user_id: Optional[int] = payload.get("sub")
    
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return {
        "user_id": user_id,
        "email": payload.get("email"),
        "role": payload.get("role"),
        "institution_id": payload.get("institution_id"),
    }


class RoleChecker:
    """
    Dependency class for checking user roles.
    """
    
    def __init__(self, allowed_roles: list):
        self.allowed_roles = allowed_roles
    
    def __call__(self, current_user: Dict[str, Any]) -> bool:
        """
        Check if current user's role is in allowed roles.
        
        Args:
            current_user: Current user information from token
            
        Returns:
            True if role is allowed, raises HTTPException otherwise
        """
        if current_user.get("role") not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions for this operation"
            )
        return True


# Role constants
ROLE_ADMIN = "admin"
ROLE_MODERATOR = "moderator"
ROLE_CREATOR = "creator"
ROLE_INSTRUCTOR = "instructor"
ROLE_STUDENT = "student"

# Role hierarchy for permission checking
ROLE_HIERARCHY = {
    ROLE_ADMIN: [ROLE_ADMIN, ROLE_MODERATOR, ROLE_CREATOR, ROLE_INSTRUCTOR, ROLE_STUDENT],
    ROLE_MODERATOR: [ROLE_MODERATOR, ROLE_CREATOR, ROLE_INSTRUCTOR, ROLE_STUDENT],
    ROLE_CREATOR: [ROLE_CREATOR, ROLE_INSTRUCTOR, ROLE_STUDENT],
    ROLE_INSTRUCTOR: [ROLE_INSTRUCTOR, ROLE_STUDENT],
    ROLE_STUDENT: [ROLE_STUDENT],
}


def has_permission(user_role: str, required_role: str) -> bool:
    """
    Check if a user role has permission for a required role.
    
    Args:
        user_role: The user's role
        required_role: The role required for the operation
        
    Returns:
        True if user has permission, False otherwise
    """
    if user_role not in ROLE_HIERARCHY:
        return False
    return required_role in ROLE_HIERARCHY[user_role]
