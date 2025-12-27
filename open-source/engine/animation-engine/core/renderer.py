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
Core rendering engine for VisualVerse animation system.
Provides high-level interface for rendering educational animations.
"""

import asyncio
import json
import logging
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List, Union
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor

import manim
from manim import config as manim_config
from manim.scene.scene import Scene
from manim.utils.file_ops import write_to_movie

from .scene_base import SceneBase
from .camera import CameraController
from .timeline import TimelineManager

logger = logging.getLogger(__name__)

@dataclass
class RenderRequest:
    """Request object for rendering animations"""
    scene_class: type
    output_path: Optional[str] = None
    quality: str = "l"
    fps: int = 30
    duration: Optional[float] = None
    resolution: Optional[tuple] = None
    transparent: bool = False
    background_color: str = "#FFFFFF"
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

@dataclass
class RenderResult:
    """Result object for rendering operations"""
    success: bool
    output_path: Optional[str] = None
    error_message: Optional[str] = None
    render_time: Optional[float] = None
    file_size: Optional[int] = None
    metadata: Optional[Dict[str, Any]] = None

class AnimationRenderer:
    """High-level animation rendering engine"""
    
    def __init__(self, max_concurrent_renders: int = 4):
        self.max_concurrent_renders = max_concurrent_renders
        self.render_executor = ThreadPoolExecutor(max_workers=max_concurrent_renders)
        self.camera_controller = CameraController()
        self.timeline_manager = TimelineManager()
        self.render_queue = []
        self.active_renders = []
        
        # Configure Manim defaults
        self._configure_manim()
    
    def _configure_manim(self):
        """Configure Manim with VisualVerse defaults"""
        manim_config.quality = "l"  # Medium quality by default
        manim_config.output_file = "visualverse_output.mp4"
        manim_config.transparent = False
        manim_config.background_color = "#FFFFFF"
        logger.info("Manim configured with VisualVerse defaults")
    
    async def render_animation(self, request: RenderRequest) -> RenderResult:
        """Render an animation asynchronously"""
        start_time = datetime.now()
        
        try:
            logger.info(f"Starting render for scene: {request.scene_class.__name__}")
            
            # Validate request
            validation_result = self._validate_render_request(request)
            if not validation_result.success:
                return validation_result
            
            # Configure rendering parameters
            self._apply_render_config(request)
            
            # Create scene instance and render
            scene_instance = request.scene_class()
            
            # Run render in thread pool
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                self.render_executor,
                self._render_scene_sync,
                scene_instance,
                request
            )
            
            # Calculate render time
            render_time = (datetime.now() - start_time).total_seconds()
            result.render_time = render_time
            
            # Get file size if successful
            if result.success and result.output_path:
                result.file_size = self._get_file_size(result.output_path)
            
            logger.info(f"Render completed: {result.success}, Time: {render_time:.2f}s")
            return result
            
        except Exception as e:
            error_message = f"Render failed: {str(e)}"
            logger.error(error_message, exc_info=True)
            return RenderResult(
                success=False,
                error_message=error_message,
                render_time=(datetime.now() - start_time).total_seconds()
            )
    
    def _validate_render_request(self, request: RenderRequest) -> RenderResult:
        """Validate render request parameters"""
        # Check if scene class is valid
        if not issubclass(request.scene_class, SceneBase):
            return RenderResult(
                success=False,
                error_message=f"Scene class must inherit from SceneBase, got {request.scene_class}"
            )
        
        # Validate quality settings
        valid_qualities = ["k", "h", "m", "l", "p"]
        if request.quality not in valid_qualities:
            return RenderResult(
                success=False,
                error_message=f"Invalid quality setting: {request.quality}. Must be one of {valid_qualities}"
            )
        
        # Validate FPS
        if request.fps < 1 or request.fps > 120:
            return RenderResult(
                success=False,
                error_message=f"Invalid FPS: {request.fps}. Must be between 1 and 120"
            )
        
        return RenderResult(success=True)
    
    def _apply_render_config(self, request: RenderRequest):
        """Apply rendering configuration to Manim"""
        manim_config.quality = request.quality
        manim_config.fps = request.fps
        manim_config.transparent = request.transparent
        manim_config.background_color = request.background_color
        
        if request.resolution:
            manim_config.pixel_width, manim_config.pixel_height = request.resolution
        
        if request.output_path:
            manim_config.output_file = request.output_path
    
    def _render_scene_sync(self, scene_instance: SceneBase, request: RenderRequest) -> RenderResult:
        """Synchronous scene rendering"""
        try:
            # Set up scene with request parameters
            if hasattr(scene_instance, 'setup_custom'):
                scene_instance.setup_custom(request)
            
            # Create temporary file if no output path specified
            if not request.output_path:
                with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as tmp_file:
                    output_path = tmp_file.name
            else:
                output_path = request.output_path
            
            # Ensure output directory exists
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            
            # Configure Manim for this render
            manim_config.output_file = output_path
            
            # Render the scene
            scene_instance.render()
            
            # Verify output file was created
            if not Path(output_path).exists():
                return RenderResult(
                    success=False,
                    error_message="Output file was not created"
                )
            
            return RenderResult(
                success=True,
                output_path=output_path,
                metadata=request.metadata.copy()
            )
            
        except Exception as e:
            return RenderResult(
                success=False,
                error_message=f"Scene rendering failed: {str(e)}"
            )
    
    def _get_file_size(self, file_path: str) -> int:
        """Get file size in bytes"""
        try:
            return Path(file_path).stat().st_size
        except (OSError, FileNotFoundError):
            return 0
    
    def get_render_status(self, render_id: str) -> Dict[str, Any]:
        """Get status of a render job"""
        # Implementation for tracking render status
        return {
            "render_id": render_id,
            "status": "unknown",
            "progress": 0
        }
    
    def cancel_render(self, render_id: str) -> bool:
        """Cancel a running render job"""
        # Implementation for canceling renders
        return False
    
    def get_queue_status(self) -> Dict[str, Any]:
        """Get overall render queue status"""
        return {
            "queued_jobs": len(self.render_queue),
            "active_renders": len(self.active_renders),
            "max_concurrent": self.max_concurrent_renders
        }
    
    def cleanup(self):
        """Cleanup resources"""
        self.render_executor.shutdown(wait=True)
        logger.info("Animation renderer cleaned up")

class AnimationEngine:
    """Main animation engine interface"""
    
    def __init__(self, max_concurrent_renders: int = 4):
        self.renderer = AnimationRenderer(max_concurrent_renders)
        self.version = "1.0.0"
        self.logger = logging.getLogger(__name__)
    
    async def render_scene(self, scene_class: type, output_path: str = None, **kwargs) -> RenderResult:
        """Render a scene to an animation file"""
        request = RenderRequest(
            scene_class=scene_class,
            output_path=output_path,
            **kwargs
        )
        return await self.renderer.render_animation(request)
    
    async def batch_render(self, requests: List[RenderRequest]) -> List[RenderResult]:
        """Render multiple scenes in batch"""
        tasks = [self.renderer.render_animation(req) for req in requests]
        return await asyncio.gather(*tasks, return_exceptions=True)
    
    def get_engine_status(self) -> Dict[str, Any]:
        """Get overall engine status"""
        return {
            "version": self.version,
            "renderer_status": self.renderer.get_queue_status(),
            "active": True
        }
    
    def shutdown(self):
        """Shutdown the animation engine"""
        self.renderer.cleanup()
        self.logger.info("Animation engine shutdown complete")

# Global engine instance
animation_engine = AnimationEngine()
