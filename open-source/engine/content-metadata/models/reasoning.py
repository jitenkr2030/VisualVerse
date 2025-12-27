"""
Semantic Reasoning Models for VisualVerse Content Metadata Layer

This module provides data models for semantic reasoning capabilities including
inference rules, inferred relationships, and knowledge gap detection.

Licensed under the Apache License, Version 2.0
"""

from typing import List, Optional, Dict, Any, Set, Tuple
from datetime import datetime
from pydantic import BaseModel, Field, validator
from enum import Enum
import uuid


class InferenceRuleType(str, Enum):
    """Types of inference rules for semantic reasoning"""
    TRANSITIVE = "transitive"           # If A→B and B→C, then A→C
    SYMMETRIC = "symmetric"             # If A relates to B, then B relates to A
    INVERSE = "inverse"                 # If A is_prerequisite_of B, then B enables A
    COMPOSITE = "composite"             # Complex rule combining multiple predicates
    PROPERTY_BASED = "property_based"   # Rule based on concept properties
    SIMILARITY = "similarity"           # Rule for finding similar concepts
    CLUSTER = "cluster"                 # Rule for concept clustering


class RelationshipDirection(str, Enum):
    """Direction of relationship propagation"""
    FORWARD = "forward"   # Source to target
    BACKWARD = "backward"  # Target to source
    BIDIRECTIONAL = "bidirectional"  # Both directions


class InferenceConfidence(str, Enum):
    """Confidence levels for inferred relationships"""
    HIGH = "high"         # Direct logical inference
    MEDIUM = "medium"     # Probabilistic inference
    LOW = "low"           # Suggestion based on weak evidence
    EXPERIMENTAL = "experimental"  # Requires validation


class ReasoningScope(str, Enum):
    """Scope of reasoning application"""
    LOCAL = "local"           # Single concept analysis
    GRAPH_WIDE = "graph_wide"  # Entire knowledge graph
    SUBJECT = "subject"       # Subject-specific reasoning
    PATHS = "paths"          # Path-based reasoning


class GapSeverity(str, Enum):
    """Severity levels for knowledge gaps"""
    CRITICAL = "critical"     # Blocks all progress
    MAJOR = "major"          # Significant gap
    MINOR = "minor"          # Minor gap, optional
    SUGGESTION = "suggestion"  # Enhancement suggestion


class InferenceRule(BaseModel):
    """
    Represents an inference rule for semantic reasoning.
    
    Inference rules define how new relationships can be derived from existing
    ones. Examples include transitivity (if A→B and B→C, then A→C).
    """
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique identifier")
    name: str = Field(..., min_length=1, max_length=200, description="Rule name")
    description: str = Field(..., max_length=1000, description="Rule description")
    
    # Rule definition
    rule_type: InferenceRuleType = Field(..., description="Type of inference rule")
    source_predicate: str = Field(..., description="Source relationship type")
    target_predicate: Optional[str] = Field(None, description="Target/inferred relationship type")
    
    # Rule configuration
    direction: RelationshipDirection = Field(
        default=RelationshipDirection.FORWARD,
        description="Direction of relationship propagation"
    )
    max_hops: int = Field(default=3, ge=1, le=10, description="Maximum hops for transitivity")
    scope: ReasoningScope = Field(
        default=ReasoningScope.GRAPH_WIDE,
        description="Scope of rule application"
    )
    
    # Rule conditions
    subject_filter: Optional[List[str]] = Field(
        default=None,
        description="Optional subject filter for rule"
    )
    difficulty_range: Optional[Tuple[str, str]] = Field(
        default=None,
        description="Optional difficulty range (min, max)"
    )
    concept_type_filter: Optional[List[str]] = Field(
        default=None,
        description="Optional concept type filter"
    )
    
    # Rule metadata
    confidence_weight: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
        description="Weight for confidence calculation"
    )
    is_active: bool = Field(default=True, description="Whether rule is active")
    priority: int = Field(default=0, description="Rule execution priority")
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update timestamp")
    
    class Config:
        schema_extra = {
            "example": {
                "id": "rule-prerequisite-transitive",
                "name": "Prerequisite Transitivity",
                "description": "If A is a prerequisite of B and B is a prerequisite of C, then A is an indirect prerequisite of C",
                "rule_type": "transitive",
                "source_predicate": "prerequisite",
                "target_predicate": "indirect_prerequisite",
                "direction": "forward",
                "max_hops": 5,
                "priority": 10,
                "is_active": True
            }
        }
    
    def matches_predicate(self, predicate: str) -> bool:
        """Check if a predicate matches this rule"""
        return (
            predicate == self.source_predicate or
            predicate == self.target_predicate
        )
    
    def should_apply(self, subject_id: str, difficulty: str) -> bool:
        """Check if rule should apply to a given concept"""
        if self.subject_filter and subject_id not in self.subject_filter:
            return False
        
        if self.difficulty_range:
            diff_order = self._get_difficulty_order(difficulty)
            min_order = self._get_difficulty_order(self.difficulty_range[0])
            max_order = self._get_difficulty_order(self.difficulty_range[1])
            if not (min_order <= diff_order <= max_order):
                return False
        
        return True
    
    def _get_difficulty_order(self, level: str) -> int:
        """Get numeric order for difficulty level"""
        order = {
            'beginner': 0, 'elementary': 1, 'intermediate': 2,
            'advanced': 3, 'expert': 4
        }
        return order.get(level.lower(), 2)


class InferredRelationship(BaseModel):
    """
    Represents an inferred (derived) relationship between concepts.
    
    Unlike explicit relationships which are human-authored, inferred
    relationships are automatically generated by the reasoning engine.
    """
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique identifier")
    
    # Relationship endpoints
    source_concept_id: str = Field(..., description="Source concept ID")
    target_concept_id: str = Field(..., description="Target concept ID")
    
    # Relationship details
    relationship_type: str = Field(..., description="Inferred relationship type")
    inverse_relationship: Optional[str] = Field(
        None,
        description="Inverse relationship type"
    )
    
    # Inference details
    rule_id: str = Field(..., description="Source inference rule ID")
    inference_confidence: InferenceConfidence = Field(
        ...,
        description="Confidence level of inference"
    )
    confidence_score: float = Field(
        default=0.8,
        ge=0.0,
        le=1.0,
        description="Numeric confidence score"
    )
    
    # Derivation path
    derivation_path: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Path of derivation (concepts involved)"
    )
    hop_count: int = Field(default=1, description="Number of hops in derivation")
    
    # Validation status
    is_validated: bool = Field(default=False, description="Whether manually validated")
    is_active: bool = Field(default=True, description="Whether still valid")
    
    # Timestamps
    inferred_at: datetime = Field(default_factory=datetime.now, description="When inferred")
    last_validated: Optional[datetime] = Field(None, description="Last validation time")
    expires_at: Optional[datetime] = Field(None, description="Optional expiration")
    
    class Config:
        schema_extra = {
            "example": {
                "id": "inferred-001",
                "source_concept_id": "basic-arithmetic",
                "target_concept_id": "quadratic-equations",
                "relationship_type": "indirect_prerequisite",
                "rule_id": "rule-prerequisite-transitive",
                "inference_confidence": "high",
                "confidence_score": 0.85,
                "hop_count": 4,
                "derivation_path": [
                    {"from": "basic-arithmetic", "to": "fractions"},
                    {"from": "fractions", "to": "algebra-basics"},
                    {"from": "algebra-basics", "to": "quadratic-equations"}
                ],
                "is_validated": False,
                "is_active": True
            }
        }
    
    def to_edge_data(self) -> Dict[str, Any]:
        """Convert to graph edge data format"""
        return {
            'relationship_type': self.relationship_type,
            'inverse_relationship': self.inverse_relationship,
            'confidence_score': self.confidence_score,
            'is_inferred': True,
            'rule_id': self.rule_id,
            'hop_count': self.hop_count
        }


class KnowledgeGap(BaseModel):
    """
    Represents a gap in a learner's knowledge.
    
    Knowledge gaps identify missing prerequisites or unconnected concepts
    that prevent the learner from progressing in their learning journey.
    """
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique identifier")
    
    # Target concept
    target_concept_id: str = Field(..., description="Concept the learner wants to learn")
    target_concept_name: str = Field(..., description="Concept name for display")
    
    # Gap details
    gap_type: str = Field(..., description="Type of gap (missing_prerequisite, disconnected, etc.)")
    severity: GapSeverity = Field(..., description="Gap severity")
    
    # Missing items
    missing_concepts: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Missing concept details"
    )
    missing_relationships: List[Dict[str, str]] = Field(
        default_factory=list,
        description="Missing relationship types"
    )
    
    # Impact analysis
    blocking_concepts: List[str] = Field(
        default_factory=list,
        description="Concepts that cannot be learned until gap is filled"
    )
    affected_paths: int = Field(
        default=0,
        description="Number of learning paths affected"
    )
    
    # Remediation
    suggested_prerequisites: List[str] = Field(
        default_factory=list,
        description="Suggested prerequisite concepts"
    )
    estimated_effort_hours: float = Field(
        default=0.0,
        description="Estimated effort to fill gap"
    )
    
    # Context
    learner_id: Optional[str] = Field(None, description="Associated learner ID")
    subject_id: str = Field(..., description="Subject ID")
    
    # Status
    is_addressed: bool = Field(default=False, description="Whether gap has been addressed")
    addressed_at: Optional[datetime] = Field(None, description="When gap was addressed")
    
    # Timestamps
    detected_at: datetime = Field(default_factory=datetime.now, description="Detection time")
    
    class Config:
        schema_extra = {
            "example": {
                "id": "gap-001",
                "target_concept_id": "quadratic-equations",
                "target_concept_name": "Quadratic Equations",
                "gap_type": "missing_prerequisite",
                "severity": "critical",
                "missing_concepts": [
                    {"id": "algebra-basics", "name": "Algebra Basics", "difficulty": "intermediate"}
                ],
                "blocking_concepts": ["quadratic-equations", "polynomials"],
                "suggested_prerequisites": ["algebra-basics"],
                "estimated_effort_hours": 4.0,
                "subject_id": "mathematics",
                "is_addressed": False
            }
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'target_concept_id': self.target_concept_id,
            'target_concept_name': self.target_concept_name,
            'gap_type': self.gap_type,
            'severity': self.severity.value,
            'missing_concepts': self.missing_concepts,
            'blocking_concepts': self.blocking_concepts,
            'suggested_prerequisites': self.suggested_prerequisites,
            'estimated_effort_hours': self.estimated_effort_hours,
            'is_addressed': self.is_addressed,
            'detected_at': self.detected_at.isoformat()
        }


class ConceptSimilarity(BaseModel):
    """
    Represents similarity between two concepts.
    
    Similarity is calculated based on multiple factors including shared
    tags, keywords, learning objectives, and structural position.
    """
    
    concept_a_id: str = Field(..., description="First concept ID")
    concept_b_id: str = Field(..., description="Second concept ID")
    
    # Similarity metrics
    overall_score: float = Field(..., ge=0.0, le=1.0, description="Overall similarity score")
    tag_similarity: float = Field(default=0.0, ge=0.0, le=1.0, description="Tag overlap similarity")
    keyword_similarity: float = Field(default=0.0, ge=0.0, le=1.0, description="Keyword overlap similarity")
    structural_similarity: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Graph position similarity"
    )
    objective_similarity: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Learning objective similarity"
    )
    
    # Similarity details
    shared_tags: List[str] = Field(default_factory=list, description="Shared tags")
    shared_keywords: List[str] = Field(default_factory=list, description="Shared keywords")
    shared_objectives: List[str] = Field(default_factory=list, description="Shared objectives")
    
    # Recommendation context
    recommended_as_prerequisite: bool = Field(
        default=False,
        description="Whether concepts should be prerequisites"
    )
    recommended_for_review: bool = Field(
        default=False,
        description="Whether concepts should be reviewed together"
    )
    
    # Metadata
    calculation_method: str = Field(
        default="jaccard",
        description="Method used for calculation"
    )
    calculated_at: datetime = Field(default_factory=datetime.now, description="Calculation time")
    
    class Config:
        schema_extra = {
            "example": {
                "concept_a_id": "velocity",
                "concept_b_id": "speed",
                "overall_score": 0.85,
                "tag_similarity": 0.9,
                "keyword_similarity": 0.8,
                "structural_similarity": 0.75,
                "objective_similarity": 0.95,
                "shared_tags": ["motion", "kinematics"],
                "shared_keywords": ["rate", "change"],
                "shared_objectives": ["Calculate motion quantities"],
                "recommended_as_prerequisite": False,
                "recommended_for_review": True,
                "calculation_method": "weighted_average"
            }
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'concept_a_id': self.concept_a_id,
            'concept_b_id': self.concept_b_id,
            'overall_score': self.overall_score,
            'tag_similarity': self.tag_similarity,
            'keyword_similarity': self.keyword_similarity,
            'structural_similarity': self.structural_similarity,
            'objective_similarity': self.objective_similarity,
            'shared_tags': self.shared_tags,
            'shared_keywords': self.shared_keywords,
            'shared_objectives': self.shared_objectives,
            'recommended_as_prerequisite': self.recommended_as_prerequisite,
            'recommended_for_review': self.recommended_for_review,
            'calculation_method': self.calculation_method,
            'calculated_at': self.calculated_at.isoformat()
        }


class ConceptCluster(BaseModel):
    """
    Represents a cluster of related concepts.
    
    Concept clusters are groups of concepts that share significant
    similarity and can be learned together or treated as a unit.
    """
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique identifier")
    name: str = Field(..., description="Cluster name")
    description: Optional[str] = Field(None, description="Cluster description")
    
    # Cluster membership
    concept_ids: List[str] = Field(..., description="Concepts in cluster")
    centroid_concept_id: Optional[str] = Field(
        None,
        description="Most central concept in cluster"
    )
    
    # Cluster metrics
    cohesion_score: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Internal cohesion of cluster"
    )
    separation_score: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Separation from other clusters"
    )
    
    # Cluster properties
    average_difficulty: str = Field(default="intermediate", description="Average difficulty")
    primary_subject: str = Field(..., description="Primary subject")
    secondary_subjects: List[str] = Field(default_factory=list, description="Secondary subjects")
    
    # Learning context
    can_learn_together: bool = Field(
        default=True,
        description="Whether concepts can be learned simultaneously"
    )
    suggested_order: List[str] = Field(
        default_factory=list,
        description="Suggested learning order within cluster"
    )
    
    # Metadata
    discovery_method: str = Field(
        default="similarity",
        description="Method used to discover cluster"
    )
    created_at: datetime = Field(default_factory=datetime.now, description="Creation time")
    
    class Config:
        schema_extra = {
            "example": {
                "id": "cluster-001",
                "name": "Linear Motion Concepts",
                "description": "Concepts related to motion in a straight line",
                "concept_ids": ["velocity", "speed", "acceleration", "displacement"],
                "centroid_concept_id": "velocity",
                "cohesion_score": 0.85,
                "separation_score": 0.75,
                "average_difficulty": "intermediate",
                "primary_subject": "physics",
                "can_learn_together": True,
                "suggested_order": ["speed", "velocity", "acceleration"],
                "discovery_method": "similarity_clustering"
            }
        }


# ============================================================================
# Request/Response Models
# ============================================================================

class InferenceRuleCreate(BaseModel):
    """Model for creating an inference rule"""
    name: str
    description: str
    rule_type: InferenceRuleType
    source_predicate: str
    target_predicate: Optional[str] = None
    direction: RelationshipDirection = RelationshipDirection.FORWARD
    max_hops: int = 3
    subject_filter: Optional[List[str]] = None
    difficulty_range: Optional[Tuple[str, str]] = None
    confidence_weight: float = 1.0
    priority: int = 0


class KnowledgeGapDetectionRequest(BaseModel):
    """Request model for knowledge gap detection"""
    learner_id: Optional[str] = None
    subject_id: Optional[str] = None
    target_concept_ids: Optional[List[str]] = None
    completed_concept_ids: Optional[List[str]] = None
    include_minor_gaps: bool = False
    max_depth: int = 5


class SimilarityCalculationRequest(BaseModel):
    """Request model for similarity calculation"""
    concept_a_id: str
    concept_b_id: str
    include_details: bool = True
    calculation_method: str = "weighted_average"


class ClusterDiscoveryRequest(BaseModel):
    """Request model for concept cluster discovery"""
    concept_ids: Optional[List[str]] = None
    subject_id: Optional[str] = None
    min_similarity: float = 0.6
    max_cluster_size: int = 20
    min_cluster_size: int = 3


class InferenceResult(BaseModel):
    """Response model for inference results"""
    new_relationships: List[Dict[str, Any]]
    total_inferred: int
    inference_time_ms: float
    rules_applied: List[str]
    warnings: List[str] = []
    
    class Config:
        schema_extra = {
            "example": {
                "new_relationships": [
                    {
                        "source": "basic-arithmetic",
                        "target": "quadratic-equations",
                        "type": "indirect_prerequisite",
                        "confidence": 0.85
                    }
                ],
                "total_inferred": 15,
                "inference_time_ms": 45.2,
                "rules_applied": ["rule-prerequisite-transitive", "rule-similarity-symmetric"]
            }
        }


# ============================================================================
# Default Inference Rules
# ============================================================================

def get_default_inference_rules() -> List[InferenceRule]:
    """Get the default set of inference rules"""
    return [
        InferenceRule(
            id="rule-prerequisite-transitive",
            name="Prerequisite Transitivity",
            description="If A is a prerequisite of B and B is a prerequisite of C, then A is an indirect prerequisite of C",
            rule_type=InferenceRuleType.TRANSITIVE,
            source_predicate="prerequisite",
            target_predicate="indirect_prerequisite",
            direction=RelationshipDirection.FORWARD,
            max_hops=5,
            priority=10,
            confidence_weight=0.9
        ),
        InferenceRule(
            id="rule-related-symmetric",
            name="Related Symmetry",
            description="If A is related to B, then B is related to A",
            rule_type=InferenceRuleType.SYMMETRIC,
            source_predicate="related_to",
            target_predicate="related_to",
            direction=RelationshipDirection.BIDIRECTIONAL,
            priority=5,
            confidence_weight=0.7
        ),
        InferenceRule(
            id="rule-prerequisite-inverse",
            name="Prerequisite Inverse",
            description="If A is a prerequisite of B, then B enables or depends on A",
            rule_type=InferenceRuleType.INVERSE,
            source_predicate="prerequisite",
            target_predicate="enables",
            direction=RelationshipDirection.BACKWARD,
            priority=5,
            confidence_weight=0.85
        ),
        InferenceRule(
            id="rule-component-transitive",
            name="Component Transitivity",
            description="If A is a component of B and B is a component of C, then A is a component of C",
            rule_type=InferenceRuleType.TRANSITIVE,
            source_predicate="component_of",
            target_predicate="component_of",
            direction=RelationshipDirection.FORWARD,
            max_hops=3,
            priority=8,
            confidence_weight=0.8
        ),
        InferenceRule(
            id="rule-similarity-symmetric",
            name="Similarity Symmetry",
            description="If A is similar to B, then B is similar to A",
            rule_type=InferenceRuleType.SYMMETRIC,
            source_predicate="similar_to",
            target_predicate="similar_to",
            direction=RelationshipDirection.BIDIRECTIONAL,
            priority=3,
            confidence_weight=0.6
        )
    ]
