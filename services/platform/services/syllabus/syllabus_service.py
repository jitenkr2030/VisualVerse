"""
Syllabus Tagging Service - Core Implementation

This module provides the core functionality for curriculum alignment and
syllabus tagging in the VisualVerse Creator Platform. It supports multiple
educational boards, grade levels, subjects, and learning objectives.

Author: MiniMax Agent
Version: 1.0.0
"""

from typing import Dict, List, Optional, Any, Tuple, Set
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json
import re
import logging
import threading

from visualverse.platform.packages.shared_types import (
    SyllabusTag as DomainSyllabusTag,
    CurriculumBoard as DomainCurriculumBoard,
)


logger = logging.getLogger(__name__)


class EducationLevel(str, Enum):
    """Education levels for content categorization."""
    PRIMARY = "primary"
    MIDDLE = "middle"
    SECONDARY = "secondary"
    HIGHER_SECONDARY = "higher_secondary"
    UNDERGRADUATE = "undergraduate"
    GRADUATE = "graduate"
    PROFESSIONAL = "professional"


class SubjectArea(str, Enum):
    """Subject areas for content categorization."""
    MATHEMATICS = "mathematics"
    PHYSICS = "physics"
    CHEMISTRY = "chemistry"
    BIOLOGY = "biology"
    COMPUTER_SCIENCE = "computer_science"
    ECONOMICS = "economics"
    FINANCE = "finance"


class DifficultyLevel(str, Enum):
    """Difficulty levels for learning content."""
    FOUNDATIONAL = "foundational"
    DEVELOPING = "developing"
    PROFICIENT = "proficient"
    ADVANCED = "advanced"
    EXPERT = "expert"


# Supported curriculum boards with their metadata
SUPPORTED_BOARDS = {
    "CBSE": {
        "name": "Central Board of Secondary Education",
        "country": "India",
        "levels": ["primary", "middle", "secondary", "higher_secondary"],
        "subjects": ["mathematics", "physics", "chemistry", "biology", "computer_science"]
    },
    "ICSE": {
        "name": "Indian Certificate of Secondary Education",
        "country": "India",
        "levels": ["secondary", "higher_secondary"],
        "subjects": ["mathematics", "physics", "chemistry", "biology", "computer_science"]
    },
    "IB": {
        "name": "International Baccalaureate",
        "country": "International",
        "levels": ["primary", "middle", "secondary", "higher_secondary"],
        "subjects": ["mathematics", "physics", "chemistry", "biology", "economics"]
    },
    "NCERT": {
        "name": "National Council of Educational Research and Training",
        "country": "India",
        "levels": ["primary", "middle", "secondary", "higher_secondary"],
        "subjects": ["mathematics", "physics", "chemistry", "biology"]
    },
    "STATE": {
        "name": "State Board",
        "country": "India",
        "levels": ["primary", "middle", "secondary", "higher_secondary"],
        "subjects": ["mathematics", "physics", "chemistry", "biology"]
    }
}


@dataclass
class CurriculumBoard:
    """
    Curriculum board representation with metadata.
    
    Attributes:
        id: Unique board identifier
        code: Board code (e.g., CBSE, ICSE)
        name: Full board name
        country: Country of origin
        description: Board description
        supported_levels: List of supported education levels
        supported_subjects: List of supported subjects
        is_active: Whether the board is active
        created_at: When the board was added
        updated_at: Last update timestamp
    """
    id: str
    code: str
    name: str
    country: str = "India"
    description: str = ""
    supported_levels: List[str] = field(default_factory=list)
    supported_subjects: List[str] = field(default_factory=list)
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "country": self.country,
            "description": self.description,
            "supportedLevels": self.supported_levels,
            "supportedSubjects": self.supported_subjects,
            "isActive": self.is_active,
            "createdAt": self.created_at.isoformat(),
            "updatedAt": self.updated_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CurriculumBoard':
        return cls(
            id=data["id"],
            code=data["code"],
            name=data["name"],
            country=data.get("country", "India"),
            description=data.get("description", ""),
            supported_levels=data.get("supportedLevels", []),
            supported_subjects=data.get("supportedSubjects", []),
            is_active=data.get("isActive", True),
            created_at=datetime.fromisoformat(data["createdAt"]) if isinstance(data["createdAt"], str) else data["createdAt"],
            updated_at=datetime.fromisoformat(data["updatedAt"]) if isinstance(data["updatedAt"], str) else data["updatedAt"]
        )


@dataclass
class SyllabusTag:
    """
    Syllabus tag representing a specific topic or standard in a curriculum.
    
    Attributes:
        id: Unique tag identifier
        board_id: Associated curriculum board
        code: Standard code (e.g., PHY-12-01)
        subject: Subject area
        topic: Main topic
        sub_topic: Sub-topic (optional)
        grade_level: Education grade level
        description: Tag description
        keywords: Searchable keywords
        prerequisites: List of prerequisite tag IDs
        learning_objectives: List of learning objectives
        estimated_hours: Suggested study hours
        difficulty: Content difficulty level
        is_active: Whether the tag is active
        usage_count: Number of times this tag is used
        created_at: When the tag was created
        updated_at: Last update timestamp
    """
    id: str
    board_id: str
    code: str
    subject: str
    topic: str
    sub_topic: Optional[str] = None
    grade_level: int = 10
    description: str = ""
    keywords: List[str] = field(default_factory=list)
    prerequisites: List[str] = field(default_factory=list)
    learning_objectives: List[str] = field(default_factory=list)
    estimated_hours: float = 1.0
    difficulty: str = "developing"
    is_active: bool = True
    usage_count: int = 0
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "boardId": self.board_id,
            "code": self.code,
            "subject": self.subject,
            "topic": self.topic,
            "subTopic": self.sub_topic,
            "gradeLevel": self.grade_level,
            "description": self.description,
            "keywords": self.keywords,
            "prerequisites": self.prerequisites,
            "learningObjectives": self.learning_objectives,
            "estimatedHours": self.estimated_hours,
            "difficulty": self.difficulty,
            "isActive": self.is_active,
            "usageCount": self.usage_count,
            "createdAt": self.created_at.isoformat(),
            "updatedAt": self.updated_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SyllabusTag':
        return cls(
            id=data["id"],
            board_id=data["boardId"],
            code=data["code"],
            subject=data["subject"],
            topic=data["topic"],
            sub_topic=data.get("subTopic"),
            grade_level=data.get("gradeLevel", 10),
            description=data.get("description", ""),
            keywords=data.get("keywords", []),
            prerequisites=data.get("prerequisites", []),
            learning_objectives=data.get("learningObjectives", []),
            estimated_hours=data.get("estimatedHours", 1.0),
            difficulty=data.get("difficulty", "developing"),
            is_active=data.get("isActive", True),
            usage_count=data.get("usageCount", 0),
            created_at=datetime.fromisoformat(data["createdAt"]) if isinstance(data["createdAt"], str) else data["createdAt"],
            updated_at=datetime.fromisoformat(data["updatedAt"]) if isinstance(data["updatedAt"], str) else data["updatedAt"]
        )
    
    @property
    def full_path(self) -> str:
        """Get the full hierarchical path for this tag."""
        path = f"{self.subject} > {self.topic}"
        if self.sub_topic:
            path += f" > {self.sub_topic}"
        path += f" (Grade {self.grade_level})"
        return path
    
    @property
    def search_text(self) -> str:
        """Get searchable text for this tag."""
        parts = [
            self.code,
            self.subject,
            self.topic,
            self.sub_topic or "",
            self.description,
            " ".join(self.keywords)
        ]
        return " ".join(parts).lower()


@dataclass
class TagSearchResult:
    """
    Result of a tag search operation.
    
    Attributes:
        tags: List of matching tags
        total_count: Total number of matches
        query: Search query used
        filters: Filters applied
        facets: Faceted search results
    """
    tags: List[SyllabusTag]
    total_count: int
    query: str = ""
    filters: Dict[str, Any] = field(default_factory=dict)
    facets: Dict[str, Dict[str, int]] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "tags": [t.to_dict() for t in self.tags],
            "totalCount": self.total_count,
            "query": self.query,
            "filters": self.filters,
            "facets": self.facets
        }


@dataclass
class ContentTagAssociation:
    """
    Association between content and syllabus tags.
    
    Attributes:
        content_id: Associated content identifier
        tag_id: Associated tag identifier
        confidence: Association confidence (0-1)
        relevance_score: Relevance score (0-1)
        manual_override: Whether this was manually assigned
        assigned_by: User who assigned the tag (if manual)
        assigned_at: When the association was created
        notes: Additional notes about the association
    """
    content_id: str
    tag_id: str
    confidence: float = 1.0
    relevance_score: float = 1.0
    manual_override: bool = False
    assigned_by: Optional[str] = None
    assigned_at: datetime = field(default_factory=datetime.utcnow)
    notes: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "contentId": self.content_id,
            "tagId": self.tag_id,
            "confidence": self.confidence,
            "relevanceScore": self.relevance_score,
            "manualOverride": self.manual_override,
            "assignedBy": self.assigned_by,
            "assignedAt": self.assigned_at.isoformat(),
            "notes": self.notes
        }


@dataclass
class ContentAlignmentReport:
    """
    Report on content alignment with curriculum standards.
    
    Attributes:
        content_id: Content identifier
        coverage_score: Percentage of topics covered
        aligned_tags: Tags that are aligned
        missing_tags: Tags that should be covered but aren't
        prerequisite_gaps: Missing prerequisite topics
        difficulty_match: How well difficulty matches target audience
        suggestions: Suggestions for improvement
    """
    content_id: str
    coverage_score: float
    aligned_tags: List[SyllabusTag] = field(default_factory=list)
    missing_tags: List[SyllabusTag] = field(default_factory=list)
    prerequisite_gaps: List[SyllabusTag] = field(default_factory=list)
    difficulty_match: float = 0.0
    suggestions: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "contentId": self.content_id,
            "coverageScore": self.coverage_score,
            "alignedTags": [t.to_dict() for t in self.aligned_tags],
            "missingTags": [t.to_dict() for t in self.missing_tags],
            "prerequisiteGaps": [t.to_dict() for t in self.prerequisite_gaps],
            "difficultyMatch": self.difficulty_match,
            "suggestions": self.suggestions
        }


class SyllabusTaggingService:
    """
    Core service for curriculum alignment and syllabus tagging.
    
    This service manages:
    - Curriculum board definitions and management
    - Syllabus tag creation, updating, and deletion
    - Content-to-tag associations
    - Tag search and discovery
    - Content alignment analysis
    - Prerequisites tracking
    
    Attributes:
        storage_dir: Directory for persisting data
        boards: Dictionary of curriculum boards by ID
        tags: Dictionary of syllabus tags by ID
        content_associations: Dictionary of content-tag associations
        index: Search index for tags
        lock: Thread lock for concurrent operations
    """
    
    def __init__(self, storage_dir: str = None):
        """
        Initialize the syllabus tagging service.
        
        Args:
            storage_dir: Directory for persisting data
        """
        self.storage_dir = storage_dir or "/tmp/visualverse-syllabus"
        
        self.boards: Dict[str, CurriculumBoard] = {}
        self.tags: Dict[str, SyllabusTag] = {}
        self.content_associations: Dict[str, List[ContentTagAssociation]] = {}
        self.tag_index: Dict[str, Set[str]] = {}  # keyword -> tag IDs
        self.code_index: Dict[str, str] = {}  # code -> tag ID
        
        self.lock = threading.RLock()
        
        # Load existing data
        self._load_state()
        
        # Initialize default boards if none exist
        if not self.boards:
            self._initialize_default_boards()
        
        logger.info(f"SyllabusTaggingService initialized with {len(self.tags)} tags")
    
    def _load_state(self):
        """Load persisted state from storage."""
        import os
        os.makedirs(self.storage_dir, exist_ok=True)
        
        boards_file = f"{self.storage_dir}/boards.json"
        tags_file = f"{self.storage_dir}/tags.json"
        associations_file = f"{self.storage_dir}/associations.json"
        
        if os.path.exists(boards_file):
            try:
                with open(boards_file, 'r') as f:
                    data = json.load(f)
                    self.boards = {
                        b["id"]: CurriculumBoard.from_dict(b) 
                        for b in data
                    }
            except Exception as e:
                logger.warning(f"Failed to load boards: {e}")
        
        if os.path.exists(tags_file):
            try:
                with open(tags_file, 'r') as f:
                    data = json.load(f)
                    self.tags = {
                        t["id"]: SyllabusTag.from_dict(t) 
                        for t in data
                    }
                    self._rebuild_index()
            except Exception as e:
                logger.warning(f"Failed to load tags: {e}")
        
        if os.path.exists(associations_file):
            try:
                with open(associations_file, 'r') as f:
                    data = json.load(f)
                    for content_id, associations in data.items():
                        self.content_associations[content_id] = [
                            ContentTagAssociation(**a) for a in associations
                        ]
            except Exception as e:
                logger.warning(f"Failed to load associations: {e}")
    
    def _save_state(self):
        """Persist state to storage."""
        with self.lock:
            boards_file = f"{self.storage_dir}/boards.json"
            tags_file = f"{self.storage_dir}/tags.json"
            associations_file = f"{self.storage_dir}/associations.json"
            
            with open(boards_file, 'w') as f:
                json.dump(
                    [b.to_dict() for b in self.boards.values()], 
                    f, indent=2
                )
            
            with open(tags_file, 'w') as f:
                json.dump(
                    [t.to_dict() for t in self.tags.values()], 
                    f, indent=2
                )
            
            with open(associations_file, 'w') as f:
                json.dump(
                    {
                        cid: [a.to_dict() for a in assoc] 
                        for cid, assoc in self.content_associations.items()
                    }, 
                    f, indent=2
                )
    
    def _rebuild_index(self):
        """Rebuild the search index."""
        self.tag_index.clear()
        self.code_index.clear()
        
        for tag_id, tag in self.tags.items():
            # Index by code
            self.code_index[tag.code.lower()] = tag_id
            
            # Index by keywords
            for keyword in tag.keywords:
                keyword = keyword.lower().strip()
                if keyword:
                    if keyword not in self.tag_index:
                        self.tag_index[keyword] = set()
                    self.tag_index[keyword].add(tag_id)
            
            # Index by subject and topic
            for word in tag.subject.lower().split():
                if len(word) > 2:
                    if word not in self.tag_index:
                        self.tag_index[word] = set()
                    self.tag_index[word].add(tag_id)
            
            for word in re.split(r'[\\s\\-]+', tag.topic.lower()):
                if len(word) > 2:
                    if word not in self.tag_index:
                        self.tag_index[word] = set()
                    self.tag_index[word].add(tag_id)
    
    def _initialize_default_boards(self):
        """Initialize default curriculum boards."""
        for code, info in SUPPORTED_BOARDS.items():
            board = CurriculumBoard(
                id=f"board-{code.lower()}",
                code=code,
                name=info["name"],
                country=info["country"],
                supported_levels=info["levels"],
                supported_subjects=info["subjects"]
            )
            self.boards[board.id] = board
        
        # Initialize common syllabus tags
        self._initialize_common_tags()
        
        self._save_state()
    
    def _initialize_common_tags(self):
        """Initialize common syllabus tags for all boards."""
        common_tags = [
            # Mathematics
            {
                "code": "MATH-ALG-01",
                "subject": "mathematics",
                "topic": "Algebra",
                "sub_topic": "Linear Equations",
                "grade_level": 8,
                "description": "Solving linear equations in one variable",
                "keywords": ["equation", "variable", "solve", "linear"]
            },
            {
                "code": "MATH-ALG-02",
                "subject": "mathematics",
                "topic": "Algebra",
                "sub_topic": "Quadratic Equations",
                "grade_level": 10,
                "description": "Solving quadratic equations using various methods",
                "keywords": ["quadratic", "parabola", "discriminant", "roots"]
            },
            {
                "code": "MATH-GEOM-01",
                "subject": "mathematics",
                "topic": "Geometry",
                "sub_topic": "Triangles",
                "grade_level": 9,
                "description": "Properties and theorems related to triangles",
                "keywords": ["triangle", "congruence", "similarity", "pythagoras"]
            },
            {
                "code": "MATH-CALC-01",
                "subject": "mathematics",
                "topic": "Calculus",
                "sub_topic": "Limits",
                "grade_level": 11,
                "description": "Introduction to limits and continuity",
                "keywords": ["limit", "continuity", "approach", "infinity"]
            },
            # Physics
            {
                "code": "PHY-KIN-01",
                "subject": "physics",
                "topic": "Kinematics",
                "sub_topic": "Motion in One Dimension",
                "grade_level": 9,
                "description": "Understanding motion along a straight line",
                "keywords": ["motion", "velocity", "acceleration", "displacement"]
            },
            {
                "code": "PHY-KIN-02",
                "subject": "physics",
                "topic": "Kinematics",
                "sub_topic": "Projectile Motion",
                "grade_level": 10,
                "description": "Analysis of projectile motion under gravity",
                "keywords": ["projectile", "trajectory", "gravity", "parabola"]
            },
            {
                "code": "PHY-DYN-01",
                "subject": "physics",
                "topic": "Dynamics",
                "sub_topic": "Newton's Laws",
                "grade_level": 9,
                "description": "Understanding Newton's three laws of motion",
                "keywords": ["newton", "force", "inertia", "action", "reaction"]
            },
            {
                "code": "PHY-WAV-01",
                "subject": "physics",
                "topic": "Waves",
                "sub_topic": "Wave Properties",
                "grade_level": 11,
                "description": "Characteristics and properties of waves",
                "keywords": ["wave", "frequency", "wavelength", "amplitude"]
            },
            # Chemistry
            {
                "code": "CHEM-ATO-01",
                "subject": "chemistry",
                "topic": "Atomic Structure",
                "sub_topic": "Electron Configuration",
                "grade_level": 9,
                "description": "Understanding electron arrangement in atoms",
                "keywords": ["atom", "electron", "orbital", "shell", "configuration"]
            },
            {
                "code": "CHEM-BON-01",
                "subject": "chemistry",
                "topic": "Chemical Bonding",
                "sub_topic": "Ionic and Covalent Bonds",
                "grade_level": 9,
                "description": "Types of chemical bonds and their properties",
                "keywords": ["bond", "ionic", "covalent", "electron", "valence"]
            },
            {
                "code": "CHEM-REA-01",
                "subject": "chemistry",
                "topic": "Chemical Reactions",
                "sub_topic": "Balancing Equations",
                "grade_level": 8,
                "description": "Writing and balancing chemical equations",
                "keywords": ["reaction", "equation", "balance", "coefficient"]
            },
            # Algorithms
            {
                "code": "ALG-SRT-01",
                "subject": "computer_science",
                "topic": "Sorting",
                "sub_topic": "Basic Sorting Algorithms",
                "grade_level": 10,
                "description": "Introduction to bubble sort, selection sort",
                "keywords": ["sort", "bubble", "selection", "algorithm"]
            },
            {
                "code": "ALG-SRH-01",
                "subject": "computer_science",
                "topic": "Searching",
                "sub_topic": "Binary Search",
                "grade_level": 10,
                "description": "Understanding binary search algorithm",
                "keywords": ["search", "binary", "divide", "conquer", "logarithmic"]
            }
        ]
        
        for i, tag_data in enumerate(common_tags):
            tag = SyllabusTag(
                id=f"tag-{i+1:03d}",
                board_id="board-cbse",
                **tag_data
            )
            self.tags[tag.id] = tag
        
        self._rebuild_index()
    
    # Board management methods
    def add_board(self, code: str, name: str, country: str = "India",
                  description: str = "", levels: List[str] = None,
                  subjects: List[str] = None) -> CurriculumBoard:
        """
        Add a new curriculum board.
        
        Args:
            code: Board code (e.g., CBSE, ICSE)
            name: Board name
            country: Country of origin
            description: Board description
            supported_levels: List of supported education levels
            supported_subjects: List of supported subjects
            
        Returns:
            Created CurriculumBoard object
        """
        with self.lock:
            board_id = f"board-{code.lower()}"
            
            if board_id in self.boards:
                raise ValueError(f"Board '{code}' already exists")
            
            board = CurriculumBoard(
                id=board_id,
                code=code,
                name=name,
                country=country,
                description=description,
                supported_levels=levels or [],
                supported_subjects=subjects or []
            )
            
            self.boards[board_id] = board
            self._save_state()
            
            logger.info(f"Board added: {code}")
            return board
    
    def get_board(self, board_id: str) -> Optional[CurriculumBoard]:
        """
        Get a curriculum board by ID.
        
        Args:
            board_id: Board identifier
            
        Returns:
            CurriculumBoard or None if not found
        """
        return self.boards.get(board_id)
    
    def list_boards(self, active_only: bool = True) -> List[CurriculumBoard]:
        """
        List all curriculum boards.
        
        Args:
            active_only: Only return active boards
            
        Returns:
            List of CurriculumBoard objects
        """
        boards = list(self.boards.values())
        if active_only:
            boards = [b for b in boards if b.is_active]
        return boards
    
    # Tag management methods
    def create_tag(self, board_id: str, code: str, subject: str, topic: str,
                   sub_topic: str = None, grade_level: int = 10,
                   description: str = "", keywords: List[str] = None,
                   prerequisites: List[str] = None,
                   learning_objectives: List[str] = None,
                   estimated_hours: float = 1.0,
                   difficulty: str = "developing") -> SyllabusTag:
        """
        Create a new syllabus tag.
        
        Args:
            board_id: Associated curriculum board
            code: Standard code
            subject: Subject area
            topic: Main topic
            sub_topic: Sub-topic (optional)
            grade_level: Target grade level
            description: Tag description
            keywords: Searchable keywords
            prerequisites: Prerequisite tag IDs
            learning_objectives: Learning objectives
            estimated_hours: Suggested study hours
            difficulty: Content difficulty level
            
        Returns:
            Created SyllabusTag object
        """
        with self.lock:
            if board_id not in self.boards:
                raise ValueError(f"Board not found: {board_id}")
            
            # Generate unique ID
            tag_id = f"tag-{len(self.tags) + 1:05d}"
            
            # Check for duplicate code
            if code.lower() in self.code_index:
                raise ValueError(f"Tag with code '{code}' already exists")
            
            tag = SyllabusTag(
                id=tag_id,
                board_id=board_id,
                code=code,
                subject=subject,
                topic=topic,
                sub_topic=sub_topic,
                grade_level=grade_level,
                description=description,
                keywords=keywords or [],
                prerequisites=prerequisites or [],
                learning_objectives=learning_objectives or [],
                estimated_hours=estimated_hours,
                difficulty=difficulty
            )
            
            self.tags[tag_id] = tag
            self.code_index[code.lower()] = tag_id
            
            # Index keywords
            for keyword in tag.keywords:
                keyword = keyword.lower().strip()
                if keyword:
                    if keyword not in self.tag_index:
                        self.tag_index[keyword] = set()
                    self.tag_index[keyword].add(tag_id)
            
            self._save_state()
            
            logger.info(f"Tag created: {code}")
            return tag
    
    def get_tag(self, tag_id: str) -> Optional[SyllabusTag]:
        """
        Get a syllabus tag by ID.
        
        Args:
            tag_id: Tag identifier
            
        Returns:
            SyllabusTag or None if not found
        """
        return self.tags.get(tag_id)
    
    def get_tag_by_code(self, code: str) -> Optional[SyllabusTag]:
        """
        Get a syllabus tag by code.
        
        Args:
            code: Tag code
            
        Returns:
            SyllabusTag or None if not found
        """
        tag_id = self.code_index.get(code.lower())
        if tag_id:
            return self.tags.get(tag_id)
        return None
    
    def update_tag(self, tag_id: str, **updates) -> Optional[SyllabusTag]:
        """
        Update a syllabus tag.
        
        Args:
            tag_id: Tag to update
            **updates: Fields to update
            
        Returns:
            Updated SyllabusTag or None if not found
        """
        with self.lock:
            if tag_id not in self.tags:
                return None
            
            tag = self.tags[tag_id]
            
            for field, value in updates.items():
                if hasattr(tag, field) and field not in ["id", "board_id", "code"]:
                    setattr(tag, field, value)
            
            tag.updated_at = datetime.utcnow()
            
            self._rebuild_index()
            self._save_state()
            
            logger.info(f"Tag updated: {tag.code}")
            return tag
    
    def delete_tag(self, tag_id: str) -> bool:
        """
        Delete a syllabus tag.
        
        Args:
            tag_id: Tag to delete
            
        Returns:
            True if deleted, False if not found
        """
        with self.lock:
            if tag_id not in self.tags:
                return False
            
            tag = self.tags[tag_id]
            del self.code_index[tag.code.lower()]
            
            # Remove from index
            for keyword in tag.keywords:
                keyword = keyword.lower()
                if keyword in self.tag_index:
                    self.tag_index[keyword].discard(tag_id)
            
            del self.tags[tag_id]
            self._save_state()
            
            logger.info(f"Tag deleted: {tag_id}")
            return True
    
    def list_tags(self, board_id: str = None, subject: str = None,
                  grade_level: int = None, active_only: bool = True) -> List[SyllabusTag]:
        """
        List syllabus tags with optional filters.
        
        Args:
            board_id: Filter by board
            subject: Filter by subject
            grade_level: Filter by grade level
            active_only: Only return active tags
            
        Returns:
            List of SyllabusTag objects
        """
        tags = list(self.tags.values())
        
        if board_id:
            tags = [t for t in tags if t.board_id == board_id]
        if subject:
            tags = [t for t in tags if t.subject == subject]
        if grade_level is not None:
            tags = [t for t in tags if t.grade_level == grade_level]
        if active_only:
            tags = [t for t in tags if t.is_active]
        
        return tags
    
    # Search methods
    def search_tags(self, query: str, board_id: str = None,
                    subject: str = None, grade_level: int = None,
                    limit: int = 20, offset: int = 0) -> TagSearchResult:
        """
        Search for syllabus tags.
        
        Args:
            query: Search query
            board_id: Filter by board
            subject: Filter by subject
            grade_level: Filter by grade level
            limit: Maximum results to return
            offset: Offset for pagination
            
        Returns:
            TagSearchResult with matching tags
        """
        query = query.lower().strip()
        matching_ids: Set[str] = None
        
        # Check for exact code match first
        if query.upper() in self.code_index:
            tag = self.tags.get(self.code_index[query.upper()])
            if tag:
                return TagSearchResult(
                    tags=[tag],
                    total_count=1,
                    query=query
                )
        
        # Search by keywords
        words = re.split(r'\\s+', query)
        for word in words:
            if len(word) > 2:
                if word in self.tag_index:
                    if matching_ids is None:
                        matching_ids = set(self.tag_index[word].copy())
                    else:
                        matching_ids &= self.tag_index[word]
        
        if matching_ids is None:
            matching_ids = set()
        
        # If no keyword matches, search in all tags
        if not matching_ids:
            for tag in self.tags.values():
                if query in tag.search_text:
                    matching_ids.add(tag.id)
        
        # Apply filters
        filtered_tags = []
        for tag_id in matching_ids:
            tag = self.tags.get(tag_id)
            if not tag:
                continue
            
            if not tag.is_active:
                continue
            
            if board_id and tag.board_id != board_id:
                continue
            
            if subject and tag.subject != subject:
                continue
            
            if grade_level is not None and tag.grade_level != grade_level:
                continue
            
            filtered_tags.append(tag)
        
        # Build facets
        subjects = {}
        grades = {}
        boards = {}
        
        for tag in filtered_tags:
            subjects[tag.subject] = subjects.get(tag.subject, 0) + 1
            grades[tag.grade_level] = grades.get(tag.grade_level, 0) + 1
            boards[tag.board_id] = boards.get(tag.board_id, 0) + 1
        
        # Sort by relevance (simple: exact matches first)
        filtered_tags.sort(key=lambda t: (
            not any(query == kw for kw in t.keywords),
            not (query in t.code.lower()),
            t.usage_count
        ), reverse=True)
        
        total = len(filtered_tags)
        paginated_tags = filtered_tags[offset:offset + limit]
        
        return TagSearchResult(
            tags=paginated_tags,
            total_count=total,
            query=query,
            filters={
                "boardId": board_id,
                "subject": subject,
                "gradeLevel": grade_level
            },
            facets={
                "subjects": subjects,
                "grades": grades,
                "boards": boards
            }
        )
    
    def get_tag_hierarchy(self, board_id: str) -> Dict[str, Any]:
        """
        Get the hierarchical structure of tags for a board.
        
        Args:
            board_id: Board identifier
            
        Returns:
            Hierarchical structure with subjects, topics, and tags
        """
        tags = self.list_tags(board_id=board_id)
        
        hierarchy = {}
        
        for tag in tags:
            if tag.subject not in hierarchy:
                hierarchy[tag.subject] = {}
            
            if tag.topic not in hierarchy[tag.subject]:
                hierarchy[tag.subject][tag.topic] = {
                    "tags": [],
                    "grade_levels": set()
                }
            
            hierarchy[tag.subject][tag.topic]["tags"].append(tag.to_dict())
            hierarchy[tag.subject][tag.topic]["grade_levels"].add(tag.grade_level)
        
        # Convert sets to lists for JSON serialization
        for subject in hierarchy:
            for topic in hierarchy[subject]:
                info = hierarchy[subject][topic]
                info["grade_levels"] = sorted(list(info["grade_levels"]))
        
        return hierarchy
    
    # Content tagging methods
    def associate_tag(self, content_id: str, tag_id: str,
                      confidence: float = 1.0, manual: bool = False,
                      assigned_by: str = None, notes: str = "") -> ContentTagAssociation:
        """
        Associate a tag with content.
        
        Args:
            content_id: Content identifier
            tag_id: Tag identifier
            confidence: Association confidence (0-1)
            manual: Whether this is a manual assignment
            assigned_by: User making the assignment
            notes: Additional notes
            
        Returns:
            Created ContentTagAssociation
        """
        with self.lock:
            if tag_id not in self.tags:
                raise ValueError(f"Tag not found: {tag_id}")
            
            if content_id not in self.content_associations:
                self.content_associations[content_id] = []
            
            # Check for existing association
            existing = None
            for assoc in self.content_associations[content_id]:
                if assoc.tag_id == tag_id:
                    existing = assoc
                    break
            
            if existing:
                # Update existing
                existing.confidence = confidence
                existing.manual_override = manual
                existing.assigned_by = assigned_by
                existing.notes = notes
                existing.assigned_at = datetime.utcnow()
                association = existing
            else:
                # Create new
                association = ContentTagAssociation(
                    content_id=content_id,
                    tag_id=tag_id,
                    confidence=confidence,
                    manual_override=manual,
                    assigned_by=assigned_by,
                    notes=notes
                )
                self.content_associations[content_id].append(association)
            
            # Update tag usage count
            if tag_id in self.tags:
                self.tags[tag_id].usage_count += 1
            
            self._save_state()
            
            logger.info(f"Tag {tag_id} associated with content {content_id}")
            return association
    
    def disassociate_tag(self, content_id: str, tag_id: str) -> bool:
        """
        Remove tag association from content.
        
        Args:
            content_id: Content identifier
            tag_id: Tag identifier
            
        Returns:
            True if removed, False if not found
        """
        with self.lock:
            if content_id not in self.content_associations:
                return False
            
            associations = self.content_associations[content_id]
            
            for i, assoc in enumerate(associations):
                if assoc.tag_id == tag_id:
                    associations.pop(i)
                    
                    # Update tag usage count
                    if tag_id in self.tags:
                        self.tags[tag_id].usage_count = max(0, self.tags[tag_id].usage_count - 1)
                    
                    self._save_state()
                    return True
            
            return False
    
    def get_content_tags(self, content_id: str) -> List[Tuple[SyllabusTag, ContentTagAssociation]]:
        """
        Get all tags associated with content.
        
        Args:
            content_id: Content identifier
            
        Returns:
            List of (tag, association) tuples
        """
        associations = self.content_associations.get(content_id, [])
        
        result = []
        for assoc in associations:
            tag = self.tags.get(assoc.tag_id)
            if tag:
                result.append((tag, assoc))
        
        return result
    
    def auto_tag_content(self, content_id: str, content_text: str,
                         board_id: str = None) -> List[ContentTagAssociation]:
        """
        Automatically tag content based on text analysis.
        
        Args:
            content_id: Content identifier
            content_text: Text to analyze
            board_id: Optional board to restrict search
            
        Returns:
            List of created associations
        """
        content_text = content_text.lower()
        associations = []
        
        for tag_id, tag in self.tags.items():
            if board_id and tag.board_id != board_id:
                continue
            
            # Calculate match score
            score = 0
            matches = []
            
            for keyword in tag.keywords:
                if keyword.lower() in content_text:
                    score += 1
                    matches.append(keyword)
            
            if tag.topic.lower() in content_text:
                score += 2
                matches.append(tag.topic)
            
            if tag.sub_topic and tag.sub_topic.lower() in content_text:
                score += 2
                matches.append(tag.sub_topic)
            
            # Create association if score is significant
            if score >= 2:
                confidence = min(1.0, score / 5.0)
                assoc = self.associate_tag(
                    content_id=content_id,
                    tag_id=tag_id,
                    confidence=confidence,
                    manual=False,
                    notes=f"Auto-matched: {', '.join(matches)}"
                )
                associations.append(assoc)
        
        logger.info(f"Auto-tagged content {content_id} with {len(associations)} tags")
        return associations
    
    def analyze_content_alignment(self, content_id: str, 
                                   target_standards: List[str]) -> ContentAlignmentReport:
        """
        Analyze how well content aligns with target standards.
        
        Args:
            content_id: Content to analyze
            target_standards: List of standard codes to check alignment
            
        Returns:
            ContentAlignmentReport with analysis results
        """
        content_tags = self.get_content_tags(content_id)
        content_tag_ids = {tag.id for tag, _ in content_tags}
        
        aligned_tags = []
        missing_tags = []
        
        for standard_code in target_standards:
            tag = self.get_tag_by_code(standard_code)
            if tag:
                if tag.id in content_tag_ids:
                    aligned_tags.append(tag)
                else:
                    missing_tags.append(tag)
        
        # Calculate coverage
        total_standards = len(target_standards)
        coverage_score = (len(aligned_tags) / total_standards * 100) if total_standards > 0 else 0
        
        # Find prerequisite gaps
        prerequisite_gaps = []
        for tag in missing_tags:
            for prereq_id in tag.prerequisites:
                if prereq_id not in content_tag_ids:
                    prereq_tag = self.tags.get(prereq_id)
                    if prereq_tag:
                        prerequisite_gaps.append(prereq_tag)
        
        # Generate suggestions
        suggestions = []
        if coverage_score < 50:
            suggestions.append("Consider adding more content to cover additional standards")
        if len(prerequisite_gaps) > 0:
            suggestions.append(f"Add content covering {len(prerequisite_gaps)} prerequisite topics")
        if aligned_tags:
            avg_difficulty = sum(int(t.difficulty == "developing") for t in aligned_tags) / len(aligned_tags)
            if avg_difficulty > 0.7:
                suggestions.append("Content difficulty may be too basic for target audience")
        
        return ContentAlignmentReport(
            content_id=content_id,
            coverage_score=coverage_score,
            aligned_tags=aligned_tags,
            missing_tags=missing_tags,
            prerequisite_gaps=prerequisite_gaps,
            suggestions=suggestions
        )
    
    def get_learning_path(self, start_tag_id: str, end_tag_id: str) -> List[SyllabusTag]:
        """
        Get a suggested learning path between two topics.
        
        Args:
            start_tag_id: Starting topic
            end_tag_id: Target topic
            
        Returns:
            List of tags forming a learning path
        """
        start_tag = self.tags.get(start_tag_id)
        end_tag = self.tags.get(end_tag_id)
        
        if not start_tag or not end_tag:
            return []
        
        path = [start_tag]
        
        # Add prerequisites of end tag that aren't in start
        for prereq_id in end_tag.prerequisites:
            if prereq_id != start_tag_id:
                prereq = self.tags.get(prereq_id)
                if prereq and prereq not in path:
                    # Recursively add prerequisites
                    prereq_path = self.get_learning_path(start_tag_id, prereq_id)
                    path.extend(prereq_path)
        
        if end_tag not in path:
            path.append(end_tag)
        
        return path


# Global service instance
_syllabus_service: Optional[SyllabusTaggingService] = None
_syllabus_lock = threading.Lock()


def create_syllabus_service(storage_dir: str = None) -> SyllabusTaggingService:
    """
    Create and return the global syllabus tagging service.
    
    Args:
        storage_dir: Optional storage directory
        
    Returns:
        SyllabusTaggingService instance
    """
    global _syllabus_service
    
    with _syllabus_lock:
        if _syllabus_service is None:
            _syllabus_service = SyllabusTaggingService(storage_dir)
        return _syllabus_service


__all__ = [
    "EducationLevel",
    "SubjectArea",
    "DifficultyLevel",
    "SUPPORTED_BOARDS",
    "CurriculumBoard",
    "SyllabusTag",
    "TagSearchResult",
    "ContentTagAssociation",
    "ContentAlignmentReport",
    "SyllabusTaggingService",
    "create_syllabus_service"
]
