"""
Curriculum Services Module for VisualVerse Content Metadata Layer

This module provides curriculum mapping and standard management functionality,
including importing standards from various frameworks and mapping concepts
to standardized benchmarks.

Licensed under the Apache License, Version 2.0
"""

from .mapper import (
    CurriculumMapper,
    ConceptMapping,
    MappingSuggestion,
    CoverageReport,
    MappingConfidence
)

__all__ = [
    'CurriculumMapper',
    'ConceptMapping',
    'MappingSuggestion',
    'CoverageReport',
    'MappingConfidence'
]
