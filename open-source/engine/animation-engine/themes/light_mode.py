"""
VisualVerse Animation Engine - Light Mode Theme

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

Specialized theme configuration optimized for bright environments
with clean, minimal design and high readability.
"""

from typing import Dict, Any
from .base_theme import BaseTheme, ColorPalette, ColorRole, FontConfiguration, StrokeConfiguration, AnimationConfiguration

class LightModeTheme(BaseTheme):
    """Light mode theme configuration"""
    
    def __init__(self):
        # Initialize with light color palette
        colors = ColorPalette(
            # Light background colors
            background=(248, 249, 250, 255),     # Very light gray
            surface=(255, 255, 255, 255),        # Pure white
            primary=(59, 130, 246, 255),         # Blue
            secondary=(107, 114, 128, 255),      # Gray
            accent=(16, 185, 129, 255),          # Green
            
            # Status colors (optimized for light backgrounds)
            error=(239, 68, 68, 255),            # Red
            warning=(245, 158, 11, 255),         # Orange
            success=(34, 197, 94, 255),          # Green
            info=(59, 130, 246, 255),            # Blue
            
            # Text colors (optimized for light backgrounds)
            text_primary=(17, 24, 39, 255),      # Dark gray
            text_secondary=(107, 114, 128, 255), # Medium gray
            text_disabled=(156, 163, 175, 255),  # Light gray
            
            # Structural colors
            border=(229, 231, 235, 255),         # Light border
            divider=(209, 213, 219, 255),        # Divider
            shadow=(0, 0, 0, 25),                # Subtle shadow
            highlight=(59, 130, 246, 64)         # Semi-transparent blue
        )
        
        # Light mode font configuration
        fonts = FontConfiguration(
            primary="Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
            secondary="Georgia, 'Times New Roman', serif",
            monospace="'Fira Code', 'Monaco', 'Cascadia Code', 'Roboto Mono', monospace",
            display="'Inter', 'Poppins', sans-serif",
            math="'STIX Two Math', 'Times New Roman', serif",
            
            # Standard font sizes
            size_xs=12,
            size_sm=14,
            size_base=16,
            size_lg=18,
            size_xl=20,
            size_2xl=24,
            size_3xl=30,
            size_4xl=36
        )
        
        # Stroke configuration for light theme
        strokes = StrokeConfiguration(
            width_thin=1.0,
            width_normal=2.0,
            width_thick=4.0,
            width_extra_thick=8.0
        )
        
        # Animation configuration (standard timing)
        animations = AnimationConfiguration(
            duration_fast=150,
            duration_normal=300,
            duration_slow=500,
            duration_very_slow=1000
        )
        
        super().__init__(
            name="Light Mode",
            description="Clean and bright theme optimized for well-lit environments and maximum readability",
            version="1.0.0",
            colors=colors,
            fonts=fonts,
            strokes=strokes,
            animations=animations
        )
        
        # Set up light mode specific component styles
        self._setup_light_mode_styles()
    
    def _setup_light_mode_styles(self):
        """Set up component styles specific to light mode"""
        
        # Button styles for light mode
        self.set_component_style("button", "primary", {
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
                "background_color": (49, 130, 206, 255),  # Darker blue
                "transform": "translateY(-1px)",
                "box_shadow": {
                    "color": (0, 0, 0, 100),
                    "blur": 4,
                    "spread": 0,
                    "offset_x": 0,
                    "offset_y": 2
                }
            },
            "active": {
                "background_color": (29, 78, 216, 255),   # Even darker blue
                "transform": "translateY(0px)"
            },
            "disabled": {
                "background_color": self.get_color(ColorRole.SECONDARY),
                "text_color": self.get_color(ColorRole.TEXT_DISABLED),
                "opacity": 0.5,
                "transform": "none"
            }
        })
        
        self.set_component_style("button", "secondary", {
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
            },
            "active": {
                "background_color": self.get_color(ColorRole.PRIMARY),
                "opacity": 0.15
            }
        })
        
        # Card styles for light mode
        self.set_component_style("card", "default", {
            "background_color": self.get_color(ColorRole.SURFACE),
            "border_color": self.get_color(ColorRole.BORDER),
            "border_width": self.get_stroke_width("thin"),
            "border_radius": 12,
            "padding": 24,
            "shadow": {
                "color": (0, 0, 0, 25),
                "blur": 10,
                "spread": 0,
                "offset_x": 0,
                "offset_y": 2
            },
            "hover": {
                "border_color": self.get_color(ColorRole.PRIMARY),
                "shadow": {
                    "color": (0, 0, 0, 50),
                    "blur": 20,
                    "spread": 0,
                    "offset_x": 0,
                    "offset_y": 4
                }
            }
        })
        
        # Elevated card for light mode (more prominent shadow)
        self.set_component_style("card", "elevated", {
            "background_color": self.get_color(ColorRole.SURFACE),
            "border_color": "transparent",
            "border_width": 0,
            "border_radius": 12,
            "padding": 24,
            "shadow": {
                "color": (0, 0, 0, 50),
                "blur": 20,
                "spread": 0,
                "offset_x": 0,
                "offset_y": 8
            }
        })
        
        # Text styles for light mode
        self.set_component_style("text", "heading", {
            "color": self.get_color(ColorRole.TEXT_PRIMARY),
            "font_family": self.get_font("primary"),
            "font_weight": self.fonts.weight_bold,
            "line_height": self.fonts.line_height_tight,
            "margin_bottom": 16,
            "letter_spacing": -0.025  # Slightly tighter spacing for headings
        })
        
        self.set_component_style("text", "body", {
            "color": self.get_color(ColorRole.TEXT_PRIMARY),
            "font_family": self.get_font("primary"),
            "font_size": self.get_font_size("base"),
            "font_weight": self.fonts.weight_normal,
            "line_height": self.fonts.line_height_normal,
            "margin_bottom": 8
        })
        
        self.set_component_style("text", "caption", {
            "color": self.get_color(ColorRole.TEXT_SECONDARY),
            "font_family": self.get_font("primary"),
            "font_size": self.get_font_size("sm"),
            "font_weight": self.fonts.weight_normal,
            "line_height": self.fonts.line_height_normal
        })
        
        self.set_component_style("text", "code", {
            "color": self.get_color(ColorRole.TEXT_PRIMARY),
            "font_family": self.get_font("monospace"),
            "font_size": self.get_font_size("sm"),
            "background_color": (243, 244, 246, 255),  # Light gray background
            "border_radius": 4,
            "padding": {"x": 4, "y": 2}
        })
        
        # Input styles for light mode
        self.set_component_style("input", "default", {
            "background_color": self.get_color(ColorRole.SURFACE),
            "border_color": self.get_color(ColorRole.BORDER),
            "border_width": self.get_stroke_width("thin"),
            "border_radius": 8,
            "padding": {"x": 12, "y": 8},
            "font_family": self.get_font("primary"),
            "font_size": self.get_font_size("base"),
            "color": self.get_color(ColorRole.TEXT_PRIMARY),
            "placeholder_color": self.get_color(ColorRole.TEXT_DISABLED),
            "focus": {
                "border_color": self.get_color(ColorRole.PRIMARY),
                "background_color": self.get_color(ColorRole.SURFACE),
                "box_shadow": {
                    "color": self.get_color(ColorRole.PRIMARY),
                    "blur": 4,
                    "spread": 0,
                    "offset_x": 0,
                    "offset_y": 0
                }
            },
            "error": {
                "border_color": self.get_color(ColorRole.ERROR)
            }
        })
        
        # Select/dropdown styles for light mode
        self.set_component_style("select", "default", {
            "background_color": self.get_color(ColorRole.SURFACE),
            "border_color": self.get_color(ColorRole.BORDER),
            "border_width": self.get_stroke_width("thin"),
            "border_radius": 8,
            "padding": {"x": 12, "y": 8},
            "font_family": self.get_font("primary"),
            "font_size": self.get_font_size("base"),
            "color": self.get_color(ColorRole.TEXT_PRIMARY)
        })
        
        # Modal styles for light mode
        self.set_component_style("modal", "overlay", {
            "background_color": (0, 0, 0, 50),  # Lighter overlay
            "backdrop_blur": 2
        })
        
        self.set_component_style("modal", "content", {
            "background_color": self.get_color(ColorRole.SURFACE),
            "border_color": self.get_color(ColorRole.BORDER),
            "border_width": self.get_stroke_width("thin"),
            "border_radius": 16,
            "padding": 32,
            "shadow": {
                "color": (0, 0, 0, 100),
                "blur": 50,
                "spread": 0,
                "offset_x": 0,
                "offset_y": 20
            }
        })
        
        # Progress bar styles for light mode
        self.set_component_style("progress", "track", {
            "background_color": self.get_color(ColorRole.BORDER),
            "border_radius": 9999
        })
        
        self.set_component_style("progress", "fill", {
            "background_color": self.get_color(ColorRole.PRIMARY),
            "border_radius": 9999,
            "gradient": {
                "start_color": self.get_color(ColorRole.PRIMARY),
                "end_color": self.get_color(ColorRole.ACCENT)
            }
        })
        
        # Badge styles for light mode
        self.set_component_style("badge", "default", {
            "background_color": self.get_color(ColorRole.SECONDARY),
            "color": self.get_color(ColorRole.TEXT_PRIMARY),
            "border_radius": 9999,
            "padding": {"x": 8, "y": 4},
            "font_size": self.get_font_size("sm"),
            "font_weight": self.fonts.weight_medium
        })
        
        self.set_component_style("badge", "primary", {
            "background_color": self.get_color(ColorRole.PRIMARY),
            "color": self.get_color(ColorRole.SURFACE),
            "border_radius": 9999,
            "padding": {"x": 8, "y": 4},
            "font_size": self.get_font_size("sm"),
            "font_weight": self.fonts.weight_medium
        })
        
        # Tooltip styles for light mode
        self.set_component_style("tooltip", "content", {
            "background_color": self.get_color(ColorRole.TEXT_PRIMARY),
            "color": self.get_color(ColorRole.SURFACE),
            "border_radius": 6,
            "padding": {"x": 8, "y": 4},
            "font_size": self.get_font_size("sm"),
            "shadow": {
                "color": (0, 0, 0, 100),
                "blur": 8,
                "spread": 0,
                "offset_x": 0,
                "offset_y": 2
            }
        })
        
        # Navigation styles for light mode
        self.set_component_style("navigation", "item", {
            "color": self.get_color(ColorRole.TEXT_SECONDARY),
            "font_family": self.get_font("primary"),
            "font_size": self.get_font_size("sm"),
            "font_weight": self.fonts.weight_medium,
            "padding": {"x": 12, "y": 8},
            "border_radius": 6,
            "hover": {
                "color": self.get_color(ColorRole.TEXT_PRIMARY),
                "background_color": self.get_color(ColorRole.BACKGROUND)
            },
            "active": {
                "color": self.get_color(ColorRole.PRIMARY),
                "background_color": self.get_color(ColorRole.PRIMARY),
                "opacity": 0.1
            }
        })
        
        # Divider styles for light mode
        self.set_component_style("divider", "default", {
            "background_color": self.get_color(ColorRole.DIVIDER),
            "height": self.get_stroke_width("thin")
        })
    
    def get_clean_aesthetic_settings(self) -> Dict[str, Any]:
        """Return settings optimized for clean, minimal aesthetic"""
        return {
            "border_radius": {
                "small": 4,
                "medium": 8,
                "large": 12,
                "extra_large": 16
            },
            "spacing": {
                "xs": 4,
                "sm": 8,
                "md": 16,
                "lg": 24,
                "xl": 32,
                "xxl": 48
            },
            "shadows": {
                "subtle": {
                    "color": (0, 0, 0, 25),
                    "blur": 10,
                    "offset_x": 0,
                    "offset_y": 2
                },
                "medium": {
                    "color": (0, 0, 0, 50),
                    "blur": 20,
                    "offset_x": 0,
                    "offset_y": 8
                },
                "strong": {
                    "color": (0, 0, 0, 100),
                    "blur": 50,
                    "offset_x": 0,
                    "offset_y": 20
                }
            },
            "transparency": {
                "hover": 0.1,
                "active": 0.15,
                "disabled": 0.5
            }
        }
    
    def get_minimal_design_principles(self) -> Dict[str, Any]:
        """Return principles for minimal design implementation"""
        return {
            "whitespace": {
                "generous": True,
                "consistent": True,
                "purposeful": True
            },
            "hierarchy": {
                "clear_visual_hierarchy": True,
                "consistent_spacing_scale": True,
                "limited_color_palette": True
            },
            "typography": {
                "legible_fonts": True,
                "appropriate_sizing": True,
                "clear_line_heights": True
            },
            "interactions": {
                "subtle_animations": True,
                "clear_feedback": True,
                "accessible_targets": True
            },
            "layout": {
                "grid_based": True,
                "consistent_margins": True,
                "logical_grouping": True
            }
        }
    
    def create_floating_action_button_style(self) -> Dict[str, Any]:
        """Create style for floating action buttons (FAB)"""
        return {
            "background_color": self.get_color(ColorRole.PRIMARY),
            "color": self.get_color(ColorRole.SURFACE),
            "border_radius": 9999,
            "width": 56,
            "height": 56,
            "shadow": {
                "color": (0, 0, 0, 100),
                "blur": 12,
                "spread": 0,
                "offset_x": 0,
                "offset_y": 6
            },
            "hover": {
                "background_color": (49, 130, 206, 255),
                "transform": "scale(1.05)",
                "shadow": {
                    "color": (0, 0, 0, 150),
                    "blur": 16,
                    "spread": 0,
                    "offset_x": 0,
                    "offset_y": 8
                }
            },
            "active": {
                "transform": "scale(0.95)"
            }
        }