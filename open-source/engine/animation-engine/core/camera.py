# Copyright 2024 VisualVerse Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Camera controller for VisualVerse animations.
Manages camera movements, positioning, and transitions.
"""

import logging
from typing import Dict, Any, Optional, Tuple, List
from dataclasses import dataclass
from enum import Enum

import manim
from manim.camera.camera import Camera
from manim.mobject.mobject import Mobject

logger = logging.getLogger(__name__)

class CameraMovementType(Enum):
    """Types of camera movements"""
    PAN = "pan"
    ZOOM = "zoom"
    ROTATE = "rotate"
    FOLLOW = "follow"
    CUSTOM = "custom"

@dataclass
class CameraConfig:
    """Configuration for camera settings"""
    position: Tuple[float, float, float] = (0, 0, 10)
    rotation: Tuple[float, float, float] = (0, 0, 0)
    zoom: float = 1.0
    focal_distance: float = 10.0
    background_color: str = "#000000"
    movement_smoothness: float = 0.8

class CameraController:
    """
    Advanced camera controller for VisualVerse animations.
    
    Provides smooth camera movements, automatic following, and
    scene-aware camera positioning.
    """
    
    def __init__(self, scene: Optional[manim.Scene] = None):
        self.scene = scene
        self.camera_config = CameraConfig()
        self.movement_history = []
        self.target_mobjects = []
        self.active_animations = []
        
        # Setup default camera
        self._setup_default_camera()
    
    def _setup_default_camera(self):
        """Setup default camera configuration"""
        logger.info("Setting up default camera configuration")
        
    def set_camera_position(self, position: Tuple[float, float, float], duration: float = 2.0):
        """Set camera position with smooth animation"""
        if self.scene:
            animation = manim.ApplyMethod(
                self.scene.camera.move_to,
                position,
                run_time=duration
            )
            self.scene.play(animation)
            self._record_movement("position", position, duration)
    
    def set_camera_rotation(self, rotation: Tuple[float, float, float], duration: float = 2.0):
        """Set camera rotation with smooth animation"""
        if self.scene:
            # Note: This is a simplified implementation
            # In practice, rotation might require more complex handling
            logger.info(f"Setting camera rotation to: {rotation}")
    
    def set_camera_zoom(self, zoom: float, duration: float = 2.0):
        """Set camera zoom level with smooth animation"""
        if self.scene:
            animation = manim.ApplyMethod(
                self.scene.camera.resize_frame_shape,
                zoom,
                run_time=duration
            )
            self.scene.play(animation)
            self._record_movement("zoom", zoom, duration)
    
    def pan_to_object(self, mobject: Mobject, duration: float = 2.0, padding: float = 0.5):
        """Pan camera to center on a specific object"""
        if self.scene and mobject:
            # Calculate center of the mobject
            center = mobject.get_center()
            
            # Add padding around the object
            bounds = mobject.get_bounding_box()
            width = bounds[1][0] - bounds[0][0]
            height = bounds[1][1] - bounds[0][1]
            
            # Determine zoom level based on object size
            target_zoom = max(0.3, min(3.0, 2.0 / max(width, height)))
            
            # Create combined animation
            position_animation = manim.ApplyMethod(
                self.scene.camera.move_to,
                center,
                run_time=duration
            )
            
            zoom_animation = manim.ApplyMethod(
                self.scene.camera.resize_frame_shape,
                target_zoom,
                run_time=duration
            )
            
            self.scene.play(position_animation, zoom_animation)
            self._record_movement("pan_to_object", center, duration)
    
    def follow_mobject(self, mobject: Mobject, offset: Tuple[float, float, float] = (0, 0, 0), 
                      duration: float = 1.0):
        """Make camera follow a moving object"""
        if self.scene and mobject:
            # This would typically be used in update functions
            # For now, we'll track the object for future movement
            if mobject not in self.target_mobjects:
                self.target_mobjects.append({
                    "mobject": mobject,
                    "offset": offset,
                    "active": True
                })
    
    def stop_following(self, mobject: Mobject):
        """Stop camera from following a specific object"""
        for target in self.target_mobjects:
            if target["mobject"] == mobject:
                target["active"] = False
    
    def create_camera_path(self, points: List[Tuple[float, float, float]], 
                          duration: float = 5.0, style: str = "smooth"):
        """Create a smooth camera path through multiple points"""
        if not self.scene or len(points) < 2:
            return
        
        # Create path animation
        from manim import ParametricCurve
        import numpy as np
        
        # Simple linear interpolation for now
        # In practice, you'd want more sophisticated path interpolation
        total_points = int(duration * 30)  # 30 FPS
        
        for i in range(total_points):
            t = i / total_points
            index = t * (len(points) - 1)
            
            # Linear interpolation between points
            if index < len(points) - 1:
                lower_idx = int(index)
                upper_idx = min(lower_idx + 1, len(points) - 1)
                local_t = index - lower_idx
                
                point1 = points[lower_idx]
                point2 = points[upper_idx]
                
                current_point = (
                    point1[0] + (point2[0] - point1[0]) * local_t,
                    point1[1] + (point2[1] - point1[1]) * local_t,
                    point1[2] + (point2[2] - point1[2]) * local_t
                )
                
                self.scene.camera.move_to(current_point)
            
            self.scene.wait(1/30)
    
    def zoom_to_fit(self, mobjects: List[Mobject], padding: float = 0.5, duration: float = 2.0):
        """Zoom camera to fit multiple objects in frame"""
        if not self.scene or not mobjects:
            return
        
        # Calculate combined bounds
        all_bounds = []
        for mobject in mobjects:
            bounds = mobject.get_bounding_box()
            all_bounds.extend(bounds)
        
        # Find min and max coordinates
        min_x = min(bound[0] for bound in all_bounds)
        max_x = max(bound[0] for bound in all_bounds)
        min_y = min(bound[1] for bound in all_bounds)
        max_y = max(bound[1] for bound in all_bounds)
        
        # Add padding
        min_x -= padding
        max_x += padding
        min_y -= padding
        max_y += padding
        
        # Calculate center and zoom
        center = ((min_x + max_x) / 2, (min_y + max_y) / 2, 0)
        width = max_x - min_x
        height = max_y - min_y
        
        # Determine zoom level
        target_zoom = max(0.2, min(4.0, 8.0 / max(width, height)))
        
        # Apply camera settings
        position_animation = manim.ApplyMethod(
            self.scene.camera.move_to,
            center,
            run_time=duration
        )
        
        zoom_animation = manim.ApplyMethod(
            self.scene.camera.resize_frame_shape,
            target_zoom,
            run_time=duration
        )
        
        self.scene.play(position_animation, zoom_animation)
        self._record_movement("zoom_to_fit", center, duration)
    
    def create_intro_camera_movement(self, start_zoom: float = 0.1, end_zoom: float = 1.0, 
                                   duration: float = 3.0):
        """Create a dramatic intro camera movement"""
        if not self.scene:
            return
        
        # Start with very wide shot
        intro_animation = manim.ApplyMethod(
            self.scene.camera.resize_frame_shape,
            start_zoom,
            run_time=0.1
        )
        
        # Zoom in to normal view
        zoom_in = manim.ApplyMethod(
            self.scene.camera.resize_frame_shape,
            end_zoom,
            run_time=duration
        )
        
        self.scene.play(intro_animation)
        self.scene.play(zoom_in)
        self._record_movement("intro", end_zoom, duration)
    
    def create_outro_camera_movement(self, end_position: Tuple[float, float, float] = (0, 0, 15),
                                   duration: float = 2.0):
        """Create a dramatic outro camera movement"""
        if not self.scene:
            return
        
        outro_animation = manim.ApplyMethod(
            self.scene.camera.move_to,
            end_position,
            run_time=duration
        )
        
        self.scene.play(outro_animation)
        self._record_movement("outro", end_position, duration)
    
    def get_camera_status(self) -> Dict[str, Any]:
        """Get current camera status and configuration"""
        return {
            "position": self.camera_config.position,
            "rotation": self.camera_config.rotation,
            "zoom": self.camera_config.zoom,
            "background_color": self.camera_config.background_color,
            "active_follows": len([t for t in self.target_mobjects if t["active"]]),
            "movement_history_count": len(self.movement_history)
        }
    
    def _record_movement(self, movement_type: str, target: Any, duration: float):
        """Record a camera movement for analytics"""
        self.movement_history.append({
            "type": movement_type,
            "target": target,
            "duration": duration,
            "timestamp": manim.utils.logger.utils.get_timestamp()
        })
        
        # Keep only last 100 movements
        if len(self.movement_history) > 100:
            self.movement_history = self.movement_history[-100:]
    
    def update_followers(self):
        """Update camera to follow tracked objects"""
        if not self.scene:
            return
        
        for target in self.target_mobjects:
            if target["active"] and target["mobject"]:
                mobject = target["mobject"]
                offset = target["offset"]
                
                # Calculate target position
                center = mobject.get_center()
                target_position = (
                    center[0] + offset[0],
                    center[1] + offset[1],
                    center[2] + offset[2]
                )
                
                # Smoothly move camera
                current_pos = self.scene.camera.position
                smooth_pos = (
                    current_pos[0] + (target_position[0] - current_pos[0]) * 0.1,
                    current_pos[1] + (target_position[1] - current_pos[1]) * 0.1,
                    current_pos[2] + (target_position[2] - current_pos[2]) * 0.1
                )
                
                self.scene.camera.move_to(smooth_pos)
    
    def reset_camera(self, duration: float = 1.0):
        """Reset camera to default position"""
        self.set_camera_position((0, 0, 10), duration)
        self.set_camera_zoom(1.0, duration)
    
    def save_camera_settings(self, filename: str):
        """Save current camera settings"""
        import json
        from pathlib import Path
        
        settings = {
            "config": {
                "position": self.camera_config.position,
                "rotation": self.camera_config.rotation,
                "zoom": self.camera_config.zoom,
                "background_color": self.camera_config.background_color
            },
            "history": self.movement_history[-10:]  # Last 10 movements
        }
        
        Path(filename).parent.mkdir(parents=True, exist_ok=True)
        with open(filename, 'w') as f:
            json.dump(settings, f, indent=2)
        
        logger.info(f"Camera settings saved to: {filename}")

# Convenience functions for common camera operations

def create_static_shot(position: Tuple[float, float, float] = (0, 0, 10), 
                      zoom: float = 1.0) -> Dict[str, Any]:
    """Create a static camera shot configuration"""
    return {
        "type": "static",
        "position": position,
        "zoom": zoom,
        "duration": 0
    }

def create_panning_shot(start_position: Tuple[float, float, float], 
                       end_position: Tuple[float, float, float],
                       duration: float = 3.0) -> Dict[str, Any]:
    """Create a panning camera shot configuration"""
    return {
        "type": "pan",
        "start_position": start_position,
        "end_position": end_position,
        "duration": duration
    }

def create_zooming_shot(start_zoom: float, end_zoom: float, 
                       duration: float = 2.0) -> Dict[str, Any]:
    """Create a zooming camera shot configuration"""
    return {
        "type": "zoom",
        "start_zoom": start_zoom,
        "end_zoom": end_zoom,
        "duration": duration
    }
