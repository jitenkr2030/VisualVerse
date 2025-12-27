"""
VisualVerse Platform Modules - Content Verticals

This package contains platform-specific modules for different
educational verticals. Licensing varies by component.

OPEN-SOURCE COMPONENTS (Apache 2.0):
- MathVerse core animations and syllabus
- PhysicsVerse core animations and syllabus
- ChemistryVerse core animations and syllabus
- AlgorithmVerse core animations and syllabus

PROPRIETARY COMPONENTS (See respective directories):
- FinVerse professional content
- Vertical-specific content packs (*/pro/)
- Premium assessment libraries

For licensing details, see:
- /platforms/*/LICENSE for open-source components
- /platforms/*/pro/LICENSE for proprietary components

For more information, visit: https://visualverse.io
"""

from .mathverse import MathVerse
from .physicsverse import PhysicsVerse
from .chemverse import ChemistryVerse
from .algverse import AlgorithmVerse

__all__ = [
    "MathVerse",
    "PhysicsVerse",
    "ChemistryVerse",
    "AlgorithmVerse",
]
