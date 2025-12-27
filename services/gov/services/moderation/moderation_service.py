"""
Content Moderation Service for Governance Platform.

Provides comprehensive content moderation, quality assessment,
review workflow management, and audit logging for the VisualVerse platform.
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
from uuid import uuid4
from collections import defaultdict
import json


class ModerationStatus(Enum):
    """Status of content moderation."""
    PENDING = "pending"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    FLAGGED = "flagged"
    ESCALATED = "escalated"
    AUTO_APPROVED = "auto_approved"
    UNDER_REVISION = "under_revision"


class ModerationPriority(Enum):
    """Priority levels for moderation queue."""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4
    CRITICAL = 5


class FlagReason(Enum):
    """Reasons for flagging content."""
    INAPPROPRIATE = "inappropriate"
    SPAM = "spam"
    COPYRIGHT = "copyright"
    MISINFORMATION = "misinformation"
    HARASSMENT = "harassment"
    VIOLENCE = "violence"
    HATE_SPEECH = "hate_speech"
    ADULT = "adult"
    PLAGIARISM = "plagiarism"
    INCORRECT = "incorrect"
    LOW_QUALITY = "low_quality"
    OTHER = "other"


class QualityDimension(Enum):
    """Dimensions for quality assessment."""
    ACCURACY = "accuracy"
    COMPLETENESS = "completeness"
    CLARITY = "clarity"
    ENGAGEMENT = "engagement"
    ACCESSIBILITY = "accessibility"
    INTERACTIVITY = "interactivity"
    PEDAGOGY = "pedagogy"
    TECHNICAL = "technical"


class ReviewAction(Enum):
    """Actions a moderator can take."""
    APPROVE = "approve"
    REJECT = "reject"
    REQUEST_CHANGES = "request_changes"
    ESCALATE = "escalate"
    FLAG = "flag"
    DEFER = "defer"
    BAN_CONTENT = "ban_content"
    BAN_USER = "ban_user"


@dataclass
class ContentFlag:
    """A flag raised on content."""
    flag_id: str
    content_id: str
    content_type: str
    reason: FlagReason
    description: str
    reporter_id: Optional[str]  # None if automated
    reporter_type: str  # "user", "automated", "system"
    severity: ModerationPriority = ModerationPriority.MEDIUM
    automated_score: Optional[float] = None
    created_at: datetime = field(default_factory=datetime.now)
    resolved: bool = False
    resolution: Optional[str] = None
    resolved_at: Optional[datetime] = None
    resolved_by: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "flag_id": self.flag_id,
            "content_id": self.content_id,
            "content_type": self.content_type,
            "reason": self.reason.value,
            "description": self.description,
            "reporter_id": self.reporter_id,
            "reporter_type": self.reporter_type,
            "severity": self.severity.value,
            "automated_score": self.automated_score,
            "created_at": self.created_at.isoformat(),
            "resolved": self.resolved,
            "resolution": self.resolution,
            "resolved_at": self.resolved_at.isoformat() if self.resolved_at else None,
            "resolved_by": self.resolved_by
        }


@dataclass
class QualityScore:
    """Quality score for content."""
    content_id: str
    overall_score: float  # 0-100
    dimension_scores: Dict[QualityDimension, float] = field(default_factory=dict)
    automated_score: float = 0.0
    manual_score: Optional[float] = None
    reviewer_id: Optional[str] = None
    reviewed_at: Optional[datetime] = None
    confidence: float = 0.0
    recommendations: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "content_id": self.content_id,
            "overall_score": self.overall_score,
            "dimension_scores": {k.value: v for k, v in self.dimension_scores.items()},
            "automated_score": self.automated_score,
            "manual_score": self.manual_score,
            "reviewer_id": self.reviewer_id,
            "reviewed_at": self.reviewed_at.isoformat() if self.reviewed_at else None,
            "confidence": self.confidence,
            "recommendations": self.recommendations
        }
    
    @property
    def is_quality_approved(self) -> bool:
        """Check if content meets quality threshold."""
        return self.overall_score >= 70.0


@dataclass
class ModerationAction:
    """Action taken by a moderator."""
    action_id: str
    ticket_id: str
    moderator_id: str
    action: ReviewAction
    reason: Optional[str] = None
    notes: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "action_id": self.action_id,
            "ticket_id": self.ticket_id,
            "moderator_id": self.moderator_id,
            "action": self.action.value,
            "reason": self.reason,
            "notes": self.notes,
            "created_at": self.created_at.isoformat()
        }


@dataclass
class ModerationTicket:
    """A moderation ticket for review."""
    ticket_id: str
    content_id: str
    content_type: str
    tenant_id: str
    status: ModerationStatus = ModerationStatus.PENDING
    priority: ModerationPriority = ModerationPriority.MEDIUM
    title: str = ""
    description: str = ""
    flags: List[str] = field(default_factory=list)  # flag_ids
    quality_score: Optional[QualityScore] = None
    assigned_moderator: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    due_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    resolution: Optional[str] = None
    actions: List[str] = field(default_factory=list)  # action_ids
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "ticket_id": self.ticket_id,
            "content_id": self.content_id,
            "content_type": self.content_type,
            "tenant_id": self.tenant_id,
            "status": self.status.value,
            "priority": self.priority.value,
            "title": self.title,
            "description": self.description,
            "flags": self.flags,
            "quality_score": self.quality_score.to_dict() if self.quality_score else None,
            "assigned_moderator": self.assigned_moderator,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "resolution": self.resolution,
            "actions": self.actions,
            "metadata": self.metadata
        }


@dataclass
class ModerationQueue:
    """A moderation queue with tickets."""
    queue_id: str
    name: str
    description: str
    tenant_id: Optional[str]  # None for global queue
    filters: Dict[str, Any] = field(default_factory=dict)
    ticket_ids: List[str] = field(default_factory=list)
    priority_order: List[ModerationPriority] = field(
        default_factory=lambda: [
            ModerationPriority.CRITICAL,
            ModerationPriority.URGENT,
            ModerationPriority.HIGH,
            ModerationPriority.MEDIUM,
            ModerationPriority.LOW
        ]
    )
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "queue_id": self.queue_id,
            "name": self.name,
            "description": self.description,
            "tenant_id": self.tenant_id,
            "filters": self.filters,
            "ticket_count": len(self.ticket_ids),
            "priority_order": [p.value for p in self.priority_order],
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


@dataclass
class ModerationRule:
    """Automated moderation rule."""
    rule_id: str
    name: str
    description: str
    condition: Dict[str, Any]
    action: str  # "flag", "auto_approve", "auto_reject", "escalate"
    is_active: bool = True
    priority: int = 0
    applies_to: List[str] = field(default_factory=list)  # content types
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "name": self.name,
            "description": self.description,
            "condition": self.condition,
            "action": self.action,
            "is_active": self.is_active,
            "priority": self.priority,
            "applies_to": self.applies_to,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


class ModerationService:
    """
    Content moderation service for the governance platform.
    
    Manages the complete moderation lifecycle including automated
    quality assessment, flagging, queue management, and audit logging.
    """
    
    def __init__(self):
        # Data stores
        self.tickets: Dict[str, ModerationTicket] = {}
        self.flags: Dict[str, ContentFlag] = {}
        self.actions: Dict[str, ModerationAction] = {}
        self.queues: Dict[str, ModerationQueue] = {}
        self.quality_scores: Dict[str, QualityScore] = {}
        self.rules: Dict[str, ModerationRule] = {}
        self.audit_logs: List[Dict[str, Any]] = []
        
        # Indexes
        self.content_tickets: Dict[str, List[str]] = defaultdict(list)
        self.tenant_queues: Dict[str, List[str]] = defaultdict(list)
        self.moderator_assignments: Dict[str, List[str]] = defaultdict(list)
        
        # Initialize default queues
        self._init_default_queues()
        
        # Initialize default rules
        self._init_default_rules()
    
    def _init_default_queues(self):
        """Initialize default moderation queues."""
        default_queues = [
            ModerationQueue(
                queue_id="queue_pending",
                name="Pending Review",
                description="Content awaiting moderation",
                tenant_id=None,
                filters={"status": "pending"}
            ),
            ModerationQueue(
                queue_id="queue_flagged",
                name="Flagged Content",
                description="Content with flags requiring attention",
                tenant_id=None,
                filters={"status": "flagged"}
            ),
            ModerationQueue(
                queue_id="queue_high_priority",
                name="High Priority",
                description="Urgent and critical content",
                tenant_id=None,
                filters={"priority": ["critical", "urgent", "high"]}
            ),
            ModerationQueue(
                queue_id="queue_education",
                name="Educational Content",
                description="K-12 educational content (higher scrutiny)",
                tenant_id=None,
                filters={"content_type": "education", "target_audience": "k12"}
            )
        ]
        
        for queue in default_queues:
            self.queues[queue.queue_id] = queue
    
    def _init_default_rules(self):
        """Initialize default moderation rules."""
        default_rules = [
            ModerationRule(
                rule_id="rule_profanity",
                name="Profanity Filter",
                description="Auto-flag content with potential profanity",
                condition={"check": "keyword_match", "list": "profanity"},
                action="flag",
                priority=10,
                applies_to=["text", "audio"]
            ),
            ModerationRule(
                rule_id="rule_low_quality",
                name="Low Quality Detection",
                description="Auto-flag content with low quality scores",
                condition={"check": "quality_threshold", "threshold": 40},
                action="flag",
                priority=5,
                applies_to=["all"]
            ),
            ModerationRule(
                rule_id="rule_copyright",
                name="Copyright Check",
                description="Check for potential copyright issues",
                condition={"check": "copyright_match"},
                action="escalate",
                priority=15,
                applies_to=["video", "audio", "image"]
            ),
            ModerationRule(
                rule_id="rule_auto_approve",
                name="Trusted Creator Auto-Approve",
                description="Auto-approve content from trusted creators",
                condition={"check": "trusted_creator"},
                action="auto_approve",
                priority=20,
                applies_to=["all"]
            )
        ]
        
        for rule in default_rules:
            self.rules[rule.rule_id] = rule
    
    # Ticket Management
    def create_ticket(
        self,
        content_id: str,
        content_type: str,
        tenant_id: str,
        title: str = "",
        description: str = "",
        priority: ModerationPriority = ModerationPriority.MEDIUM,
        metadata: Optional[Dict[str, Any]] = None,
        automated_score: Optional[float] = None
    ) -> ModerationTicket:
        """Create a new moderation ticket."""
        ticket_id = f"ticket_{uuid4().hex[:12]}"
        
        ticket = ModerationTicket(
            ticket_id=ticket_id,
            content_id=content_id,
            content_type=content_type,
            tenant_id=tenant_id,
            title=title or f"Moderation review: {content_id}",
            description=description,
            priority=priority,
            metadata=metadata or {}
        )
        
        # Set due date based on priority
        ticket.due_date = self._calculate_due_date(priority)
        
        # Create initial quality score if automated score provided
        if automated_score is not None:
            ticket.quality_score = QualityScore(
                content_id=content_id,
                overall_score=automated_score,
                automated_score=automated_score
            )
        
        self.tickets[ticket_id] = ticket
        self.content_tickets[content_id].append(ticket_id)
        
        # Add to appropriate queue
        self._add_to_queue(ticket)
        
        # Audit log
        self._audit_log(
            action="ticket_created",
            ticket_id=ticket_id,
            content_id=content_id,
            tenant_id=tenant_id
        )
        
        return ticket
    
    def get_ticket(self, ticket_id: str) -> Optional[ModerationTicket]:
        """Get a moderation ticket by ID."""
        return self.tickets.get(ticket_id)
    
    def get_tickets_for_content(
        self,
        content_id: str
    ) -> List[ModerationTicket]:
        """Get all tickets for a content item."""
        ticket_ids = self.content_tickets.get(content_id, [])
        return [
            self.tickets[tid] for tid in ticket_ids
            if tid in self.tickets
        ]
    
    def update_ticket_status(
        self,
        ticket_id: str,
        status: ModerationStatus,
        moderator_id: Optional[str] = None
    ) -> Optional[ModerationTicket]:
        """Update ticket status."""
        ticket = self.tickets.get(ticket_id)
        if not ticket:
            return None
        
        old_status = ticket.status
        ticket.status = status
        ticket.updated_at = datetime.now()
        
        if status in [ModerationStatus.APPROVED, ModerationStatus.REJECTED]:
            ticket.completed_at = datetime.now()
        
        # Audit log
        self._audit_log(
            action="status_changed",
            ticket_id=ticket_id,
            old_status=old_status.value,
            new_status=status.value,
            moderator_id=moderator_id
        )
        
        return ticket
    
    def assign_moderator(
        self,
        ticket_id: str,
        moderator_id: str
    ) -> Optional[ModerationTicket]:
        """Assign a moderator to a ticket."""
        ticket = self.tickets.get(ticket_id)
        if not ticket:
            return None
        
        ticket.assigned_moderator = moderator_id
        ticket.status = ModerationStatus.IN_REVIEW
        ticket.updated_at = datetime.now()
        
        self.moderator_assignments[moderator_id].append(ticket_id)
        
        self._audit_log(
            action="moderator_assigned",
            ticket_id=ticket_id,
            moderator_id=moderator_id
        )
        
        return ticket
    
    def list_tickets(
        self,
        tenant_id: Optional[str] = None,
        status: Optional[ModerationStatus] = None,
        priority: Optional[ModerationPriority] = None,
        assigned_moderator: Optional[str] = None,
        limit: int = 100
    ) -> List[ModerationTicket]:
        """List tickets with filters."""
        tickets = list(self.tickets.values())
        
        if tenant_id:
            tickets = [t for t in tickets if t.tenant_id == tenant_id]
        if status:
            tickets = [t for t in tickets if t.status == status]
        if priority:
            tickets = [t for t in tickets if t.priority == priority]
        if assigned_moderator:
            tickets = [t for t in tickets if t.assigned_moderator == assigned_moderator]
        
        # Sort by priority (descending) and creation date
        tickets.sort(
            key=lambda t: (t.priority.value, -t.created_at.timestamp()),
            reverse=True
        )
        
        return tickets[:limit]
    
    # Flag Management
    def create_flag(
        self,
        content_id: str,
        content_type: str,
        reason: FlagReason,
        description: str,
        reporter_id: Optional[str] = None,
        reporter_type: str = "user",
        severity: ModerationPriority = ModerationPriority.MEDIUM,
        automated_score: Optional[float] = None
    ) -> ContentFlag:
        """Create a flag on content."""
        flag_id = f"flag_{uuid4().hex[:12]}"
        
        flag = ContentFlag(
            flag_id=flag_id,
            content_id=content_id,
            content_type=content_type,
            reason=reason,
            description=description,
            reporter_id=reporter_id,
            reporter_type=reporter_type,
            severity=severity,
            automated_score=automated_score
        )
        
        self.flags[flag_id] = flag
        
        # Create ticket if severe enough
        if severity in [ModerationPriority.HIGH, ModerationPriority.URGENT, ModerationPriority.CRITICAL]:
            self.create_ticket(
                content_id=content_id,
                content_type=content_type,
                tenant_id="",  # Would be determined from content
                title=f"Flagged content: {reason.value}",
                description=description,
                priority=ModerationPriority(severity.value + 1) if severity.value < 4 else ModerationPriority.CRITICAL,
                automated_score=automated_score
            )
        
        self._audit_log(
            action="flag_created",
            flag_id=flag_id,
            content_id=content_id,
            reason=reason.value,
            reporter_id=reporter_id
        )
        
        return flag
    
    def resolve_flag(
        self,
        flag_id: str,
        resolution: str,
        resolved_by: str
    ) -> Optional[ContentFlag]:
        """Resolve a flag."""
        flag = self.flags.get(flag_id)
        if not flag:
            return None
        
        flag.resolved = True
        flag.resolution = resolution
        flag.resolved_at = datetime.now()
        flag.resolved_by = resolved_by
        
        self._audit_log(
            action="flag_resolved",
            flag_id=flag_id,
            resolution=resolution,
            resolved_by=resolved_by
        )
        
        return flag
    
    def get_flags_for_content(
        self,
        content_id: str,
        resolved_only: bool = False
    ) -> List[ContentFlag]:
        """Get all flags for content."""
        flags = [f for f in self.flags.values() if f.content_id == content_id]
        
        if resolved_only:
            flags = [f for f in flags if f.resolved]
        
        return flags
    
    # Quality Assessment
    def calculate_quality_score(
        self,
        content_id: str,
        dimension_scores: Dict[QualityDimension, float],
        reviewer_id: Optional[str] = None
    ) -> QualityScore:
        """Calculate overall quality score from dimension scores."""
        if not dimension_scores:
            return QualityScore(
                content_id=content_id,
                overall_score=0.0,
                dimension_scores={},
                confidence=0.0
            )
        
        # Calculate weighted average
        weights = {
            QualityDimension.ACCURACY: 0.25,
            QualityDimension.COMPLETENESS: 0.15,
            QualityDimension.CLARITY: 0.20,
            QualityDimension.ENGAGEMENT: 0.15,
            QualityDimension.PEDAGOGY: 0.25
        }
        
        total_weight = 0.0
        weighted_sum = 0.0
        
        for dimension, score in dimension_scores.items():
            weight = weights.get(dimension, 0.1)
            weighted_sum += score * weight
            total_weight += weight
        
        overall_score = weighted_sum / total_weight if total_weight > 0 else 0.0
        
        # Generate recommendations
        recommendations = []
        for dimension, score in dimension_scores.items():
            if score < 60:
                recommendations.append(f"Improve {dimension.value}: Score is {score:.1f}")
        
        quality_score = QualityScore(
            content_id=content_id,
            overall_score=overall_score,
            dimension_scores=dimension_scores,
            automated_score=overall_score,
            manual_score=overall_score,
            reviewer_id=reviewer_id,
            reviewed_at=datetime.now(),
            confidence=0.85,
            recommendations=recommendations
        )
        
        self.quality_scores[content_id] = quality_score
        
        # Update any existing tickets
        for ticket_id in self.content_tickets.get(content_id, []):
            ticket = self.tickets.get(ticket_id)
            if ticket:
                ticket.quality_score = quality_score
        
        return quality_score
    
    def get_quality_score(self, content_id: str) -> Optional[QualityScore]:
        """Get quality score for content."""
        return self.quality_scores.get(content_id)
    
    # Moderation Actions
    def take_action(
        self,
        ticket_id: str,
        moderator_id: str,
        action: ReviewAction,
        reason: Optional[str] = None,
        notes: str = ""
    ) -> Tuple[Optional[ModerationAction], Optional[ModerationTicket]]:
        """Perform a moderation action."""
        ticket = self.tickets.get(ticket_id)
        if not ticket:
            return None, None
        
        action_record = ModerationAction(
            action_id=f"action_{uuid4().hex[:12]}",
            ticket_id=ticket_id,
            moderator_id=moderator_id,
            action=action,
            reason=reason,
            notes=notes
        )
        
        self.actions[action_record.action_id] = action_record
        ticket.actions.append(action_record.action_id)
        
        # Update ticket based on action
        if action == ReviewAction.APPROVE:
            ticket.status = ModerationStatus.APPROVED
            ticket.resolution = f"Approved by moderator"
            ticket.completed_at = datetime.now()
        
        elif action == ReviewAction.REJECT:
            ticket.status = ModerationStatus.REJECTED
            ticket.resolution = f"Rejected: {reason}"
            ticket.completed_at = datetime.now()
        
        elif action == ReviewAction.REQUEST_CHANGES:
            ticket.status = ModerationStatus.UNDER_REVISION
            ticket.resolution = "Changes requested"
        
        elif action == ReviewAction.ESCALATE:
            ticket.status = ModerationStatus.ESCALATED
            ticket.priority = ModerationPriority(max(ticket.priority.value + 1, 5))
        
        elif action == ReviewAction.FLAG:
            if reason:
                self.create_flag(
                    content_id=ticket.content_id,
                    content_type=ticket.content_type,
                    reason=FlagReason(reason) if reason in [e.value for e in FlagReason] else FlagReason.OTHER,
                    description=notes or reason or "Flagged by moderator",
                    reporter_id=moderator_id,
                    reporter_type="moderator",
                    severity=ModerationPriority.HIGH
                )
        
        ticket.updated_at = datetime.now()
        
        self._audit_log(
            action="moderation_action",
            ticket_id=ticket_id,
            action=action.value,
            moderator_id=moderator_id,
            notes=notes
        )
        
        return action_record, ticket
    
    # Queue Management
    def get_queue(
        self,
        queue_id: str
    ) -> Optional[ModerationQueue]:
        """Get a moderation queue."""
        return self.queues.get(queue_id)
    
    def get_queue_tickets(
        self,
        queue_id: str,
        limit: int = 50
    ) -> List[ModerationTicket]:
        """Get tickets in a queue."""
        queue = self.queues.get(queue_id)
        if not queue:
            return []
        
        tickets = [
            self.tickets[tid] for tid in queue.ticket_ids
            if tid in self.tickets
        ]
        
        # Sort by priority order
        priority_order = {p: i for i, p in enumerate(queue.priority_order)}
        tickets.sort(key=lambda t: priority_order.get(t.priority, 99))
        
        return tickets[:limit]
    
    def _add_to_queue(self, ticket: ModerationTicket):
        """Add ticket to appropriate queue."""
        for queue in self.queues.values():
            if self._ticket_matches_queue(ticket, queue):
                queue.ticket_ids.append(ticket.ticket_id)
                queue.updated_at = datetime.now()
                break
    
    def _ticket_matches_queue(
        self,
        ticket: ModerationTicket,
        queue: ModerationQueue
    ) -> bool:
        """Check if ticket matches queue filters."""
        filters = queue.filters
        
        if "status" in filters:
            if ticket.status.value != filters["status"]:
                return False
        
        if "priority" in filters:
            if ticket.priority.value not in [ModerationPriority(p).value for p in filters["priority"]]:
                return False
        
        if "content_type" in filters:
            if ticket.content_type != filters["content_type"]:
                return False
        
        return True
    
    def _calculate_due_date(
        self,
        priority: ModerationPriority
    ) -> datetime:
        """Calculate due date based on priority."""
        hours = {
            ModerationPriority.LOW: 168,      # 7 days
            ModerationPriority.MEDIUM: 72,     # 3 days
            ModerationPriority.HIGH: 24,       # 1 day
            ModerationPriority.URGENT: 4,      # 4 hours
            ModerationPriority.CRITICAL: 1     # 1 hour
        }
        
        return datetime.now() + timedelta(hours=hours.get(priority, 72))
    
    # Rules Engine
    def apply_automated_rules(
        self,
        content_id: str,
        content_type: str,
        content_data: Dict[str, Any]
    ) -> List[str]:
        """Apply automated moderation rules to content."""
        applied = []
        
        for rule in self.rules.values():
            if not rule.is_active:
                continue
            
            if content_type not in rule.applies_to and "all" not in rule.applies_to:
                continue
            
            if self._check_rule_condition(rule.condition, content_data):
                applied.append(rule.rule_id)
                
                if rule.action == "flag":
                    self.create_flag(
                        content_id=content_id,
                        content_type=content_type,
                        reason=FlagReason.OTHER,
                        description=f"Auto-flagged by rule: {rule.name}",
                        reporter_type="automated",
                        severity=ModerationPriority.MEDIUM,
                        automated_score=content_data.get("quality_score", 0)
                    )
                elif rule.action == "auto_approve":
                    self.create_ticket(
                        content_id=content_id,
                        content_type=content_type,
                        tenant_id=content_data.get("tenant_id", ""),
                        priority=ModerationPriority.LOW,
                        automated_score=content_data.get("quality_score", 0)
                    )
                    ticket = self.get_tickets_for_content(content_id)[-1] if self.get_tickets_for_content(content_id) else None
                    if ticket:
                        ticket.status = ModerationStatus.AUTO_APPROVED
                        ticket.resolution = f"Auto-approved by rule: {rule.name}"
        
        return applied
    
    def _check_rule_condition(
        self,
        condition: Dict[str, Any],
        content_data: Dict[str, Any]
    ) -> bool:
        """Check if rule condition is met."""
        check_type = condition.get("check")
        
        if check_type == "quality_threshold":
            threshold = condition.get("threshold", 0)
            score = content_data.get("quality_score", 100)
            return score < threshold
        
        elif check_type == "keyword_match":
            # Simplified keyword matching
            text = content_data.get("text", "").lower()
            keywords = condition.get("list", [])
            return any(kw.lower() in text for kw in keywords)
        
        elif check_type == "trusted_creator":
            return content_data.get("is_trusted", False)
        
        elif check_type == "copyright_match":
            return content_data.get("copyright_risk", False)
        
        return False
    
    def add_rule(self, rule: ModerationRule):
        """Add a new moderation rule."""
        self.rules[rule.rule_id] = rule
        # Sort rules by priority
        self.rules = dict(sorted(self.rules.items(), key=lambda x: x[1].priority, reverse=True))
    
    # Audit Logging
    def _audit_log(
        self,
        action: str,
        **kwargs
    ):
        """Create an audit log entry."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            **kwargs
        }
        self.audit_logs.append(entry)
    
    def get_audit_logs(
        self,
        ticket_id: Optional[str] = None,
        moderator_id: Optional[str] = None,
        action: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 500
    ) -> List[Dict[str, Any]]:
        """Get audit logs with filters."""
        logs = self.audit_logs
        
        if ticket_id:
            logs = [l for l in logs if l.get("ticket_id") == ticket_id]
        if moderator_id:
            logs = [l for l in logs if l.get("moderator_id") == moderator_id]
        if action:
            logs = [l for l in logs if l.get("action") == action]
        if start_date:
            logs = [l for l in logs if datetime.fromisoformat(l["timestamp"]) >= start_date]
        if end_date:
            logs = [l for l in logs if datetime.fromisoformat(l["timestamp"]) <= end_date]
        
        return logs[-limit:]
    
    # Analytics
    def get_moderation_stats(
        self,
        tenant_id: Optional[str] = None,
        days: int = 30
    ) -> Dict[str, Any]:
        """Get moderation statistics."""
        start_date = datetime.now() - timedelta(days=days)
        
        tickets = [
            t for t in self.tickets.values()
            if t.created_at >= start_date and (not tenant_id or t.tenant_id == tenant_id)
        ]
        
        flags = [
            f for f in self.flags.values()
            if f.created_at >= start_date
        ]
        
        # Calculate stats
        status_counts: Dict[str, int] = defaultdict(int)
        priority_counts: Dict[str, int] = defaultdict(int)
        reason_counts: Dict[str, int] = defaultdict(int)
        
        for ticket in tickets:
            status_counts[ticket.status.value] += 1
            priority_counts[ticket.priority.value] += 1
        
        for flag in flags:
            reason_counts[flag.reason.value] += 1
        
        # Calculate averages
        avg_resolution_time = 0.0
        resolved = [t for t in tickets if t.completed_at]
        if resolved:
            total_time = sum(
                (t.completed_at - t.created_at).total_seconds()
                for t in resolved
            )
            avg_resolution_time = total_time / len(resolved) / 3600  # hours
        
        return {
            "period_days": days,
            "total_tickets": len(tickets),
            "total_flags": len(flags),
            "by_status": dict(status_counts),
            "by_priority": dict(priority_counts),
            "flag_reasons": dict(reason_counts),
            "avg_resolution_hours": round(avg_resolution_time, 2),
            "pending_count": status_counts.get("pending", 0) + status_counts.get("in_review", 0),
            "resolved_count": status_counts.get("approved", 0) + status_counts.get("rejected", 0)
        }
    
    def get_moderator_stats(
        self,
        moderator_id: str,
        days: int = 30
    ) -> Dict[str, Any]:
        """Get statistics for a specific moderator."""
        start_date = datetime.now() - timedelta(days=days)
        
        actions = [
            a for a in self.actions.values()
            if a.moderator_id == moderator_id and a.created_at >= start_date
        ]
        
        action_counts: Dict[str, int] = defaultdict(int)
        for action in actions:
            action_counts[action.action.value] += 1
        
        tickets = [
            t for t in self.tickets.values()
            if t.assigned_moderator == moderator_id and t.created_at >= start_date
        ]
        
        return {
            "moderator_id": moderator_id,
            "period_days": days,
            "total_actions": len(actions),
            "actions_by_type": dict(action_counts),
            "tickets_assigned": len(tickets),
            "tickets_completed": sum(1 for t in tickets if t.completed_at)
        }


# Service factory function
def create_moderation_service() -> ModerationService:
    """Create and configure a new moderation service instance."""
    return ModerationService()
