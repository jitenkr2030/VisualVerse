"""
Shared Pydantic Schemas for VisualVerse
API request and response validation models.
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, EmailStr, Field
from enum import Enum


# ============== User Schemas ==============

class UserBase(BaseModel):
    """Base user schema with common fields."""
    email: EmailStr
    full_name: str
    is_creator: bool = False
    is_instructor: bool = False


class UserCreate(UserBase):
    """Schema for creating a new user."""
    password: str = Field(..., min_length=8)
    institution_id: Optional[int] = None


class UserUpdate(BaseModel):
    """Schema for updating user information."""
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    preferences: Optional[Dict[str, Any]] = None


class UserResponse(UserBase):
    """Schema for user response."""
    id: int
    status: str
    institution_id: Optional[int]
    role: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """Schema for user login request."""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Schema for authentication token response."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse


# ============== Content Schemas ==============

class ContentBase(BaseModel):
    """Base content schema."""
    title: str
    description: Optional[str] = None
    platform: str
    difficulty: str = "beginner"
    is_premium: bool = False
    metadata: Optional[Dict[str, Any]] = None


class ContentCreate(ContentBase):
    """Schema for creating content."""
    animation_script: Optional[str] = None
    concepts: Optional[List[int]] = None


class ContentUpdate(BaseModel):
    """Schema for updating content."""
    title: Optional[str] = None
    description: Optional[str] = None
    animation_script: Optional[str] = None
    is_premium: Optional[bool] = None
    metadata: Optional[Dict[str, Any]] = None


class ContentResponse(ContentBase):
    """Schema for content response."""
    id: int
    creator_id: int
    status: str
    is_sample: bool
    animation_output_url: Optional[str]
    thumbnail_url: Optional[str]
    duration_seconds: Optional[int]
    version: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ContentListResponse(BaseModel):
    """Schema for content list response."""
    items: List[ContentResponse]
    total: int
    page: int
    page_size: int


# ============== Concept Schemas ==============

class ConceptBase(BaseModel):
    """Base concept schema."""
    name: str
    description: Optional[str] = None
    platform: str
    difficulty: str = "beginner"
    prerequisites: Optional[List[int]] = None
    estimated_duration: Optional[int] = None


class ConceptCreate(ConceptBase):
    """Schema for creating a concept."""
    pass


class ConceptResponse(ConceptBase):
    """Schema for concept response."""
    id: int
    slug: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ============== Progress Schemas ==============

class ProgressBase(BaseModel):
    """Base progress schema."""
    content_id: Optional[int] = None
    lesson_id: Optional[int] = None
    concept_id: Optional[int] = None
    progress_percentage: float = 0.0
    score: Optional[float] = None
    time_spent_seconds: int = 0


class ProgressUpdate(BaseModel):
    """Schema for updating progress."""
    progress_percentage: Optional[float] = None
    score: Optional[float] = None
    time_spent_seconds: Optional[int] = None
    last_position_seconds: Optional[int] = None


class ProgressResponse(ProgressBase):
    """Schema for progress response."""
    id: int
    user_id: int
    status: str
    attempts: int
    completed_at: Optional[datetime]
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ============== Assessment Schemas ==============

class QuestionBase(BaseModel):
    """Base question schema."""
    question_text: str
    question_type: str  # multiple_choice, true_false, short_answer
    options: Optional[List[str]] = None
    correct_answer: str
    explanation: Optional[str] = None
    points: int = 1


class AssessmentBase(BaseModel):
    """Base assessment schema."""
    content_id: int
    title: str
    passing_score: float = 70.0
    time_limit_minutes: Optional[int] = None
    difficulty_weight: float = 1.0


class AssessmentCreate(AssessmentBase):
    """Schema for creating an assessment."""
    questions: List[QuestionBase]


class AssessmentResponse(AssessmentBase):
    """Schema for assessment response."""
    id: int
    questions: List[Dict[str, Any]]
    created_at: datetime
    
    class Config:
        from_attributes = True


class AssessmentSubmission(BaseModel):
    """Schema for submitting assessment answers."""
    assessment_id: int
    answers: Dict[int, str]  # question_id -> answer


class AssessmentResultResponse(BaseModel):
    """Schema for assessment result response."""
    assessment_id: int
    score: float
    passed: bool
    correct_answers: int
    total_questions: int
    time_taken_seconds: int
    attempt_number: int
    completed_at: datetime


# ============== License Schemas ==============

class LicenseBase(BaseModel):
    """Base license schema."""
    license_type: str
    institution_id: Optional[int] = None
    user_id: Optional[int] = None
    start_date: datetime
    end_date: datetime
    max_seats: int = 1
    features: Optional[Dict[str, Any]] = None


class LicenseCreate(LicenseBase):
    """Schema for creating a license."""
    pass


class LicenseResponse(LicenseBase):
    """Schema for license response."""
    id: int
    current_seats: int
    status: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class LicenseVerify(BaseModel):
    """Schema for verifying license access."""
    license_id: Optional[int] = None
    user_id: Optional[int] = None
    content_id: Optional[int] = None
    feature: Optional[str] = None


class LicenseVerifyResponse(BaseModel):
    """Schema for license verification response."""
    valid: bool
    license_type: Optional[str]
    can_access_premium: bool
    features: Dict[str, bool]
    expires_at: Optional[datetime]


# ============== Syllabus Schemas ==============

class SyllabusNode(BaseModel):
    """Node in a syllabus tree."""
    id: Optional[int] = None
    title: str
    type: str  # subject, unit, topic, lesson
    children: List["SyllabusNode"] = []
    content_ids: List[int] = []


class SyllabusBase(BaseModel):
    """Base syllabus schema."""
    title: str
    description: Optional[str] = None
    platform: str
    is_public: bool = True


class SyllabusCreate(SyllabusBase):
    """Schema for creating a syllabus."""
    structure: Dict[str, Any]


class SyllabusResponse(SyllabusBase):
    """Schema for syllabus response."""
    id: int
    institution_id: Optional[int]
    structure: Optional[Dict[str, Any]]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ============== Moderation Schemas ==============

class ModerationBase(BaseModel):
    """Base moderation schema."""
    content_id: int
    status: str = "pending"


class ModerationReview(BaseModel):
    """Schema for reviewing content in moderation."""
    status: str  # approved, rejected
    review_notes: Optional[str] = None


class ModerationResponse(BaseModel):
    """Schema for moderation response."""
    id: int
    content_id: int
    status: str
    reviewer_id: Optional[int]
    review_notes: Optional[str]
    created_at: datetime
    reviewed_at: Optional[datetime]
    content: Optional[ContentResponse] = None
    
    class Config:
        from_attributes = True


# ============== Analytics Schemas ==============

class AnalyticsQuery(BaseModel):
    """Schema for analytics query parameters."""
    start_date: datetime
    end_date: datetime
    group_by: str = "day"  # day, week, month
    institution_id: Optional[int] = None


class AnalyticsResponse(BaseModel):
    """Schema for analytics response."""
    total_users: int
    active_users: int
    total_content: int
    total_views: int
    total_completions: int
    average_score: float
    time_series_data: List[Dict[str, Any]]
    top_content: List[Dict[str, Any]]
    platform_breakdown: Dict[str, int]


# ============== Recommendation Schemas ==============

class RecommendationRequest(BaseModel):
    """Schema for requesting recommendations."""
    user_id: int
    platform: Optional[str] = None
    limit: int = 10


class RecommendationResponse(BaseModel):
    """Schema for recommendation response."""
    recommendations: List[Dict[str, Any]]
    based_on: str  # "progress", "popularity", "similar_users"
    generated_at: datetime


# ============== Audit Schemas ==============

class AuditLogQuery(BaseModel):
    """Schema for querying audit logs."""
    user_id: Optional[int] = None
    action: Optional[str] = None
    resource_type: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    limit: int = 100


class AuditLogResponse(BaseModel):
    """Schema for audit log response."""
    id: int
    user_id: Optional[int]
    action: str
    resource_type: str
    resource_id: Optional[str]
    details: Optional[Dict[str, Any]]
    ip_address: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============== API Response Wrappers ==============

class ApiResponse(BaseModel):
    """Generic API response wrapper."""
    success: bool = True
    message: Optional[str] = None
    data: Optional[Dict[str, Any]] = None


class PaginatedResponse(BaseModel):
    """Paginated API response wrapper."""
    items: List[Any]
    total: int
    page: int
    page_size: int
    total_pages: int


class ErrorResponse(BaseModel):
    """Error response schema."""
    success: bool = False
    error: str
    detail: Optional[str] = None
    code: Optional[str] = None
