"""
Services Module for VisualVerse Content Metadata Layer

This module provides services for concept management, graph operations,
reasoning, animation metadata, curriculum mapping, content recommendations,
and learner mastery tracking.

Licensed under the Apache License, Version 2.0
"""

from .concept_service import ConceptService
from .search_service import SearchService
from .learning_path_service import (
    LearningPathGenerator,
    DependencyGraph,
    calculate_estimated_completion_time,
    find_optimal_starting_point,
    group_by_difficulty
)

from .graph.engine import (
    DependencyGraphEngine,
    GraphNode,
    GraphEdge,
    PathResult,
    GraphStats,
    RelationshipType
)

from .graph.linker import (
    InterdisciplinaryLinker,
    CrossSubjectLink,
    InterdisciplinaryPath,
    SharedPrerequisite,
    TransferabilityScore
)

from .curriculum.mapper import (
    CurriculumMapper,
    ConceptMapping,
    MappingSuggestion,
    CoverageReport,
    MappingConfidence
)

from .reasoning_engine import (
    ReasoningEngine,
    ReasoningStats,
    SimpleGraph
)

from .animation_service import (
    AnimationMetadataService,
    AnimationServiceStats
)

from .recommendation import (
    RecommendationService,
    LearnerProfile,
    ContentRecommendation,
    LearningSession,
    RecommendationType,
    LearnerLevel
)

from .mastery_service import (
    MasteryService,
    MasteryServiceStats
)

from .learner_profile_service import (
    LearnerProfileService,
    ProfileAnalysisResult,
    ProfileInferenceStatus
)

from .extensions.service_extension_base import (
    ExtensionRegistry,
    ServiceExtension,
    ConceptServiceExtension,
    VisualServiceExtension,
    AnimationServiceExtension,
    ReasoningEngineExtension,
    ExtensionContext,
    MathConceptServiceExtension,
    PhysicsConceptServiceExtension,
    ChemistryConceptServiceExtension,
    AlgorithmVisualServiceExtension,
    FinanceAnimationServiceExtension,
    MathReasoningEngineExtension,
    get_extension_registry,
    get_vertical_loader,
    VerticalLoader
)

__all__ = [
    # Core services
    'ConceptService',
    'SearchService',
    
    # Learning path services
    'LearningPathGenerator',
    'DependencyGraph',
    'calculate_estimated_completion_time',
    'find_optimal_starting_point',
    'group_by_difficulty',
    
    # Graph services
    'DependencyGraphEngine',
    'GraphNode',
    'GraphEdge',
    'PathResult',
    'GraphStats',
    'RelationshipType',
    
    # Cross-subject linking
    'InterdisciplinaryLinker',
    'CrossSubjectLink',
    'InterdisciplinaryPath',
    'SharedPrerequisite',
    'TransferabilityScore',
    
    # Curriculum mapping
    'CurriculumMapper',
    'ConceptMapping',
    'MappingSuggestion',
    'CoverageReport',
    'MappingConfidence',
    
    # Reasoning engine
    'ReasoningEngine',
    'ReasoningStats',
    'SimpleGraph',
    
    # Animation metadata
    'AnimationMetadataService',
    'AnimationServiceStats',
    
    # Recommendation service
    'RecommendationService',
    'LearnerProfile',
    'ContentRecommendation',
    'LearningSession',
    'RecommendationType',
    'LearnerLevel',
    
    # Mastery service
    'MasteryService',
    'MasteryServiceStats',
    
    # Learner profile service
    'LearnerProfileService',
    'ProfileAnalysisResult',
    'ProfileInferenceStatus',
    
    # Service extensions
    'ExtensionRegistry',
    'ServiceExtension',
    'ConceptServiceExtension',
    'VisualServiceExtension',
    'AnimationServiceExtension',
    'ReasoningEngineExtension',
    'ExtensionContext',
    'MathConceptServiceExtension',
    'PhysicsConceptServiceExtension',
    'ChemistryConceptServiceExtension',
    'AlgorithmVisualServiceExtension',
    'FinanceAnimationServiceExtension',
    'MathReasoningEngineExtension',
    'get_extension_registry',
    'get_vertical_loader',
    'VerticalLoader'
]
