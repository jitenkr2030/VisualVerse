"""
Core schema definitions for VisualVerse.
These are the universal data structures that all subjects must use.
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from enum import Enum
import uuid

class DifficultyLevel(str, Enum):
    """Difficulty levels for any concept"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate" 
    ADVANCED = "advanced"
    EXPERT = "expert"

class LessonType(str, Enum):
    """Types of lessons across all subjects"""
    CONCEPT = "concept"
    EXAMPLE = "example"
    PRACTICE = "practice"
    ASSESSMENT = "assessment"
    REVIEW = "review"

class ConceptNode(BaseModel):
    """
    Universal content node that all subjects must inherit from.
    This represents any learning concept across any subject.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    difficulty: DifficultyLevel
    estimated_duration: int = Field(ge=1, le=180, description="Duration in minutes")
    prerequisites: List[str] = Field(default_factory=list, description="IDs of prerequisite concepts")
    learning_objectives: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "derivative_basic",
                "title": "Introduction to Derivatives",
                "description": "Understanding the concept of derivatives in calculus",
                "difficulty": "intermediate",
                "estimated_duration": 30,
                "prerequisites": ["limits_basic"],
                "learning_objectives": [
                    "Understand the geometric meaning of derivatives",
                    "Calculate basic derivatives using limit definition"
                ],
                "tags": ["calculus", "derivatives", "limits"],
                "metadata": {
                    "subject": "mathematics",
                    "chapter": "calculus",
                    "visual_elements": ["graphs", "tangents"]
                }
            }
        }

class LessonNode(BaseModel):
    """
    A specific lesson that teaches a concept.
    Contains the actual content and visual elements.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    concept_id: str
    title: str
    content: str = Field(description="Lesson content in Markdown format")
    lesson_type: LessonType
    visual_script: Optional[str] = Field(None, description="Manim animation script")
    exercises: List[Dict] = Field(default_factory=list)
    media_files: List[str] = Field(default_factory=list)
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "derivative_intro_lesson",
                "concept_id": "derivative_basic",
                "title": "What is a Derivative?",
                "content": "A derivative represents the rate of change of a function...",
                "lesson_type": "concept",
                "visual_script": "manim_script_here",
                "exercises": [
                    {
                        "type": "multiple_choice",
                        "question": "What does a derivative represent?",
                        "options": ["Slope", "Area", "Volume", "Distance"]
                    }
                ]
            }
        }

class UserProgress(BaseModel):
    """
    Tracks a student's progress through concepts.
    """
    user_id: str
    concept_id: str
    status: str = Field(ge=1, description="Completion percentage")
    last_accessed: str
    time_spent: int = Field(default=0, description="Time spent in minutes")
    score: Optional[float] = Field(None, ge=0, le=100)
    
class DependencyGraph:
    """
    Manages the dependency relationships between concepts.
    This is a Directed Acyclic Graph (DAG) where nodes represent concepts.
    """
    
    def __init__(self):
        self.graph: Dict[str, List[str]] = {}  # concept_id -> list of dependent concept_ids
        self.reverse_graph: Dict[str, List[str]] = {}  # concept_id -> list of prerequisite concept_ids
        
    def add_dependency(self, concept_id: str, depends_on: str):
        """Add a dependency relationship"""
        if concept_id not in self.graph:
            self.graph[concept_id] = []
        if depends_on not in self.reverse_graph:
            self.reverse_graph[depends_on] = []
            
        self.graph[concept_id].append(depends_on)
        self.reverse_graph[depends_on].append(concept_id)
        
    def get_prerequisites(self, concept_id: str) -> List[str]:
        """Get all prerequisites for a concept"""
        return self.graph.get(concept_id, [])
        
    def get_dependents(self, concept_id: str) -> List[str]:
        """Get all concepts that depend on this concept"""
        return self.reverse_graph.get(concept_id, [])
        
    def is_unlocked(self, concept_id: str, completed_concepts: List[str]) -> bool:
        """Check if a concept is unlocked based on completed prerequisites"""
        prerequisites = self.get_prerequisites(concept_id)
        return all(req in completed_concepts for req in prerequisites)
        
    def get_next_available(self, completed_concepts: List[str], all_concepts: List[str]) -> List[str]:
        """Get concepts that are available for learning next"""
        available = []
        for concept_id in all_concepts:
            if concept_id not in completed_concepts and self.is_unlocked(concept_id, completed_concepts):
                available.append(concept_id)
        return available

class ConceptMap(BaseModel):
    """
    Complete map of all concepts in a subject vertical.
    """
    subject: str
    version: str
    concepts: Dict[str, ConceptNode]
    lessons: Dict[str, LessonNode]
    dependency_graph: Dict[str, List[str]]
    
    def get_concept(self, concept_id: str) -> Optional[ConceptNode]:
        """Get a specific concept by ID"""
        return self.concepts.get(concept_id)
        
    def get_lesson(self, lesson_id: str) -> Optional[LessonNode]:
        """Get a specific lesson by ID"""
        return self.lessons.get(lesson_id)
        
    def get_concept_lessons(self, concept_id: str) -> List[LessonNode]:
        """Get all lessons for a specific concept"""
        return [lesson for lesson in self.lessons.values() if lesson.concept_id == concept_id]