"""
VisualVerse Animation Engine - Dark Mode Theme

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

Specialized theme configuration optimized for dark environments
with appropriate contrast and accessibility considerations.
"""

from typing import Dict, Any
from .base_theme import BaseTheme, ColorPalette, ColorRole, FontConfiguration, StrokeConfiguration, AnimationConfiguration

class DarkModeTheme(BaseTheme):
    """Dark mode theme configuration"""
    
    def __init__(self):
        # Initialize with dark color palette
        colors = ColorPalette(
            # Dark background colors
            background=(17, 24, 39, 255),        # Dark blue-gray
            surface=(31, 41, 55, 255),           # Medium dark gray
            primary=(59, 130, 246, 255),         # Bright blue (maintained for consistency)
            secondary=(107, 114, 128, 255),      # Medium gray
            accent=(16, 185, 129, 255),          # Green
            
            # Status colors (adjusted for dark theme)
            error=(248, 113, 113, 255),          # Lighter red
            warning=(251, 191, 36, 255),         # Lighter orange
            success=(74, 222, 128, 255),         # Lighter green
            info=(96, 165, 250, 255),            # Lighter blue
            
            # Text colors (high contrast for dark background)
            text_primary=(248, 250, 252, 255),   # Very light gray
            text_secondary=(203, 213, 225, 255), # Light gray
            text_disabled=(107, 114, 128, 255),  # Medium gray
            
            # Structural colors
            border=(75, 85, 99, 255),            # Dark border
            divider=(55, 65, 81, 255),           # Dark divider
            shadow=(0, 0, 0, 128),               # Darker shadow
            highlight=(59, 130, 246, 64)         # Semi-transparent blue
        )
        
        # Dark mode font configuration (slightly larger for readability)
        fonts = FontConfiguration(
            primary="Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
            secondary="Georgia, 'Times New Roman', serif",
            monospace="'Fira Code', 'Monaco', 'Cascadia Code', 'Roboto Mono', monospace",
            display="'Inter', 'Poppins', sans-serif",
            math="'STIX Two Math', 'Times New Roman', serif",
            
            # Slightly larger font sizes for dark theme
            size_xs=12,
            size_sm=14,
            size_base=16,
            size_lg=18,
            size_xl=20,
            size_2xl=24,
            size_3xl=30,
            size_4xl=36
        )
        
        # Stroke configuration optimized for dark theme
        strokes = StrokeConfiguration(
            width_thin=1.0,
            width_normal=2.0,
            width_thick=4.0,
            width_extra_thick=8.0
        )
        
        # Animation configuration (slightly faster for dark theme)
        animations = AnimationConfiguration(
            duration_fast=120,
            duration_normal=250,
            duration_slow=400,
            duration_very_slow=800
        )
        
        super().__init__(
            name="Dark Mode",
            description="Dark theme optimized for low-light environments and reduced eye strain",
            version="1.0.0",
            colors=colors,
            fonts=fonts,
            strokes=strokes,
            animations=animations
        )
        
        # Set up dark mode specific component styles
        self._setup_dark_mode_styles()
    
    def _setup_dark_mode_styles(self):
        """Set up component styles specific to dark mode"""
        
        # Button styles for dark mode
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
                "background_color": self.get_color(ColorRole.PRIMARY),
                "opacity": 0.9,
                "transform": "translateY(-1px)"
            },
            "active": {
                "background_color": self.get_color(ColorRole.PRIMARY),
                "opacity": 0.8,
                "transform": "translateY(0px)"
            },
            "disabled": {
                "background_color": self.get_color(ColorRole.SECONDARY),
                "text_color": self.get_color(ColorRole.TEXT_DISABLED),
                "opacity": 0.5
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
                "opacity": 0.15
            },
            "active": {
                "background_color": self.get_color(ColorRole.PRIMARY),
                "opacity": 0.25
            }
        })
        
        # Card styles for dark mode
        self.set_component_style("card", "default", {
            "background_color": self.get_color(ColorRole.SURFACE),
            "border_color": self.get_color(ColorRole.BORDER),
            "border_width": self.get_stroke_width("thin"),
            "border_radius": 12,
            "padding": 24,
            "shadow": {
                "color": (0, 0, 0, 200),
                "blur": 20,
                "spread": 0,
                "offset_x": 0,
                "offset_y": 4
            },
            "hover": {
                "border_color": self.get_color(ColorRole.PRIMARY),
                "shadow": {
                    "color": (0, 0, 0, 250),
                    "blur": 25,
                    "spread": 0,
                    "offset_x": 0,
                    "offset_y": 8
                }
            }
        })
        
        # Text styles for dark mode
        self.set_component_style("text", "heading", {
            "color": self.get_color(ColorRole.TEXT_PRIMARY),
            "font_family": self.get_font("primary"),
            "font_weight": self.fonts.weight_bold,
            "line_height": self.fonts.line_height_tight,
            "margin_bottom": 16,
            "text_shadow": {
                "color": (0, 0, 0, 100),
                "blur": 2,
                "offset_x": 0,
                "offset_y": 1
            }
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
        
        # Input styles for dark mode
        self.set_component_style("input", "default", {
            "background_color": self.get_color(ColorRole.BACKGROUND),
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
            }
        })
        
        # Modal styles for dark mode
        self.set_component_style("modal", "overlay", {
            "background_color": (0, 0, 0, 128),
            "backdrop_blur": 4
        })
        
        self.set_component_style("modal", "content", {
            "background_color": self.get_color(ColorRole.SURFACE),
            "border_color": self.get_color(ColorRole.BORDER),
            "border_width": self.get_stroke_width("thin"),
            "border_radius": 16,
            "padding": 32,
            "shadow": {
                "color": (0, 0, 0, 200),
                "blur": 50,
                "spread": 0,
                "offset_x": 0,
                "offset_y": 20
            }
        })
        
        # Progress bar styles for dark mode
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
        
        # Tooltip styles for dark mode
        self.set_component_style("tooltip", "content", {
            "background_color": self.get_color(ColorRole.TEXT_PRIMARY),
            "color": self.get_color(ColorRole.BACKGROUND),
            "border_radius": 6,
            "padding": {"x": 8, "y": 4},
            "font_size": self.get_font_size("sm"),
            "shadow": {
                "color": (0, 0, 0, 200),
                "blur": 8,
                "spread": 0,
                "offset_x": 0,
                "offset_y": 2
            }
        })
    
    def get_accessibility_contrast_ratio(self, foreground_role: ColorRole, background_role: ColorRole) -> float:
        """
        Calculate contrast ratio for accessibility compliance
        Returns ratio between 1.0 and 21.0 (WCAG AA requires 4.5:1 for normal text, 3:1 for large text)
        """
        fg_color = self.get_color(foreground_role)
        bg_color = self.get_color(background_role)
        
        # Convert to relative luminance
        def relative_luminance(r, g, b):
            def linearize(c):
                c = c / 255.0
                return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
            
            r_lin = linearize(r)
            g_lin = linearize(g)
            b_lin = linearize(b)
            
            return 0.2126 * r_lin + 0.7152 * g_lin + 0.0722 * b_lin
        
        fg_lum = relative_luminance(fg_color[0], fg_color[1], fg_color[2])
        bg_lum = relative_luminance(bg_color[0], bg_color[1], bg_color[2])
        
        # Calculate contrast ratio
        if fg_lum > bg_lum:
            return (fg_lum + 0.05) / (bg_lum + 0.05)
        else:
            return (bg_lum + 0.05) / (fg_lum + 0.05)
    
    def meets_contrast_requirements(self, foreground_role: ColorRole, background_role: ColorRole, level: str = "AA") -> bool:
        """
        Check if color combination meets WCAG contrast requirements
        level: "AA" (4.5:1) or "AAA" (7:1) for normal text, "AAL" (3:1) for large text
        """
        ratio = self.get_accessibility_contrast_ratio(foreground_role, background_role)
        
        if level == "AA":
            return ratio >= 4.5
        elif level == "AAA":
            return ratio >= 7.0
        elif level == "AAL":  # AA Large
            return ratio >= 3.0
        else:
            return False
    
    def optimize_for_accessibility(self) -> Dict[str, Any]:
        """Return accessibility optimization recommendations"""
        recommendations = {
            "text_contrast": {},
            "status_colors": {},
            "suggestions": []
        }
        
        # Check text color contrast
        text_combinations = [
            (ColorRole.TEXT_PRIMARY, ColorRole.BACKGROUND),
            (ColorRole.TEXT_PRIMARY, ColorRole.SURFACE),
            (ColorRole.TEXT_SECONDARY, ColorRole.BACKGROUND),
            (ColorRole.TEXT_SECONDARY, ColorRole.SURFACE),
            (ColorRole.TEXT_DISABLED, ColorRole.BACKGROUND),
            (ColorRole.TEXT_DISABLED, ColorRole.SURFACE)
        ]
        
        for fg_role, bg_role in text_combinations:
            ratio = self.get_accessibility_contrast_ratio(fg_role, bg_role)
            recommendations["text_contrast"][f"{fg_role.value}_on_{bg_role.value}"] = {
                "ratio": round(ratio, 2),
                "meets_aa": self.meets_contrast_requirements(fg_role, bg_role, "AA"),
                "meets_aaa": self.meets_contrast_requirements(fg_role, bg_role, "AAA")
            }
        
        # Check status colors
        status_combinations = [
            (ColorRole.ERROR, ColorRole.BACKGROUND),
            (ColorRole.WARNING, ColorRole.BACKGROUND),
            (ColorRole.SUCCESS, ColorRole.BACKGROUND),
            (ColorRole.INFO, ColorRole.BACKGROUND)
        ]
        
        for fg_role, bg_role in status_combinations:
            ratio = self.get_accessibility_contrast_ratio(fg_role, bg_role)
            recommendations["status_colors"][f"{fg_role.value}_on_{bg_role.value}"] = {
                "ratio": round(ratio, 2),
                "meets_aa": self.meets_contrast_requirements(fg_role, bg_role, "AA")
            }
        
        # Generate suggestions
        for key, data in recommendations["text_contrast"].items():
            if not data["meets_aa"]:
                recommendations["suggestions"].append(
                    f"Text contrast for {key} is {data['ratio']}:1 - consider adjusting colors for better accessibility"
                )
        
        return recommendations