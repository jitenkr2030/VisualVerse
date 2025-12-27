"""
AlgoVerse - Algorithm Visualization and Learning Platform

This package provides comprehensive algorithm visualization and educational
capabilities for the VisualVerse learning platform. It includes services for
concept understanding, visual representation, animation generation, and
algorithmic reasoning.

Submodules:
- algo_concept_service: Code parsing and complexity analysis
- algo_visual_service: Data structure and algorithm visualization
- algo_animation_service: Animation frame generation for algorithms
- algo_reasoning_engine: Algorithm analysis and explanation generation

Author: MiniMax Agent
Version: 1.0.0
"""

from .algo_concept_service import (
    AlgoVerseConceptService,
    CodeElement,
    CodeElementType,
    ComplexityMetrics,
    ControlFlowGraph,
    AlgoConceptConfig
)

from .algo_visual_service import (
    AlgoVerseVisualService,
    VisualStyle,
    VisualizationType,
    NodeStyle,
    EdgeStyle,
    LayoutAlgorithm,
    GraphVisualization,
    TreeVisualization,
    ArrayVisualization,
    VisualizationResult
)

from .algo_animation_service import (
    AlgoVerseAnimationService,
    AnimationType,
    SortingAlgorithm,
    GraphTraversalType,
    TreeTraversalType,
    ElementState,
    AnimationFrame,
    GraphAnimationFrame,
    TreeAnimationFrame,
    AnimationSequence
)

from .algo_reasoning_engine import (
    AlgoVerseReasoningEngine,
    ComplexityClass,
    AlgorithmCategory,
    CorrectnessStatus,
    ComplexityAnalysis,
    CorrectnessVerification,
    OptimizationSuggestion,
    AlgorithmExplanation,
    AlgorithmComparison
)


# Factory functions for service creation
def create_algo_concept_service(config: dict = None) -> AlgoVerseConceptService:
    """
    Create an AlgoVerseConceptService instance.
    
    Args:
        config: Optional configuration dictionary
        
    Returns:
        Configured AlgoVerseConceptService instance
    """
    service = AlgoVerseConceptService()
    if config:
        service.configure(config)
    return service


def create_algo_visual_service(config: dict = None) -> AlgoVerseVisualService:
    """
    Create an AlgoVerseVisualService instance.
    
    Args:
        config: Optional configuration dictionary
        
    Returns:
        Configured AlgoVerseVisualService instance
    """
    service = AlgoVerseVisualService()
    if config:
        service.configure(config)
    return service


def create_algo_animation_service(config: dict = None) -> AlgoVerseAnimationService:
    """
    Create an AlgoVerseAnimationService instance.
    
    Args:
        config: Optional configuration dictionary
        
    Returns:
        Configured AlgoVerseAnimationService instance
    """
    service = AlgoVerseAnimationService()
    if config:
        service.configure(config)
    return service


def create_algo_reasoning_engine(config: dict = None) -> AlgoVerseReasoningEngine:
    """
    Create an AlgoVerseReasoningEngine instance.
    
    Args:
        config: Optional configuration dictionary
        
    Returns:
        Configured AlgoVerseReasoningEngine instance
    """
    engine = AlgoVerseReasoningEngine()
    if config:
        engine.configure(config)
    return engine


__all__ = [
    # Concept Service
    "AlgoVerseConceptService",
    "CodeElement",
    "CodeElementType",
    "ComplexityMetrics",
    "ControlFlowGraph",
    "AlgoConceptConfig",
    
    # Visual Service
    "AlgoVerseVisualService",
    "VisualStyle",
    "VisualizationType",
    "NodeStyle",
    "EdgeStyle",
    "LayoutAlgorithm",
    "GraphVisualization",
    "TreeVisualization",
    "ArrayVisualization",
    "VisualizationResult",
    
    # Animation Service
    "AlgoVerseAnimationService",
    "AnimationType",
    "SortingAlgorithm",
    "GraphTraversalType",
    "TreeTraversalType",
    "ElementState",
    "AnimationFrame",
    "GraphAnimationFrame",
    "TreeAnimationFrame",
    "AnimationSequence",
    
    # Reasoning Engine
    "AlgoVerseReasoningEngine",
    "ComplexityClass",
    "AlgorithmCategory",
    "CorrectnessStatus",
    "ComplexityAnalysis",
    "CorrectnessVerification",
    "OptimizationSuggestion",
    "AlgorithmExplanation",
    "AlgorithmComparison",
    
    # Factory Functions
    "create_algo_concept_service",
    "create_algo_visual_service",
    "create_algo_animation_service",
    "create_algo_reasoning_engine"
]

__version__ = "1.0.0"
__author__ = "MiniMax Agent"
