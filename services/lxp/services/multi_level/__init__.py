"""
Multi-Level Content Services Package.

Provides multi-level content adaptation, curriculum management,
and educational level support for the VisualVerse platform.
"""

from .multi_level_service import (
    MultiLevelService,
    LevelType,
    ContentVariant,
    AdaptiveRule,
    LearnerPreferences,
    DifficultyLevel,
    ContentFormat,
    create_multi_level_service
)

from .curriculum_service import (
    CurriculumService,
    Curriculum,
    CurriculumModule,
    CurriculumUnit,
    LearningStandard,
    LearnerCurriculumProgress,
    CurriculumType,
    StandardType,
    create_curriculum_service
)

__all__ = [
    # Multi-Level Service
    "MultiLevelService",
    "LevelType",
    "ContentVariant",
    "AdaptiveRule",
    "LearnerPreferences",
    "DifficultyLevel",
    "ContentFormat",
    "create_multi_level_service",
    
    # Curriculum Service
    "CurriculumService",
    "Curriculum",
    "CurriculumModule",
    "CurriculumUnit",
    "LearningStandard",
    "LearnerCurriculumProgress",
    "CurriculumType",
    "StandardType",
    "create_curriculum_service"
]
