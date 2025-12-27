"""
Identity & Access Management Service module.

This module provides comprehensive user management, role-based access control,
tenant isolation, and authentication services for institutional deployments.
"""

from .identity_service import (
    IdentityService,
    Tenant,
    User,
    Role,
    Permission,
    UserTenantAssociation,
    AuthenticationEvent,
    Session,
    UserStatus,
    AuthMethod,
    SessionStatus,
    create_identity_service
)

__all__ = [
    "IdentityService",
    "Tenant",
    "User",
    "Role",
    "Permission",
    "UserTenantAssociation",
    "AuthenticationEvent",
    "Session",
    "UserStatus",
    "AuthMethod",
    "SessionStatus",
    "create_identity_service"
]
