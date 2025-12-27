"""
VerseScript DSL (Domain Specific Language) Package

This package provides the domain-specific language infrastructure for creating
educational content across math, physics, chemistry, algorithms, and finance
domains in the VisualVerse platform.

Author: MiniMax Agent
Version: 1.0.0
"""

from .parser import VerseScriptParser
from .compiler import DSLCompiler
from .templates import ContentTemplate, TemplateRegistry

__version__ = "1.0.0"

__all__ = [
    "VerseScriptParser",
    "DSLCompiler",
    "ContentTemplate",
    "TemplateRegistry"
]
