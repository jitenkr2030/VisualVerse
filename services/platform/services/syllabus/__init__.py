"""
Syllabus Tagging Service for VisualVerse Creator Platform

This module provides curriculum alignment and syllabus tagging functionality
for organizing educational content by educational standards, boards, and
learning objectives.

Author: MiniMax Agent
Version: 1.0.0
"""

from .syllabus_service import (
    SyllabusTaggingService,
    CurriculumBoard,
    SyllabusTag,
    TagSearchResult,
    ContentTagAssociation,
    ContentAlignmentReport,
    EducationLevel,
    SubjectArea,
    DifficultyLevel,
    SUPPORTED_BOARDS,
    create_syllabus_service
)

__version__ = "1.0.0"

__all__ = [
    "SyllabusTaggingService",
    "CurriculumBoard",
    "SyllabusTag",
    "TagSearchResult",
    "ContentTagAssociation",
    "ContentAlignmentReport",
    "EducationLevel",
    "SubjectArea",
    "DifficultyLevel",
    "SUPPORTED_BOARDS",
    "create_syllabus_service"
]
