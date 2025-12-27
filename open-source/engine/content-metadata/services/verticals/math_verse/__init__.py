"""
MathVerse Services Package

This package contains MathVerse-specific service implementations:
- MathConceptService: Mathematical concept processing and validation
- MathVisualService: Mathematical visualization rendering
- MathReasoningEngine: Proof decomposition and reasoning
- MathAnimationService: Mathematical animations

Licensed under the Apache License, Version 2.0
"""

from .math_concept_service import (
    MathVerseConceptService,
    MathConceptMetadata,
    create_math_concept_service
)

from .math_visual_service import (
    MathVerseVisualService,
    EquationRenderConfig,
    GraphConfig,
    ProofVisualConfig,
    create_math_visual_service
)

from .math_reasoning_engine import (
    MathVerseReasoningEngine,
    ProofStrategy,
    ReasoningStepType,
    ReasoningStep,
    ProofStructure,
    ExplanationTemplate,
    create_math_reasoning_engine
)

from .math_animation_service import (
    MathVerseAnimationService,
    AnimationPreset,
    AnimationKeyframe,
    AnimationConfig,
    FunctionAnimationParams,
    create_math_animation_service
)

__all__ = [
    # Concept Service
    'MathVerseConceptService',
    'MathConceptMetadata',
    'create_math_concept_service',
    
    # Visual Service
    'MathVerseVisualService',
    'EquationRenderConfig',
    'GraphConfig',
    'ProofVisualConfig',
    'create_math_visual_service',
    
    # Reasoning Engine
    'MathVerseReasoningEngine',
    'ProofStrategy',
    'ReasoningStepType',
    'ReasoningStep',
    'ProofStructure',
    'ExplanationTemplate',
    'create_math_reasoning_engine',
    
    # Animation Service
    'MathVerseAnimationService',
    'AnimationPreset',
    'AnimationKeyframe',
    'AnimationConfig',
    'FunctionAnimationParams',
    'create_math_animation_service'
]
