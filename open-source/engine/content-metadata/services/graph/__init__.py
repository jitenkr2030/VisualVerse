"""
Graph Services Module for VisualVerse Content Metadata Layer

This module provides graph-based services for managing concept dependencies,
including the NetworkX-based dependency graph engine and cross-subject linking
functionality.

Licensed under the Apache License, Version 2.0
"""

from .engine import (
    DependencyGraphEngine,
    GraphNode,
    GraphEdge,
    PathResult,
    GraphStats,
    RelationshipType
)

from .linker import (
    InterdisciplinaryLinker,
    CrossSubjectLink,
    InterdisciplinaryPath,
    SharedPrerequisite,
    TransferabilityScore
)

__all__ = [
    # Engine
    'DependencyGraphEngine',
    'GraphNode',
    'GraphEdge',
    'PathResult',
    'GraphStats',
    'RelationshipType',
    
    # Linker
    'InterdisciplinaryLinker',
    'CrossSubjectLink',
    'InterdisciplinaryPath',
    'SharedPrerequisite',
    'TransferabilityScore'
]
