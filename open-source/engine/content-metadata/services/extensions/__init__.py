"""
Service Extensions Package

This package contains base classes and utilities for extending core services
with domain-specific functionality for different verticals.
"""

from .service_extension_base import (
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
    # Registry
    'ExtensionRegistry',
    'get_extension_registry',
    
    # Base classes
    'ServiceExtension',
    'ConceptServiceExtension',
    'VisualServiceExtension',
    'AnimationServiceExtension',
    'ReasoningEngineExtension',
    
    # Context
    'ExtensionContext',
    
    # Implementations
    'MathConceptServiceExtension',
    'PhysicsConceptServiceExtension',
    'ChemistryConceptServiceExtension',
    'AlgorithmVisualServiceExtension',
    'FinanceAnimationServiceExtension',
    'MathReasoningEngineExtension',
    
    # Loaders
    'VerticalLoader',
    'get_vertical_loader'
]
