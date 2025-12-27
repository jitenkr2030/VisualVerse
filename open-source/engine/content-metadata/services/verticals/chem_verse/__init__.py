"""
ChemVerse - Chemistry Visualization and Learning Platform

This package provides comprehensive chemistry visualization and educational
capabilities for the VisualVerse learning platform. It includes services for
chemistry concept management, molecular visualization, reaction animations,
and algorithmic problem solving.

Submodules:
- chem_core: Mathematical foundations and chemistry data structures
- chem_concept_service: Formula management and educational content
- chem_visual_service: Molecular structure and compound visualization
- chem_animation_service: Chemical reaction animations
- chem_reasoning_engine: Chemical problem analysis and solving

Author: MiniMax Agent
Version: 1.0.0
"""

from .chem_core import (
    ElementSymbol,
    BondType,
    HybridizationType,
    ReactionType,
    Phase,
    ElementData,
    Vector3D,
    Atom,
    Bond,
    Molecule,
    ChemicalReaction,
    ChemicalConstants,
    UnitConverter,
    StoichiometryCalculator,
    PHCalculator,
    ElectrochemistryCalculator,
    ReactionAnimationConfig,
    MoleculeVisualConfig
)

from .chem_concept_service import (
    ChemDomain,
    DifficultyLevel,
    ChemistryConcept,
    LessonContent,
    PracticeProblem,
    PeriodicTable,
    ConceptRepository,
    ChemVerseConceptService,
    create_chem_concept_service
)

from .chem_visual_service import (
    RenderStyle,
    ColorScheme,
    VectorDisplayStyle,
    AtomVisual,
    BondVisual,
    MoleculeVisual,
    VectorField,
    ElectronOrbital,
    ReactionCoordinateDiagram,
    MoleculeRenderer,
    StructureComparator,
    ChemVerseVisualService,
    create_chem_visual_service
)

from .chem_animation_service import (
    AnimationState,
    AnimationEasing,
    ParticleEffectType,
    AnimationKeyframe,
    AnimationFrame,
    TransitionState,
    ReactionAnimation,
    MolecularMotion,
    ParticleEffect,
    EasingFunction,
    ReactionAnimator,
    MolecularDynamics,
    ChemVerseAnimationService,
    create_chem_animation_service
)

from .chem_reasoning_engine import (
    ProblemDifficulty,
    SolutionStatus,
    SolutionStep,
    ConceptualAnalysis,
    DimensionalAnalysis,
    ChemistrySolution,
    EquationBalancer,
    StoichiometrySolver,
    AcidBaseSolver,
    ElectrochemistrySolver,
    ThermodynamicsSolver,
    ChemVerseReasoningEngine,
    create_chem_reasoning_engine
)


# Factory functions for service creation
def create_chem_concept_service(config: dict = None) -> ChemVerseConceptService:
    """
    Create a ChemVerseConceptService instance.
    
    Args:
        config: Optional configuration dictionary
        
    Returns:
        Configured ChemVerseConceptService instance
    """
    service = ChemVerseConceptService(config)
    return service


def create_chem_visual_service(config: dict = None) -> ChemVerseVisualService:
    """
    Create a ChemVerseVisualService instance.
    
    Args:
        config: Optional configuration dictionary
        
    Returns:
        Configured ChemVerseVisualService instance
    """
    service = ChemVerseVisualService(config)
    return service


def create_chem_animation_service(config: dict = None) -> ChemVerseAnimationService:
    """
    Create a ChemVerseAnimationService instance.
    
    Args:
        config: Optional configuration dictionary
        
    Returns:
        Configured ChemVerseAnimationService instance
    """
    service = ChemVerseAnimationService(config)
    return service


def create_chem_reasoning_engine(config: dict = None) -> ChemVerseReasoningEngine:
    """
    Create a ChemVerseReasoningEngine instance.
    
    Args:
        config: Optional configuration dictionary
        
    Returns:
        Configured ChemVerseReasoningEngine instance
    """
    engine = ChemVerseReasoningEngine(config)
    return engine


__all__ = [
    # Core Module
    "ElementSymbol",
    "BondType",
    "HybridizationType",
    "ReactionType",
    "Phase",
    "ElementData",
    "Vector3D",
    "Atom",
    "Bond",
    "Molecule",
    "ChemicalReaction",
    "ChemicalConstants",
    "UnitConverter",
    "StoichiometryCalculator",
    "PHCalculator",
    "ElectrochemistryCalculator",
    "ReactionAnimationConfig",
    "MoleculeVisualConfig",
    
    # Concept Service
    "ChemDomain",
    "DifficultyLevel",
    "ChemistryConcept",
    "LessonContent",
    "PracticeProblem",
    "PeriodicTable",
    "ConceptRepository",
    "ChemVerseConceptService",
    "create_chem_concept_service",
    
    # Visual Service
    "RenderStyle",
    "ColorScheme",
    "VectorDisplayStyle",
    "AtomVisual",
    "BondVisual",
    "MoleculeVisual",
    "VectorField",
    "ElectronOrbital",
    "ReactionCoordinateDiagram",
    "MoleculeRenderer",
    "StructureComparator",
    "ChemVerseVisualService",
    "create_chem_visual_service",
    
    # Animation Service
    "AnimationState",
    "AnimationEasing",
    "ParticleEffectType",
    "AnimationKeyframe",
    "AnimationFrame",
    "TransitionState",
    "ReactionAnimation",
    "MolecularMotion",
    "ParticleEffect",
    "EasingFunction",
    "ReactionAnimator",
    "MolecularDynamics",
    "ChemVerseAnimationService",
    "create_chem_animation_service",
    
    # Reasoning Engine
    "ProblemDifficulty",
    "SolutionStatus",
    "SolutionStep",
    "ConceptualAnalysis",
    "DimensionalAnalysis",
    "ChemistrySolution",
    "EquationBalancer",
    "StoichiometrySolver",
    "AcidBaseSolver",
    "ElectrochemistrySolver",
    "ThermodynamicsSolver",
    "ChemVerseReasoningEngine",
    "create_chem_reasoning_engine"
]

__version__ = "1.0.0"
__author__ = "MiniMax Agent"
