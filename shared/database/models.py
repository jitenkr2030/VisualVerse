"""
Database Models for VisualVerse
SQLAlchemy ORM models for all platform entities.
"""

from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Text, DateTime, ForeignKey, 
    Boolean, Float, JSON, Enum as SQLEnum
)
from sqlalchemy.orm import relationship
import enum

from shared.database import Base


class ContentType(enum.Enum):
    """Enumeration of content types in the platform."""
    LESSON = "lesson"
    ANIMATION = "animation"
    ASSESSMENT = "assessment"
    EXERCISE = "exercise"


class LicenseType(enum.Enum):
    """Enumeration of license types."""
    INSTITUTIONAL = "institutional"
    PERSONAL = "personal"
    TRIAL = "trial"


class UserStatus(enum.Enum):
    """User account status."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING_VERIFICATION = "pending_verification"


class ContentStatus(enum.Enum):
    """Content moderation status."""
    DRAFT = "draft"
    PENDING_REVIEW = "pending_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    ARCHIVED = "archived"


class DifficultyLevel(enum.Enum):
    """Content difficulty levels."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class User(Base):
    """User model for all platform users."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    avatar_url = Column(String(512), nullable=True)
    institution_id = Column(Integer, ForeignKey("institutions.id"), nullable=True)
    role_id = Column(Integer, ForeignKey("roles.id"), default=1)
    status = Column(SQLEnum(UserStatus), default=UserStatus.PENDING_VERIFICATION)
    is_creator = Column(Boolean, default=False)
    is_instructor = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login_at = Column(DateTime, nullable=True)
    preferences = Column(JSON, nullable=True)
    
    # Relationships
    institution = relationship("Institution", back_populates="users")
    role = relationship("Role")
    progress = relationship("UserProgress", back_populates="user")
    created_content = relationship("Content", back_populates="creator")
    assessments = relationship("AssessmentResult", back_populates="user")
    audit_logs = relationship("AuditLog", back_populates="user")
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', role='{self.role.name}')>"


class Role(Base):
    """Role model for RBAC."""
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    permissions = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    users = relationship("User", back_populates="role")
    
    def __repr__(self):
        return f"<Role(id={self.id}, name='{self.name}')>"


class Institution(Base):
    """Institution model for organizational accounts."""
    __tablename__ = "institutions"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    domain = Column(String(255), nullable=True)
    license_id = Column(Integer, ForeignKey("licenses.id"), nullable=True)
    settings = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    users = relationship("User", back_populates="institution")
    license = relationship("License")
    
    def __repr__(self):
        return f"<Institution(id={self.id}, name='{self.name}')>"


class License(Base):
    """License model for commercial licensing."""
    __tablename__ = "licenses"
    
    id = Column(Integer, primary_key=True, index=True)
    license_type = Column(SQLEnum(LicenseType), nullable=False)
    institution_id = Column(Integer, ForeignKey("institutions.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    max_seats = Column(Integer, default=1)
    current_seats = Column(Integer, default=0)
    features = Column(JSON, nullable=True)
    status = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<License(id={self.id}, type='{self.license_type.value}', status={self.status})>"


class Content(Base):
    """Content model for educational content."""
    __tablename__ = "content"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    content_type = Column(SQLEnum(ContentType), nullable=False)
    platform = Column(String(50), nullable=False)  # mathverse, physicsverse, etc.
    difficulty = Column(SQLEnum(DifficultyLevel), default=DifficultyLevel.BEGINNER)
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(SQLEnum(ContentStatus), default=ContentStatus.DRAFT)
    is_premium = Column(Boolean, default=False)
    is_sample = Column(Boolean, default=True)
    metadata = Column(JSON, nullable=True)
    animation_script = Column(Text, nullable=True)
    animation_output_url = Column(String(512), nullable=True)
    thumbnail_url = Column(String(512), nullable=True)
    duration_seconds = Column(Integer, nullable=True)
    version = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    creator = relationship("User", back_populates="created_content")
    concepts = relationship("ContentConcept", back_populates="content")
    lessons = relationship("Lesson", back_populates="content")
    progress = relationship("UserProgress", back_populates="content")
    versions = relationship("ContentVersion", back_populates="content")
    moderation_queue = relationship("ModerationQueue", back_populates="content")
    
    def __repr__(self):
        return f"<Content(id={self.id}, title='{self.title}', platform='{self.platform}')>"


class ContentVersion(Base):
    """Version tracking for content updates."""
    __tablename__ = "content_versions"
    
    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, ForeignKey("content.id"), nullable=False)
    version = Column(Integer, nullable=False)
    change_log = Column(Text, nullable=True)
    animation_script = Column(Text, nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    content = relationship("Content", back_populates="versions")
    
    def __repr__(self):
        return f"<ContentVersion(id={self.id}, content_id={self.content_id}, version={self.version})>"


class Concept(Base):
    """Concept model for knowledge graph nodes."""
    __tablename__ = "concepts"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    platform = Column(String(50), nullable=False)
    difficulty = Column(SQLEnum(DifficultyLevel), default=DifficultyLevel.BEGINNER)
    prerequisites = Column(JSON, nullable=True)  # List of concept IDs
    estimated_duration = Column(Integer, nullable=True)  # Minutes
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Concept(id={self.id}, name='{self.name}', platform='{self.platform}')>"


class ContentConcept(Base):
    """Many-to-many relationship between content and concepts."""
    __tablename__ = "content_concepts"
    
    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, ForeignKey("content.id"), nullable=False)
    concept_id = Column(Integer, ForeignKey("concepts.id"), nullable=False)
    order_index = Column(Integer, default=0)
    
    # Relationships
    content = relationship("Content", back_populates="concepts")
    concept = relationship("Concept")
    
    def __repr__(self):
        return f"<ContentConcept(id={self.id}, content_id={self.content_id}, concept_id={self.concept_id})>"


class Lesson(Base):
    """Lesson model for structured learning content."""
    __tablename__ = "lessons"
    
    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, ForeignKey("content.id"), nullable=False)
    title = Column(String(255), nullable=False)
    order_index = Column(Integer, default=0)
    duration_seconds = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    content = relationship("Content", back_populates="lessons")
    progress = relationship("UserProgress", back_populates="lesson")
    
    def __repr__(self):
        return f"<Lesson(id={self.id}, title='{self.title}', content_id={self.content_id})>"


class Syllabus(Base):
    """Syllabus model for curriculum organization."""
    __tablename__ = "syllabi"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    platform = Column(String(50), nullable=False)
    institution_id = Column(Integer, ForeignKey("institutions.id"), nullable=True)
    is_public = Column(Boolean, default=True)
    structure = Column(JSON, nullable=True)  # Hierarchical structure
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Syllabus(id={self.id}, title='{self.title}', platform='{self.platform}')>"


class UserProgress(Base):
    """User progress tracking for lessons and concepts."""
    __tablename__ = "user_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content_id = Column(Integer, ForeignKey("content.id"), nullable=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=True)
    concept_id = Column(Integer, ForeignKey("concepts.id"), nullable=True)
    status = Column(String(50), default="not_started")  # not_started, in_progress, completed
    progress_percentage = Column(Float, default=0.0)
    score = Column(Float, nullable=True)
    time_spent_seconds = Column(Integer, default=0)
    last_position_seconds = Column(Integer, nullable=True)
    attempts = Column(Integer, default=0)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="progress")
    content = relationship("Content", back_populates="progress")
    lesson = relationship("Lesson", back_populates="progress")
    
    def __repr__(self):
        return f"<UserProgress(id={self.id}, user_id={self.user_id}, content_id={self.content_id}, status='{self.status}')>"


class Assessment(Base):
    """Assessment model for evaluating learner understanding."""
    __tablename__ = "assessments"
    
    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, ForeignKey("content.id"), nullable=False)
    title = Column(String(255), nullable=False)
    questions = Column(JSON, nullable=True)  # List of questions with answers
    passing_score = Column(Float, default=70.0)
    time_limit_minutes = Column(Integer, nullable=True)
    difficulty_weight = Column(Float, default=1.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Assessment(id={self.id}, title='{this.title}', content_id={self.content_id})>"


class AssessmentResult(Base):
    """Assessment result tracking."""
    __tablename__ = "assessment_results"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assessment_id = Column(Integer, ForeignKey("assessments.id"), nullable=False)
    score = Column(Float, nullable=True)
    passed = Column(Boolean, default=False)
    answers = Column(JSON, nullable=True)
    time_taken_seconds = Column(Integer, nullable=True)
    attempt_number = Column(Integer, default=1)
    completed_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="assessments")
    
    def __repr__(self):
        return f"<AssessmentResult(id={self.id}, user_id={self.user_id}, assessment_id={self.assessment_id}, score={self.score})>"


class AuditLog(Base):
    """Audit log for governance and compliance."""
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action = Column(String(100), nullable=False)
    resource_type = Column(String(50), nullable=False)
    resource_id = Column(String(100), nullable=True)
    details = Column(JSON, nullable=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(512), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="audit_logs")
    
    def __repr__(self):
        return f"<AuditLog(id={self.id}, action='{self.action}', resource_type='{self.resource_type}')>"


class ModerationQueue(Base):
    """Content moderation queue for governance."""
    __tablename__ = "moderation_queue"
    
    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, ForeignKey("content.id"), nullable=False)
    status = Column(String(50), default="pending")  # pending, approved, rejected
    reviewer_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    review_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    reviewed_at = Column(DateTime, nullable=True)
    
    # Relationships
    content = relationship("Content", back_populates="moderation_queue")
    
    def __repr__(self):
        return f"<ModerationQueue(id={self.id}, content_id={self.content_id}, status='{self.status}')>"
