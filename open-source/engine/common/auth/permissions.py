"""
Authentication and authorization utilities for VisualVerse.
Shared authentication components used across all services.
"""

from enum import Enum
from typing import Dict, List, Optional, Set
from pydantic import BaseModel
import jwt
from datetime import datetime, timedelta


class Permission(str, Enum):
    """System permissions"""
    # Content management
    CREATE_CONTENT = "create_content"
    EDIT_CONTENT = "edit_content"
    DELETE_CONTENT = "delete_content"
    VIEW_CONTENT = "view_content"
    
    # User management
    MANAGE_USERS = "manage_users"
    VIEW_USER_PROGRESS = "view_user_progress"
    
    # System administration
    SYSTEM_ADMIN = "system_admin"
    VIEW_ANALYTICS = "view_analytics"
    MANAGE_SYSTEM = "manage_system"
    
    # Learning
    CREATE_LESSONS = "create_lessons"
    VIEW_LEARNING_PATHS = "view_learning_paths"
    TRACK_PROGRESS = "track_progress"


class Role(str, Enum):
    """System roles"""
    STUDENT = "student"
    TEACHER = "teacher"
    CREATOR = "creator"
    ADMIN = "admin"
    SYSTEM_ADMIN = "system_admin"


class User(BaseModel):
    """User model for authentication"""
    
    user_id: str
    username: str
    email: str
    role: Role
    permissions: Set[Permission]
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.now)
    last_login: Optional[datetime] = None
    
    def has_permission(self, permission: Permission) -> bool:
        """Check if user has specific permission"""
        return permission in self.permissions
    
    def has_any_permission(self, permissions: List[Permission]) -> bool:
        """Check if user has any of the specified permissions"""
        return any(self.has_permission(p) for p in permissions)
    
    def has_all_permissions(self, permissions: List[Permission]) -> bool:
        """Check if user has all specified permissions"""
        return all(self.has_permission(p) for p in permissions)


class AuthContext(BaseModel):
    """Authentication context for API requests"""
    
    user: User
    token: str
    expires_at: datetime
    scope: List[str] = []
    
    def is_expired(self) -> bool:
        """Check if authentication token is expired"""
        return datetime.now() > self.expires_at
    
    def has_scope(self, scope: str) -> bool:
        """Check if token has specific scope"""
        return scope in self.scope


class AuthService:
    """Authentication service for managing user sessions"""
    
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
        self.algorithm = "HS256"
    
    def create_token(self, user: User, expires_in: int = 3600) -> str:
        """Create JWT token for user"""
        payload = {
            "user_id": user.user_id,
            "username": user.username,
            "role": user.role,
            "permissions": list(user.permissions),
            "exp": datetime.utcnow() + timedelta(seconds=expires_in),
            "iat": datetime.utcnow()
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    def verify_token(self, token: str) -> Optional[AuthContext]:
        """Verify JWT token and return auth context"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            
            user = User(
                user_id=payload["user_id"],
                username=payload["username"],
                role=Role(payload["role"]),
                permissions=set(Permission(p) for p in payload["permissions"])
            )
            
            expires_at = datetime.utcfromtimestamp(payload["exp"])
            
            return AuthContext(
                user=user,
                token=token,
                expires_at=expires_at,
                scope=payload.get("scope", [])
            )
        
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def create_user(self, username: str, email: str, role: Role) -> User:
        """Create a new user with default permissions"""
        from .permissions import get_default_permissions
        
        user_id = f"{username}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        permissions = get_default_permissions(role)
        
        return User(
            user_id=user_id,
            username=username,
            email=email,
            role=role,
            permissions=permissions
        )


# Permission management
def require_permission(permission: Permission):
    """Decorator to require specific permission"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            # This would be implemented with actual request context
            # For now, it's a placeholder
            return func(*args, **kwargs)
        return wrapper
    return decorator


def require_any_permission(permissions: List[Permission]):
    """Decorator to require any of the specified permissions"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            # This would be implemented with actual request context
            # For now, it's a placeholder
            return func(*args, **kwargs)
        return wrapper
    return decorator


# Role-based access control
ROLE_PERMISSIONS = {
    Role.STUDENT: {
        Permission.VIEW_CONTENT,
        Permission.VIEW_LEARNING_PATHS,
        Permission.TRACK_PROGRESS,
        Permission.VIEW_USER_PROGRESS
    },
    Role.TEACHER: {
        Permission.CREATE_CONTENT,
        Permission.EDIT_CONTENT,
        Permission.VIEW_CONTENT,
        Permission.CREATE_LESSONS,
        Permission.VIEW_LEARNING_PATHS,
        Permission.TRACK_PROGRESS,
        Permission.VIEW_USER_PROGRESS
    },
    Role.CREATOR: {
        Permission.CREATE_CONTENT,
        Permission.EDIT_CONTENT,
        Permission.DELETE_CONTENT,
        Permission.VIEW_CONTENT,
        Permission.CREATE_LESSONS,
        Permission.VIEW_LEARNING_PATHS,
        Permission.TRACK_PROGRESS
    },
    Role.ADMIN: {
        Permission.CREATE_CONTENT,
        Permission.EDIT_CONTENT,
        Permission.DELETE_CONTENT,
        Permission.VIEW_CONTENT,
        Permission.MANAGE_USERS,
        Permission.VIEW_USER_PROGRESS,
        Permission.CREATE_LESSONS,
        Permission.VIEW_LEARNING_PATHS,
        Permission.TRACK_PROGRESS,
        Permission.VIEW_ANALYTICS
    },
    Role.SYSTEM_ADMIN: {
        Permission.SYSTEM_ADMIN,
        Permission.MANAGE_SYSTEM,
        Permission.VIEW_ANALYTICS,
        Permission.MANAGE_USERS,
        Permission.CREATE_CONTENT,
        Permission.EDIT_CONTENT,
        Permission.DELETE_CONTENT,
        Permission.VIEW_CONTENT
    }
}


def get_default_permissions(role: Role) -> Set[Permission]:
    """Get default permissions for a role"""
    return ROLE_PERMISSIONS.get(role, set())


def check_permission(user: User, permission: Permission) -> bool:
    """Check if user has specific permission"""
    return user.has_permission(permission)


def check_role_access(user: User, allowed_roles: List[Role]) -> bool:
    """Check if user has any of the allowed roles"""
    return user.role in allowed_roles
