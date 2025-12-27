"""
VisualVerse Creator Platform - Shared Type Definitions

This module provides TypeScript interfaces and data types shared across
the VisualVerse platform including content models, user management,
licensing, and version control.

Author: MiniMax Agent
Version: 1.0.0
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Union
from enum import Enum
from datetime import datetime
from pathlib import Path


class UserRole(str, Enum):
    """User roles in the creator platform."""
    CREATOR = "creator"
    EDUCATOR = "educator"
    STUDENT = "student"
    ADMIN = "admin"
    INSTITUTION_ADMIN = "institution_admin"


class ContentDomain(str, Enum):
    """Content domains supported by VisualVerse."""
    MATH = "math"
    ALGORITHMS = "algorithms"
    PHYSICS = "physics"
    CHEMISTRY = "chemistry"
    FINANCE = "finance"


class ContentStatus(str, Enum):
    """Status of content in the platform."""
    DRAFT = "draft"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class LicenseType(str, Enum):
    """Types of content licenses."""
    FREE = "free"
    PERSONAL = "personal"
    COMMERCIAL = "commercial"
    INSTITUTIONAL = "institutional"
    SUBSCRIPTION = "subscription"


class SubscriptionTier(str, Enum):
    """Subscription tiers for creators and consumers."""
    FREE = "free"
    CREATOR = "creator"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"


class VisibilityLevel(str, Enum):
    """Content visibility levels."""
    PRIVATE = "private"
    COLLABORATORS = "collaborators"
    SUBSCRIBERS = "subscribers"
    PUBLIC = "public"
    MARKETPLACE = "marketplace"


@dataclass
class User:
    """User model for the platform."""
    id: str
    email: str
    name: str
    role: UserRole
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    subscription_tier: SubscriptionTier = SubscriptionTier.FREE
    stripe_customer_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "role": self.role.value,
            "avatarUrl": self.avatar_url,
            "bio": self.bio,
            "subscriptionTier": self.subscription_tier.value,
            "stripeCustomerId": self.stripe_customer_id,
            "createdAt": self.created_at.isoformat(),
            "updatedAt": self.updated_at.isoformat()
        }


@dataclass
class ContentMetadata:
    """Metadata for content items."""
    id: str
    title: str
    description: str
    domain: ContentDomain
    status: ContentStatus
    author_id: str
    version: int = 1
    tags: List[str] = field(default_factory=list)
    syllabus_tags: List[str] = field(default_factory=list)
    difficulty_level: str = "beginner"
    estimated_minutes: int = 15
    language: str = "en"
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    published_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "domain": self.domain.value,
            "status": self.status.value,
            "authorId": self.author_id,
            "version": self.version,
            "tags": self.tags,
            "syllabusTags": self.syllabus_tags,
            "difficultyLevel": self.difficulty_level,
            "estimatedMinutes": self.estimated_minutes,
            "language": self.language,
            "createdAt": self.created_at.isoformat(),
            "updatedAt": self.updated_at.isoformat(),
            "publishedAt": self.published_at.isoformat() if self.published_at else None
        }


@dataclass
class Project:
    """Content project model."""
    id: str
    owner_id: str
    title: str
    domain: ContentDomain
    current_head: str
    collaborators: List[str] = field(default_factory=list)
    visibility: VisibilityLevel = VisibilityLevel.PRIVATE
    is_template: bool = False
    parent_project_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "ownerId": self.owner_id,
            "title": self.title,
            "domain": self.domain.value,
            "currentHead": self.current_head,
            "collaborators": self.collaborators,
            "visibility": self.visibility.value,
            "isTemplate": self.is_template,
            "parentProjectId": self.parent_project_id,
            "createdAt": self.created_at.isoformat(),
            "updatedAt": self.updated_at.isoformat()
        }


@dataclass
class Commit:
    """Version commit model."""
    id: str
    project_id: str
    hash: str
    parent_hash: Optional[str]
    author_id: str
    message: str
    script_content: str
    compiled_config: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "projectId": self.project_id,
            "hash": self.hash,
            "parentHash": self.parent_hash,
            "authorId": self.author_id,
            "message": self.message,
            "scriptContent": self.script_content,
            "compiledConfig": self.compiled_config,
            "timestamp": self.timestamp.isoformat()
        }


@dataclass
class Branch:
    """Branch model for version control."""
    id: str
    project_id: str
    name: str
    head_commit: str
    author_id: str
    is_default: bool = False
    created_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "projectId": self.project_id,
            "name": self.name,
            "headCommit": self.head_commit,
            "authorId": self.author_id,
            "isDefault": self.is_default,
            "createdAt": self.created_at.isoformat()
        }


@dataclass
class SyllabusTag:
    """Syllabus tag for curriculum alignment."""
    id: str
    board_id: str
    grade_level: int
    subject: str
    topic: str
    sub_topic: Optional[str]
    standard_code: Optional[str]
    description: Optional[str]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "boardId": self.board_id,
            "gradeLevel": self.grade_level,
            "subject": self.subject,
            "topic": self.topic,
            "subTopic": self.sub_topic,
            "standardCode": self.standard_code,
            "description": self.description
        }


@dataclass
class CurriculumBoard:
    """Curriculum board (CBSE, ICSE, IB, etc.)."""
    id: str
    name: str
    country: str
    description: Optional[str]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "country": self.country,
            "description": self.description
        }


@dataclass
class Product:
    """Marketplace product."""
    id: str
    project_id: str
    seller_id: str
    price: float
    currency: str = "USD"
    license_type: LicenseType = LicenseType.PERSONAL
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "projectId": self.project_id,
            "sellerId": self.seller_id,
            "price": self.price,
            "currency": self.currency,
            "licenseType": self.license_type.value,
            "isActive": self.is_active,
            "createdAt": self.created_at.isoformat()
        }


@dataclass
class Transaction:
    """Transaction record for monetization."""
    id: str
    buyer_id: str
    seller_id: str
    product_id: str
    amount: float
    platform_fee: float
    net_amount: float
    currency: str = "USD"
    status: str = "completed"
    stripe_payment_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "buyerId": self.buyer_id,
            "sellerId": self.seller_id,
            "productId": self.product_id,
            "amount": self.amount,
            "platformFee": self.platform_fee,
            "netAmount": self.net_amount,
            "currency": self.currency,
            "status": self.status,
            "stripePaymentId": self.stripe_payment_id,
            "createdAt": self.created_at.isoformat()
        }


@dataclass
class License:
    """Content license record."""
    id: str
    user_id: str
    product_id: str
    license_type: LicenseType
    starts_at: datetime = field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None
    is_active: bool = True
    usage_count: int = 0
    max_uses: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "userId": self.user_id,
            "productId": self.product_id,
            "licenseType": self.license_type.value,
            "startsAt": self.starts_at.isoformat(),
            "expiresAt": self.expires_at.isoformat() if self.expires_at else None,
            "isActive": self.is_active,
            "usageCount": self.usage_count,
            "maxUses": self.max_uses
        }
    
    def is_valid(self) -> bool:
        """Check if license is currently valid."""
        now = datetime.utcnow()
        if not self.is_active:
            return False
        if self.expires_at and now > self.expires_at:
            return False
        if self.max_uses and self.usage_count >= self.max_uses:
            return False
        return True


@dataclass
class CreatorStats:
    """Creator statistics and analytics."""
    user_id: str
    total_projects: int = 0
    total_revenue: float = 0.0
    total_sales: int = 0
    total_views: int = 0
    average_rating: float = 0.0
    total_followers: int = 0
    period_start: Optional[datetime] = None
    period_end: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "userId": self.user_id,
            "totalProjects": self.total_projects,
            "totalRevenue": self.total_revenue,
            "totalSales": self.total_sales,
            "totalViews": self.total_views,
            "averageRating": self.average_rating,
            "totalFollowers": self.total_followers,
            "periodStart": self.period_start.isoformat() if self.period_start else None,
            "periodEnd": self.period_end.isoformat() if self.period_end else None
        }


__all__ = [
    "UserRole",
    "ContentDomain",
    "ContentStatus",
    "LicenseType",
    "SubscriptionTier",
    "VisibilityLevel",
    "User",
    "ContentMetadata",
    "Project",
    "Commit",
    "Branch",
    "SyllabusTag",
    "CurriculumBoard",
    "Product",
    "Transaction",
    "License",
    "CreatorStats"
]
