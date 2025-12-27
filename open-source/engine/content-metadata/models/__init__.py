"""
Models Module for VisualVerse Content Metadata Layer

This module provides data models for the knowledge and content metadata layer
including concepts, subjects, curriculum, reasoning, visual metadata, and learner profiles.

Licensed under the Apache License, Version 2.0
"""

from .concept import (
    Concept,
    ConceptCreate,
    ConceptUpdate,
    ConceptResponse,
    ConceptListResponse,
    LearningPath,
    DifficultyLevel,
    ConceptType,
    LearningStyle,
    create_concept_id,
    calculate_concept_difficulty
)

from .subject import (
    Subject,
    SubjectCreate,
    SubjectUpdate,
    SubjectResponse,
    SubjectListResponse,
    SubjectStatistics,
    SubjectLevel,
    SubjectCategory,
    get_default_subjects
)

from .curriculum import (
    CurriculumFramework,
    StandardBenchmark,
    SyllabusUnit,
    LearningOutcome,
    Curriculum,
    CurriculumSection,
    CurriculumFrameworkType,
    DifficultyScale,
    AssessmentType,
    GradeLevel,
    CurriculumFrameworkCreate,
    StandardBenchmarkCreate,
    SyllabusUnitCreate,
    LearningOutcomeCreate,
    parse_standards_file,
    create_standards_from_data
)

from .reasoning import (
    InferenceRule,
    InferenceRuleType,
    RelationshipDirection,
    ReasoningScope,
    InferenceConfidence,
    GapSeverity,
    InferredRelationship,
    KnowledgeGap,
    ConceptSimilarity,
    ConceptCluster,
    InferenceRuleCreate,
    KnowledgeGapDetectionRequest,
    SimilarityCalculationRequest,
    ClusterDiscoveryRequest,
    InferenceResult,
    get_default_inference_rules
)

from .visual_meta import (
    AnimationAsset,
    ConceptVisualMapping,
    VisualLearningPath,
    AssetFormat,
    AssetType,
    RelevanceType,
    AssetComplexity,
    AssetStatus,
    AssetSearchRequest,
    AssetSearchResult,
    AssetGenerationRequest,
    parse_asset_path,
    extract_keywords_from_description
)

from .learner_profile import (
    LearnerProfile,
    ConceptMastery,
    LearningSession,
    MasteryMetrics,
    InteractionResult,
    ReviewSchedule,
    MasteryLevel,
    InteractionType
)

from .enhanced_learner_profile import (
    EnhancedLearnerProfile,
    CognitiveProfile,
    LearningStyleProfile,
    TemporalPreferences,
    MotivationProfile,
    EngagementPattern,
    AccessibilityNeeds,
    ProfileSnapshot,
    LearningStyleDimension,
    CognitiveStyle,
    MotivationType,
    FeedbackPreference,
    DifficultyPacing,
    SessionPattern
)

from .vertical_visual_meta import (
    # Domain enums
    MathVisualType,
    PhysicsVisualType,
    ChemistryVisualType,
    AlgorithmVisualType,
    FinanceVisualType,
    VerticalDomain,
    AnimationStyle,
    ColorSchemeType,
    
    # Extended models
    VisualizationTemplate,
    DomainColorScheme,
    VisualStylePreset,
    ServiceExtensionConfig,
    ServiceExtensionPoint,
    VerticalConfig,
    VerticalConfigMetadata,
    VerticalDomainConfig,
    FeatureToggle,
    LayoutPattern,
    
    # Utility functions
    get_domain_visual_types,
    create_domain_color_scheme,
    validate_visualization_config
)

__all__ = [
    # Concept models
    'Concept',
    'ConceptCreate',
    'ConceptUpdate',
    'ConceptResponse',
    'ConceptListResponse',
    'LearningPath',
    'DifficultyLevel',
    'ConceptType',
    'LearningStyle',
    'create_concept_id',
    'calculate_concept_difficulty',
    
    # Subject models
    'Subject',
    'SubjectCreate',
    'SubjectUpdate',
    'SubjectResponse',
    'SubjectListResponse',
    'SubjectStatistics',
    'SubjectLevel',
    'SubjectCategory',
    'get_default_subjects',
    
    # Curriculum models
    'CurriculumFramework',
    'StandardBenchmark',
    'SyllabusUnit',
    'LearningOutcome',
    'Curriculum',
    'CurriculumSection',
    'CurriculumFrameworkType',
    'DifficultyScale',
    'AssessmentType',
    'GradeLevel',
    'CurriculumFrameworkCreate',
    'StandardBenchmarkCreate',
    'SyllabusUnitCreate',
    'LearningOutcomeCreate',
    'parse_standards_file',
    'create_standards_from_data',
    
    # Reasoning models
    'InferenceRule',
    'InferenceRuleType',
    'RelationshipDirection',
    'ReasoningScope',
    'InferenceConfidence',
    'GapSeverity',
    'InferredRelationship',
    'KnowledgeGap',
    'ConceptSimilarity',
    'ConceptCluster',
    'InferenceRuleCreate',
    'KnowledgeGapDetectionRequest',
    'SimilarityCalculationRequest',
    'ClusterDiscoveryRequest',
    'InferenceResult',
    'get_default_inference_rules',
    
    # Visual metadata models
    'AnimationAsset',
    'ConceptVisualMapping',
    'VisualLearningPath',
    'AssetFormat',
    'AssetType',
    'RelevanceType',
    'AssetComplexity',
    'AssetStatus',
    'AssetSearchRequest',
    'AssetSearchResult',
    'AssetGenerationRequest',
    'parse_asset_path',
    'extract_keywords_from_description',
    
    # Learner profile and mastery models
    'LearnerProfile',
    'ConceptMastery',
    'LearningSession',
    'MasteryMetrics',
    'InteractionResult',
    'ReviewSchedule',
    'MasteryLevel',
    'InteractionType',
    
    # Enhanced learner profile models
    'EnhancedLearnerProfile',
    'CognitiveProfile',
    'LearningStyleProfile',
    'TemporalPreferences',
    'MotivationProfile',
    'EngagementPattern',
    'AccessibilityNeeds',
    'ProfileSnapshot',
    'LearningStyleDimension',
    'CognitiveStyle',
    'MotivationType',
    'FeedbackPreference',
    'DifficultyPacing',
    'SessionPattern',
    
    # Vertical visual metadata models
    'MathVisualType',
    'PhysicsVisualType',
    'ChemistryVisualType',
    'AlgorithmVisualType',
    'FinanceVisualType',
    'VerticalDomain',
    'AnimationStyle',
    'ColorSchemeType',
    'VisualizationTemplate',
    'DomainColorScheme',
    'VisualStylePreset',
    'ServiceExtensionConfig',
    'ServiceExtensionPoint',
    'VerticalConfig',
    'VerticalConfigMetadata',
    'VerticalDomainConfig',
    'FeatureToggle',
    'LayoutPattern',
    'get_domain_visual_types',
    'create_domain_color_scheme',
    'validate_visualization_config'
]
