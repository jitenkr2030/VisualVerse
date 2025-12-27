"""
Compliance & Audit Service for Governance Platform.

Provides comprehensive compliance management, audit logging,
data privacy enforcement, and security auditing for institutional deployments.
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
from uuid import uuid4
from collections import defaultdict
import json


class PrivacyRegulation(Enum):
    """Data privacy regulations."""
    GDPR = "gdpr"
    CCPA = "ccpa"
    FERPA = "ferpa"
    HIPAA = "hipaa"
    COPPA = "coppa"
    LGPD = "lgpd"
    CUSTOM = "custom"


class AuditAction(Enum):
    """Types of audit actions."""
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    LOGIN = "login"
    LOGOUT = "logout"
    EXPORT = "export"
    SHARE = "share"
    PERMISSION_CHANGE = "permission_change"
    DATA_ACCESS = "data_access"
    CONFIG_CHANGE = "config_change"
    API_CALL = "api_call"


class PrivacyRequestStatus(Enum):
    """Status of privacy requests."""
    PENDING = "pending"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    DENIED = "denied"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class PrivacyRequestType(Enum):
    """Types of privacy requests."""
    ACCESS = "access"  # Data Subject Access Request (DSAR)
    RECTIFICATION = "rectification"
    ERASURE = "erasure"  # Right to be forgotten
    PORTABILITY = "portability"
    RESTRICTION = "restriction"
    OBJECTION = "objection"


class SecuritySeverity(Enum):
    """Security alert severity levels."""
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class PolicyEffect(Enum):
    """Policy rule effects."""
    ALLOW = "allow"
    DENY = "deny"
    REQUIRE = "require"
    LOG = "log"


@dataclass
class AuditLog:
    """Immutable audit log entry."""
    log_id: str
    timestamp: datetime
    actor_id: str
    actor_type: str  # "user", "system", "service"
    tenant_id: Optional[str]
    
    action: AuditAction
    resource_type: str
    resource_id: Optional[str]
    
    # Details
    description: str
    old_value: Optional[Dict[str, Any]] = None
    new_value: Optional[Dict[str, Any]] = None
    change_summary: Optional[str] = None
    
    # Context
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    session_id: Optional[str] = None
    request_id: Optional[str] = None
    
    # Compliance
    regulation: Optional[PrivacyRegulation] = None
    data_categories: List[str] = field(default_factory=list)
    sensitive_data: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "log_id": self.log_id,
            "timestamp": self.timestamp.isoformat(),
            "actor_id": self.actor_id,
            "actor_type": self.actor_type,
            "tenant_id": self.tenant_id,
            "action": self.action.value,
            "resource_type": self.resource_type,
            "resource_id": self.resource_id,
            "description": self.description,
            "old_value": self.old_value,
            "new_value": self.new_value,
            "change_summary": self.change_summary,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "session_id": self.session_id,
            "request_id": self.request_id,
            "regulation": self.regulation.value if self.regulation else None,
            "data_categories": self.data_categories,
            "sensitive_data": self.sensitive_data
        }


@dataclass
class DataPrivacyRequest:
    """Data Subject Access Request (DSAR) or similar privacy request."""
    request_id: str
    user_id: str
    tenant_id: str
    request_type: PrivacyRequestType
    status: PrivacyRequestStatus = PrivacyRequestStatus.PENDING
    
    description: str = ""
    justification: str = ""
    
    requested_at: datetime = field(default_factory=datetime.now)
    due_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    assigned_to: Optional[str] = None
    notes: List[str] = field(default_factory=list)
    
    # Request details
    data_scope: List[str] = field(default_factory=list)  # Categories of data
    verification_method: str = "email"
    verified: bool = False
    
    # Results
    response_data: Optional[Dict[str, Any]] = None
    denied_reason: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "request_id": self.request_id,
            "user_id": self.user_id,
            "tenant_id": self.tenant_id,
            "request_type": self.request_type.value,
            "status": self.status.value,
            "description": self.description,
            "justification": self.justification,
            "requested_at": self.requested_at.isoformat(),
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "assigned_to": self.assigned_to,
            "notes": self.notes,
            "data_scope": self.data_scope,
            "verified": self.verified,
            "response_data_keys": list(self.response_data.keys()) if self.response_data else None,
            "denied_reason": self.denied_reason
        }


@dataclass
class PolicyRule:
    """Policy enforcement rule."""
    rule_id: str
    name: str
    description: str
    regulation: Optional[PrivacyRegulation]
    
    # Rule definition
    condition: Dict[str, Any]
    effect: PolicyEffect
    actions: List[str] = field(default_factory=list)
    
    # Scope
    resource_types: List[str] = field(default_factory=list)
    user_roles: List[str] = field(default_factory=list)
    tenant_id: Optional[str] = None
    
    # Metadata
    priority: int = 0
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    created_by: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "name": self.name,
            "description": self.description,
            "regulation": self.regulation.value if self.regulation else None,
            "condition": self.condition,
            "effect": self.effect.value,
            "actions": self.actions,
            "resource_types": self.resource_types,
            "user_roles": self.user_roles,
            "tenant_id": self.tenant_id,
            "priority": self.priority,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "created_by": self.created_by
        }


@dataclass
class SecurityAlert:
    """Security alert."""
    alert_id: str
    alert_type: str
    severity: SecuritySeverity
    
    title: str
    description: str
    
    tenant_id: Optional[str]
    affected_users: List[str] = field(default_factory=list)
    affected_resources: List[str] = field(default_factory=list)
    
    detected_at: datetime = field(default_factory=datetime.now)
    resolved_at: Optional[datetime] = None
    resolved_by: Optional[str] = None
    
    status: str = "open"  # open, investigating, resolved, dismissed
    resolution: Optional[str] = None
    
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "alert_id": self.alert_id,
            "alert_type": self.alert_type,
            "severity": self.severity.value,
            "title": self.title,
            "description": self.description,
            "tenant_id": self.tenant_id,
            "affected_user_count": len(self.affected_users),
            "affected_resource_count": len(self.affected_resources),
            "detected_at": self.detected_at.isoformat(),
            "resolved_at": self.resolved_at.isoformat() if self.resolved_at else None,
            "resolved_by": self.resolved_by,
            "status": self.status,
            "resolution": self.resolution,
            "metadata": self.metadata
        }


@dataclass
class ComplianceReport:
    """Compliance report."""
    report_id: str
    report_type: str
    tenant_id: str
    regulation: Optional[PrivacyRegulation]
    
    period_start: datetime
    period_end: datetime
    
    # Report data
    summary: Dict[str, Any] = field(default_factory=dict)
    findings: List[Dict[str, Any]] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)
    
    # Generation
    generated_at: datetime = field(default_factory=datetime.now)
    generated_by: Optional[str] = None
    
    # Status
    status: str = "draft"  # draft, review, approved, published
    approved_by: Optional[str] = None
    approved_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "report_id": self.report_id,
            "report_type": self.report_type,
            "tenant_id": self.tenant_id,
            "regulation": self.regulation.value if self.regulation else None,
            "period": {
                "start": self.period_start.isoformat(),
                "end": self.period_end.isoformat()
            },
            "summary": self.summary,
            "findings_count": len(self.findings),
            "recommendations_count": len(self.recommendations),
            "metrics": self.metrics,
            "generated_at": self.generated_at.isoformat(),
            "generated_by": self.generated_by,
            "status": self.status,
            "approved_by": self.approved_by,
            "approved_at": self.approved_at.isoformat() if self.approved_at else None
        }


@dataclass
class DataRetentionPolicy:
    """Data retention policy."""
    policy_id: str
    name: str
    description: str
    
    data_category: str
    retention_days: int
    deletion_action: str = "anonymize"  # anonymize, delete, archive
    
    # Scope
    resource_types: List[str] = field(default_factory=list)
    tenant_id: Optional[str] = None
    
    # Compliance
    regulation: Optional[PrivacyRegulation] = None
    legal_hold: bool = False
    
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "policy_id": self.policy_id,
            "name": self.name,
            "description": self.description,
            "data_category": self.data_category,
            "retention_days": self.retention_days,
            "deletion_action": self.deletion_action,
            "resource_types": self.resource_types,
            "tenant_id": self.tenant_id,
            "regulation": self.regulation.value if self.regulation else None,
            "legal_hold": self.legal_hold,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


class ComplianceService:
    """
    Compliance and audit service for the governance platform.
    
    Provides comprehensive compliance management including audit logging,
    data privacy enforcement, policy management, security monitoring,
    and regulatory reporting.
    """
    
    def __init__(self):
        # Audit logging
        self.audit_logs: List[AuditLog] = []
        self.logs_by_actor: Dict[str, List[str]] = defaultdict(list)
        self.logs_by_resource: Dict[str, List[str]] = defaultdict(list)
        
        # Privacy requests
        self.privacy_requests: Dict[str, DataPrivacyRequest] = {}
        self.user_requests: Dict[str, List[str]] = defaultdict(list)
        
        # Policy rules
        self.policy_rules: Dict[str, PolicyRule] = {}
        
        # Security alerts
        self.security_alerts: Dict[str, SecurityAlert] = {}
        self.alerts_by_tenant: Dict[str, List[str]] = defaultdict(list)
        
        # Compliance reports
        self.compliance_reports: Dict[str, ComplianceReport] = {}
        
        # Retention policies
        self.retention_policies: Dict[str, DataRetentionPolicy] = {}
        
        # Initialize default policies and rules
        self._init_defaults()
    
    def _init_defaults(self):
        """Initialize default policies and rules."""
        # Default retention policies
        default_retention = [
            DataRetentionPolicy(
                policy_id="retention_user_activity",
                name="User Activity Logs",
                description="Retention for user activity and session data",
                data_category="activity_logs",
                retention_days=365,
                resource_types=["session", "activity"]
            ),
            DataRetentionPolicy(
                policy_id="retention_user_profile",
                name="User Profile Data",
                description="Retention for user profile and account data",
                data_category="user_profile",
                retention_days=2555,  # 7 years
                deletion_action="anonymize",
                resource_types=["user", "profile"]
            ),
            DataRetentionPolicy(
                policy_id="retention_learning_history",
                name="Learning History",
                description="Retention for learning and progress data",
                data_category="learning_history",
                retention_days=3650,  # 10 years
                resource_types=["progress", "assessment", "certificate"]
            ),
            DataRetentionPolicy(
                policy_id="retention_financial",
                name="Financial Transactions",
                description="Retention for financial and billing data",
                data_category="financial",
                retention_days=2190,  # 6 years
                deletion_action="archive",
                resource_types=["transaction", "invoice", "subscription"]
            ),
            DataRetentionPolicy(
                policy_id="retention_communications",
                name="Communications",
                description="Retention for user communications",
                data_category="communications",
                retention_days=90,
                resource_types=["message", "notification", "support_ticket"]
            )
        ]
        
        for policy in default_retention:
            self.retention_policies[policy.policy_id] = policy
        
        # Default policy rules
        default_rules = [
            PolicyRule(
                rule_id="rule_pii_access",
                name="PII Access Logging",
                description="Log all access to personally identifiable information",
                regulation=PrivacyRegulation.GDPR,
                condition={"check": "contains_pii", "value": True},
                effect=PolicyEffect.LOG,
                actions=["log_access", "notify_dpo"],
                resource_types=["user", "profile", "assessment"],
                priority=100
            ),
            PolicyRule(
                rule_id="rule_export_approval",
                name="Bulk Export Approval",
                description="Require approval for bulk data exports",
                regulation=PrivacyRegulation.GDPR,
                condition={"check": "export_size", "threshold": 1000},
                effect=PolicyEffect.REQUIRE,
                actions=["require_approval", "log_export"],
                resource_types=["export", "report"],
                priority=90
            ),
            PolicyRule(
                rule_id="rule_minor_consent",
                name="Minor Consent Verification",
                description="Verify parental consent for users under 16",
                regulation=PrivacyRegulation.COPPA,
                condition={"check": "user_age", "threshold": 16},
                effect=PolicyEffect.REQUIRE,
                actions=["verify_consent", "restrict_access"],
                resource_types=["account", "content_access"],
                priority=95
            ),
            PolicyRule(
                rule_id="rule_data_retention",
                name="Data Retention Enforcement",
                description="Enforce data retention policies",
                regulation=PrivacyRegulation.GDPR,
                condition={"check": "retention_expired"},
                effect=PolicyEffect.REQUIRE,
                actions=["schedule_deletion", "notify_user"],
                resource_types=["all"],
                priority=80
            )
        ]
        
        for rule in default_rules:
            self.policy_rules[rule.rule_id] = rule
    
    # Audit Logging
    def log_audit_event(
        self,
        actor_id: str,
        actor_type: str,
        action: AuditAction,
        resource_type: str,
        description: str,
        tenant_id: Optional[str] = None,
        resource_id: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        session_id: Optional[str] = None,
        old_value: Optional[Dict[str, Any]] = None,
        new_value: Optional[Dict[str, Any]] = None,
        regulation: Optional[PrivacyRegulation] = None,
        data_categories: Optional[List[str]] = None,
        sensitive_data: bool = False
    ) -> AuditLog:
        """Create an audit log entry."""
        log_id = f"audit_{uuid4().hex[:16]}"
        
        # Generate change summary
        change_summary = None
        if old_value is not None and new_value is not None:
            changes = []
            for key in set(old_value.keys()) | set(new_value.keys()):
                if old_value.get(key) != new_value.get(key):
                    changes.append(f"{key}: {old_value.get(key)} -> {new_value.get(key)}")
            change_summary = "; ".join(changes) if changes else None
        
        log = AuditLog(
            log_id=log_id,
            timestamp=datetime.now(),
            actor_id=actor_id,
            actor_type=actor_type,
            tenant_id=tenant_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            description=description,
            old_value=old_value,
            new_value=new_value,
            change_summary=change_summary,
            ip_address=ip_address,
            user_agent=user_agent,
            session_id=session_id,
            regulation=regulation,
            data_categories=data_categories or [],
            sensitive_data=sensitive_data
        )
        
        self.audit_logs.append(log)
        self.logs_by_actor[actor_id].append(log_id)
        
        if resource_id:
            self.logs_by_resource[resource_id].append(log_id)
        
        return log
    
    def query_audit_logs(
        self,
        actor_id: Optional[str] = None,
        tenant_id: Optional[str] = None,
        action: Optional[AuditAction] = None,
        resource_type: Optional[str] = None,
        resource_id: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        regulation: Optional[PrivacyRegulation] = None,
        sensitive_only: bool = False,
        limit: int = 500
    ) -> List[AuditLog]:
        """Query audit logs with filters."""
        logs = self.audit_logs
        
        if actor_id:
            logs = [l for l in logs if l.actor_id == actor_id]
        if tenant_id:
            logs = [l for l in logs if l.tenant_id == tenant_id]
        if action:
            logs = [l for l in logs if l.action == action]
        if resource_type:
            logs = [l for l in logs if l.resource_type == resource_type]
        if resource_id:
            logs = [l for l in logs if l.resource_id == resource_id]
        if regulation:
            logs = [l for l in logs if l.regulation == regulation]
        if sensitive_only:
            logs = [l for l in logs if l.sensitive_data]
        if start_date:
            logs = [l for l in logs if l.timestamp >= start_date]
        if end_date:
            logs = [l for l in logs if l.timestamp <= end_date]
        
        logs.sort(key=lambda l: l.timestamp, reverse=True)
        return logs[:limit]
    
    def get_audit_log(self, log_id: str) -> Optional[AuditLog]:
        """Get a specific audit log entry."""
        for log in self.audit_logs:
            if log.log_id == log_id:
                return log
        return None
    
    def get_user_activity_summary(
        self,
        user_id: str,
        days: int = 30
    ) -> Dict[str, Any]:
        """Get activity summary for a user."""
        start_date = datetime.now() - timedelta(days=days)
        
        logs = self.query_audit_logs(
            actor_id=user_id,
            start_date=start_date
        )
        
        action_counts: Dict[str, int] = defaultdict(int)
        resource_counts: Dict[str, int] = defaultdict(int)
        
        for log in logs:
            action_counts[log.action.value] += 1
            resource_counts[log.resource_type] += 1
        
        return {
            "user_id": user_id,
            "period_days": days,
            "total_actions": len(logs),
            "by_action": dict(action_counts),
            "by_resource": dict(resource_counts),
            "first_activity": logs[-1].timestamp.isoformat() if logs else None,
            "last_activity": logs[0].timestamp.isoformat() if logs else None
        }
    
    # Privacy Requests (DSAR)
    def create_privacy_request(
        self,
        user_id: str,
        tenant_id: str,
        request_type: PrivacyRequestType,
        description: str = "",
        data_scope: Optional[List[str]] = None
    ) -> DataPrivacyRequest:
        """Create a new privacy request."""
        request_id = f"privacy_{uuid4().hex[:12]}"
        
        # Calculate due date based on regulation
        due_days = 30  # GDPR default
        if request_type == PrivacyRequestType.ERASURE:
            due_days = 30
        elif request_type == PrivacyRequestType.PORTABILITY:
            due_days = 30
        
        request = DataPrivacyRequest(
            request_id=request_id,
            user_id=user_id,
            tenant_id=tenant_id,
            request_type=request_type,
            description=description,
            due_date=datetime.now() + timedelta(days=due_days),
            data_scope=data_scope or ["all"]
        )
        
        self.privacy_requests[request_id] = request
        self.user_requests[user_id].append(request_id)
        
        # Audit log
        self.log_audit_event(
            actor_id=user_id,
            actor_type="user",
            action=AuditAction.CREATE,
            resource_type="privacy_request",
            description=f"Privacy request submitted: {request_type.value}",
            tenant_id=tenant_id,
            resource_id=request_id,
            regulation=PrivacyRegulation.GDPR
        )
        
        return request
    
    def get_privacy_request(self, request_id: str) -> Optional[DataPrivacyRequest]:
        """Get a privacy request."""
        return self.privacy_requests.get(request_id)
    
    def update_privacy_request_status(
        self,
        request_id: str,
        status: PrivacyRequestStatus,
        assigned_to: Optional[str] = None,
        notes: Optional[str] = None
    ) -> Optional[DataPrivacyRequest]:
        """Update privacy request status."""
        request = self.privacy_requests.get(request_id)
        if not request:
            return None
        
        old_status = request.status
        request.status = status
        
        if assigned_to:
            request.assigned_to = assigned_to
        
        if notes:
            request.notes.append(f"[{datetime.now().isoformat()}] {notes}")
        
        # Audit log
        self.log_audit_event(
            actor_id=assigned_to or "system",
            actor_type="user",
            action=AuditAction.UPDATE,
            resource_type="privacy_request",
            description=f"Privacy request status changed: {old_status.value} -> {status.value}",
            resource_id=request_id,
            tenant_id=request.tenant_id,
            new_value={"status": status.value}
        )
        
        if status == PrivacyRequestStatus.COMPLETED:
            request.completed_at = datetime.now()
        
        return request
    
    def complete_privacy_request(
        self,
        request_id: str,
        response_data: Dict[str, Any],
        completed_by: str
    ) -> Optional[DataPrivacyRequest]:
        """Complete a privacy request with response data."""
        request = self.privacy_requests.get(request_id)
        if not request:
            return None
        
        request.status = PrivacyRequestStatus.COMPLETED
        request.response_data = response_data
        request.completed_at = datetime.now()
        
        # Audit log
        self.log_audit_event(
            actor_id=completed_by,
            actor_type="user",
            action=AuditAction.UPDATE,
            resource_type="privacy_request",
            description=f"Privacy request completed: {request.request_type.value}",
            resource_id=request_id,
            tenant_id=request.tenant_id,
            new_value={"status": "completed", "data_categories": list(response_data.keys())}
        )
        
        return request
    
    def list_privacy_requests(
        self,
        tenant_id: Optional[str] = None,
        user_id: Optional[str] = None,
        status: Optional[PrivacyRequestStatus] = None,
        request_type: Optional[PrivacyRequestType] = None,
        limit: int = 50
    ) -> List[DataPrivacyRequest]:
        """List privacy requests with filters."""
        requests = list(self.privacy_requests.values())
        
        if tenant_id:
            requests = [r for r in requests if r.tenant_id == tenant_id]
        if user_id:
            requests = [r for r in requests if r.user_id == user_id]
        if status:
            requests = [r for r in requests if r.status == status]
        if request_type:
            requests = [r for r in requests if r.request_type == request_type]
        
        requests.sort(key=lambda r: r.requested_at, reverse=True)
        return requests[:limit]
    
    # Policy Rules
    def add_policy_rule(self, rule: PolicyRule):
        """Add a new policy rule."""
        self.policy_rules[rule.rule_id] = rule
        self.policy_rules = dict(
            sorted(self.policy_rules.items(), key=lambda x: x[1].priority, reverse=True)
        )
    
    def get_policy_rules(
        self,
        tenant_id: Optional[str] = None,
        regulation: Optional[PrivacyRegulation] = None,
        resource_type: Optional[str] = None,
        active_only: bool = True
    ) -> List[PolicyRule]:
        """Get policy rules with filters."""
        rules = list(self.policy_rules.values())
        
        if active_only:
            rules = [r for r in rules if r.is_active]
        if tenant_id:
            rules = [r for r in rules if r.tenant_id is None or r.tenant_id == tenant_id]
        if regulation:
            rules = [r for r in rules if r.regulation == regulation]
        if resource_type:
            rules = [
                r for r in rules
                if not r.resource_types or resource_type in r.resource_types
            ]
        
        return rules
    
    def evaluate_policy(
        self,
        context: Dict[str, Any]
    ) -> Tuple[bool, List[PolicyRule]]:
        """Evaluate policy rules against a context."""
        matched_rules = []
        allowed = True
        
        for rule in self.policy_rules.values():
            if not rule.is_active:
                continue
            
            if self._matches_rule_conditions(rule, context):
                matched_rules.append(rule)
                
                if rule.effect == PolicyEffect.DENY:
                    allowed = False
                elif rule.effect == PolicyEffect.REQUIRE:
                    allowed = False  # Requires additional action
        
        return allowed, matched_rules
    
    def _matches_rule_conditions(
        self,
        rule: PolicyRule,
        context: Dict[str, Any]
    ) -> bool:
        """Check if context matches rule conditions."""
        condition = rule.condition
        check_type = condition.get("check")
        
        if check_type == "contains_pii":
            return context.get("contains_pii", False) == condition.get("value", True)
        
        elif check_type == "export_size":
            return context.get("export_size", 0) >= condition.get("threshold", 0)
        
        elif check_type == "user_age":
            return context.get("user_age", 100) < condition.get("threshold", 18)
        
        elif check_type == "retention_expired":
            return context.get("retention_expired", False)
        
        elif check_type == "user_role":
            return context.get("user_role") in condition.get("roles", [])
        
        return False
    
    # Security Alerts
    def create_security_alert(
        self,
        alert_type: str,
        severity: SecuritySeverity,
        title: str,
        description: str,
        tenant_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> SecurityAlert:
        """Create a new security alert."""
        alert = SecurityAlert(
            alert_id=f"alert_{uuid4().hex[:12]}",
            alert_type=alert_type,
            severity=severity,
            title=title,
            description=description,
            tenant_id=tenant_id,
            metadata=metadata or {}
        )
        
        self.security_alerts[alert.alert_id] = alert
        if tenant_id:
            self.alerts_by_tenant[tenant_id].append(alert.alert_id)
        
        return alert
    
    def resolve_alert(
        self,
        alert_id: str,
        resolved_by: str,
        resolution: str
    ) -> Optional[SecurityAlert]:
        """Resolve a security alert."""
        alert = self.security_alerts.get(alert_id)
        if not alert:
            return None
        
        alert.status = "resolved"
        alert.resolved_at = datetime.now()
        alert.resolved_by = resolved_by
        alert.resolution = resolution
        
        # Audit log
        self.log_audit_event(
            actor_id=resolved_by,
            actor_type="user",
            action=AuditAction.UPDATE,
            resource_type="security_alert",
            description=f"Security alert resolved: {alert.title}",
            resource_id=alert_id,
            tenant_id=alert.tenant_id
        )
        
        return alert
    
    def list_security_alerts(
        self,
        tenant_id: Optional[str] = None,
        severity: Optional[SecuritySeverity] = None,
        status: Optional[str] = None,
        limit: int = 100
    ) -> List[SecurityAlert]:
        """List security alerts with filters."""
        alerts = list(self.security_alerts.values())
        
        if tenant_id:
            alerts = [a for a in alerts if a.tenant_id == tenant_id]
        if severity:
            alerts = [a for a in alerts if a.severity == severity]
        if status:
            alerts = [a for a in alerts if a.status == status]
        
        alerts.sort(key=lambda a: a.detected_at, reverse=True)
        return alerts[:limit]
    
    # Compliance Reports
    def generate_compliance_report(
        self,
        tenant_id: str,
        report_type: str,
        regulation: Optional[PrivacyRegulation],
        period_start: datetime,
        period_end: datetime,
        generated_by: Optional[str] = None
    ) -> ComplianceReport:
        """Generate a compliance report."""
        report_id = f"compliance_{uuid4().hex[:12]}"
        
        # Gather metrics
        audit_logs = self.query_audit_logs(
            tenant_id=tenant_id,
            start_date=period_start,
            end_date=period_end
        )
        
        privacy_requests = self.list_privacy_requests(
            tenant_id=tenant_id,
            status=PrivacyRequestStatus.COMPLETED
        )
        
        security_alerts = self.list_security_alerts(
            tenant_id=tenant_id,
            status="resolved"
        )
        
        report = ComplianceReport(
            report_id=report_id,
            report_type=report_type,
            tenant_id=tenant_id,
            regulation=regulation,
            period_start=period_start,
            period_end=period_end,
            summary={
                "total_actions": len(audit_logs),
                "privacy_requests_handled": len(privacy_requests),
                "security_incidents": len(security_alerts),
                "data_access_events": sum(1 for l in audit_logs if l.sensitive_data)
            },
            findings=[
                {
                    "type": "info",
                    "description": f"Audited {len(audit_logs)} actions",
                    "severity": "low"
                },
                {
                    "type": "privacy",
                    "description": f"Processed {len(privacy_requests)} privacy requests",
                    "severity": "info"
                }
            ],
            recommendations=[
                "Continue monitoring data access patterns",
                "Review privacy request response times",
                "Conduct regular security audits"
            ],
            metrics={
                "audit_log_count": len(audit_logs),
                "privacy_request_count": len(privacy_requests),
                "security_alert_count": len(security_alerts),
                "pii_access_count": sum(1 for l in audit_logs if l.sensitive_data)
            },
            generated_by=generated_by
        )
        
        self.compliance_reports[report_id] = report
        return report
    
    def get_compliance_report(self, report_id: str) -> Optional[ComplianceReport]:
        """Get a compliance report."""
        return self.compliance_reports.get(report_id)
    
    def list_compliance_reports(
        self,
        tenant_id: Optional[str] = None,
        regulation: Optional[PrivacyRegulation] = None,
        limit: int = 50
    ) -> List[ComplianceReport]:
        """List compliance reports."""
        reports = list(self.compliance_reports.values())
        
        if tenant_id:
            reports = [r for r in reports if r.tenant_id == tenant_id]
        if regulation:
            reports = [r for r in reports if r.regulation == regulation]
        
        reports.sort(key=lambda r: r.generated_at, reverse=True)
        return reports[:limit]
    
    # Retention Policies
    def get_retention_policies(
        self,
        tenant_id: Optional[str] = None,
        data_category: Optional[str] = None
    ) -> List[DataRetentionPolicy]:
        """Get data retention policies."""
        policies = list(self.retention_policies.values())
        
        if tenant_id:
            policies = [
                p for p in policies
                if p.tenant_id is None or p.tenant_id == tenant_id
            ]
        if data_category:
            policies = [p for p in policies if p.data_category == data_category]
        
        return policies
    
    def check_data_for_deletion(
        self,
        data_category: str,
        created_before: datetime
    ) -> List[str]:
        """Check data eligible for deletion based on retention policy."""
        policies = self.get_retention_policies(data_category=data_category)
        
        eligible_data = []
        for policy in policies:
            if policy.tenant_id:
                continue  # Skip tenant-specific policies
            
            cutoff_date = datetime.now() - timedelta(days=policy.retention_days)
            if created_before < cutoff_date:
                # In production, query actual data store
                eligible_data.append(f"data_category_{data_category}")
        
        return eligible_data
    
    # Dashboard & Reporting
    def get_compliance_dashboard(self, tenant_id: Optional[str] = None) -> Dict[str, Any]:
        """Get compliance dashboard data."""
        alerts = self.list_security_alerts(tenant_id=tenant_id, status="open")
        requests = self.list_privacy_requests(tenant_id=tenant_id)
        pending_requests = [r for r in requests if r.status in [
            PrivacyRequestStatus.PENDING,
            PrivacyRequestStatus.IN_REVIEW
        ]]
        
        return {
            "security_alerts": {
                "open": len(alerts),
                "critical": len([a for a in alerts if a.severity == SecuritySeverity.CRITICAL]),
                "high": len([a for a in alerts if a.severity == SecuritySeverity.HIGH])
            },
            "privacy_requests": {
                "pending": len(pending_requests),
                "completed_this_month": len([
                    r for r in requests
                    if r.completed_at and r.completed_at.month == datetime.now().month
                ])
            },
            "compliance_status": {
                "gdpr": "compliant",
                "ccpa": "compliant",
                "ferpa": "review_needed"
            },
            "recent_alerts": [
                {
                    "id": a.alert_id,
                    "title": a.title,
                    "severity": a.severity.value
                }
                for a in alerts[:5]
            ]
        }


# Service factory function
def create_compliance_service() -> ComplianceService:
    """Create and configure a new compliance service instance."""
    return ComplianceService()
