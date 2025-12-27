"""
Version Control Service for VisualVerse Creator Platform

This module provides Git-like version control functionality for managing
content versions, branching, merging, and collaboration in the VisualVerse
Creator Platform.

Author: MiniMax Agent
Version: 1.0.0
"""

from .version_control import (
    VersionControlService,
    Commit,
    Branch,
    DiffResult,
    MergeResult,
    ConflictType,
    create_commit_hash,
    get_version_control_service
)

__version__ = "1.0.0"

__all__ = [
    "VersionControlService",
    "Commit",
    "Branch",
    "DiffResult",
    "MergeResult",
    "ConflictType",
    "create_commit_hash",
    "get_version_control_service"
]
