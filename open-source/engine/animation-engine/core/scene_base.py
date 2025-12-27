"""
VisualVerse Animation Engine - Core Scene Base

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

Base scene class for all VisualVerse animations.
Provides common functionality and lifecycle management.
"""

import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from datetime import datetime

import manim
from manim.scene.scene import Scene
from manim.mobject.mobject import Mobject

from .renderer import RenderRequest

logger = logging.getLogger(__name__)

class SceneBase(Scene, ABC):
    """
    Abstract base class for all VisualVerse scenes.
    
    This class provides common functionality for educational animations
    and enforces a consistent lifecycle across all scenes.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scene_metadata = {
            "title": self.__class__.__name__,
            "created_at": datetime.now().isoformat(),
            "version": "1.0",
            "subject": "general",
            "difficulty": "intermediate",
            "estimated_duration": 30.0
        }
        self.render_config = {}
        self.animations_completed = []
        self.objects_created = []
        
        # Setup logging
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    def setup_custom(self, request: RenderRequest):
        """Custom setup called before rendering"""
        self.render_config = {
            "quality": request.quality,
            "fps": request.fps,
            "transparent": request.transparent,
            "background_color": request.background_color,
            "metadata": request.metadata or {}
        }
        
        # Apply metadata from request
        if request.metadata:
            self.scene_metadata.update(request.metadata)
        
        self.logger.info(f"Setting up scene with config: {self.render_config}")
    
    @abstractmethod
    def construct(self):
        """
        Abstract method for scene construction.
        All subclasses must implement this method with their animation logic.
        """
        pass
    
    def setup(self):
        """Override setup to add custom initialization"""
        self.logger.info(f"Setting up scene: {self.scene_metadata['title']}")
        
        # Call parent setup
        super().setup()
        
        # Custom setup logic can be added here
        self._setup_scene_objects()
    
    def _setup_scene_objects(self):
        """Setup common scene objects and utilities"""
        # This can be overridden by subclasses for custom setup
        pass
    
    def teardown(self):
        """Cleanup called after rendering"""
        self.logger.info(f"Tearing down scene: {self.scene_metadata['title']}")
        
        # Log statistics
        stats = self._get_scene_statistics()
        self.logger.info(f"Scene statistics: {stats}")
    
    def _get_scene_statistics(self) -> Dict[str, Any]:
        """Get statistics about the rendered scene"""
        return {
            "animations_count": len(self.animations_completed),
            "objects_created": len(self.objects_created),
            "duration": self.duration if hasattr(self, 'duration') else None,
            "metadata": self.scene_metadata
        }
    
    def add_title(self, text: str, position: tuple = (0, 3, 0), color: str = manim.WHITE):
        """Add a title to the scene"""
        title = manim.Text(text, font_size=48, color=color)
        title.move_to(position)
        self.add(title)
        return title
    
    def add_subtitle(self, text: str, position: tuple = (0, -3, 0), color: str = manim.GRAY):
        """Add a subtitle to the scene"""
        subtitle = manim.Text(text, font_size=24, color=color)
        subtitle.move_to(position)
        self.add(subtitle)
        return subtitle
    
    def add_step_number(self, step: int, position: tuple = (-6, 3, 0)):
        """Add a step number indicator"""
        step_text = manim.Text(f"Step {step}", font_size=20, color=manim.BLUE)
        step_text.move_to(position)
        self.add(step_text)
        return step_text
    
    def create_highlight_box(self, mobject: Mobject, color: str = manim.YELLOW, buff: float = 0.1):
        """Create a highlight box around a mobject"""
        return manim.SurroundingRectangle(mobject, color=color, buff=buff)
    
    def add_formula(self, formula: str, position: tuple = (0, 0, 0), font_size: int = 36):
        """Add a mathematical formula"""
        from manim import MathTex
        math_tex = MathTex(formula, font_size=font_size)
        math_tex.move_to(position)
        self.add(math_tex)
        return math_tex
    
    def create_progress_bar(self, progress: float, width: float = 6, position: tuple = (0, -3.5, 0)):
        """Create a progress bar"""
        # Background bar
        background = manim.Rectangle(width=width, height=0.2, color=manim.GRAY)
        background.move_to(position)
        
        # Progress bar
        progress_width = width * progress
        progress_bar = manim.Rectangle(width=progress_width, height=0.2, color=manim.GREEN)
        progress_bar.move_to(position - manim.RIGHT * (width - progress_width) / 2)
        
        self.add(background, progress_bar)
        return progress_bar
    
    def track_animation(self, animation):
        """Track an animation for statistics"""
        self.animations_completed.append({
            "animation": animation.__class__.__name__,
            "timestamp": datetime.now().isoformat()
        })
        return animation
    
    def track_object(self, mobject: Mobject, object_type: str = "unknown"):
        """Track a created object for statistics"""
        self.objects_created.append({
            "type": object_type,
            "class": mobject.__class__.__name__,
            "timestamp": datetime.now().isoformat()
        })
        return mobject
    
    def wait_with_progress(self, duration: float, show_progress: bool = True):
        """Wait with optional progress indication"""
        if show_progress:
            progress_bar = self.create_progress_bar(0)
            for i in range(int(duration * 30)):  # 30 fps
                progress = i / (duration * 30)
                progress_bar.become(self.create_progress_bar(progress))
                self.wait(1/30)
            # Complete the progress bar
            progress_bar.become(self.create_progress_bar(1))
            self.wait(0.5)
        else:
            self.wait(duration)
    
    def save_scene_data(self, filename: str):
        """Save scene metadata and statistics"""
        import json
        from pathlib import Path
        
        data = {
            "metadata": self.scene_metadata,
            "statistics": self._get_scene_statistics(),
            "render_config": self.render_config
        }
        
        Path(filename).parent.mkdir(parents=True, exist_ok=True)
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        self.logger.info(f"Scene data saved to: {filename}")
    
    def get_scene_info(self) -> Dict[str, Any]:
        """Get comprehensive scene information"""
        return {
            "class_name": self.__class__.__name__,
            "metadata": self.scene_metadata,
            "statistics": self._get_scene_statistics(),
            "config": self.render_config,
            "objects_count": len(self.objects_created),
            "animations_count": len(self.animations_completed)
        }

# Common scene mixins for specific use cases

class MathSceneBase(SceneBase):
    """Base class for mathematical scenes"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scene_metadata["subject"] = "mathematics"
        self.coordinate_system = None
    
    def setup_coordinate_system(self, x_range=(-7, 7, 1), y_range=(-4, 4, 1)):
        """Setup a coordinate system for the scene"""
        self.coordinate_system = manim.Axes(x_range=x_range, y_range=y_range)
        self.add(self.coordinate_system)
        return self.coordinate_system
    
    def add_grid(self, x_range=(-8, 8, 1), y_range=(-5, 5, 1), color=manim.GRAY):
        """Add a grid to the scene"""
        grid = manim.NumberPlane(x_range=x_range, y_range=y_range, background_line_style={"stroke_color": color, "stroke_width": 1})
        self.add(grid)
        return grid

class PhysicsSceneBase(SceneBase):
    """Base class for physics scenes"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scene_metadata["subject"] = "physics"
        self.objects = []
    
    def add_force_arrow(self, start_point, direction, magnitude=1.0, color=manim.RED):
        """Add a force arrow"""
        arrow = manim.Arrow(start_point, start_point + direction * magnitude, color=color)
        self.add(arrow)
        return arrow
    
    def add_vector_field(self, function, region=((-4, 4), (-3, 3)), density=8):
        """Add a vector field visualization"""
        # Implementation for vector fields
        pass

class TextSceneBase(SceneBase):
    """Base class for text-heavy scenes"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scene_metadata["subject"] = "text"
        self.text_objects = []
    
    def add_text_block(self, text: str, position: tuple = (0, 0, 0), font_size: int = 24, color=manim.WHITE):
        """Add a block of text"""
        text_mobject = manim.Text(text, font_size=font_size, color=color)
        text_mobject.move_to(position)
        self.add(text_mobject)
        self.text_objects.append(text_mobject)
        return text_mobject
    
    def create_text_animation(self, text: str, position: tuple = (0, 0, 0), 
                             font_size: int = 24, color=manim.WHITE, animation_time=1.0):
        """Create animated text appearance"""
        text_mobject = manim.Text(text, font_size=font_size, color=color)
        text_mobject.move_to(position)
        text_mobject.scale(0)
        self.add(text_mobject)
        
        return self.track_animation(
            manim.Transform(text_mobject, text_mobject.copy().scale(1))
        )
