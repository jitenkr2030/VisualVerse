"""
Admin Console Service for Governance Platform.

Provides comprehensive administrative operations, system configuration,
batch operations, and unified management interfaces for the governance platform.
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
from uuid import uuid4
from collections import defaultdict
import json


class BatchOperationType(Enum):
    """Types of batch operations."""
    USER_IMPORT = "user_import"
    USER_EXPORT = "user_export"
    USER_UPDATE = "user_update"
    USER_DEACTIVATE = "user_deactivate"
    CONTENT_PUBLISH = "content_publish"
    CONTENT_UNPUBLISH = "content_unpublish"
    CONTENT_DELETE = "content_delete"
    ROLE_ASSIGN = "role_assign"
    PERMISSION_UPDATE = "permission_update"
    TENANT_CONFIG = "tenant_config"
    DATA_MIGRATION = "data_migration"
    REPORT_GENERATION = "report_generation"


class BatchOperationStatus(Enum):
    """Status of batch operations."""
    PENDING = "pending"
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    PAUSED = "paused"


class ConfigCategory(Enum):
    """Categories of system configuration."""
    SYSTEM = "system"
    SECURITY = "security"
    FEATURES = "features"
    INTEGRATIONS = "integrations"
    NOTIFICATIONS = "notifications"
    STORAGE = "storage"
    LIMITS = "limits"
    CUSTOM = "custom"


@dataclass
class BatchOperation:
    """Batch operation job."""
    operation_id: str
    operation_type: BatchOperationType
    tenant_id: Optional[str]
    created_by: str
    
    status: BatchOperationStatus = BatchOperationStatus.PENDING
    progress: float = 0.0
    
    # Operation details
    parameters: Dict[str, Any] = field(default_factory=dict)
    filters: Dict[str, Any] = field(default_factory=dict)
    
    # Execution
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    estimated_completion: Optional[datetime] = None
    
    # Results
    total_items: int = 0
    processed_items: int = 0
    success_count: int = 0
    failure_count: int = 0
    skipped_count: int = 0
    
    errors: List[Dict[str, Any]] = field(default_factory=list)
    results_summary: Dict[str, Any] = field(default_factory=dict)
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    priority: int = 5  # 1-10, higher = more priority
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "operation_id": self.operation_id,
            "operation_type": self.operation_type.value,
            "tenant_id": self.tenant_id,
            "created_by": self.created_by,
            "status": self.status.value,
            "progress": f"{self.progress:.1f}%",
            "total_items": self.total_items,
            "processed_items": self.processed_items,
            "success_count": self.success_count,
            "failure_count": self.failure_count,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "created_at": self.created_at.isoformat()
        }


@dataclass
class SystemConfig:
    """System configuration entry."""
    config_id: str
    category: ConfigCategory
    key: str
    value: Any
    description: str = ""
    
    is_sensitive: bool = False
    is_editable: bool = True
    
    # Validation
    validation_rule: Optional[str] = None
    default_value: Optional[Any] = None
    
    # Scope
    tenant_id: Optional[str] = None
    
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    updated_by: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "config_id": self.config_id,
            "category": self.category.value,
            "key": self.key,
            "value": self.value if not self.is_sensitive else "***",
            "description": self.description,
            "is_sensitive": self.is_sensitive,
            "is_editable": self.is_editable,
            "tenant_id": self.tenant_id,
            "updated_at": self.updated_at.isoformat(),
            "updated_by": self.updated_by
        }


@dataclass
class AdminDashboard:
    """Admin dashboard configuration."""
    dashboard_id: str
    name: str
    description: str = ""
    
    # Widgets
    widgets: List[Dict[str, Any]] = field(default_factory=list)
    
    # Layout
    layout: Dict[str, Any] = field(default_factory=lambda: {"columns": 3, "rows": 3})
    
    # Scope
    tenant_id: Optional[str] = None
    is_default: bool = False
    created_by: Optional[str] = None
    
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "dashboard_id": self.dashboard_id,
            "name": self.name,
            "description": self.description,
            "widget_count": len(self.widgets),
            "tenant_id": self.tenant_id,
            "is_default": self.is_default,
            "created_at": self.created_at.isoformat()
        }


@dataclass
class SystemHealth:
    """System health status."""
    service_name: str
    status: str  # healthy, degraded, unhealthy
    last_check: datetime
    
    # Metrics
    uptime_seconds: int = 0
    request_count: int = 0
    error_count: int = 0
    latency_ms: float = 0.0
    
    # Component health
    components: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    
    # Alerts
    active_alerts: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "service_name": self.service_name,
            "status": self.status,
            "last_check": self.last_check.isoformat(),
            "metrics": {
                "uptime_hours": round(self.uptime_seconds / 3600, 2),
                "request_count": self.request_count,
                "error_rate": f"{(self.error_count / max(1, self.request_count) * 100):.2f}%",
                "latency_ms": round(self.latency_ms, 2)
            },
            "components": self.components,
            "active_alerts": self.active_alerts
        }


@dataclass
class TenantStats:
    """Statistics for a tenant."""
    tenant_id: str
    snapshot_date: datetime
    
    # User stats
    total_users: int = 0
    active_users_30d: int = 0
    new_users_30d: int = 0
    
    # Content stats
    total_content: int = 0
    published_content: int = 0
    pending_moderation: int = 0
    
    # Usage stats
    total_sessions_30d: int = 0
    total_time_hours_30d: float = 0.0
    average_completion_rate: float = 0.0
    
    # Storage
    storage_used_mb: float = 0.0
    storage_limit_mb: float = 0.0
    
    # API usage
    api_calls_30d: int = 0
    api_limit_30d: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "tenant_id": self.tenant_id,
            "snapshot_date": self.snapshot_date.isoformat(),
            "users": {
                "total": self.total_users,
                "active_30d": self.active_users_30d,
                "new_30d": self.new_users_30d
            },
            "content": {
                "total": self.total_content,
                "published": self.published_content,
                "pending_moderation": self.pending_moderation
            },
            "usage": {
                "sessions_30d": self.total_sessions_30d,
                "time_hours_30d": round(self.total_time_hours_30d, 2),
                "completion_rate": f"{self.average_completion_rate:.1f}%"
            },
            "storage": {
                "used_mb": round(self.storage_used_mb, 2),
                "limit_mb": self.storage_limit_mb,
                "usage_percent": f"{(self.storage_used_mb / max(1, self.storage_limit_mb) * 100):.1f}%"
            },
            "api": {
                "calls_30d": self.api_calls_30d,
                "limit_30d": self.api_limit_30d,
                "usage_percent": f"{(self.api_calls_30d / max(1, self.api_limit_30d) * 100):.1f}%"
            }
        }


@dataclass
class AdminNotification:
    """Admin notification."""
    notification_id: str
    type: str  # alert, info, warning, action_required
    title: str
    message: str
    
    priority: str = "normal"  # low, normal, high, urgent
    category: str = "general"
    
    tenant_id: Optional[str] = None
    action_url: Optional[str] = None
    action_label: Optional[str] = None
    
    created_at: datetime = field(default_factory=datetime.now)
    expires_at: Optional[datetime] = None
    read: bool = False
    read_at: Optional[datetime] = None
    
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "notification_id": self.notification_id,
            "type": self.type,
            "title": self.title,
            "message": self.message,
            "priority": self.priority,
            "category": self.category,
            "tenant_id": self.tenant_id,
            "action_url": self.action_url,
            "action_label": self.action_label,
            "created_at": self.created_at.isoformat(),
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "read": self.read,
            "read_at": self.read_at.isoformat() if self.read_at else None
        }


class AdminService:
    """
    Admin console service for the governance platform.
    
    Provides comprehensive administrative operations including batch
    processing, system configuration, health monitoring, and unified
    management interfaces.
    """
    
    def __init__(self):
        # Batch operations
        self.batch_operations: Dict[str, BatchOperation] = {}
        self.operations_by_tenant: Dict[str, List[str]] = defaultdict(list)
        
        # System configuration
        self.system_configs: Dict[str, SystemConfig] = {}
        
        # Dashboards
        self.dashboards: Dict[str, AdminDashboard] = {}
        
        # Health monitoring
        self.health_status: Dict[str, SystemHealth] = {}
        
        # Tenant statistics
        self.tenant_stats: Dict[str, TenantStats] = {}
        
        # Notifications
        self.notifications: Dict[str, AdminNotification] = {}
        self.notifications_by_tenant: Dict[str, List[str]] = defaultdict(list)
        
        # Initialize defaults
        self._init_default_configs()
        self._init_default_dashboard()
    
    def _init_default_configs(self):
        """Initialize default system configurations."""
        default_configs = [
            SystemConfig(
                config_id="cfg_max_users",
                category=ConfigCategory.LIMITS,
                key="max_users_per_tenant",
                value=1000,
                description="Maximum number of users per tenant",
                validation_rule="integer,min=1,max=1000000",
                default_value=1000
            ),
            SystemConfig(
                config_id="cfg_session_timeout",
                category=ConfigCategory.SECURITY,
                key="session_timeout_minutes",
                value=60,
                description="Session timeout in minutes",
                validation_rule="integer,min=5,max=1440",
                default_value=60
            ),
            SystemConfig(
                config_id="cfg_mfa_required",
                category=ConfigCategory.SECURITY,
                key="mfa_required_for_admin",
                value=False,
                description="Require MFA for admin accounts",
                default_value=False
            ),
            SystemConfig(
                config_id="cfg_content_approval",
                category=ConfigCategory.FEATURES,
                key="require_content_approval",
                value=True,
                description="Require moderation approval for published content",
                default_value=True
            ),
            SystemConfig(
                config_id="cfg_registration",
                category=ConfigCategory.FEATURES,
                key="allow_self_registration",
                value=True,
                description="Allow users to register without invitation",
                default_value=True
            ),
            SystemConfig(
                config_id="cfg_api_rate_limit",
                category=ConfigCategory.LIMITS,
                key="api_rate_limit_per_minute",
                value=100,
                description="API rate limit per minute",
                validation_rule="integer,min=1,max=10000",
                default_value=100
            ),
            SystemConfig(
                config_id="cfg_storage_limit",
                category=ConfigCategory.STORAGE,
                key="default_storage_limit_mb",
                value=10240,
                description="Default storage limit per tenant in MB",
                validation_rule="integer,min=1024,max=1048576",
                default_value=10240
            ),
            SystemConfig(
                config_id="cfg_data_retention",
                category=ConfigCategory.SYSTEM,
                key="audit_log_retention_days",
                value=365,
                description="Retention period for audit logs in days",
                validation_rule="integer,min=30,max=3650",
                default_value=365
            )
        ]
        
        for config in default_configs:
            self.system_configs[config.config_id] = config
    
    def _init_default_dashboard(self):
        """Initialize default admin dashboard."""
        dashboard = AdminDashboard(
            dashboard_id="admin_default",
            name="Admin Dashboard",
            description="Default administration dashboard",
            widgets=[
                {"id": "w1", "type": "metric", "title": "Total Users", "data_source": "user_count"},
                {"id": "w2", "type": "metric", "title": "Active Sessions", "data_source": "active_sessions"},
                {"id": "w3", "type": "metric", "title": "Pending Moderation", "data_source": "pending_moderation"},
                {"id": "w4", "type": "chart", "title": "User Activity", "data_source": "activity_trend", "config": {"days": 7}},
                {"id": "w5", "type": "table", "title": "Recent Alerts", "data_source": "recent_alerts"},
                {"id": "w6", "type": "status", "title": "System Health", "data_source": "system_health"}
            ],
            is_default=True
        )
        
        self.dashboards[dashboard.dashboard_id] = dashboard
    
    # Batch Operations
    def create_batch_operation(
        self,
        operation_type: BatchOperationType,
        created_by: str,
        tenant_id: Optional[str] = None,
        parameters: Optional[Dict[str, Any]] = None,
        filters: Optional[Dict[str, Any]] = None,
        priority: int = 5
    ) -> BatchOperation:
        """Create a new batch operation."""
        operation_id = f"batch_{uuid4().hex[:12]}"
        
        operation = BatchOperation(
            operation_id=operation_id,
            operation_type=operation_type,
            tenant_id=tenant_id,
            created_by=created_by,
            parameters=parameters or {},
            filters=filters or {},
            priority=min(10, max(1, priority))
        )
        
        self.batch_operations[operation_id] = operation
        if tenant_id:
            self.operations_by_tenant[tenant_id].append(operation_id)
        
        return operation
    
    def start_batch_operation(
        self,
        operation_id: str
    ) -> Optional[BatchOperation]:
        """Start a batch operation."""
        operation = self.batch_operations.get(operation_id)
        if not operation:
            return None
        
        operation.status = BatchOperationStatus.RUNNING
        operation.started_at = datetime.now()
        operation.estimated_completion = datetime.now() + timedelta(minutes=30)
        operation.updated_at = datetime.now()
        
        return operation
    
    def update_batch_operation_progress(
        self,
        operation_id: str,
        progress: float,
        processed_items: Optional[int] = None,
        success_count: Optional[int] = None,
        failure_count: Optional[int] = None
    ) -> Optional[BatchOperation]:
        """Update batch operation progress."""
        operation = self.batch_operations.get(operation_id)
        if not operation:
            return None
        
        operation.progress = progress
        operation.updated_at = datetime.now()
        
        if processed_items is not None:
            operation.processed_items = processed_items
        if success_count is not None:
            operation.success_count = success_count
        if failure_count is not None:
            operation.failure_count = failure_count
        
        return operation
    
    def complete_batch_operation(
        self,
        operation_id: str,
        results_summary: Optional[Dict[str, Any]] = None,
        errors: Optional[List[Dict[str, Any]]] = None
    ) -> Optional[BatchOperation]:
        """Complete a batch operation."""
        operation = self.batch_operations.get(operation_id)
        if not operation:
            return None
        
        operation.status = BatchOperationStatus.COMPLETED
        operation.progress = 100.0
        operation.completed_at = datetime.now()
        operation.updated_at = datetime.now()
        
        if results_summary:
            operation.results_summary = results_summary
        if errors:
            operation.errors = errors
        
        return operation
    
    def fail_batch_operation(
        self,
        operation_id: str,
        error_message: str
    ) -> Optional[BatchOperation]:
        """Mark a batch operation as failed."""
        operation = self.batch_operations.get(operation_id)
        if not operation:
            return None
        
        operation.status = BatchOperationStatus.FAILED
        operation.completed_at = datetime.now()
        operation.errors.append({
            "timestamp": datetime.now().isoformat(),
            "error": error_message
        })
        operation.updated_at = datetime.now()
        
        return operation
    
    def cancel_batch_operation(
        self,
        operation_id: str,
        cancelled_by: str
    ) -> Optional[BatchOperation]:
        """Cancel a batch operation."""
        operation = self.batch_operations.get(operation_id)
        if not operation:
            return None
        
        operation.status = BatchOperationStatus.CANCELLED
        operation.completed_at = datetime.now()
        operation.notes = operation.notes + [f"Cancelled by {cancelled_by} at {datetime.now().isoformat()}"] if hasattr(operation, 'notes') else f"Cancelled by {cancelled_by}"
        operation.updated_at = datetime.now()
        
        return operation
    
    def get_batch_operation(
        self,
        operation_id: str
    ) -> Optional[BatchOperation]:
        """Get a batch operation by ID."""
        return self.batch_operations.get(operation_id)
    
    def list_batch_operations(
        self,
        tenant_id: Optional[str] = None,
        status: Optional[BatchOperationStatus] = None,
        operation_type: Optional[BatchOperationType] = None,
        limit: int = 50
    ) -> List[BatchOperation]:
        """List batch operations with filters."""
        operations = list(self.batch_operations.values())
        
        if tenant_id:
            operations = [o for o in operations if o.tenant_id == tenant_id]
        if status:
            operations = [o for o in operations if o.status == status]
        if operation_type:
            operations = [o for o in operations if o.operation_type == operation_type]
        
        operations.sort(key=lambda o: o.created_at, reverse=True)
        return operations[:limit]
    
    # System Configuration
    def get_config(
        self,
        config_id: str
    ) -> Optional[SystemConfig]:
        """Get a system configuration."""
        return self.system_configs.get(config_id)
    
    def get_config_value(
        self,
        key: str,
        tenant_id: Optional[str] = None
    ) -> Any:
        """Get a configuration value."""
        for config in self.system_configs.values():
            if config.key == key and config.tenant_id == tenant_id:
                return config.value
            if config.key == key and config.tenant_id is None:
                return config.value
        return None
    
    def set_config(
        self,
        key: str,
        value: Any,
        category: ConfigCategory,
        updated_by: str,
        description: str = "",
        tenant_id: Optional[str] = None,
        is_sensitive: bool = False
    ) -> SystemConfig:
        """Set a configuration value."""
        # Find existing or create new
        config_id = f"cfg_{tenant_id or 'global'}_{key}" if tenant_id else f"cfg_{key}"
        
        if config_id in self.system_configs:
            config = self.system_configs[config_id]
            config.value = value
            config.updated_at = datetime.now()
            config.updated_by = updated_by
        else:
            config = SystemConfig(
                config_id=config_id,
                category=category,
                key=key,
                value=value,
                description=description,
                tenant_id=tenant_id,
                is_sensitive=is_sensitive,
                updated_by=updated_by
            )
        
        self.system_configs[config_id] = config
        return config
    
    def list_configs(
        self,
        category: Optional[ConfigCategory] = None,
        tenant_id: Optional[str] = None
    ) -> List[SystemConfig]:
        """List system configurations."""
        configs = list(self.system_configs.values())
        
        if category:
            configs = [c for c in configs if c.category == category]
        if tenant_id:
            configs = [
                c for c in configs
                if c.tenant_id is None or c.tenant_id == tenant_id
            ]
        
        return configs
    
    # Dashboard Management
    def get_dashboard(
        self,
        dashboard_id: str
    ) -> Optional[AdminDashboard]:
        """Get a dashboard."""
        return self.dashboards.get(dashboard_id)
    
    def get_default_dashboard(self) -> Optional[AdminDashboard]:
        """Get the default dashboard."""
        for dashboard in self.dashboards.values():
            if dashboard.is_default:
                return dashboard
        return None
    
    def create_dashboard(
        self,
        name: str,
        created_by: str,
        description: str = "",
        tenant_id: Optional[str] = None
    ) -> AdminDashboard:
        """Create a new dashboard."""
        dashboard = AdminDashboard(
            dashboard_id=f"dash_{uuid4().hex[:12]}",
            name=name,
            description=description,
            tenant_id=tenant_id,
            created_by=created_by
        )
        
        self.dashboards[dashboard.dashboard_id] = dashboard
        return dashboard
    
    def update_dashboard(
        self,
        dashboard_id: str,
        updates: Dict[str, Any]
    ) -> Optional[AdminDashboard]:
        """Update a dashboard."""
        dashboard = self.dashboards.get(dashboard_id)
        if not dashboard:
            return None
        
        for key, value in updates.items():
            if hasattr(dashboard, key) and key not in ["dashboard_id", "created_at", "created_by"]:
                setattr(dashboard, key, value)
        
        dashboard.updated_at = datetime.now()
        return dashboard
    
    # Health Monitoring
    def update_health_status(
        self,
        service_name: str,
        status: str,
        metrics: Optional[Dict[str, Any]] = None,
        components: Optional[Dict[str, Dict[str, Any]]] = None
    ) -> SystemHealth:
        """Update health status for a service."""
        health = SystemHealth(
            service_name=service_name,
            status=status,
            last_check=datetime.now()
        )
        
        if metrics:
            if "uptime_seconds" in metrics:
                health.uptime_seconds = metrics["uptime_seconds"]
            if "request_count" in metrics:
                health.request_count = metrics["request_count"]
            if "error_count" in metrics:
                health.error_count = metrics["error_count"]
            if "latency_ms" in metrics:
                health.latency_ms = metrics["latency_ms"]
        
        if components:
            health.components = components
        
        self.health_status[service_name] = health
        return health
    
    def get_health_status(self, service_name: Optional[str] = None) -> Dict[str, Any]:
        """Get health status."""
        if service_name:
            health = self.health_status.get(service_name)
            return health.to_dict() if health else {"status": "unknown"}
        
        # Return aggregate status
        services = list(self.health_status.values())
        
        if not services:
            return {"overall_status": "unknown", "services": {}}
        
        status_counts = {"healthy": 0, "degraded": 0, "unhealthy": 0}
        for s in services:
            status_counts[s.status] += 1
        
        overall = "healthy"
        if status_counts["unhealthy"] > 0:
            overall = "unhealthy"
        elif status_counts["degraded"] > 0:
            overall = "degraded"
        
        return {
            "overall_status": overall,
            "summary": status_counts,
            "services": {
                s.service_name: {
                    "status": s.status,
                    "latency_ms": s.latency_ms,
                    "error_count": s.error_count
                }
                for s in services
            },
            "last_check": datetime.now().isoformat()
        }
    
    # Tenant Statistics
    def update_tenant_stats(
        self,
        tenant_id: str,
        stats: Dict[str, Any]
    ) -> TenantStats:
        """Update tenant statistics."""
        if tenant_id not in self.tenant_stats:
            self.tenant_stats[tenant_id] = TenantStats(
                tenant_id=tenant_id,
                snapshot_date=datetime.now()
            )
        
        tenant_stats = self.tenant_stats[tenant_id]
        
        # Update user stats
        if "total_users" in stats:
            tenant_stats.total_users = stats["total_users"]
        if "active_users_30d" in stats:
            tenant_stats.active_users_30d = stats["active_users_30d"]
        if "new_users_30d" in stats:
            tenant_stats.new_users_30d = stats["new_users_30d"]
        
        # Update content stats
        if "total_content" in stats:
            tenant_stats.total_content = stats["total_content"]
        if "published_content" in stats:
            tenant_stats.published_content = stats["published_content"]
        if "pending_moderation" in stats:
            tenant_stats.pending_moderation = stats["pending_moderation"]
        
        # Update usage stats
        if "total_sessions_30d" in stats:
            tenant_stats.total_sessions_30d = stats["total_sessions_30d"]
        if "total_time_hours_30d" in stats:
            tenant_stats.total_time_hours_30d = stats["total_time_hours_30d"]
        if "average_completion_rate" in stats:
            tenant_stats.average_completion_rate = stats["average_completion_rate"]
        
        # Update storage
        if "storage_used_mb" in stats:
            tenant_stats.storage_used_mb = stats["storage_used_mb"]
        if "storage_limit_mb" in stats:
            tenant_stats.storage_limit_mb = stats["storage_limit_mb"]
        
        # Update API usage
        if "api_calls_30d" in stats:
            tenant_stats.api_calls_30d = stats["api_calls_30d"]
        if "api_limit_30d" in stats:
            tenant_stats.api_limit_30d = stats["api_limit_30d"]
        
        tenant_stats.snapshot_date = datetime.now()
        return tenant_stats
    
    def get_tenant_stats(self, tenant_id: str) -> Optional[TenantStats]:
        """Get tenant statistics."""
        return self.tenant_stats.get(tenant_id)
    
    def get_all_tenant_stats(self) -> List[TenantStats]:
        """Get statistics for all tenants."""
        return list(self.tenant_stats.values())
    
    # Notifications
    def create_notification(
        self,
        notification_type: str,
        title: str,
        message: str,
        priority: str = "normal",
        category: str = "general",
        tenant_id: Optional[str] = None,
        action_url: Optional[str] = None,
        action_label: Optional[str] = None,
        expires_at: Optional[datetime] = None
    ) -> AdminNotification:
        """Create an admin notification."""
        notification = AdminNotification(
            notification_id=f"notif_{uuid4().hex[:12]}",
            type=notification_type,
            title=title,
            message=message,
            priority=priority,
            category=category,
            tenant_id=tenant_id,
            action_url=action_url,
            action_label=action_label,
            expires_at=expires_at
        )
        
        self.notifications[notification.notification_id] = notification
        if tenant_id:
            self.notifications_by_tenant[tenant_id].append(notification.notification_id)
        
        return notification
    
    def get_notification(
        self,
        notification_id: str
    ) -> Optional[AdminNotification]:
        """Get a notification."""
        return self.notifications.get(notification_id)
    
    def mark_notification_read(
        self,
        notification_id: str
    ) -> Optional[AdminNotification]:
        """Mark a notification as read."""
        notification = self.notifications.get(notification_id)
        if notification:
            notification.read = True
            notification.read_at = datetime.now()
        return notification
    
    def list_notifications(
        self,
        tenant_id: Optional[str] = None,
        unread_only: bool = False,
        category: Optional[str] = None,
        limit: int = 50
    ) -> List[AdminNotification]:
        """List notifications."""
        notifications = list(self.notifications.values())
        
        if tenant_id:
            notifications = [n for n in notifications if n.tenant_id == tenant_id]
        if unread_only:
            notifications = [n for n in notifications if not n.read]
        if category:
            notifications = [n for n in notifications if n.category == category]
        
        notifications.sort(key=lambda n: n.created_at, reverse=True)
        return notifications[:limit]
    
    # Utility Methods
    def get_admin_summary(self, tenant_id: Optional[str] = None) -> Dict[str, Any]:
        """Get admin summary dashboard data."""
        # Count active operations
        active_ops = [
            o for o in self.batch_operations.values()
            if o.status == BatchOperationStatus.RUNNING
        ]
        
        # Count unread notifications
        unread_count = len([
            n for n in self.notifications.values()
            if not n.read and (not tenant_id or n.tenant_id == tenant_id)
        ])
        
        # Get health status
        health = self.get_health_status()
        
        # Get recent alerts
        recent_notifications = self.list_notifications(
            tenant_id=tenant_id,
            limit=5
        )
        
        return {
            "system_health": health,
            "active_operations": len(active_ops),
            "unread_notifications": unread_count,
            "total_configs": len(self.system_configs),
            "total_dashboards": len(self.dashboards),
            "recent_notifications": [
                {
                    "id": n.notification_id,
                    "type": n.type,
                    "title": n.title,
                    "priority": n.priority
                }
                for n in recent_notifications
            ]
        }
    
    def execute_user_import(
        self,
        tenant_id: str,
        users: List[Dict[str, Any]],
        created_by: str,
        default_role: str = "learner"
    ) -> BatchOperation:
        """Execute a batch user import."""
        operation = self.create_batch_operation(
            operation_type=BatchOperationType.USER_IMPORT,
            created_by=created_by,
            tenant_id=tenant_id,
            parameters={"default_role": default_role, "user_count": len(users)},
            priority=7
        )
        
        # Simulate processing
        self.start_batch_operation(operation.operation_id)
        
        # In production, this would process users in batches
        success_count = len(users)
        
        self.update_batch_operation_progress(
            operation.operation_id,
            progress=100.0,
            processed_items=len(users),
            success_count=success_count
        )
        
        self.complete_batch_operation(
            operation.operation_id,
            results_summary={
                "imported": success_count,
                "failed": 0,
                "role_assigned": default_role
            }
        )
        
        return operation


# Service factory function
def create_admin_service() -> AdminService:
    """Create and configure a new admin service instance."""
    return AdminService()
