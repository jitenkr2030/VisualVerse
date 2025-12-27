"""
Shared schemas and data contracts for VisualVerse engine.
Common Pydantic models used across all modules.
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from enum import Enum
import uuid


class BaseModel(BaseModel):
    """Extended base model with common functionality"""
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
    
    def update_timestamp(self):
        """Update the updated_at timestamp"""
        self.updated_at = datetime.now()


class ConceptSchema(BaseModel):
    """Schema for concept data exchange"""
    
    id: str
    name: str
    display_name: str
    description: str
    subject_id: str
    difficulty_level: str
    estimated_duration: int
    prerequisites: List[str]
    learning_objectives: List[str]
    tags: List[str]
    is_active: bool = True


class LessonSchema(BaseModel):
    """Schema for lesson data exchange"""
    
    id: str
    concept_id: str
    title: str
    content: str
    animation_config: Dict[str, Any]
    duration: int
    difficulty_level: str
    learning_objectives: List[str]
    prerequisites: List[str]


class AnimationSchema(BaseModel):
    """Schema for animation configuration"""
    
    id: str
    lesson_id: str
    scene_class: str
    render_config: Dict[str, Any]
    output_format: str = "mp4"
    quality: str = "l"
    duration: Optional[int] = None
    metadata: Dict[str, Any] = {}


class ResponseStatus(str, Enum):
    """API response status values"""
    SUCCESS = "success"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


class ApiResponse(BaseModel):
    """Standard API response format"""
    
    status: ResponseStatus
    message: str
    data: Optional[Any] = None
    errors: List[str] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.now)
    
    @classmethod
    def success(cls, message: str, data: Any = None):
        """Create a success response"""
        return cls(status=ResponseStatus.SUCCESS, message=message, data=data)
    
    @classmethod
    def error(cls, message: str, errors: List[str] = None):
        """Create an error response"""
        return cls(status=ResponseStatus.ERROR, message=message, errors=errors or [])


class PaginationParams(BaseModel):
    """Pagination parameters for list endpoints"""
    
    page: int = Field(default=1, ge=1)
    per_page: int = Field(default=20, ge=1, le=100)
    
    @property
    def offset(self) -> int:
        return (self.page - 1) * self.per_page


class PaginatedResponse(BaseModel):
    """Paginated response format"""
    
    items: List[Any]
    total_count: int
    page: int
    per_page: int
    has_next: bool
    has_previous: bool
    total_pages: int
    
    @classmethod
    def create(cls, items: List[Any], total_count: int, pagination: PaginationParams):
        """Create paginated response"""
        total_pages = (total_count + pagination.per_page - 1) // pagination.per_page
        has_next = pagination.page < total_pages
        has_previous = pagination.page > 1
        
        return cls(
            items=items,
            total_count=total_count,
            page=pagination.page,
            per_page=pagination.per_page,
            has_next=has_next,
            has_previous=has_previous,
            total_pages=total_pages
        )


# Event schemas for real-time communication
class EventType(str, Enum):
    """Event types for real-time communication"""
    LESSON_CREATED = "lesson_created"
    RENDER_STARTED = "render_started"
    RENDER_COMPLETED = "render_completed"
    PROGRESS_UPDATED = "progress_updated"
    RECOMMENDATION_GENERATED = "recommendation_generated"


class Event(BaseModel):
    """Event schema for real-time updates"""
    
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    event_type: EventType
    user_id: Optional[str] = None
    data: Dict[str, Any] = {}
    timestamp: datetime = Field(default_factory=datetime.now)


# Configuration schemas
class ServiceConfig(BaseModel):
    """Service configuration schema"""
    
    service_name: str
    version: str
    environment: str
    debug: bool = False
    host: str = "0.0.0.0"
    port: int
    database_url: str
    cache_url: Optional[str] = None
    metrics_enabled: bool = True
    logging_level: str = "INFO"


class EngineConfig(BaseModel):
    """Engine configuration schema"""
    
    max_concurrent_renders: int = Field(default=4, ge=1, le=16)
    default_render_quality: str = Field(default="l")
    default_fps: int = Field(default=30, ge=1, le=120)
    render_timeout: int = Field(default=300, ge=30)  # seconds
    temp_dir: str = "/tmp/visualverse"
    output_dir: str = "/app/renders"
    backup_enabled: bool = True


class RecommendationConfig(BaseModel):
    """Recommendation engine configuration"""
    
    algorithm: str = Field(default="adaptive")  # rule_based, graph_based, adaptive
    confidence_threshold: float = Field(default=0.7, ge=0.0, le=1.0)
    max_recommendations: int = Field(default=10, ge=1, le=50)
    learning_rate: float = Field(default=0.01, ge=0.001, le=0.1)
    adaptation_enabled: bool = True
    feedback_weight: float = Field(default=0.3, ge=0.0, le=1.0)


# Validation utilities
def validate_concept_data(data: Dict[str, Any]) -> bool:
    """Validate concept data structure"""
    required_fields = ["name", "display_name", "description", "subject_id"]
    return all(field in data and data[field] for field in required_fields)


def validate_lesson_data(data: Dict[str, Any]) -> bool:
    """Validate lesson data structure"""
    required_fields = ["concept_id", "title", "content"]
    return all(field in data and data[field] for field in required_fields)


def validate_animation_config(config: Dict[str, Any]) -> bool:
    """Validate animation configuration"""
    valid_qualities = ["k", "h", "m", "l", "p"]
    valid_formats = ["mp4", "gif", "webm", "avi"]
    
    quality = config.get("quality", "l")
    format_type = config.get("format", "mp4")
    
    return quality in valid_qualities and format_type in valid_formats
