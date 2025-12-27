"""
Visual Metadata Models for VisualVerse Content Metadata Layer

This module provides data models for linking concept knowledge to visual
animation assets, enabling searchable visual content and intelligent
content reuse across subject domains.

Licensed under the Apache License, Version 2.0
"""

from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime
from pydantic import BaseModel, Field, validator
from enum import Enum
import uuid
import os


class AssetFormat(str, Enum):
    """Animation asset format types"""
    MP4 = "mp4"
    GIF = "gif"
    WEBP = "webp"
    SVG = "svg"
    LOTTIE = "lottie"
    HTML5 = "html5"
    CANVAS = "canvas"
    WEBGL = "webgl"


class AssetType(str, Enum):
    """Types of visual assets"""
    ANIMATION = "animation"
    DIAGRAM = "diagram"
    CHART = "chart"
    INTERACTIVE = "interactive"
    SIMULATION = "simulation"
    EXPLAINER = "explainer"
    DIAGRAM_SEQUENCE = "diagram_sequence"
    INTERACTIVE_SIMULATION = "interactive_simulation"


class RelevanceType(str, Enum):
    """How an animation relates to a concept"""
    PRIMARY_EXPLANATION = "primary_explanation"  # Main explanation of concept
    VISUAL_EXAMPLE = "visual_example"            # Example demonstrating concept
    METAPHOR = "metaphor"                        # Conceptual metaphor
    SUMMARY = "summary"                          # Summary/recap animation
    PRACTICE = "practice"                        # Practice problem animation
    COUNTEREXAMPLE = "counterexample"            # Shows what happens when concept doesn't apply
    DERIVATION = "derivation"                    # Shows mathematical derivation
    APPLICATION = "application"                  # Real-world application


class AssetComplexity(str, Enum):
    """Complexity level of visual assets"""
    SIMPLE = 1  # Single concept, basic animation
    MODERATE = 2  # Multiple elements, moderate complexity
    COMPLEX = 3  # Many elements, sophisticated animation
    ADVANCED = 4  # Complex interactions, expert level
    EXPERT = 5  # Highly sophisticated, research-grade


class AssetStatus(str, Enum):
    """Status of animation asset"""
    DRAFT = "draft"
    REVIEW = "review"
    APPROVED = "approved"
    PUBLISHED = "published"
    DEPRECATED = "deprecated"
    ARCHIVED = "archived"


class AnimationAsset(BaseModel):
    """
    Represents a visual/animation asset in the VisualVerse.
    
    Animation assets are stored in the animation engine directory and
    indexed here for concept linking and search functionality.
    """
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique identifier")
    
    # Asset identification
    asset_key: str = Field(..., description="Unique asset key/path identifier")
    file_name: str = Field(..., description="Original file name")
    display_name: str = Field(..., min_length=1, max_length=200, description="Human-readable name")
    description: Optional[str] = Field(None, max_length=1000, description="Asset description")
    
    # File information
    file_path: str = Field(..., description="Relative path from assets root")
    file_size_bytes: int = Field(default=0, description="File size in bytes")
    format: AssetFormat = Field(..., description="Asset format")
    asset_type: AssetType = AssetType.ANIMATION
    
    # Technical properties
    duration_seconds: Optional[float] = Field(None, description="Duration in seconds (for video)")
    width: Optional[int] = Field(None, description="Display width in pixels")
    height: Optional[int] = Field(None, description="Display height in pixels")
    frame_rate: Optional[float] = Field(None, description="Frame rate FPS")
    
    # Complexity and quality
    complexity_level: AssetComplexity = Field(
        default=AssetComplexity.MODERATE,
        description="Complexity level (1-5)"
    )
    quality_score: float = Field(default=0.8, ge=0.0, le=1.0, description="Quality assessment score")
    
    # Concept mappings
    concept_ids: List[str] = Field(default_factory=list, description="Mapped concept IDs")
    primary_concept_id: Optional[str] = Field(
        None,
        description="Primary concept this asset teaches"
    )
    
    # Content metadata
    tags: List[str] = Field(default_factory=list, description="Searchable tags")
    keywords: List[str] = Field(default_factory=list, description="Search keywords")
    subject_ids: List[str] = Field(default_factory=list, description="Applicable subjects")
    grade_levels: List[str] = Field(default_factory=list, description="Target grade levels")
    
    # Visual content analysis
    visual_elements: List[str] = Field(default_factory=list, description="Visual elements present")
    motion_types: List[str] = Field(default_factory=list, description="Types of motion/animation")
    color_scheme: Optional[str] = Field(None, description="Color scheme description")
    style: Optional[str] = Field(None, description="Visual style (flat, realistic, etc.)")
    
    # Accessibility
    has_audio: bool = Field(default=False, description="Has audio narration")
    has_captions: bool = Field(default=False, description="Has closed captions")
    accessibility_notes: Optional[str] = Field(None, description="Accessibility information")
    
    # Usage rights
    license_type: str = Field(default="proprietary", description="License type")
    is_creative_commons: bool = Field(default=False, description="Is Creative Commons licensed")
    cc_license: Optional[str] = Field(None, description="CC license code")
    
    # Status and versioning
    status: AssetStatus = Field(default=AssetStatus.DRAFT, description="Asset status")
    version: str = Field(default="1.0.0", description="Asset version")
    is_active: bool = Field(default=True, description="Whether asset is active")
    
    # Usage statistics
    view_count: int = Field(default=0, description="Number of views")
    like_count: int = Field(default=0, description="Number of likes")
    usage_count: int = Field(default=0, description="Times used in content")
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update timestamp")
    generated_at: Optional[datetime] = Field(None, description="When animation was generated")
    
    class Config:
        schema_extra = {
            "example": {
                "id": "asset-001",
                "asset_key": "math/algebra/quadratic-formula",
                "file_name": "quadratic-formula.mp4",
                "display_name": "Quadratic Formula Visualization",
                "description": "Animated visualization of solving quadratic equations using the formula",
                "file_path": "math/algebra/quadratic-formula.mp4",
                "file_size_bytes": 5242880,
                "format": "mp4",
                "asset_type": "animation",
                "duration_seconds": 45.0,
                "width": 1280,
                "height": 720,
                "complexity_level": 2,
                "concept_ids": ["quadratic-equations", "discriminant"],
                "primary_concept_id": "quadratic-equations",
                "tags": ["algebra", "equations", "visualization"],
                "subject_ids": ["mathematics"],
                "grade_levels": ["9", "10", "11"],
                "visual_elements": ["graph", "formula", "animation"],
                "motion_types": ["slide", "fade", "highlight"],
                "has_audio": True,
                "has_captions": True,
                "status": "published",
                "version": "1.0.0"
            }
        }
    
    @validator('asset_key')
    def validate_asset_key(cls, v):
        """Validate asset key format"""
        if not v.replace('/', '').replace('-', '').replace('_', '').isalnum():
            raise ValueError('Asset key must be alphanumeric with hyphens/underscores')
        return v.lower()
    
    @validator('file_path')
    def validate_file_path(cls, v):
        """Validate file path doesn't contain invalid characters"""
        if '..' in v:
            raise ValueError('File path cannot contain parent directory references')
        return v
    
    def get_full_path(self, base_path: str) -> str:
        """Get full file path"""
        return os.path.join(base_path, self.file_path)
    
    def to_search_result(self) -> Dict[str, Any]:
        """Convert to search result format"""
        return {
            'id': self.id,
            'asset_key': self.asset_key,
            'display_name': self.display_name,
            'description': self.description,
            'format': self.format.value,
            'duration_seconds': self.duration_seconds,
            'concepts': self.concept_ids,
            'subjects': self.subject_ids,
            'tags': self.tags,
            'thumbnail_url': f"/api/v1/animations/{self.id}/thumbnail",
            'view_url': f"/api/v1/animations/{self.id}/view"
        }


class ConceptVisualMapping(BaseModel):
    """
    Represents the mapping between a concept and visual animation assets.
    
    This is the bridge that links pedagogical concepts to their visual
    representations, enabling intelligent content discovery and reuse.
    """
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique identifier")
    
    # Link endpoints
    concept_id: str = Field(..., description="Linked concept ID")
    asset_id: str = Field(..., description="Linked animation asset ID")
    
    # Relationship details
    relevance_type: RelevanceType = Field(
        ...,
        description="How the asset relates to the concept"
    )
    relevance_score: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
        description="Strength of relevance (0-1)"
    )
    
    # Time segments (for video assets)
    start_time: Optional[float] = Field(
        None,
        ge=0,
        description="Start time of relevant segment in seconds"
    )
    end_time: Optional[float] = Field(
        None,
        description="End time of relevant segment in seconds"
    )
    
    # Content annotations
    annotations: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Time-based annotations for this mapping"
    )
    visual_highlights: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Key visual moments to highlight"
    )
    
    # Teaching context
    teaching_notes: Optional[str] = Field(
        None,
        description="Notes for educators using this mapping"
    )
    difficulty_adjustment: Optional[str] = Field(
        None,
        description="How to adjust for different difficulty levels"
    )
    
    # Validation
    is_approved: bool = Field(default=False, description="Whether mapping is approved")
    approval_notes: Optional[str] = Field(None, description="Approval notes")
    is_automatic: bool = Field(
        default=False,
        description="Whether this was auto-generated"
    )
    confidence_score: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Confidence in auto-generated mapping"
    )
    
    # Usage
    usage_count: int = Field(default=0, description="Times this mapping has been used")
    last_used_at: Optional[datetime] = Field(None, description="Last usage timestamp")
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update timestamp")
    
    class Config:
        schema_extra = {
            "example": {
                "id": "mapping-001",
                "concept_id": "quadratic-equations",
                "asset_id": "asset-001",
                "relevance_type": "primary_explanation",
                "relevance_score": 1.0,
                "start_time": 0.0,
                "end_time": 45.0,
                "annotations": [
                    {"time": 5.0, "text": "Introduction to quadratic equations"},
                    {"time": 15.0, "text": "Standard form explanation"}
                ],
                "is_approved": True,
                "is_automatic": False,
                "confidence_score": 0.95,
                "usage_count": 150
            }
        }
    
    def get_time_segment(self) -> Optional[Tuple[float, float]]:
        """Get time segment tuple"""
        if self.start_time is not None and self.end_time is not None:
            return (self.start_time, self.end_time)
        return None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'concept_id': self.concept_id,
            'asset_id': self.asset_id,
            'relevance_type': self.relevance_type.value,
            'relevance_score': self.relevance_score,
            'time_segment': self.get_time_segment(),
            'annotations': self.annotations,
            'is_approved': self.is_approved,
            'is_automatic': self.is_automatic,
            'confidence_score': self.confidence_score,
            'usage_count': self.usage_count
        }


class VisualLearningPath(BaseModel):
    """
    Represents a learning path enriched with visual animation assets.
    
    This extends the basic learning path with visual content, creating
    an engaging multimedia learning experience.
    """
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique identifier")
    name: str = Field(..., min_length=1, max_length=200, description="Path name")
    description: Optional[str] = Field(None, max_length=1000, description="Path description")
    
    # Path structure
    concept_ids: List[str] = Field(..., description="Ordered concept IDs")
    visual_assets: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Associated visual assets per step"
    )
    
    # Visual enrichment
    has_overview_video: bool = Field(default=False, description="Has overview video")
    overview_asset_id: Optional[str] = Field(None, description="Overview video asset ID")
    has_summary_video: bool = Field(default=False, description="Has summary video")
    summary_asset_id: Optional[str] = Field(None, description="Summary video asset ID")
    
    # Statistics
    total_duration_seconds: float = Field(default=0.0, description="Total video duration")
    total_assets: int = Field(default=0, description="Total visual assets")
    asset_coverage: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Percentage of steps with visual assets"
    )
    
    # Quality metrics
    average_asset_quality: float = Field(
        default=0.8,
        ge=0.0,
        le=1.0,
        description="Average quality of included assets"
    )
    interactivity_score: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Level of interactivity"
    )
    
    # Metadata
    subject_id: str = Field(..., description="Primary subject ID")
    difficulty_level: str = Field(default="intermediate", description="Difficulty level")
    estimated_minutes: int = Field(default=60, description="Estimated completion time")
    
    # Status
    is_published: bool = Field(default=False, description="Whether published")
    version: str = Field(default="1.0.0", description="Path version")
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update timestamp")
    
    class Config:
        schema_extra = {
            "example": {
                "id": "vpath-001",
                "name": "Visual Algebra Journey",
                "description": "Algebra concepts explained through animations",
                "concept_ids": ["basic-arithmetic", "fractions", "algebra-basics", "linear-equations"],
                "total_duration_seconds": 600.0,
                "total_assets": 8,
                "asset_coverage": 1.0,
                "subject_id": "mathematics",
                "difficulty_level": "intermediate",
                "is_published": True,
                "version": "1.0.0"
            }
        }
    
    def calculate_coverage(self) -> float:
        """Calculate visual asset coverage"""
        if not self.concept_ids:
            return 0.0
        covered_steps = sum(
            1 for asset_info in self.visual_assets
            if asset_info.get('concept_id') in self.concept_ids
        )
        return covered_steps / len(self.concept_ids)
    
    def to_enriched_response(self) -> Dict[str, Any]:
        """Convert to enriched response format with URLs"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'subject_id': self.subject_id,
            'difficulty_level': self.difficulty_level,
            'estimated_minutes': self.estimated_minutes,
            'steps': [
                {
                    'concept_id': concept_id,
                    'assets': self._get_assets_for_concept(concept_id),
                    'visual_url': self._get_visual_url(concept_id)
                }
                for concept_id in self.concept_ids
            ],
            'overview_video': f"/api/v1/animations/{self.overview_asset_id}/view" if self.overview_asset_id else None,
            'summary_video': f"/api/v1/animations/{self.summary_asset_id}/view" if self.summary_asset_id else None,
            'statistics': {
                'total_duration_seconds': self.total_duration_seconds,
                'total_assets': self.total_assets,
                'asset_coverage': self.asset_coverage,
                'average_quality': self.average_asset_quality
            },
            'is_published': self.is_published,
            'created_at': self.created_at.isoformat()
        }
    
    def _get_assets_for_concept(self, concept_id: str) -> List[Dict[str, Any]]:
        """Get assets for a specific concept"""
        return [
            {
                'asset_id': a['asset_id'],
                'type': a.get('relevance_type', 'visual_example'),
                'url': f"/api/v1/animations/{a['asset_id']}/view"
            }
            for a in self.visual_assets
            if a.get('concept_id') == concept_id
        ]
    
    def _get_visual_url(self, concept_id: str) -> Optional[str]:
        """Get primary visual URL for a concept"""
        for a in self.visual_assets:
            if a.get('concept_id') == concept_id:
                return f"/api/v1/animations/{a['asset_id']}/view"
        return None


class AssetGenerationRequest(BaseModel):
    """Request model for animation generation"""
    concept_id: str = Field(..., description="Concept to generate animation for")
    concept_name: str = Field(..., description="Concept name")
    concept_description: str = Field(..., description="Concept description")
    animation_type: AssetType = Field(default=AssetType.ANIMATION, description="Type of animation")
    style_preferences: Optional[Dict[str, Any]] = Field(
        None,
        description="Style preferences"
    )
    duration_seconds: float = Field(default=30.0, description="Target duration")
    generate_multiple: bool = Field(
        default=False,
        description="Generate multiple variations"
    )
    priority: int = Field(default=5, ge=1, le=10, description="Generation priority")


class AssetSearchRequest(BaseModel):
    """Request model for asset search"""
    query: Optional[str] = None
    concept_ids: Optional[List[str]] = None
    subject_ids: Optional[List[str]] = None
    format: Optional[AssetFormat] = None
    asset_type: Optional[AssetType] = None
    relevance_types: Optional[List[RelevanceType]] = None
    min_quality: float = 0.5
    min_duration: Optional[float] = None
    max_duration: Optional[float] = None
    tags: Optional[List[str]] = None
    has_audio: Optional[bool] = None
    page: int = 1
    page_size: int = 20
    sort_by: str = "relevance"
    sort_order: str = "desc"


class AssetSearchResult(BaseModel):
    """Response model for asset search"""
    assets: List[Dict[str, Any]]
    total_count: int
    page: int
    page_size: int
    has_next: bool
    facets: Dict[str, Dict[str, int]] = {}
    
    class Config:
        schema_extra = {
            "example": {
                "assets": [
                    {
                        "id": "asset-001",
                        "display_name": "Quadratic Formula Visualization",
                        "format": "mp4",
                        "duration_seconds": 45.0,
                        "concepts": ["quadratic-equations"],
                        "quality": 0.9,
                        "url": "/api/v1/animations/asset-001/view"
                    }
                ],
                "total_count": 1,
                "page": 1,
                "page_size": 20,
                "has_next": False,
                "facets": {
                    "subjects": {"mathematics": 1},
                    "formats": {"mp4": 1}
                }
            }
        }


# ============================================================================
# Utility Functions
# ============================================================================

def parse_asset_path(file_path: str, assets_root: str) -> Dict[str, str]:
    """
    Parse a file path to extract asset metadata.
    
    Args:
        file_path: Relative file path
        assets_root: Root directory for assets
        
    Returns:
        Dictionary with asset metadata
    """
    # Get file name and extension
    file_name = os.path.basename(file_path)
    name, ext = os.path.splitext(file_name)
    
    # Clean up extension
    format_map = {
        '.mp4': 'mp4', '.gif': 'gif', '.webp': 'webp',
        '.svg': 'svg', '.json': 'lottie', '.html': 'html5'
    }
    format_type = format_map.get(ext.lower(), ext.lower().lstrip('.'))
    
    # Generate asset key from path
    asset_key = file_path.replace(assets_root, '').lstrip('/')
    asset_key = asset_key.replace('/', '-').replace('\\', '-')
    
    return {
        'file_name': file_name,
        'format': format_type,
        'asset_key': asset_key
    }


def extract_keywords_from_description(description: str) -> List[str]:
    """
    Extract searchable keywords from a description.
    
    Args:
        description: Text description
        
    Returns:
        List of extracted keywords
    """
    import re
    
    # Extract words
    words = re.findall(r'\b[a-zA-Z]{3,}\b', description.lower())
    
    # Filter common words
    stop_words = {
        'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can',
        'her', 'was', 'one', 'our', 'out', 'has', 'have', 'been', 'this'
    }
    
    keywords = [w for w in words if w not in stop_words]
    
    # Return unique keywords
    return list(set(keywords))[:20]
