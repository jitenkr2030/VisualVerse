"""
Curriculum Models for VisualVerse Content Metadata Layer

This module provides structured data models for curriculum mapping, including
syllabus units, learning outcomes, assessment criteria, and standardized
benchmarks from common educational frameworks.

Licensed under the Apache License, Version 2.0
"""

from typing import List, Optional, Dict, Any, Set
from datetime import datetime
from pydantic import BaseModel, Field, validator
from enum import Enum
import uuid


class CurriculumFrameworkType(str, Enum):
    """Types of curriculum frameworks"""
    NATIONAL = "national"
    INTERNATIONAL = "international"
    STATE = "state"
    PROPRIETARY = "proprietary"
    CUSTOM = "custom"


class GradeLevel(str, Enum):
    """Educational grade levels"""
    KINDERGARTEN = "K"
    GRADE_1 = "1"
    GRADE_2 = "2"
    GRADE_3 = "3"
    GRADE_4 = "4"
    GRADE_5 = "5"
    GRADE_6 = "6"
    GRADE_7 = "7"
    GRADE_8 = "8"
    GRADE_9 = "9"
    GRADE_10 = "10"
    GRADE_11 = "11"
    GRADE_12 = "12"
    UNDERGRADUATE = "UG"
    GRADUATE = "G"
    PROFESSIONAL = "PROF"


class AssessmentType(str, Enum):
    """Types of assessments"""
    FORMATIVE = "formative"
    SUMMATIVE = "summative"
    DIAGNOSTIC = "diagnostic"
    BENCHMARK = "benchmark"
    PORTFOLIO = "portfolio"
    PERFORMANCE = "performance"


class DifficultyScale(str, Enum):
    """Difficulty scale for curriculum items"""
    FOUNDATIONAL = "foundational"
    DEVELOPING = "developing"
    PROFICIENT = "proficient"
    ADVANCED = "advanced"
    DISTINGUISHED = "distinguished"


class CurriculumFramework(BaseModel):
    """
    Represents a curriculum framework or standard set.
    
    Examples include Common Core State Standards, NGSS, Cambridge International,
    IB Diploma Programme, etc.
    """
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique identifier")
    name: str = Field(..., min_length=1, max_length=200, description="Framework name")
    code: str = Field(..., min_length=1, max_length=50, description="Framework code (e.g., 'CCSS', 'NGSS')")
    framework_type: CurriculumFrameworkType = Field(..., description="Type of framework")
    version: str = Field(default="1.0", description="Framework version")
    region: Optional[str] = Field(None, description="Geographic region (e.g., 'US', 'UK', 'International')")
    description: Optional[str] = Field(None, max_length=2000, description="Framework description")
    subject_scope: List[str] = Field(default_factory=list, description="Subjects covered by this framework")
    grade_range: Tuple[str, str] = Field(default=("K", "12"), description="Grade range (start, end)")
    
    # Metadata
    publisher: Optional[str] = Field(None, description="Organization that publishes the framework")
    publication_date: Optional[datetime] = Field(None, description="Original publication date")
    last_updated: datetime = Field(default_factory=datetime.now, description="Last update timestamp")
    is_active: bool = Field(default=True, description="Whether the framework is active")
    
    class Config:
        schema_extra = {
            "example": {
                "id": "ccss-math",
                "name": "Common Core State Standards - Mathematics",
                "code": "CCSS",
                "framework_type": "national",
                "version": "2023",
                "region": "United States",
                "description": "A set of high-quality academic standards in mathematics",
                "subject_scope": ["mathematics"],
                "grade_range": ("K", "12"),
                "publisher": "National Governors Association",
                "is_active": True
            }
        }


class StandardBenchmark(BaseModel):
    """
    Represents a specific standard or benchmark within a curriculum framework.
    
    These are the granular learning outcomes that students should achieve.
    Example: "CCSS.MATH.CONTENT.HSF.IF.A.1 - Understand that a function..."
    """
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique identifier")
    framework_id: str = Field(..., description="Parent curriculum framework ID")
    code: str = Field(..., max_length=100, description="Standard code (e.g., 'CCSS.MATH.CONTENT.HSF.IF.A.1')")
    category: str = Field(..., max_length=100, description="Category or domain within framework")
    subcategory: Optional[str] = Field(None, max_length=100, description="Subcategory or cluster")
    description: str = Field(..., max_length=2000, description="Standard description")
    
    # Complexity
    difficulty: DifficultyScale = Field(default=DifficultyScale.DEVELOPING, description="Difficulty level")
    grade_levels: List[GradeLevel] = Field(default_factory=list, description="Applicable grade levels")
    
    # Relationships
    parent_standard_id: Optional[str] = Field(None, description="Parent standard ID for hierarchy")
    related_standard_ids: List[str] = Field(default_factory=list, description="Related standard IDs")
    prerequisite_standard_ids: List[str] = Field(default_factory=list, description="Prerequisite standards")
    
    # Content mapping
    suggested_instructional_hours: Optional[float] = Field(None, ge=0, description="Suggested hours")
    assessment_methods: List[AssessmentType] = Field(default_factory=list, description="Recommended assessments")
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update timestamp")
    
    class Config:
        schema_extra = {
            "example": {
                "id": "ccss-hsf-if-a-1",
                "framework_id": "ccss-math",
                "code": "CCSS.MATH.CONTENT.HSF.IF.A.1",
                "category": "Interpreting Functions",
                "subcategory": "Understand the concept of a function",
                "description": "Understand that a function from one set (called the domain) to another set (called the range) assigns to each element of the domain exactly one element of the range.",
                "difficulty": "developing",
                "grade_levels": ["9", "10", "11"],
                "suggested_instructional_hours": 4.0,
                "assessment_methods": ["formative", "summative"]
            }
        }
    
    @validator('code')
    def validate_code(cls, v):
        """Validate standard code format"""
        return v.strip().upper().replace(' ', '-')


class LearningOutcome(BaseModel):
    """
    Represents a specific learning outcome within a syllabus unit.
    
    Learning outcomes are what students should know or be able to do after
    instruction. They are more specific than standards and often derived from
    multiple standards.
    """
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique identifier")
    syllabus_unit_id: str = Field(..., description="Parent syllabus unit ID")
    
    # Content
    outcome_text: str = Field(..., min_length=10, max_length=500, description="Learning outcome description")
    bloom_taxonomy_level: str = Field(default="understand", description="Bloom's taxonomy level")
    cognitive_level: int = Field(default=2, ge=1, le=6, description="Cognitive level (1-6)")
    
    # Standards alignment
    aligned_standard_ids: List[str] = Field(default_factory=list, description="Aligned standard IDs")
    
    # Assessment
    assessment_criteria: List[str] = Field(default_factory=list, description="How to assess this outcome")
    assessment_type: AssessmentType = Field(default=AssessmentType.FORMATIVE, description="Assessment type")
    
    # Metadata
    is_core: bool = Field(default=True, description="Whether this is a core outcome")
    is_optional: bool = Field(default=False, description="Whether this outcome is optional")
    estimated_minutes: int = Field(default=30, ge=5, description="Estimated instructional time")
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    
    class Config:
        schema_extra = {
            "example": {
                "id": "lo-001",
                "syllabus_unit_id": "unit-algebra-basics",
                "outcome_text": "Students will be able to solve linear equations with one variable",
                "bloom_taxonomy_level": "apply",
                "cognitive_level": 3,
                "aligned_standard_ids": ["ccss-8-ee-c7"],
                "assessment_criteria": ["Correctly identifies solution", "Shows work systematically"],
                "assessment_type": "summative",
                "is_core": True,
                "estimated_minutes": 45
            }
        }
    
    @validator('bloom_taxonomy_level')
    def validate_bloom_level(cls, v):
        """Validate Bloom's taxonomy level"""
        valid_levels = ['remember', 'understand', 'apply', 'analyze', 'evaluate', 'create']
        if v.lower() not in valid_levels:
            raise ValueError(f"Bloom's level must be one of: {valid_levels}")
        return v.lower()


class SyllabusUnit(BaseModel):
    """
    Represents a unit within a syllabus or curriculum.
    
    Syllabus units organize learning content into coherent blocks that can
    be delivered over a specific time period (e.g., weeks, months).
    """
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique identifier")
    subject_id: str = Field(..., description="Associated subject ID")
    
    # Identification
    title: str = Field(..., min_length=1, max_length=200, description="Unit title")
    unit_number: int = Field(..., ge=1, description="Unit number in sequence")
    description: Optional[str] = Field(None, max_length=1000, description="Unit description")
    
    # Structure
    section_id: Optional[str] = Field(None, description="Parent section ID")
    parent_unit_id: Optional[str] = Field(None, description="Parent unit ID for nested units")
    sub_units: List[str] = Field(default_factory=list, description="Child unit IDs")
    
    # Learning content
    learning_outcomes: List[LearningOutcome] = Field(default_factory=list, description="Learning outcomes")
    concepts_covered: List[str] = Field(default_factory=list, description="Concept IDs covered in this unit")
    key_topics: List[str] = Field(default_factory=list, description="Key topics")
    
    # Duration
    duration_weeks: float = Field(default=1.0, ge=0.5, description="Duration in weeks")
    total_instructional_hours: float = Field(default=5.0, ge=0.5, description="Total instructional hours")
    
    # Standards alignment
    aligned_standard_ids: List[str] = Field(default_factory=list, description="Aligned standard IDs")
    framework_id: Optional[str] = Field(None, description="Primary framework used")
    
    # Assessment
    assessments: List[Dict[str, Any]] = Field(default_factory=list, description="Unit assessments")
    capstone_activity: Optional[str] = Field(None, description="Capstone or culminating activity")
    
    # Resources
    required_materials: List[str] = Field(default_factory=list, description="Required materials")
    recommended_reading: List[str] = Field(default_factory=list, description="Recommended reading")
    
    # Metadata
    is_required: bool = Field(default=True, description="Whether this unit is required")
    is_elective: bool = Field(default=False, description="Whether this is an elective unit")
    version: str = Field(default="1.0", description="Unit version")
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update timestamp")
    
    class Config:
        schema_extra = {
            "example": {
                "id": "unit-algebra-basics",
                "subject_id": "mathematics",
                "title": "Algebra Basics",
                "unit_number": 1,
                "description": "Introduction to algebraic expressions, equations, and inequalities",
                "duration_weeks": 2.0,
                "total_instructional_hours": 10.0,
                "concepts_covered": ["variables", "expressions", "equations"],
                "key_topics": ["Variables and expressions", "Linear equations", "Inequalities"],
                "aligned_standard_ids": ["ccss-6-ee-a", "ccss-6-ee-b"],
                "is_required": True,
                "version": "1.0"
            }
        }
    
    def add_learning_outcome(self, outcome: LearningOutcome) -> None:
        """Add a learning outcome to this unit"""
        self.learning_outcomes.append(outcome)
        self.update_timestamp()
    
    def add_concept(self, concept_id: str) -> None:
        """Add a concept to this unit"""
        if concept_id not in self.concepts_covered:
            self.concepts_covered.append(concept_id)
            self.update_timestamp()
    
    def update_timestamp(self) -> None:
        """Update the timestamp"""
        self.updated_at = datetime.now()
    
    def get_total_assessment_minutes(self) -> int:
        """Calculate total estimated time for assessments"""
        return sum(outcome.estimated_minutes for outcome in self.learning_outcomes)
    
    def validate_outcomes_coverage(self, concept_ids: Set[str]) -> Dict[str, Any]:
        """Validate that all concepts are covered by learning outcomes"""
        covered = set()
        missing = []
        
        for outcome in self.learning_outcomes:
            # This is a simplified check - in practice would use semantic analysis
            for concept_id in concept_ids:
                if concept_id.lower() in outcome.outcome_text.lower():
                    covered.add(concept_id)
        
        for concept_id in concept_ids:
            if concept_id not in covered:
                missing.append(concept_id)
        
        return {
            "covered_count": len(covered),
            "missing_count": len(missing),
            "missing_concepts": missing,
            "is_complete": len(missing) == 0
        }


class CurriculumSection(BaseModel):
    """
    Represents a major section within a curriculum.
    
    Sections group related syllabus units together and typically correspond
    to major reporting periods (quarters, semesters) or thematic units.
    """
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique identifier")
    subject_id: str = Field(..., description="Associated subject ID")
    curriculum_id: str = Field(..., description="Parent curriculum ID")
    
    # Identification
    name: str = Field(..., min_length=1, max_length=200, description="Section name")
    section_number: int = Field(..., ge=1, description="Section number in sequence")
    description: Optional[str] = Field(None, max_length=1000, description="Section description")
    
    # Content
    unit_ids: List[str] = Field(default_factory=list, description="Unit IDs in this section")
    
    # Duration
    duration_weeks: float = Field(default=9.0, ge=1, description="Duration in weeks")
    
    # Standards coverage
    standard_coverage: Dict[str, List[str]] = Field(default_factory=dict, description="Standards covered by section")
    
    # Assessment
    section_assessment_id: Optional[str] = Field(None, description="Section-wide assessment ID")
    
    # Metadata
    is_required: bool = Field(default=True, description="Whether this section is required")
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    
    class Config:
        schema_extra = {
            "example": {
                "id": "section-algebra-1",
                "subject_id": "mathematics",
                "curriculum_id": "math-hs-algebra",
                "name": "Expressions and Equations",
                "section_number": 2,
                "description": "Students will work with expressions and formulate and solve equations",
                "duration_weeks": 9.0,
                "unit_ids": ["unit-variables", "unit-expressions", "unit-equations"],
                "is_required": True
            }
        }


class Curriculum(BaseModel):
    """
    Represents a complete curriculum for a subject.
    
    A curriculum encompasses the entire scope and sequence of learning for
    a course or program, including all sections, units, and assessments.
    """
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique identifier")
    subject_id: str = Field(..., description="Associated subject ID")
    
    # Identification
    name: str = Field(..., min_length=1, max_length=200, description="Curriculum name")
    description: Optional[str] = Field(None, max_length=2000, description="Curriculum description")
    version: str = Field(default="1.0", description="Curriculum version")
    
    # Structure
    framework_id: Optional[str] = Field(None, description="Primary framework used")
    sections: List[CurriculumSection] = Field(default_factory=list, description="Curriculum sections")
    
    # Duration
    total_weeks: float = Field(default=36.0, ge=1, description="Total curriculum duration in weeks")
    total_instructional_hours: float = Field(default=180.0, ge=1, description="Total instructional hours")
    
    # Standards coverage
    framework_ids: List[str] = Field(default_factory=list, description="Framework IDs referenced")
    standards_covered: List[str] = Field(default_factory=list, description="Standard IDs covered")
    
    # Metadata
    grade_level: GradeLevel = Field(default=GradeLevel.GRADE_9, description="Target grade level")
    is_active: bool = Field(default=True, description="Whether curriculum is active")
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update timestamp")
    
    class Config:
        schema_extra = {
            "example": {
                "id": "math-hs-algebra",
                "subject_id": "mathematics",
                "name": "High School Algebra I",
                "description": "Complete Algebra I curriculum aligned to Common Core standards",
                "version": "2.0",
                "total_weeks": 36.0,
                "total_instructional_hours": 180.0,
                "framework_ids": ["ccss-math"],
                "grade_level": "9",
                "is_active": True
            }
        }
    
    def add_section(self, section: CurriculumSection) -> None:
        """Add a section to the curriculum"""
        self.sections.append(section)
        self.update_timestamp()
    
    def update_timestamp(self) -> None:
        """Update the timestamp"""
        self.updated_at = datetime.now()
    
    def get_standards_coverage_report(self) -> Dict[str, Any]:
        """Generate a report on standards coverage"""
        all_standards = set()
        covered_standards = set()
        
        for section in self.sections:
            for std_list in section.standard_coverage.values():
                all_standards.update(std_list)
        
        for std_id in self.standards_covered:
            covered_standards.add(std_id)
        
        return {
            "total_standards": len(all_standards),
            "covered_standards": len(covered_standards),
            "coverage_percentage": (len(covered_standards) / len(all_standards) * 100) if all_standards else 0,
            "uncovered_standards": list(all_standards - covered_standards)
        }
    
    def calculate_completion_metrics(self, completed_unit_ids: Set[str]) -> Dict[str, Any]:
        """Calculate curriculum completion metrics"""
        total_units = sum(len(section.unit_ids) for section in self.sections)
        completed_units = sum(
            1 for section in self.sections
            for unit_id in section.unit_ids
            if unit_id in completed_unit_ids
        )
        
        return {
            "total_units": total_units,
            "completed_units": completed_units,
            "completion_percentage": (completed_units / total_units * 100) if total_units else 0,
            "estimated_remaining_weeks": (
                (total_units - completed_units) / (total_units / self.total_weeks)
                if total_units > 0 else 0
            )
        }


# ============================================================================
# Request/Response Models
# ============================================================================

class CurriculumFrameworkCreate(BaseModel):
    """Model for creating a curriculum framework"""
    name: str
    code: str
    framework_type: CurriculumFrameworkType
    version: str = "1.0"
    region: Optional[str] = None
    description: Optional[str] = None
    subject_scope: List[str] = None
    grade_range: Tuple[str, str] = ("K", "12")
    publisher: Optional[str] = None


class StandardBenchmarkCreate(BaseModel):
    """Model for creating a standard benchmark"""
    framework_id: str
    code: str
    category: str
    subcategory: Optional[str] = None
    description: str
    difficulty: DifficultyScale = DifficultyScale.DEVELOPING
    grade_levels: List[GradeLevel] = None
    suggested_instructional_hours: Optional[float] = None
    assessment_methods: List[AssessmentType] = None


class SyllabusUnitCreate(BaseModel):
    """Model for creating a syllabus unit"""
    subject_id: str
    title: str
    unit_number: int
    section_id: Optional[str] = None
    description: Optional[str] = None
    duration_weeks: float = 1.0
    total_instructional_hours: float = 5.0
    concepts_covered: List[str] = None
    key_topics: List[str] = None
    aligned_standard_ids: List[str] = None


class LearningOutcomeCreate(BaseModel):
    """Model for creating a learning outcome"""
    syllabus_unit_id: str
    outcome_text: str
    bloom_taxonomy_level: str = "understand"
    aligned_standard_ids: List[str] = None
    assessment_criteria: List[str] = None
    assessment_type: AssessmentType = AssessmentType.FORMATIVE
    is_core: bool = True
    estimated_minutes: int = 30


# ============================================================================
# Import Utility Functions
# ============================================================================

def parse_standards_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Parse a standards file (JSON or YAML) into a list of benchmark dictionaries.
    
    Args:
        file_path: Path to the standards file
        
    Returns:
        List of standard benchmark data dictionaries
    """
    import json
    import yaml
    
    with open(file_path, 'r', encoding='utf-8') as f:
        if file_path.endswith('.yaml') or file_path.endswith('.yml'):
            data = yaml.safe_load(f)
        else:
            data = json.load(f)
    
    if isinstance(data, dict):
        if 'standards' in data:
            return data['standards']
        elif 'benchmarks' in data:
            return data['benchmarks']
        elif 'items' in data:
            return data['items']
        else:
            return [data]
    elif isinstance(data, list):
        return data
    else:
        return []


def create_standards_from_data(
    framework_id: str,
    standards_data: List[Dict[str, Any]]
) -> List[StandardBenchmark]:
    """
    Create StandardBenchmark objects from parsed data.
    
    Args:
        framework_id: Parent framework ID
        standards_data: List of standard data dictionaries
        
    Returns:
        List of StandardBenchmark objects
    """
    benchmarks = []
    
    for item in standards_data:
        grade_levels = item.get('grade_levels', [])
        if isinstance(grade_levels, str):
            grade_levels = [grade_levels]
        
        assessment_methods = item.get('assessment_methods', [])
        if isinstance(assessment_methods, str):
            assessment_methods = [assessment_methods]
        
        benchmark = StandardBenchmark(
            framework_id=framework_id,
            code=item.get('code', ''),
            category=item.get('category', ''),
            subcategory=item.get('subcategory'),
            description=item.get('description', ''),
            difficulty=DifficultyScale(item.get('difficulty', 'developing')),
            grade_levels=[GradeLevel(g) for g in grade_levels],
            suggested_instructional_hours=item.get('suggested_instructional_hours'),
            assessment_methods=[AssessmentType(a) for a in assessment_methods]
        )
        benchmarks.append(benchmark)
    
    return benchmarks
