"""
Subject model for VisualVerse content metadata.
Represents educational domains and subject areas.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, validator
from enum import Enum


class SubjectLevel(str, Enum):
    """Subject difficulty levels"""
    ELEMENTARY = "elementary"
    MIDDLE_SCHOOL = "middle_school"
    HIGH_SCHOOL = "high_school"
    UNDERGRADUATE = "undergraduate"
    GRADUATE = "graduate"
    PROFESSIONAL = "professional"


class SubjectCategory(str, Enum):
    """Subject categories"""
    STEM = "stem"
    HUMANITIES = "humanities"
    SOCIAL_SCIENCES = "social_sciences"
    ARTS = "arts"
    BUSINESS = "business"
    HEALTH = "health"


class Subject(BaseModel):
    """Subject model representing educational domains"""
    
    id: str = Field(..., description="Unique identifier for the subject")
    name: str = Field(..., min_length=1, max_length=100, description="Subject name")
    display_name: str = Field(..., min_length=1, max_length=100, description="Human-readable subject name")
    description: Optional[str] = Field(None, max_length=1000, description="Subject description")
    
    # Subject metadata
    category: SubjectCategory = Field(..., description="Subject category")
    level: SubjectLevel = Field(..., description="Difficulty level")
    icon_url: Optional[str] = Field(None, description="Subject icon URL")
    color_theme: Optional[str] = Field(None, description="Subject color theme")
    
    # Curriculum standards
    curriculum_standards: List[str] = Field(default_factory=list, description="Associated curriculum standards")
    
    # Statistics
    course_count: int = Field(default=0, description="Number of courses in this subject")
    concept_count: int = Field(default=0, description="Number of concepts in this subject")
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update timestamp")
    
    # Status
    is_active: bool = Field(default=True, description="Whether the subject is active")
    is_featured: bool = Field(default=False, description="Whether the subject is featured")
    
    class Config:
        schema_extra = {
            "example": {
                "id": "mathematics",
                "name": "mathematics",
                "display_name": "Mathematics",
                "description": "Mathematical concepts, theories, and applications",
                "category": "stem",
                "level": "high_school",
                "icon_url": "/icons/mathematics.svg",
                "color_theme": "#3B82F6",
                "curriculum_standards": ["CBSE", "ICSE", "GCSE", "AP", "JEE"],
                "course_count": 15,
                "concept_count": 150,
                "is_active": True,
                "is_featured": True
            }
        }
    
    @validator('id')
    def validate_id(cls, v):
        """Validate subject ID format"""
        if not v.replace('_', '').replace('-', '').isalnum():
            raise ValueError('Subject ID must contain only alphanumeric characters, hyphens, and underscores')
        return v.lower()
    
    @validator('name')
    def validate_name(cls, v):
        """Validate subject name format"""
        return v.strip().title()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert subject to dictionary"""
        return self.dict()
    
    def update_timestamp(self):
        """Update the updated_at timestamp"""
        self.updated_at = datetime.now()
    
    def increment_course_count(self):
        """Increment course count"""
        self.course_count += 1
        self.update_timestamp()
    
    def decrement_course_count(self):
        """Decrement course count (minimum 0)"""
        self.course_count = max(0, self.course_count - 1)
        self.update_timestamp()
    
    def increment_concept_count(self):
        """Increment concept count"""
        self.concept_count += 1
        self.update_timestamp()
    
    def decrement_concept_count(self):
        """Decrement concept count (minimum 0)"""
        self.concept_count = max(0, self.concept_count - 1)
        self.update_timestamp()


class SubjectCreate(BaseModel):
    """Model for creating a new subject"""
    
    name: str = Field(..., min_length=1, max_length=100, description="Subject name")
    display_name: str = Field(..., min_length=1, max_length=100, description="Human-readable subject name")
    description: Optional[str] = Field(None, max_length=1000, description="Subject description")
    category: SubjectCategory = Field(..., description="Subject category")
    level: SubjectLevel = Field(..., description="Difficulty level")
    icon_url: Optional[str] = Field(None, description="Subject icon URL")
    color_theme: Optional[str] = Field(None, description="Subject color theme")
    curriculum_standards: List[str] = Field(default_factory=list, description="Associated curriculum standards")
    is_featured: bool = Field(default=False, description="Whether the subject is featured")


class SubjectUpdate(BaseModel):
    """Model for updating an existing subject"""
    
    display_name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    icon_url: Optional[str] = Field(None)
    color_theme: Optional[str] = Field(None)
    curriculum_standards: Optional[List[str]] = Field(None)
    is_active: Optional[bool] = Field(None)
    is_featured: Optional[bool] = Field(None)


class SubjectResponse(BaseModel):
    """Response model for subject data"""
    
    success: bool = Field(..., description="Whether the request was successful")
    subject: Optional[Subject] = Field(None, description="Subject data")
    message: Optional[str] = Field(None, description="Response message")


class SubjectListResponse(BaseModel):
    """Response model for subject list"""
    
    success: bool = Field(..., description="Whether the request was successful")
    subjects: List[Subject] = Field(..., description="List of subjects")
    total_count: int = Field(..., description="Total number of subjects")
    page: int = Field(default=1, description="Current page number")
    per_page: int = Field(default=20, description="Number of subjects per page")
    has_next: bool = Field(..., description="Whether there are more subjects")
    has_previous: bool = Field(..., description="Whether there are previous subjects")


class SubjectStatistics(BaseModel):
    """Subject statistics model"""
    
    total_subjects: int = Field(..., description="Total number of subjects")
    active_subjects: int = Field(..., description="Number of active subjects")
    featured_subjects: int = Field(..., description="Number of featured subjects")
    subjects_by_category: Dict[str, int] = Field(..., description="Subjects count by category")
    subjects_by_level: Dict[str, int] = Field(..., description="Subjects count by level")
    most_popular_subjects: List[Subject] = Field(default_factory=list, description="Most popular subjects")


# Subject utility functions
def create_subject_id(name: str) -> str:
    """Create a subject ID from a name"""
    return name.lower().replace(' ', '_').replace('-', '_')

def validate_subject_data(data: dict) -> bool:
    """Validate subject data"""
    required_fields = ['name', 'display_name', 'category', 'level']
    return all(field in data and data[field] for field in required_fields)

def get_default_subjects() -> List[Subject]:
    """Get default subjects for the platform"""
    default_subjects = [
        {
            "id": "mathematics",
            "name": "mathematics",
            "display_name": "Mathematics",
            "description": "Mathematical concepts, theories, and applications",
            "category": "stem",
            "level": "high_school",
            "color_theme": "#3B82F6",
            "curriculum_standards": ["CBSE", "ICSE", "GCSE", "AP", "JEE"],
            "is_featured": True
        },
        {
            "id": "physics",
            "name": "physics",
            "display_name": "Physics",
            "description": "Physical laws, phenomena, and scientific principles",
            "category": "stem",
            "level": "high_school",
            "color_theme": "#10B981",
            "curriculum_standards": ["CBSE", "ICSE", "GCSE", "AP"],
            "is_featured": True
        },
        {
            "id": "chemistry",
            "name": "chemistry",
            "display_name": "Chemistry",
            "description": "Chemical compounds, reactions, and molecular structures",
            "category": "stem",
            "level": "high_school",
            "color_theme": "#F59E0B",
            "curriculum_standards": ["CBSE", "ICSE", "GCSE", "AP"],
            "is_featured": True
        },
        {
            "id": "biology",
            "name": "biology",
            "display_name": "Biology",
            "description": "Living organisms, biological processes, and life sciences",
            "category": "stem",
            "level": "high_school",
            "color_theme": "#8B5CF6",
            "curriculum_standards": ["CBSE", "ICSE", "GCSE", "AP"],
            "is_featured": True
        },
        {
            "id": "computer_science",
            "name": "computer_science",
            "display_name": "Computer Science",
            "description": "Programming, algorithms, and computational thinking",
            "category": "stem",
            "level": "high_school",
            "color_theme": "#EF4444",
            "curriculum_standards": ["CBSE", "ICSE", "AP"],
            "is_featured": True
        },
        {
            "id": "economics",
            "name": "economics",
            "display_name": "Economics",
            "description": "Economic principles, markets, and financial systems",
            "category": "social_sciences",
            "level": "high_school",
            "color_theme": "#06B6D4",
            "curriculum_standards": ["CBSE", "ICSE", "GCSE", "AP"],
            "is_featured": False
        },
        {
            "id": "history",
            "name": "history",
            "display_name": "History",
            "description": "Historical events, civilizations, and human development",
            "category": "humanities",
            "level": "high_school",
            "color_theme": "#84CC16",
            "curriculum_standards": ["CBSE", "ICSE", "GCSE", "AP"],
            "is_featured": False
        },
        {
            "id": "literature",
            "name": "literature",
            "display_name": "Literature",
            "description": "Literary works, analysis, and creative writing",
            "category": "humanities",
            "level": "high_school",
            "color_theme": "#EC4899",
            "curriculum_standards": ["CBSE", "ICSE", "GCSE", "AP"],
            "is_featured": False
        }
    ]
    
    return [Subject(**subject_data) for subject_data in default_subjects]
