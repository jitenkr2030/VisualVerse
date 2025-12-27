# Copyright 2025 VisualVerse Contributors

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
VisualVerse Animation Engine - Open-Source Core

This module is part of the VisualVerse Animation Engine,
which is licensed under the Apache License, Version 2.0.

The Animation Engine provides:
- Scene composition and rendering primitives
- Animation timeline and transformation capabilities
- Export functionality for multiple formats
- Theme support for consistent visual presentation

For more information, visit: https://visualverse.io
"""

from .core.scene_base import Scene, Mobject
from .primitives.geometry import Rectangle, Circle, Line, Arrow
from .primitives.text import Text, Tex
from .primitives.layout import VGroup, HGroup
from .exporters.ffmpeg_exporter import FFmpegExporter
from .exporters.gif_exporter import GIFExporter
from .exporters.image_exporter import ImageExporter
from .themes.base_theme import BaseTheme
from .themes.light_mode import LightTheme
from .themes.dark_mode import DarkTheme
from .validation.scene_validator import SceneValidator

__version__ = "1.0.0"
__author__ = "VisualVerse Contributors"

__all__ = [
    # Core
    "Scene",
    "Mobject",
    # Primitives
    "Rectangle",
    "Circle",
    "Line",
    "Arrow",
    "Text",
    "Tex",
    "VGroup",
    "HGroup",
    # Exporters
    "FFmpegExporter",
    "GIFExporter",
    "ImageExporter",
    # Themes
    "BaseTheme",
    "LightTheme",
    "DarkTheme",
    # Validation
    "SceneValidator",
]
