"""
VisualVerse Animation Engine - Base Theme

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

Defines the standard color palette, default font families, and stroke widths
that form the foundation for all visual themes.
"""

from typing import Dict, Tuple, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
import json
from pathlib import Path

class ColorRole(Enum):
    """Color role enumeration"""
    BACKGROUND = "background"
    SURFACE = "surface"
    PRIMARY = "primary"
    SECONDARY = "secondary"
    ACCENT = "accent"
    ERROR = "error"
    WARNING = "warning"
    SUCCESS = "success"
    INFO = "info"
    TEXT_PRIMARY = "text_primary"
    TEXT_SECONDARY = "text_secondary"
    TEXT_DISABLED = "text_disabled"
    BORDER = "border"
    DIVIDER = "divider"
    SHADOW = "shadow"
    HIGHLIGHT = "highlight"

@dataclass
class ColorPalette:
    """Color palette configuration"""
    background: Tuple[int, int, int, int] = (248, 249, 250, 255)  # Light gray
    surface: Tuple[int, int, int, int] = (255, 255, 255, 255)     # White
    primary: Tuple[int, int, int, int] = (59, 130, 246, 255)      # Blue
    secondary: Tuple[int, int, int, int] = (107, 114, 128, 255)   # Gray
    accent: Tuple[int, int, int, int] = (16, 185, 129, 255)       # Green
    error: Tuple[int, int, int, int] = (239, 68, 68, 255)         # Red
    warning: Tuple[int, int, int, int] = (245, 158, 11, 255)      # Orange
    success: Tuple[int, int, int, int] = (34, 197, 94, 255)       # Green
    info: Tuple[int, int, int, int] = (59, 130, 246, 255)         # Blue
    
    # Text colors
    text_primary: Tuple[int, int, int, int] = (17, 24, 39, 255)   # Dark gray
    text_secondary: Tuple[int, int, int, int] = (107, 114, 128, 255)  # Medium gray
    text_disabled: Tuple[int, int, int, int] = (156, 163, 175, 255)   # Light gray
    
    # Structural colors
    border: Tuple[int, int, int, int] = (229, 231, 235, 255)      # Light border
    divider: Tuple[int, int, int, int] = (209, 213, 219, 255)     # Divider
    shadow: Tuple[int, int, int, int] = (0, 0, 0, 25)             # Semi-transparent black
    highlight: Tuple[int, int, int, int] = (59, 130, 246, 64)     # Semi-transparent blue
    
    def get_color(self, role: ColorRole) -> Tuple[int, int, int, int]:
        """Get color for a specific role"""
        return getattr(self, role.value, self.background)
    
    def to_dict(self) -> Dict[str, List[int]]:
        """Convert color palette to dictionary"""
        return {
            role.value: list(getattr(self, role.value))
            for role in ColorRole
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, List[int]]) -> 'ColorPalette':
        """Create color palette from dictionary"""
        kwargs = {}
        for role in ColorRole:
            if role.value in data:
                kwargs[role.value] = tuple(data[role.value])
        return cls(**kwargs)

@dataclass
class FontConfiguration:
    """Font family configuration"""
    primary: str = "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
    secondary: str = "Georgia, 'Times New Roman', serif"
    monospace: str = "'Fira Code', 'Monaco', 'Cascadia Code', 'Roboto Mono', monospace"
    display: str = "'Inter', 'Poppins', sans-serif"
    math: str = "'STIX Two Math', 'Times New Roman', serif"
    
    # Font sizes
    size_xs: int = 12
    size_sm: int = 14
    size_base: int = 16
    size_lg: int = 18
    size_xl: int = 20
    size_2xl: int = 24
    size_3xl: int = 30
    size_4xl: int = 36
    
    # Line heights
    line_height_tight: float = 1.25
    line_height_snug: float = 1.375
    line_height_normal: float = 1.5
    line_height_relaxed: float = 1.625
    line_height_loose: float = 2.0
    
    # Font weights
    weight_thin: int = 100
    weight_light: int = 300
    weight_normal: int = 400
    weight_medium: int = 500
    weight_semibold: int = 600
    weight_bold: int = 700
    weight_extrabold: int = 800
    weight_black: int = 900
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert font configuration to dictionary"""
        return {
            "families": {
                "primary": self.primary,
                "secondary": self.secondary,
                "monospace": self.monospace,
                "display": self.display,
                "math": self.math
            },
            "sizes": {
                "xs": self.size_xs,
                "sm": self.size_sm,
                "base": self.size_base,
                "lg": self.size_lg,
                "xl": self.size_xl,
                "2xl": self.size_2xl,
                "3xl": self.size_3xl,
                "4xl": self.size_4xl
            },
            "line_heights": {
                "tight": self.line_height_tight,
                "snug": self.line_height_snug,
                "normal": self.line_height_normal,
                "relaxed": self.line_height_relaxed,
                "loose": self.line_height_loose
            },
            "weights": {
                "thin": self.weight_thin,
                "light": self.weight_light,
                "normal": self.weight_normal,
                "medium": self.weight_medium,
                "semibold": self.weight_semibold,
                "bold": self.weight_bold,
                "extrabold": self.weight_extrabold,
                "black": self.weight_black
            }
        }

@dataclass
class StrokeConfiguration:
    """Stroke width and style configuration"""
    width_thin: float = 1.0
    width_normal: float = 2.0
    width_thick: float = 4.0
    width_extra_thick: float = 8.0
    
    # Line styles
    style_solid: str = "solid"
    style_dashed: str = "dashed"
    style_dotted: str = "dotted"
    style_dashdot: str = "dashdot"
    
    # Line caps
    cap_butt: str = "butt"
    cap_round: str = "round"
    cap_square: str = "square"
    
    # Line joins
    join_miter: str = "miter"
    join_bevel: str = "bevel"
    join_round: str = "round"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert stroke configuration to dictionary"""
        return {
            "widths": {
                "thin": self.width_thin,
                "normal": self.width_normal,
                "thick": self.width_thick,
                "extra_thick": self.width_extra_thick
            },
            "styles": {
                "solid": self.style_solid,
                "dashed": self.style_dashed,
                "dotted": self.style_dotted,
                "dashdot": self.style_dashdot
            },
            "caps": {
                "butt": self.cap_butt,
                "round": self.cap_round,
                "square": self.cap_square
            },
            "joins": {
                "miter": self.join_miter,
                "bevel": self.join_bevel,
                "round": self.join_round
            }
        }

@dataclass
class AnimationConfiguration:
    """Animation timing and easing configuration"""
    # Duration presets (in milliseconds)
    duration_fast: int = 150
    duration_normal: int = 300
    duration_slow: int = 500
    duration_very_slow: int = 1000
    
    # Easing functions
    easing_linear: str = "linear"
    easing_ease: str = "ease"
    easing_ease_in: str = "ease-in"
    easing_ease_out: str = "ease-out"
    easing_ease_in_out: str = "ease-in-out"
    
    # Animation curves
    curve_bounce: str = "cubic-bezier(0.68, -0.55, 0.265, 1.55)"
    curve_elastic: str = "cubic-bezier(0.175, 0.885, 0.32, 1.275)"
    curve_smooth: str = "cubic-bezier(0.25, 0.46, 0.45, 0.94)"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert animation configuration to dictionary"""
        return {
            "durations": {
                "fast": self.duration_fast,
                "normal": self.duration_normal,
                "slow": self.duration_slow,
                "very_slow": self.duration_very_slow
            },
            "easing": {
                "linear": self.easing_linear,
                "ease": self.easing_ease,
                "ease_in": self.easing_ease_in,
                "ease_out": self.easing_ease_out,
                "ease_in_out": self.easing_ease_in_out
            },
            "curves": {
                "bounce": self.curve_bounce,
                "elastic": self.curve_elastic,
                "smooth": self.curve_smooth
            }
        }

@dataclass
class BaseTheme:
    """Base theme configuration"""
    name: str = "Base Theme"
    description: str = "Default theme for VisualVerse"
    version: str = "1.0.0"
    
    # Theme components
    colors: ColorPalette = field(default_factory=ColorPalette)
    fonts: FontConfiguration = field(default_factory=FontConfiguration)
    strokes: StrokeConfiguration = field(default_factory=StrokeConfiguration)
    animations: AnimationConfiguration = field(default_factory=AnimationConfiguration)
    
    # Component-specific styles
    component_styles: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    
    def get_color(self, role: ColorRole) -> Tuple[int, int, int, int]:
        """Get color for a specific role"""
        return self.colors.get_color(role)
    
    def get_font(self, family: str = "primary") -> str:
        """Get font family"""
        return getattr(self.fonts, family, self.fonts.primary)
    
    def get_font_size(self, size: str = "base") -> int:
        """Get font size"""
        return getattr(self.fonts, f"size_{size}", self.fonts.size_base)
    
    def get_stroke_width(self, width: str = "normal") -> float:
        """Get stroke width"""
        return getattr(self.strokes, f"width_{width}", self.strokes.width_normal)
    
    def get_animation_duration(self, duration: str = "normal") -> int:
        """Get animation duration"""
        return getattr(self.animations, f"duration_{duration}", self.animations.duration_normal)
    
    def get_component_style(self, component: str, property: str, default: Any = None) -> Any:
        """Get component-specific style"""
        if component in self.component_styles and property in self.component_styles[component]:
            return self.component_styles[component][property]
        return default
    
    def set_component_style(self, component: str, property: str, value: Any):
        """Set component-specific style"""
        if component not in self.component_styles:
            self.component_styles[component] = {}
        self.component_styles[component][property] = value
    
    def create_button_style(self, variant: str = "primary") -> Dict[str, Any]:
        """Create button style configuration"""
        if variant == "primary":
            return {
                "background_color": self.get_color(ColorRole.PRIMARY),
                "text_color": self.get_color(ColorRole.SURFACE),
                "border_color": self.get_color(ColorRole.PRIMARY),
                "border_width": self.get_stroke_width("thin"),
                "border_radius": 8,
                "padding": {"x": 16, "y": 8},
                "font_family": self.get_font("primary"),
                "font_size": self.get_font_size("base"),
                "font_weight": self.fonts.weight_medium,
                "hover": {
                    "background_color": self.get_color(ColorRole.PRIMARY),
                    "opacity": 0.9
                }
            }
        elif variant == "secondary":
            return {
                "background_color": "transparent",
                "text_color": self.get_color(ColorRole.PRIMARY),
                "border_color": self.get_color(ColorRole.PRIMARY),
                "border_width": self.get_stroke_width("thin"),
                "border_radius": 8,
                "padding": {"x": 16, "y": 8},
                "font_family": self.get_font("primary"),
                "font_size": self.get_font_size("base"),
                "font_weight": self.fonts.weight_medium,
                "hover": {
                    "background_color": self.get_color(ColorRole.PRIMARY),
                    "opacity": 0.1
                }
            }
        else:
            return {}
    
    def create_card_style(self) -> Dict[str, Any]:
        """Create card style configuration"""
        return {
            "background_color": self.get_color(ColorRole.SURFACE),
            "border_color": self.get_color(ColorRole.BORDER),
            "border_width": self.get_stroke_width("thin"),
            "border_radius": 12,
            "padding": 24,
            "shadow": {
                "color": self.get_color(ColorRole.SHADOW),
                "blur": 10,
                "spread": 0,
                "offset_x": 0,
                "offset_y": 2
            }
        }
    
    def create_text_style(self, variant: str = "body") -> Dict[str, Any]:
        """Create text style configuration"""
        if variant == "heading":
            return {
                "color": self.get_color(ColorRole.TEXT_PRIMARY),
                "font_family": self.get_font("primary"),
                "font_weight": self.fonts.weight_bold,
                "line_height": self.fonts.line_height_tight,
                "margin_bottom": 16
            }
        elif variant == "body":
            return {
                "color": self.get_color(ColorRole.TEXT_PRIMARY),
                "font_family": self.get_font("primary"),
                "font_size": self.get_font_size("base"),
                "font_weight": self.fonts.weight_normal,
                "line_height": self.fonts.line_height_normal,
                "margin_bottom": 8
            }
        elif variant == "caption":
            return {
                "color": self.get_color(ColorRole.TEXT_SECONDARY),
                "font_family": self.get_font("primary"),
                "font_size": self.get_font_size("sm"),
                "font_weight": self.fonts.weight_normal,
                "line_height": self.fonts.line_height_normal
            }
        else:
            return {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert theme to dictionary"""
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "colors": self.colors.to_dict(),
            "fonts": self.fonts.to_dict(),
            "strokes": self.strokes.to_dict(),
            "animations": self.animations.to_dict(),
            "component_styles": self.component_styles
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BaseTheme':
        """Create theme from dictionary"""
        # Extract nested configurations
        colors_data = data.get("colors", {})
        fonts_data = data.get("fonts", {})
        strokes_data = data.get("strokes", {})
        animations_data = data.get("animations", {})
        
        colors = ColorPalette.from_dict(colors_data) if colors_data else ColorPalette()
        fonts = FontConfiguration(**fonts_data) if fonts_data else FontConfiguration()
        strokes = StrokeConfiguration(**strokes_data) if strokes_data else StrokeConfiguration()
        animations = AnimationConfiguration(**animations_data) if animations_data else AnimationConfiguration()
        
        return cls(
            name=data.get("name", "Base Theme"),
            description=data.get("description", ""),
            version=data.get("version", "1.0.0"),
            colors=colors,
            fonts=fonts,
            strokes=strokes,
            animations=animations,
            component_styles=data.get("component_styles", {})
        )
    
    def save_to_file(self, file_path: Path):
        """Save theme to JSON file"""
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2)
    
    @classmethod
    def load_from_file(cls, file_path: Path) -> 'BaseTheme':
        """Load theme from JSON file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls.from_dict(data)
    
    def create_variation(self, name: str, modifications: Dict[str, Any]) -> 'BaseTheme':
        """Create a variation of this theme with modifications"""
        import copy
        new_theme = copy.deepcopy(self)
        new_theme.name = name
        
        # Apply modifications
        for key, value in modifications.items():
            if hasattr(new_theme, key):
                setattr(new_theme, key, value)
            elif key in ["colors", "fonts", "strokes", "animations"]:
                # Handle nested configurations
                config_obj = getattr(new_theme, key)
                for sub_key, sub_value in value.items():
                    if hasattr(config_obj, sub_key):
                        setattr(config_obj, sub_key, sub_value)
        
        return new_theme