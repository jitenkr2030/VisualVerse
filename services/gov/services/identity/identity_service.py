"""
Identity & Access Management Service for Governance Platform.

Provides comprehensive user management, role-based access control,
tenant isolation, and authentication services for institutional deployments.
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
from uuid import uuid4
from collections import defaultdict
import json


class UserStatus(Enum):
    """User account status."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING_VERIFICATION = "pending_verification"
    DEACTIVATED = "deactivated"
    PENDING_APPROVAL = "pending_approval"


class AuthMethod(Enum):
    """Authentication methods."""
    PASSWORD = "password"
    SSO_SAML = "sso_saml"
    SSO_OIDC = "sso_oidc"
    MFA_SMS = "mfa_sms"
    MFA_TOTP = "mfa_totp"
    API_KEY = "api_key"
    JWT = "jwt"


class SessionStatus(Enum):
    """Session status."""
    ACTIVE = "active"
    EXPIRED = "expired"
    REVOKED = "revoked"


@dataclass
class Tenant:
    """Institutional tenant configuration."""
    tenant_id: str
    name: str
    domain: str
    status: str = "active"
    plan_tier: str = "basic"  # basic, professional, enterprise
    max_users: int = 100
    features_enabled: Dict[str, bool] = field(default_factory=dict)
    sso_config: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "tenant_id": self.tenant_id,
            "name": self.name,
            "domain": self.domain,
            "status": self.status,
            "plan_tier": self.plan_tier,
            "max_users": self.max_users,
            "features_enabled": self.features_enabled,
            "sso_config": self.sso_config,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "metadata": self.metadata
        }


@dataclass
class Permission:
    """Permission definition."""
    permission_id: str
    name: str
    description: str
    resource: str
    action: str
    conditions: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "permission_id": self.permission_id,
            "name": self.name,
            "description": self.description,
            "resource": self.resource,
            "action": self.action,
            "conditions": self.conditions
        }


@dataclass
class Role:
    """Role with associated permissions."""
    role_id: str
    tenant_id: Optional[str]
    name: str
    description: str
    level: int = 0  # Hierarchy level (higher = more privileged)
    is_system: bool = False
    permissions: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def has_permission(self, permission_id: str) -> bool:
        """Check if role has a specific permission."""
        # Wildcard permission check
        if "*" in self.permissions:
            return True
        if f"{permission_id}" in self.permissions:
            return True
        return False
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "role_id": self.role_id,
            "tenant_id": self.tenant_id,
            "name": self.name,
            "description": self.description,
            "level": self.level,
            "is_system": self.is_system,
            "permissions": self.permissions,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


@dataclass
class User:
    """User account."""
    user_id: str
    email: str
    username: str
    status: UserStatus = UserStatus.PENDING_VERIFICATION
    email_verified: bool = False
    mfa_enabled: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    last_login: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "email": self.email,
            "username": self.username,
            "status": self.status.value,
            "email_verified": self.email_verified,
            "mfa_enabled": self.mfa_enabled,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "metadata": self.metadata
        }


@dataclass
class UserTenantAssociation:
    """User association with a tenant."""
    association_id: str
    user_id: str
    tenant_id: str
    status: UserStatus = UserStatus.PENDING_APPROVAL
    roles: List[str] = field(default_factory=list)
    department: Optional[str] = None
    title: Optional[str] = None
    joined_at: datetime = field(default_factory=datetime.now)
    last_access: Optional[datetime] = None
    approval_date: Optional[datetime] = None
    approved_by: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "association_id": self.association_id,
            "user_id": self.user_id,
            "tenant_id": self.tenant_id,
            "status": self.status.value,
            "roles": self.roles,
            "department": self.department,
            "title": self.title,
            "joined_at": self.joined_at.isoformat(),
            "last_access": self.last_access.isoformat() if self.last_access else None,
            "approval_date": self.approval_date.isoformat() if self.approval_date else None,
            "approved_by": self.approved_by
        }


@dataclass
class Session:
    """User session."""
    session_id: str
    user_id: str
    tenant_id: Optional[str]
    token: str
    status: SessionStatus = SessionStatus.ACTIVE
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    expires_at: datetime = field(default_factory=lambda: datetime.now() + timedelta(hours=24))
    last_activity: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def is_valid(self) -> bool:
        """Check if session is still valid."""
        return (
            self.status == SessionStatus.ACTIVE and
            datetime.now() < self.expires_at
        )
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "user_id": self.user_id,
            "tenant_id": self.tenant_id,
            "status": self.status.value,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "created_at": self.created_at.isoformat(),
            "expires_at": self.expires_at.isoformat(),
            "last_activity": self.last_activity.isoformat(),
            "metadata": self.metadata
        }


@dataclass
class AuthenticationEvent:
    """Authentication event log."""
    event_id: str
    user_id: str
    tenant_id: Optional[str]
    event_type: str  # login, logout, mfa_challenge, password_change, etc.
    success: bool
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    failure_reason: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


class IdentityService:
    """
    Core identity and access management service.
    
    Handles user management, tenant administration, role-based access control,
    and authentication for the VisualVerse governance platform.
    """
    
    def __init__(self):
        # Data stores
        self.tenants: Dict[str, Tenant] = {}
        self.users: Dict[str, User] = {}
        self.roles: Dict[str, Role] = {}
        self.permissions: Dict[str, Permission] = {}
        self.user_associations: Dict[str, UserTenantAssociation] = {}
        self.sessions: Dict[str, Session] = {}
        self.auth_events: List[AuthenticationEvent] = []
        
        # Indexes for efficient lookup
        self.email_index: Dict[str, str] = {}  # email -> user_id
        self.tenant_users: Dict[str, List[str]] = defaultdict(list)  # tenant_id -> user_ids
        self.user_roles: Dict[str, List[str]] = defaultdict(list)  # user_id -> role_ids
        
        # Initialize default roles and permissions
        self._init_defaults()
    
    def _init_defaults(self):
        """Initialize default permissions and roles."""
        # Define core permissions
        default_permissions = [
            # User management
            ("user:read", "View user information", "user", "read"),
            ("user:create", "Create new users", "user", "create"),
            ("user:update", "Update user information", "user", "update"),
            ("user:delete", "Delete or deactivate users", "user", "delete"),
            ("user:approve", "Approve user registrations", "user", "approve"),
            
            # Role management
            ("role:read", "View roles", "role", "read"),
            ("role:create", "Create new roles", "role", "create"),
            ("role:update", "Update roles", "role", "update"),
            ("role:delete", "Delete roles", "role", "delete"),
            
            # Content moderation
            ("content:read", "View content", "content", "read"),
            ("content:moderate", "Moderate content", "content", "moderate"),
            ("content:approve", "Approve content", "content", "approve"),
            ("content:reject", "Reject content", "content", "reject"),
            ("content:delete", "Delete content", "content", "delete"),
            
            # Analytics
            ("analytics:read", "View analytics", "analytics", "read"),
            ("analytics:export", "Export analytics data", "analytics", "export"),
            ("analytics:admin", "Configure analytics", "analytics", "admin"),
            
            # Compliance
            ("compliance:read", "View compliance data", "compliance", "read"),
            ("compliance:audit", "Access audit logs", "compliance", "audit"),
            ("compliance:manage", "Manage compliance settings", "compliance", "manage"),
            
            # Admin
            ("admin:settings", "Manage system settings", "admin", "settings"),
            ("admin:tenants", "Manage tenants", "admin", "tenants"),
            ("admin:super", "Super administrator access", "admin", "super"),
        ]
        
        for perm_id, desc, resource, action in default_permissions:
            permission = Permission(
                permission_id=perm_id,
                name=perm_id,
                description=desc,
                resource=resource,
                action=action
            )
            self.permissions[perm_id] = permission
        
        # Define default roles
        default_roles = [
            Role(
                role_id="super_admin",
                tenant_id=None,
                name="Super Administrator",
                description="Full system access",
                level=100,
                is_system=True,
                permissions=["*"]
            ),
            Role(
                role_id="tenant_admin",
                tenant_id=None,
                name="Tenant Administrator",
                description="Full tenant administration",
                level=80,
                is_system=True,
                permissions=[
                    "user:read", "user:create", "user:update", "user:delete", "user:approve",
                    "role:read", "role:create", "role:update", "role:delete",
                    "content:read", "content:moderate", "content:approve", "content:reject",
                    "analytics:read", "analytics:export",
                    "compliance:read", "compliance:audit"
                ]
            ),
            Role(
                role_id="moderator",
                tenant_id=None,
                name="Content Moderator",
                description="Content review and moderation",
                level=50,
                is_system=True,
                permissions=[
                    "content:read", "content:moderate", "content:approve", "content:reject",
                    "analytics:read"
                ]
            ),
            Role(
                role_id="analyst",
                tenant_id=None,
                name="Analytics Analyst",
                description="View and export analytics",
                level=40,
                is_system=True,
                permissions=[
                    "analytics:read", "analytics:export"
                ]
            ),
            Role(
                role_id="educator",
                tenant_id=None,
                name="Educator",
                description="Basic educator access",
                level=20,
                is_system=True,
                permissions=[
                    "user:read", "content:read", "analytics:read"
                ]
            ),
            Role(
                role_id="learner",
                tenant_id=None,
                name="Learner",
                description="Basic learner access",
                level=10,
                is_system=True,
                permissions=[
                    "content:read"
                ]
            )
        ]
        
        for role in default_roles:
            self.roles[role.role_id] = role
    
    # Tenant Management
    def create_tenant(
        self,
        name: str,
        domain: str,
        plan_tier: str = "basic",
        max_users: int = 100,
        **kwargs
    ) -> Tenant:
        """Create a new tenant."""
        tenant_id = f"tenant_{uuid4().hex[:12]}"
        
        tenant = Tenant(
            tenant_id=tenant_id,
            name=name,
            domain=domain,
            plan_tier=plan_tier,
            max_users=max_users,
            features_enabled=kwargs.get("features_enabled", {}),
            sso_config=kwargs.get("sso_config", {}),
            metadata=kwargs.get("metadata", {})
        )
        
        self.tenants[tenant_id] = tenant
        return tenant
    
    def get_tenant(self, tenant_id: str) -> Optional[Tenant]:
        """Get tenant by ID."""
        return self.tenants.get(tenant_id)
    
    def get_tenant_by_domain(self, domain: str) -> Optional[Tenant]:
        """Get tenant by domain."""
        for tenant in self.tenants.values():
            if tenant.domain == domain:
                return tenant
        return None
    
    def update_tenant(
        self,
        tenant_id: str,
        **updates
    ) -> Optional[Tenant]:
        """Update tenant configuration."""
        if tenant_id not in self.tenants:
            return None
        
        tenant = self.tenants[tenant_id]
        
        for key, value in updates.items():
            if hasattr(tenant, key) and key not in ["tenant_id", "created_at"]:
                setattr(tenant, key, value)
        
        tenant.updated_at = datetime.now()
        return tenant
    
    def list_tenants(
        self,
        status: Optional[str] = None,
        plan_tier: Optional[str] = None
    ) -> List[Tenant]:
        """List tenants with optional filters."""
        tenants = list(self.tenants.values())
        
        if status:
            tenants = [t for t in tenants if t.status == status]
        if plan_tier:
            tenants = [t for t in tenants if t.plan_tier == plan_tier]
        
        return tenants
    
    # User Management
    def create_user(
        self,
        email: str,
        username: str,
        **kwargs
    ) -> Tuple[User, str]:
        """Create a new user account. Returns user and temporary password."""
        # Check for existing email
        if email in self.email_index:
            raise ValueError(f"User with email {email} already exists")
        
        user_id = f"user_{uuid4().hex[:12]}"
        temp_password = uuid4().hex[:16]  # Temporary password
        
        user = User(
            user_id=user_id,
            email=email,
            username=username,
            status=kwargs.get("status", UserStatus.PENDING_VERIFICATION),
            email_verified=False,
            mfa_enabled=False,
            metadata=kwargs.get("metadata", {})
        )
        
        self.users[user_id] = user
        self.email_index[email] = user_id
        
        return user, temp_password
    
    def get_user(self, user_id: str) -> Optional[User]:
        """Get user by ID."""
        return self.users.get(user_id)
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        user_id = self.email_index.get(email)
        if user_id:
            return self.users.get(user_id)
        return None
    
    def update_user(
        self,
        user_id: str,
        **updates
    ) -> Optional[User]:
        """Update user information."""
        if user_id not in self.users:
            return None
        
        user = self.users[user_id]
        
        for key, value in updates.items():
            if hasattr(user, key) and key not in ["user_id", "created_at"]:
                setattr(user, key, value)
        
        user.updated_at = datetime.now()
        return user
    
    def list_users(
        self,
        tenant_id: Optional[str] = None,
        status: Optional[UserStatus] = None
    ) -> List[User]:
        """List users with optional filters."""
        if tenant_id:
            user_ids = self.tenant_users.get(tenant_id, [])
            users = [self.users[uid] for uid in user_ids if uid in self.users]
        else:
            users = list(self.users.values())
        
        if status:
            users = [u for u in users if u.status == status]
        
        return users
    
    # Role Management
    def create_role(
        self,
        name: str,
        description: str,
        tenant_id: Optional[str] = None,
        level: int = 0,
        permissions: Optional[List[str]] = None
    ) -> Role:
        """Create a new role."""
        role_id = f"role_{uuid4().hex[:12]}"
        
        role = Role(
            role_id=role_id,
            tenant_id=tenant_id,
            name=name,
            description=description,
            level=level,
            permissions=permissions or []
        )
        
        self.roles[role_id] = role
        return role
    
    def get_role(self, role_id: str) -> Optional[Role]:
        """Get role by ID."""
        return self.roles.get(role_id)
    
    def update_role(
        self,
        role_id: str,
        **updates
    ) -> Optional[Role]:
        """Update role."""
        if role_id not in self.roles:
            return None
        
        role = self.roles[role_id]
        
        for key, value in updates.items():
            if hasattr(role, key) and key not in ["role_id", "created_at"]:
                setattr(role, key, value)
        
        return role
    
    def assign_permissions(
        self,
        role_id: str,
        permission_ids: List[str]
    ) -> Optional[Role]:
        """Assign permissions to a role."""
        if role_id not in self.roles:
            return None
        
        role = self.roles[role_id]
        
        # Validate permissions exist
        valid_permissions = [
            p for p in permission_ids
            if p in self.permissions or p == "*"
        ]
        
        role.permissions = list(set(role.permissions + valid_permissions))
        return role
    
    def get_effective_permissions(
        self,
        user_id: str,
        tenant_id: Optional[str] = None
    ) -> List[str]:
        """Get all effective permissions for a user."""
        user = self.users.get(user_id)
        if not user:
            return []
        
        # Get user's roles for this tenant
        associations = [
            a for a in self.user_associations.values()
            if a.user_id == user_id and a.tenant_id == tenant_id
        ]
        
        permissions = set()
        for association in associations:
            for role_id in association.roles:
                role = self.roles.get(role_id)
                if role:
                    # Check if role is tenant-specific or global
                    if role.tenant_id is None or role.tenant_id == tenant_id:
                        permissions.update(role.permissions)
        
        return list(permissions)
    
    # Tenant-User Association
    def add_user_to_tenant(
        self,
        user_id: str,
        tenant_id: str,
        roles: Optional[List[str]] = None,
        department: Optional[str] = None,
        title: Optional[str] = None
    ) -> UserTenantAssociation:
        """Add user to a tenant with specified roles."""
        user = self.users.get(user_id)
        tenant = self.tenants.get(tenant_id)
        
        if not user or not tenant:
            raise ValueError("User or tenant not found")
        
        association_id = f"assoc_{uuid4().hex[:12]}"
        
        association = UserTenantAssociation(
            association_id=association_id,
            user_id=user_id,
            tenant_id=tenant_id,
            roles=roles or [],
            department=department,
            title=title
        )
        
        self.user_associations[association_id] = association
        self.tenant_users[tenant_id].append(user_id)
        
        # Add default role if none specified
        if not association.roles:
            association.roles = ["learner"]
        
        return association
    
    def get_user_tenant_association(
        self,
        user_id: str,
        tenant_id: str
    ) -> Optional[UserTenantAssociation]:
        """Get user's association with a specific tenant."""
        for association in self.user_associations.values():
            if association.user_id == user_id and association.tenant_id == tenant_id:
                return association
        return None
    
    def update_user_roles(
        self,
        user_id: str,
        tenant_id: str,
        roles: List[str]
    ) -> Optional[UserTenantAssociation]:
        """Update user's roles for a tenant."""
        association = self.get_user_tenant_association(user_id, tenant_id)
        if not association:
            return None
        
        association.roles = roles
        return association
    
    def get_users_in_tenant(
        self,
        tenant_id: str,
        status: Optional[UserStatus] = None
    ) -> List[User]:
        """Get all users in a tenant."""
        user_ids = self.tenant_users.get(tenant_id, [])
        users = [self.users[uid] for uid in user_ids if uid in self.users]
        
        if status:
            users = [u for u in users if u.status == status]
        
        return users
    
    def get_user_roles_in_tenant(
        self,
        user_id: str,
        tenant_id: str
    ) -> List[Role]:
        """Get all roles a user has in a tenant."""
        association = self.get_user_tenant_association(user_id, tenant_id)
        if not association:
            return []
        
        return [
            self.roles[rid] for rid in association.roles
            if rid in self.roles
        ]
    
    # Authentication
    def authenticate(
        self,
        email: str,
        password: str,
        tenant_id: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> Tuple[bool, Optional[Session], Optional[str]]:
        """
        Authenticate a user.
        
        Returns:
            Tuple of (success, session, error_message)
        """
        user = self.get_user_by_email(email)
        
        if not user:
            self._log_auth_event(
                user_id=None,
                tenant_id=tenant_id,
                event_type="login",
                success=False,
                ip_address=ip_address,
                user_agent=user_agent,
                failure_reason="User not found"
            )
            return False, None, "Invalid credentials"
        
        # Check user status
        if user.status == UserStatus.SUSPENDED:
            self._log_auth_event(
                user_id=user.user_id,
                tenant_id=tenant_id,
                event_type="login",
                success=False,
                ip_address=ip_address,
                user_agent=user_agent,
                failure_reason="Account suspended"
            )
            return False, None, "Account suspended"
        
        if user.status == UserStatus.DEACTIVATED:
            self._log_auth_event(
                user_id=user.user_id,
                tenant_id=tenant_id,
                event_type="login",
                success=False,
                ip_address=ip_address,
                user_agent=user_agent,
                failure_reason="Account deactivated"
            )
            return False, None, "Account deactivated"
        
        # In a real implementation, verify password hash
        # For demo, accept any non-empty password
        if not password:
            self._log_auth_event(
                user_id=user.user_id,
                tenant_id=tenant_id,
                event_type="login",
                success=False,
                ip_address=ip_address,
                user_agent=user_agent,
                failure_reason="Invalid password"
            )
            return False, None, "Invalid credentials"
        
        # Create session
        session = self.create_session(
            user_id=user.user_id,
            tenant_id=tenant_id,
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        # Update last login
        user.last_login = datetime.now()
        
        self._log_auth_event(
            user_id=user.user_id,
            tenant_id=tenant_id,
            event_type="login",
            success=True,
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        return True, session, None
    
    def create_session(
        self,
        user_id: str,
        tenant_id: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        expires_hours: int = 24
    ) -> Session:
        """Create a new user session."""
        session_id = f"sess_{uuid4().hex[:16]}"
        token = uuid4().hex[:48]
        
        session = Session(
            session_id=session_id,
            user_id=user_id,
            tenant_id=tenant_id,
            token=token,
            ip_address=ip_address,
            user_agent=user_agent,
            expires_at=datetime.now() + timedelta(hours=expires_hours)
        )
        
        self.sessions[session_id] = session
        return session
    
    def get_session(self, session_id: str) -> Optional[Session]:
        """Get session by ID."""
        session = self.sessions.get(session_id)
        if session and not session.is_valid():
            return None
        return session
    
    def validate_session_token(self, token: str) -> Optional[Session]:
        """Validate session token and return session."""
        for session in self.sessions.values():
            if session.token == token and session.is_valid():
                return session
        return None
    
    def revoke_session(self, session_id: str) -> bool:
        """Revoke a session."""
        if session_id in self.sessions:
            self.sessions[session_id].status = SessionStatus.REVOKED
            return True
        return False
    
    def revoke_all_user_sessions(self, user_id: str) -> int:
        """Revoke all sessions for a user."""
        count = 0
        for session in self.sessions.values():
            if session.user_id == user_id:
                session.status = SessionStatus.REVOKED
                count += 1
        return count
    
    def _log_auth_event(
        self,
        user_id: Optional[str],
        tenant_id: Optional[str],
        event_type: str,
        success: bool,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        failure_reason: Optional[str] = None
    ):
        """Log an authentication event."""
        event = AuthenticationEvent(
            event_id=f"auth_{uuid4().hex[:12]}",
            user_id=user_id,
            tenant_id=tenant_id,
            event_type=event_type,
            success=success,
            ip_address=ip_address,
            user_agent=user_agent,
            failure_reason=failure_reason
        )
        
        self.auth_events.append(event)
    
    def get_auth_events(
        self,
        user_id: Optional[str] = None,
        tenant_id: Optional[str] = None,
        event_type: Optional[str] = None,
        limit: int = 100
    ) -> List[AuthenticationEvent]:
        """Get authentication events with filters."""
        events = self.auth_events
        
        if user_id:
            events = [e for e in events if e.user_id == user_id]
        if tenant_id:
            events = [e for e in events if e.tenant_id == tenant_id]
        if event_type:
            events = [e for e in events if e.event_type == event_type]
        
        return events[-limit:]
    
    # Authorization
    def check_permission(
        self,
        user_id: str,
        permission: str,
        tenant_id: Optional[str] = None
    ) -> bool:
        """Check if user has a specific permission."""
        permissions = self.get_effective_permissions(user_id, tenant_id)
        
        # Check for wildcard
        if "*" in permissions:
            return True
        
        # Check for specific permission
        if permission in permissions:
            return True
        
        # Check for resource-level permission
        resource, action = permission.split(":") if ":" in permission else (permission, "*")
        
        for perm in permissions:
            if ":" in perm:
                r, a = perm.split(":")
                if (r == resource or r == "*") and (a == action or a == "*"):
                    return True
        
        return False
    
    def require_permission(
        self,
        user_id: str,
        permission: str,
        tenant_id: Optional[str] = None
    ) -> bool:
        """Require a permission, raise exception if not granted."""
        if not self.check_permission(user_id, permission, tenant_id):
            raise PermissionError(f"Permission denied: {permission}")
        return True
    
    # Batch Operations
    def batch_add_users_to_tenant(
        self,
        tenant_id: str,
        user_emails: List[str],
        role_ids: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Add multiple users to a tenant."""
        results = {"added": [], "failed": []}
        
        for email in user_emails:
            user = self.get_user_by_email(email)
            if user:
                try:
                    self.add_user_to_tenant(
                        user_id=user.user_id,
                        tenant_id=tenant_id,
                        roles=role_ids or ["learner"]
                    )
                    results["added"].append(email)
                except Exception as e:
                    results["failed"].append({"email": email, "reason": str(e)})
            else:
                results["failed"].append({"email": email, "reason": "User not found"})
        
        return results
    
    def batch_update_user_status(
        self,
        tenant_id: str,
        user_ids: List[str],
        status: UserStatus
    ) -> Dict[str, Any]:
        """Update status for multiple users."""
        results = {"updated": [], "failed": []}
        
        for user_id in user_ids:
            association = self.get_user_tenant_association(user_id, tenant_id)
            if association:
                association.status = status
                results["updated"].append(user_id)
            else:
                results["failed"].append({"user_id": user_id, "reason": "Not in tenant"})
        
        return results
    
    def get_tenant_user_count(self, tenant_id: str) -> int:
        """Get the count of users in a tenant."""
        return len(self.tenant_users.get(tenant_id, []))


# Service factory function
def create_identity_service() -> IdentityService:
    """Create and configure a new identity service instance."""
    return IdentityService()
