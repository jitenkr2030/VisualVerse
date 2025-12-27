"""
VisualVerse Animation Engine - Text Primitive

This module is part of the VisualVerse Animation Engine,
which is licensed under the Apache License, Version 2.0.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Manages font loading, text wrapping, and glyph rendering paths.
Supports LaTeX parsing for mathematical rendering.
"""

import re
import math
from typing import List, Tuple, Optional, Dict, Any, Union
from dataclasses import dataclass
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import logging

from .geometry import Shape, Point, ShapeType

logger = logging.getLogger(__name__)

@dataclass
class TextConfig:
    """Configuration for text rendering"""
    font_size: int = 16
    font_family: str = "Arial"
    font_path: Optional[str] = None
    color: Tuple[int, int, int] = (0, 0, 0)  # RGB
    background_color: Optional[Tuple[int, int, int]] = None
    alignment: str = "left"  # left, center, right
    line_spacing: float = 1.2
    character_spacing: float = 0.0
    max_width: Optional[float] = None
    max_lines: Optional[int] = None
    
    def validate(self):
        """Validate text configuration"""
        if self.font_size <= 0:
            raise ValueError("Font size must be positive")
        if self.alignment not in ["left", "center", "right"]:
            raise ValueError("Alignment must be left, center, or right")
        if self.line_spacing <= 0:
            raise ValueError("Line spacing must be positive")

class Glyph:
    """Represents a single character glyph"""
    
    def __init__(self, char: str, x: float, y: float, width: float, height: float):
        self.char = char
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def get_bounding_box(self) -> Tuple[Point, Point]:
        """Get bounding box of glyph"""
        top_left = Point(self.x, self.y)
        bottom_right = Point(self.x + self.width, self.y + self.height)
        return (top_left, bottom_right)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert glyph to dictionary"""
        return {
            "char": self.char,
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height
        }

class Text(Shape):
    """Represents text with advanced formatting and layout"""
    
    def __init__(self, text: str, position: Point, config: Optional[TextConfig] = None):
        super().__init__(ShapeType.POLYGON)  # Text is treated as polygon for now
        self.text = text
        self.position = position
        self.config = config or TextConfig()
        self.config.validate()
        
        self.font: Optional[ImageFont.FreeTypeFont] = None
        self.glyphs: List[Glyph] = []
        self.latex_processed: bool = False
        
        # Load font
        self._load_font()
        
        # Process text
        self._process_text()
    
    def _load_font(self):
        """Load the specified font"""
        try:
            if self.config.font_path and Path(self.config.font_path).exists():
                self.font = ImageFont.truetype(self.config.font_path, self.config.font_size)
            else:
                # Try to find system fonts
                font_paths = [
                    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
                    "/System/Library/Fonts/Arial.ttf",
                    "C:/Windows/Fonts/arial.ttf"
                ]
                
                font_loaded = False
                for font_path in font_paths:
                    try:
                        if Path(font_path).exists():
                            self.font = ImageFont.truetype(font_path, self.config.font_loaded = True
                            break
_size)
                            font                    except (OSError, IOError):
                        continue
                
                if not font_loaded:
                    self.font = ImageFont.load_default()
                    logger.warning("Could not load custom font, using default")
                    
        except Exception as e:
            logger.warning(f"Failed to load font: {e}, using default")
            self.font = ImageFont.load_default()
    
    def _process_text(self):
        """Process text for rendering"""
        if self._is_latex_text(self.text):
            self.text = self._process_latex(self.text)
            self.latex_processed = True
        
        self.glyphs = self._create_glyphs()
    
    def _is_latex_text(self, text: str) -> bool:
        """Check if text contains LaTeX syntax"""
        latex_patterns = [
            r'\\frac\{', r'\\sqrt\{', r'\\sum\{', r'\\int\{',
            r'\$[^$]*\$', r'\\\w+\{', r'\\[a-zA-Z]+\s'
        ]
        
        for pattern in latex_patterns:
            if re.search(pattern, text):
                return True
        return False
    
    def _process_latex(self, text: str) -> str:
        """Basic LaTeX processing (simplified)"""
        # This is a simplified LaTeX processor
        # In a full implementation, you'd use a proper LaTeX renderer
        
        # Replace common LaTeX commands with Unicode equivalents
        replacements = {
            r'\\alpha': 'α',
            r'\\beta': 'β',
            r'\\gamma': 'γ',
            r'\\delta': 'δ',
            r'\\theta': 'θ',
            r'\\lambda': 'λ',
            r'\\mu': 'μ',
            r'\\pi': 'π',
            r'\\sigma': 'σ',
            r'\\phi': 'φ',
            r'\\psi': 'ψ',
            r'\\omega': 'ω',
            r'\\cdot': '·',
            r'\\times': '×',
            r'\\pm': '±',
            r'\\infty': '∞',
            r'\\leq': '≤',
            r'\\geq': '≥',
            r'\\neq': '≠',
            r'\\approx': '≈',
            r'\\rightarrow': '→',
            r'\\leftarrow': '←',
            r'\\leftrightarrow': '↔'
        }
        
        processed_text = text
        for latex, unicode_char in replacements.items():
            processed_text = re.sub(latex, unicode_char, processed_text)
        
        # Handle fractions (simplified)
        processed_text = re.sub(r'\\frac\{([^}]+)\}\{([^}]+)\}', r'\1/\2', processed_text)
        
        # Handle square roots
        processed_text = re.sub(r'\\sqrt\{([^}]+)\}', r'√\1', processed_text)
        
        # Remove remaining LaTeX formatting
        processed_text = re.sub(r'\\[a-zA-Z]+\{?([^}]*)\}?', r'\1', processed_text)
        processed_text = re.sub(r'[\$\\{\}]', '', processed_text)
        
        return processed_text.strip()
    
    def _create_glyphs(self) -> List[Glyph]:
        """Create glyphs from text"""
        if not self.font:
            return []
        
        glyphs = []
        x_offset = 0
        y_offset = 0
        line_height = self.config.font_size * self.config.line_spacing
        
        lines = self._wrap_text()
        
        for line_idx, line in enumerate(lines):
            y_pos = self.position.y + line_idx * line_height
            
            for char in line:
                if char == '\n':
                    continue
                
                # Get character dimensions
                bbox = self.font.getbbox(char)
                char_width = bbox[2] - bbox[0]
                char_height = bbox[3] - bbox[1]
                
                # Apply character spacing
                char_width += self.config.character_spacing
                
                # Create glyph
                glyph = Glyph(char, self.position.x + x_offset, y_pos, char_width, char_height)
                glyphs.append(glyph)
                
                x_offset += char_width
            
            # Move to next line
            x_offset = 0
        
        return glyphs
    
    def _wrap_text(self) -> List[str]:
        """Wrap text according to max_width"""
        if not self.config.max_width:
            return [self.text]
        
        if not self.font:
            return [self.text]
        
        lines = []
        words = self.text.split()
        current_line = ""
        
        for word in words:
            test_line = current_line + (" " if current_line else "") + word
            test_bbox = self.font.getbbox(test_line)
            test_width = test_bbox[2] - test_bbox[0]
            
            if test_width <= self.config.max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                    current_line = word
                else:
                    # Word is longer than max_width, force break
                    lines.append(word)
                    current_line = ""
        
        if current_line:
            lines.append(current_line)
        
        # Apply max_lines limit
        if self.config.max_lines and len(lines) > self.config.max_lines:
            lines = lines[:self.config.max_lines]
            # Add ellipsis to last line if truncated
            if len(lines) > 0:
                last_line = lines[-1]
                if len(last_line) > 3:
                    lines[-1] = last_line[:-3] + "..."
        
        return lines
    
    def get_coordinates(self) -> List[Point]:
        """Get bounding box coordinates of text"""
        if not self.glyphs:
            return [self.position]
        
        min_x = min(g.x for g in self.glyphs)
        min_y = min(g.y for g in self.glyphs)
        max_x = max(g.x + g.width for g in self.glyphs)
        max_y = max(g.y + g.height for g in self.glyphs)
        
        return [
            Point(min_x, min_y),
            Point(max_x, min_y),
            Point(max_x, max_y),
            Point(min_x, max_y)
        ]
    
    def get_bounding_box(self) -> Tuple[Point, Point]:
        """Get bounding box of text"""
        if not self.glyphs:
            return (self.position, self.position)
        
        min_x = min(g.x for g in self.glyphs)
        min_y = min(g.y for g in self.glyphs)
        max_x = max(g.x + g.width for g in self.glyphs)
        max_y = max(g.y + g.height for g in self.glyphs)
        
        return (Point(min_x, min_y), Point(max_x, max_y))
    
    def get_text_dimensions(self) -> Tuple[float, float]:
        """Get total text width and height"""
        if not self.glyphs:
            return (0, 0)
        
        min_x = min(g.x for g in self.glyphs)
        max_x = max(g.x + g.width for g in self.glyphs)
        min_y = min(g.y for g in self.glyphs)
        max_y = max(g.y + g.height for g in self.glyphs)
        
        return (max_x - min_x, max_y - min_y)
    
    def render_to_image(self, width: Optional[int] = None, height: Optional[int] = None) -> Image.Image:
        """Render text to a PIL Image"""
        if not self.glyphs:
            # Create empty image
            w = width or self.config.font_size * len(self.text)
            h = height or self.config.font_size
            return Image.new("RGBA", (w, h), (0, 0, 0, 0))
        
        # Calculate image dimensions
        bbox = self.get_bounding_box()
        img_width = width or int(bbox[1].x - bbox[0].x)
        img_height = height or int(bbox[1].y - bbox[0].y)
        
        # Create image
        img = Image.new("RGBA", (img_width, img_height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Draw each glyph
        for glyph in self.glyphs:
            if self.font:
                # Calculate position relative to image
                x = int(glyph.x - bbox[0].x)
                y = int(glyph.y - bbox[0].y)
                
                # Draw character
                draw.text(
                    (x, y),
                    glyph.char,
                    fill=self.config.color,
                    font=self.font
                )
        
        return img
    
    def update_text(self, new_text: str):
        """Update the text content"""
        self.text = new_text
        self.glyphs = []
        self.latex_processed = False
        self._process_text()
    
    def update_config(self, new_config: TextConfig):
        """Update text configuration"""
        self.config = new_config
        self.config.validate()
        self._load_font()
        self.glyphs = []
        self._process_text()
    
    def split_into_lines(self) -> List[str]:
        """Split text into individual lines"""
        return self.text.split('\n')
    
    def get_line_count(self) -> int:
        """Get number of lines"""
        return len(self.split_into_lines())
    
    def get_word_count(self) -> int:
        """Get number of words"""
        return len(self.text.split())
    
    def get_character_count(self, include_spaces: bool = True) -> int:
        """Get number of characters"""
        if include_spaces:
            return len(self.text)
        return len(self.text.replace(' ', ''))
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert text to dictionary representation"""
        width, height = self.get_text_dimensions()
        bbox = self.get_bounding_box()
        
        return {
            **super().to_dict(),
            "text": self.text,
            "position": {"x": self.position.x, "y": self.position.y},
            "config": {
                "font_size": self.config.font_size,
                "font_family": self.config.font_family,
                "color": self.config.color,
                "alignment": self.config.alignment,
                "line_spacing": self.config.line_spacing,
                "max_width": self.config.max_width,
                "max_lines": self.config.max_lines
            },
            "dimensions": {"width": width, "height": height},
            "bounding_box": {
                "top_left": {"x": bbox[0].x, "y": bbox[0].y},
                "bottom_right": {"x": bbox[1].x, "y": bbox[1].y}
            },
            "glyphs": [glyph.to_dict() for glyph in self.glyphs],
            "latex_processed": self.latex_processed,
            "statistics": {
                "line_count": self.get_line_count(),
                "word_count": self.get_word_count(),
                "character_count": self.get_character_count(),
                "character_count_no_spaces": self.get_character_count(False)
            }
        }

# Utility functions for text creation
def create_text(
    content: str,
    x: float,
    y: float,
    font_size: int = 16,
    font_family: str = "Arial",
    color: Tuple[int, int, int] = (0, 0, 0),
    max_width: Optional[float] = None
) -> Text:
    """Create a text object with basic configuration"""
    config = TextConfig(
        font_size=font_size,
        font_family=font_family,
        color=color,
        max_width=max_width
    )
    return Text(content, Point(x, y), config)

def create_math_text(
    latex_content: str,
    x: float,
    y: float,
    font_size: int = 16,
    color: Tuple[int, int, int] = (0, 0, 0)
) -> Text:
    """Create text with LaTeX math support"""
    config = TextConfig(
        font_size=font_size,
        color=color,
        font_family="Times New Roman"  # Better for math
    )
    return Text(latex_content, Point(x, y), config)