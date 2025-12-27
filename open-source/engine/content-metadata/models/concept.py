"""
Concept model for VisualVerse content metadata.
Represents individual learning concepts within subjects.
"""

from typing import List, Optional, Dict, Any, Set
from datetime import datetime
from pydantic import BaseModel, Field, validator
from enum import Enum
import uuid


class DifficultyLevel(str, Enum):
    """Concept difficulty levels"""
    BEGINNER = "beginner"
    ELEMENTARY = "elementary"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class ConceptType(str, Enum):
    """Types of concepts"""
    THEORETICAL = "theoretical"
    PRACTICAL = "practical"
    PROCEDURAL = "procedural"
    CONCEPTUAL = "conceptual"
    ANALYTICAL = "analytical"


class LearningStyle(str, Enum):
    """Preferred learning styles"""
    VISUAL = "visual"
    AUDITORY = "auditory"
    KINESTHETIC = "kinesthetic"
    READING_WRITING = "reading_writing"
    MULTIMODAL = "multimodal"


class Concept(BaseModel):
    """Concept model representing individual learning concepts"""
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique identifier")
    subject_id: str = Field(..., description="Associated subject ID")
    name: str = Field(..., min_length=1, max_length=200, description="Concept name")
    display_name: str = Field(..., min_length=1, max_length=200, description="Human-readable concept name")
    description: str = Field(..., min_length=10, max_length=2000, description="Concept description")
    
    # Concept classification
    type: ConceptType = Field(..., description="Type of concept")
    difficulty_level: DifficultyLevel = Field(..., description="Difficulty level")
    estimated_duration: int = Field(..., ge=1, le=300, description="Estimated learning time in minutes")
    
    # Learning objectives and outcomes
    learning_objectives: List[str] = Field(default_factory=list, description="Learning objectives")
    key_concepts: List[str] = Field(default_factory=list, description="Key concepts covered")
    prerequisites: List[str] = Field(default_factory=list, description="Prerequisite concept IDs")
    
    # Content metadata
    tags: List[str] = Field(default_factory=list, description="Concept tags")
    keywords: List[str] = Field(default_factory=list, description="Search keywords")
    
    # Curriculum alignment
    curriculum_standards: List[str] = Field(default_factory=list, description="Associated curriculum standards")
    grade_levels: List[str] = Field(default_factory=list, description="Applicable grade levels")
    
    # Assessment and evaluation
    assessment_criteria: List[str] = Field(default_factory=list, description="Assessment criteria")
    evaluation_methods: List[str] = Field(default_factory=list, description="Evaluation methods")
    
    # Multimedia content
    visual_assets: List[str] = Field(default_factory=list, description="Visual asset URLs")
    audio_resources: List[str] = Field(default_factory=list, description="Audio resource URLs")
    interactive_elements: List[str] = Field(default_factory=list, description="Interactive element specifications")
    
    # Adaptive learning preferences
    preferred_learning_styles: List[LearningStyle] = Field(default_factory=list, description="Preferred learning styles")
    
    # Statistics and metrics
    completion_rate: float = Field(default=0.0, ge=0.0, le=1.0, description="Average completion rate")
    average_score: float = Field(default=0.0, ge=0.0, le=100.0, description="Average achievement score")
    difficulty_rating: float = Field(default=0.0, ge=0.0, le=5.0, description="User-rated difficulty")
    
    # Metadata and status
    is_active: bool = Field(default=True, description="Whether the concept is active")
    is_premium: bool = Field(default=False, description="Whether the concept requires premium access")
    version: str = Field(default="1.0.0", description="Concept version")
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update timestamp")
    
    class Config:
        schema_extra = {
            "example": {
                "id": "quadratic-equations",
                "subject_id": "mathematics",
                "name": "quadratic_equations",
                "display_name": "Quadratic Equations",
                "description": "Understanding and solving quadratic equations using various methods including factoring, completing the square, and the quadratic formula.",
                "type": "theoretical",
                "difficulty_level": "intermediate",
                "estimated_duration": 45,
                "learning_objectives": [
                    "Understand the standard form of quadratic equations",
                    "Solve quadratic equations by factoring",
                    "Solve quadratic equations using the quadratic formula",
                    "Analyze the discriminant and its implications"
                ],
                "key_concepts": ["quadratic formula", "discriminant", "factoring", "completing the square"],
                "prerequisites": ["linear-equations", "polynomials"],
                "tags": ["algebra", "equations", "mathematics"],
                "keywords": ["quadratic", "equation", "formula", "discriminant"],
                "curriculum_standards": ["CBSE", "ICSE", "GCSE", "AP"],
                "grade_levels": ["9", "10", "11"],
                "assessment_criteria": ["Solve problems", "Apply concepts", "Analyze solutions"],
                "preferred_learning_styles": ["visual", "reading_writing"],
                "is_active": True,
                "is_premium": False
            }
        }
    
    @validator('name')
    def validate_name(cls, v):
        """Validate concept name format"""
        return v.strip().lower().replace(' ', '_')
    
    @validator('display_name')
    def validate_display_name(cls, v):
        """Validate display name format"""
        return v.strip().title()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert concept to dictionary"""
        return self.dict()
    
    def update_timestamp(self):
        """Update the updated_at timestamp"""
        self.updated_at = datetime.now()
    
    def add_prerequisite(self, prerequisite_id: str):
        """Add a prerequisite concept"""
        if prerequisite_id not in self.prerequisites:
            self.prerequisites.append(prerequisite_id)
            self.update_timestamp()
    
    def remove_prerequisite(self, prerequisite_id: str):
        """Remove a prerequisite concept"""
        if prerequisite_id in self.prerequisites:
            self.prerequisites.remove(prerequisite_id)
            self.update_timestamp()
    
    def add_tag(self, tag: str):
        """Add a tag"""
        if tag not in self.tags:
            self.tags.append(tag.lower())
            self.update_timestamp()
    
    def remove_tag(self, tag: str):
        """Remove a tag"""
        if tag in self.tags:
            self.tags.remove(tag)
            self.update_timestamp()
    
    def update_completion_stats(self, score: float):
        """Update completion statistics"""
        # Simple moving average calculation
        if self.average_score == 0:
            self.average_score = score
        else:
            self.average_score = (self.average_score + score) / 2
        self.update_timestamp()
    
    def is_ready_to_learn(self, completed_concepts: Set[str]) -> bool:
        """Check if concept is ready to learn based on prerequisites"""
        return all(prereq in completed_concepts for prereq in self.prerequisites)
    
    def get_learning_path_position(self, all_concepts: Dict[str, 'Concept']) -> int:
        """Calculate position in learning path based on prerequisites"""
        max_prereq_depth = 0
        for prereq_id in self.prerequisites:
            if prereq_id in all_concepts:
                prereq_concept = all_concepts[prereq_id]
                depth = prereq_concept.get_learning_path_position(all_concepts)
                max_prereq_depth = max(max_prereq_depth, depth)
        return max_prereq_depth + 1


class ConceptCreate(BaseModel):
    """Model for creating a new concept"""
    
    subject_id: str = Field(..., description="Associated subject ID")
    name: str = Field(..., min_length=1, max_length=200, description="Concept name")
    display_name: str = Field(..., min_length=1, max_length=200, description="Human-readable concept name")
    description: str = Field(..., min_length=10, max_length=2000, description="Concept description")
    type: ConceptType = Field(..., description="Type of concept")
    difficulty_level: DifficultyLevel = Field(..., description="Difficulty level")
    estimated_duration: int = Field(..., ge=1, le=300, description="Estimated learning time in minutes")
    learning_objectives: List[str] = Field(default_factory=list, description="Learning objectives")
    key_concepts: List[str] = Field(default_factory=list, description="Key concepts covered")
    prerequisites: List[str] = Field(default_factory=list, description="Prerequisite concept IDs")
    tags: List[str] = Field(default_factory=list, description="Concept tags")
    keywords: List[str] = Field(default_factory=list, description="Search keywords")
    curriculum_standards: List[str] = Field(default_factory=list, description="Associated curriculum standards")
    grade_levels: List[str] = Field(default_factory=list, description="Applicable grade levels")
    preferred_learning_styles: List[LearningStyle] = Field(default_factory=list, description="Preferred learning styles")
    is_premium: bool = Field(default=False, description="Whether the concept requires premium access")


class ConceptUpdate(BaseModel):
    """Model for updating an existing concept"""
    
    display_name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=10, max_length=2000)
    type: Optional[ConceptType] = Field(None)
    difficulty_level: Optional[DifficultyLevel] = Field(None)
    estimated_duration: Optional[int] = Field(None, ge=1, le=300)
    learning_objectives: Optional[List[str]] = Field(None)
    key_concepts: Optional[List[str]] = Field(None)
    prerequisites: Optional[List[str]] = Field(None)
    tags: Optional[List[str]] = Field(None)
    keywords: Optional[List[str]] = Field(None)
    curriculum_standards: Optional[List[str]] = Field(None)
    grade_levels: Optional[List[str]] = Field(None)
    assessment_criteria: Optional[List[str]] = Field(None)
    evaluation_methods: Optional[List[str]] = Field(None)
    visual_assets: Optional[List[str]] = Field(None)
    audio_resources: Optional[List[str]] = Field(None)
    interactive_elements: Optional[List[str]] = Field(None)
    preferred_learning_styles: Optional[List[LearningStyle]] = Field(None)
    is_active: Optional[bool] = Field(None)
    is_premium: Optional[bool] = Field(None)
    version: Optional[str] = Field(None)


class ConceptResponse(BaseModel):
    """Response model for concept data"""
    
    success: bool = Field(..., description="Whether the request was successful")
    concept: Optional[Concept] = Field(None, description="Concept data")
    message: Optional[str] = Field(None, description="Response message")


class ConceptListResponse(BaseModel):
    """Response model for concept list"""
    
    success: bool = Field(..., description="Whether the request was successful")
    concepts: List[Concept] = Field(..., description="List of concepts")
    total_count: int = Field(..., description="Total number of concepts")
    page: int = Field(default=1, description="Current page number")
    per_page: int = Field(default=20, description="Number of concepts per page")
    has_next: bool = Field(..., description="Whether there are more concepts")
    has_previous: bool = Field(..., description="Whether there are previous concepts")


class LearningPath(BaseModel):
    """Learning path model"""
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Learning path ID")
    user_id: Optional[str] = Field(None, description="Associated user ID")
    subject_id: str = Field(..., description="Subject ID")
    name: str = Field(..., min_length=1, max_length=200, description="Path name")
    description: Optional[str] = Field(None, max_length=1000, description="Path description")
    
    # Path configuration
    concepts: List[str] = Field(..., description="Ordered list of concept IDs")
    start_level: DifficultyLevel = Field(..., description="Starting difficulty level")
    target_level: DifficultyLevel = Field(..., description="Target difficulty level")
    adaptive: bool = Field(default=True, description="Whether path adapts to user performance")
    
    # Progress tracking
    completed_concepts: List[str] = Field(default_factory=list, description="Completed concept IDs")
    current_concept: Optional[str] = Field(None, description="Current concept being studied")
    progress_percentage: float = Field(default=0.0, ge=0.0, le=100.0, description="Overall progress percentage")
    
    # Metadata
    estimated_total_duration: int = Field(default=0, description="Estimated total duration in minutes")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update timestamp")
    
    class Config:
        schema_extra = {
            "example": {
                "id": "math-beginner-to-advanced",
                "subject_id": "mathematics",
                "name": "Mathematics: Beginner to Advanced",
                "description": "Complete mathematics learning path from basic arithmetic to advanced calculus",
                "concepts": ["basic-arithmetic", "fractions", "algebra-basics", "linear-equations", "quadratic-equations", "functions", "calculus-intro"],
                "start_level": "beginner",
                "target_level": "advanced",
                "adaptive": True,
                "estimated_total_duration": 3000
            }
        }
    
    def update_progress(self):
        """Update progress percentage"""
        if self.concepts:
            self.progress_percentage = (len(self.completed_concepts) / len(self.concepts)) * 100
        self.updated_at = datetime.now()
    
    def add_completed_concept(self, concept_id: str):
        """Mark a concept as completed"""
        if concept_id not in self.completed_concepts and concept_id in self.concepts:
            self.completed_concepts.append(concept_id)
            self.update_progress()
    
    def get_next_concept(self, available_concepts: Dict[str, Concept]) -> Optional[str]:
        """Get the next concept in the learning path"""
        for concept_id in self.concepts:
            if concept_id not in self.completed_concepts:
                concept = available_concepts.get(concept_id)
                if concept and concept.is_ready_to_learn(set(self.completed_concepts)):
                    return concept_id
        return None


# Concept utility functions
def create_concept_id(name: str) -> str:
    """Create a concept ID from a name"""
    return name.lower().replace(' ', '-').replace('_', '-')

def calculate_concept_difficulty(prerequisites: List[str], complexity_score: float) -> DifficultyLevel:
    """Calculate concept difficulty based on prerequisites and complexity"""
    prerequisite_count = len(prerequisites)
    
    if complexity_score < 2 and prerequisite_count == 0:
        return DifficultyLevel.BEGINNER
    elif complexity_score < 3 and prerequisite_count <= 1:
        return DifficultyLevel.ELEMENTARY
    elif complexity_score < 4 and prerequisite_count <= 2:
        return DifficultyLevel.INTERMEDIATE
    elif complexity_score < 5 and prerequisite_count <= 3:
        return DifficultyLevel.ADVANCED
    else:
        return DifficultyLevel.EXPERT

def generate_learning_objectives(description: str, key_concepts: List[str]) -> List[str]:
    """Generate learning objectives based on description and key concepts"""
    # This would typically use AI/ML to generate meaningful objectives
    # For now, we'll create a simple template-based approach
    objectives = [
        f"Understand the concept of {key_concepts[0] if key_concepts else 'the topic'}",
        f"Apply {key_concepts[1] if len(key_concepts) > 1 else 'the knowledge'} in practical scenarios",
        f"Analyze relationships between {', '.join(key_concepts[:3])}",
        f"Demonstrate mastery through problem-solving"
    ]
    return objectives
