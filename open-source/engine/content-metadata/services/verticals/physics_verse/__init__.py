"""
PhysicsVerse - Physics Visualization and Learning Platform

This package provides comprehensive physics simulation and educational
capabilities for the VisualVerse learning platform. It includes services for
physics concept understanding, visual representation, animation generation,
and algorithmic reasoning.

Submodules:
- physics_core: Mathematical foundations and physics calculations
- physics_concept_service: Formula management and educational content
- physics_visual_service: Physics simulation and diagram rendering
- physics_animation_service: Physics process animations
- physics_reasoning_engine: Physics problem analysis and solving

Author: MiniMax Agent
Version: 1.0.0
"""

from .physics_core import (
    Vector2D,
    Vector3D,
    Complex,
    Matrix3x3,
    PhysicsState,
    PhysicsConstants,
    UnitConverter,
    NumericalIntegrator,
    PhysicsFormula,
    PhysicsFormulaRegistry,
    PhysicsVisualConfig,
    calculate_kinematic_motion,
    calculate_projectile_motion,
    calculate_orbit_parameters,
    calculate_shock_parameters,
    calculate_wave_properties,
    calculate_rc_circuit,
    calculate_rlc_circuit,
    VectorOperationType,
    IntegrationMethod
)

from .physics_concept_service import (
    PhysicsVerseConceptService,
    PhysicsDomain,
    MechanicsSubdomain,
    OpticsSubdomain,
    ElectromagnetismSubdomain,
    PhysicsConceptType,
    PhysicsParameter,
    PhysicsProblem,
    PhysicsSolution,
    PhysicsConcept,
    PhysicsVisualConfig
)

from .physics_visual_service import (
    PhysicsVerseVisualService,
    PhysicsVisualType,
    VectorDisplayType,
    ColorScheme,
    VectorStyle,
    GraphConfig,
    FieldVisualConfig,
    CircuitVisualConfig,
    OpticalConfig,
    PhysicsVisualization
)

from .physics_animation_service import (
    PhysicsVerseAnimationService,
    AnimationState,
    AnimationType,
    EasingFunction,
    AnimationKeyframe,
    AnimationFrame,
    MotionAnimationConfig,
    WaveAnimationConfig,
    CircuitAnimationConfig,
    PhysicsAnimation
)

from .physics_reasoning_engine import (
    PhysicsVerseReasoningEngine,
    PhysicsDomain as ReasoningPhysicsDomain,
    ProblemDifficulty,
    SolutionStatus,
    PhysicsProblem as ReasoningPhysicsProblem,
    SolutionStep,
    PhysicsSolution as ReasoningPhysicsSolution,
    ConceptualAnalysis,
    DimensionalAnalysis
)


# Factory functions for service creation
def create_physics_concept_service(config: dict = None) -> PhysicsVerseConceptService:
    """
    Create a PhysicsVerseConceptService instance.
    
    Args:
        config: Optional configuration dictionary
        
    Returns:
        Configured PhysicsVerseConceptService instance
    """
    service = PhysicsVerseConceptService()
    if config:
        service.configure(config)
    return service


def create_physics_visual_service(config: dict = None) -> PhysicsVerseVisualService:
    """
    Create a PhysicsVerseVisualService instance.
    
    Args:
        config: Optional configuration dictionary
        
    Returns:
        Configured PhysicsVerseVisualService instance
    """
    service = PhysicsVerseVisualService()
    if config:
        service.configure(config)
    return service


def create_physics_animation_service(config: dict = None) -> PhysicsVerseAnimationService:
    """
    Create a PhysicsVerseAnimationService instance.
    
    Args:
        config: Optional configuration dictionary
        
    Returns:
        Configured PhysicsVerseAnimationService instance
    """
    service = PhysicsVerseAnimationService()
    if config:
        service.configure(config)
    return service


def create_physics_reasoning_engine(config: dict = None) -> PhysicsVerseReasoningEngine:
    """
    Create a PhysicsVerseReasoningEngine instance.
    
    Args:
        config: Optional configuration dictionary
        
    Returns:
        Configured PhysicsVerseReasoningEngine instance
    """
    engine = PhysicsVerseReasoningEngine()
    if config:
        engine.configure(config)
    return engine


__all__ = [
    # Core Module
    "Vector2D",
    "Vector3D",
    "Complex",
    "Matrix3x3",
    "PhysicsState",
    "PhysicsConstants",
    "UnitConverter",
    "NumericalIntegrator",
    "PhysicsFormula",
    "PhysicsFormulaRegistry",
    "PhysicsVisualConfig",
    "calculate_kinematic_motion",
    "calculate_projectile_motion",
    "calculate_orbit_parameters",
    "calculate_shock_parameters",
    "calculate_wave_properties",
    "calculate_rc_circuit",
    "calculate_rlc_circuit",
    "VectorOperationType",
    "IntegrationMethod",
    
    # Concept Service
    "PhysicsVerseConceptService",
    "PhysicsDomain",
    "MechanicsSubdomain",
    "OpticsSubdomain",
    "ElectromagnetismSubdomain",
    "PhysicsConceptType",
    "PhysicsParameter",
    "PhysicsProblem",
    "PhysicsSolution",
    "PhysicsConcept",
    
    # Visual Service
    "PhysicsVerseVisualService",
    "PhysicsVisualType",
    "VectorDisplayType",
    "ColorScheme",
    "VectorStyle",
    "GraphConfig",
    "FieldVisualConfig",
    "CircuitVisualConfig",
    "OpticalConfig",
    "PhysicsVisualization",
    
    # Animation Service
    "PhysicsVerseAnimationService",
    "AnimationState",
    "AnimationType",
    "EasingFunction",
    "AnimationKeyframe",
    "AnimationFrame",
    "MotionAnimationConfig",
    "WaveAnimationConfig",
    "CircuitAnimationConfig",
    "PhysicsAnimation",
    
    # Reasoning Engine
    "PhysicsVerseReasoningEngine",
    "ProblemDifficulty",
    "SolutionStatus",
    "SolutionStep",
    "ConceptualAnalysis",
    "DimensionalAnalysis",
    
    # Factory Functions
    "create_physics_concept_service",
    "create_physics_visual_service",
    "create_physics_animation_service",
    "create_physics_reasoning_engine"
]

__version__ = "1.0.0"
__author__ = "MiniMax Agent"
