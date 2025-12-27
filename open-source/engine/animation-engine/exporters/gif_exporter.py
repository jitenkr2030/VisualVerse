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
GIF Exporter for VisualVerse Animation Engine

Specialized optimization for GIF generation including color palette reduction
and dithering logic for efficient animated GIF creation.
"""

import io
import math
from pathlib import Path
from typing import List, Union, Optional, Dict, Any, Tuple
from dataclasses import dataclass
from PIL import Image, ImageSequence
import numpy as np
import logging

logger = logging.getLogger(__name__)

@dataclass
class GIFConfig:
    """Configuration for GIF export"""
    width: int = 800
    height: int = 600
    fps: int = 10
    loop: int = 0  # 0 = infinite loop
    optimize: bool = True
    palette_size: int = 256  # Max colors in palette (2-256)
    dither: str = "FLOYD_STEINBERG"  # NONE, FLOYD_STEINBERG, BAYER
    disposal: int = 2  # 0=no disposal, 1=do not dispose, 2=restore to background, 3=restore to previous
    
    def validate(self):
        """Validate GIF configuration"""
        if self.width <= 0 or self.height <= 0:
            raise ValueError("Width and height must be positive")
        if not (2 <= self.palette_size <= 256):
            raise ValueError("Palette size must be between 2 and 256")
        if self.fps <= 0:
            raise ValueError("FPS must be positive")
        if self.disposal not in [0, 1, 2, 3]:
            raise ValueError("Disposal method must be 0, 1, 2, or 3")

class GIFExporter:
    """Exports animation frames to optimized GIF format"""
    
    def __init__(self):
        """Initialize GIF exporter"""
        self.dither_methods = {
            "NONE": Image.NEAREST,
            "FLOYD_STEINBERG": Image.FLOYDSTEINBERG,
            "BAYER": Image.BAYER
        }
    
    def export_frames_to_gif(
        self,
        frames: List[Union[Image.Image, bytes]],
        output_path: Path,
        config: Optional[GIFConfig] = None,
        overwrite: bool = False
    ) -> Dict[str, Any]:
        """
        Export frames to animated GIF
        
        Args:
            frames: List of frames (PIL Image or bytes)
            output_path: Path for output GIF file
            config: GIF configuration options
            overwrite: Whether to overwrite existing file
            
        Returns:
            Dictionary with export results
        """
        if config is None:
            config = GIFConfig()
        
        config.validate()
        
        if not frames:
            raise ValueError("No frames provided for GIF export")
        
        # Create output directory if it doesn't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Check for overwrite
        if output_path.exists() and not overwrite:
            raise FileExistsError(f"Output file already exists: {output_path}")
        
        try:
            # Process frames
            processed_frames = self._process_frames(frames, config)
            
            # Create GIF
            self._create_gif(processed_frames, output_path, config)
            
            # Calculate frame duration
            frame_duration = int(1000 / config.fps)  # milliseconds
            
            # Get file info
            file_size = output_path.stat().st_size if output_path.exists() else 0
            
            logger.info(f"Successfully exported GIF to {output_path}")
            
            return {
                "success": True,
                "output_path": str(output_path),
                "frame_count": len(processed_frames),
                "width": config.width,
                "height": config.height,
                "fps": config.fps,
                "duration_seconds": len(processed_frames) / config.fps,
                "frame_duration_ms": frame_duration,
                "loop": config.loop,
                "file_size_bytes": file_size,
                "palette_size": config.palette_size
            }
            
        except Exception as e:
            error_msg = f"GIF export failed: {e}"
            logger.error(error_msg)
            
            return {
                "success": False,
                "error": error_msg,
                "frame_count": len(frames) if frames else 0
            }
    
    def _process_frames(self, frames: List[Union[Image.Image, bytes]], config: GIFConfig) -> List[Image.Image]:
        """Process and optimize frames for GIF"""
        processed_frames = []
        
        for i, frame_data in enumerate(frames):
            try:
                # Convert to PIL Image if needed
                if isinstance(frame_data, bytes):
                    frame = Image.open(io.BytesIO(frame_data))
                else:
                    frame = frame_data.copy()
                
                # Resize if needed
                if frame.size != (config.width, config.height):
                    frame = frame.resize((config.width, config.height), Image.LANCZOS)
                
                # Convert to RGB if necessary (GIF requires RGB or P mode)
                if frame.mode not in ["RGB", "P"]:
                    if frame.mode == "RGBA":
                        # Create a background for transparent areas
                        background = Image.new("RGB", frame.size, (255, 255, 255))
                        background.paste(frame, mask=frame.split()[3] if frame.mode == "RGBA" else None)
                        frame = background
                    else:
                        frame = frame.convert("RGB")
                
                # Reduce colors and apply dithering
                if config.palette_size < 256:
                    frame = self._reduce_colors(frame, config)
                
                processed_frames.append(frame)
                
            except Exception as e:
                logger.warning(f"Failed to process frame {i}: {e}")
                continue
        
        if not processed_frames:
            raise ValueError("No frames could be processed successfully")
        
        return processed_frames
    
    def _reduce_colors(self, frame: Image.Image, config: GIFConfig) -> Image.Image:
        """Reduce color palette and apply dithering"""
        # Convert to palette mode with reduced colors
        frame = frame.convert("P", palette=Image.ADAPTIVE, colors=config.palette_size)
        
        # Apply dithering if specified
        if config.dither != "NONE" and config.dither in self.dither_methods:
            # Note: PIL doesn't directly support dithering in quantize,
            # so we use a different approach
            # Create a new image with reduced colors using quantize
            frame = frame.quantize(colors=config.palette_size, method=Image.MEDIANCUT)
        
        return frame
    
    def _create_gif(self, frames: List[Image.Image], output_path: Path, config: GIFConfig):
        """Create the actual GIF file"""
        frame_duration = int(1000 / config.fps)  # milliseconds
        
        # Prepare frames for GIF
        gif_frames = []
        for frame in frames:
            # Ensure frame is in a GIF-compatible mode
            if frame.mode == "P":
                # Frame is already in palette mode
                gif_frame = frame.copy()
            else:
                # Convert to palette mode
                gif_frame = frame.convert("P", palette=Image.ADAPTIVE, colors=config.palette_size)
            
            gif_frames.append(gif_frame)
        
        # Create the GIF
        gif_frames[0].save(
            output_path,
            save_all=True,
            append_images=gif_frames[1:],
            duration=frame_duration,
            loop=config.loop,
            optimize=config.optimize,
            disposal=config.disposal
        )
    
    def optimize_gif(
        self,
        input_path: Path,
        output_path: Path,
        target_size_mb: Optional[float] = None,
        config: Optional[GIFConfig] = None
    ) -> Dict[str, Any]:
        """
        Optimize an existing GIF file
        
        Args:
            input_path: Source GIF file
            output_path: Output optimized GIF file
            target_size_mb: Target file size in MB (optional)
            config: Optimization configuration
            
        Returns:
            Dictionary with optimization results
        """
        if not input_path.exists():
            raise FileNotFoundError(f"Input GIF not found: {input_path}")
        
        if config is None:
            config = GIFConfig()
        
        config.validate()
        
        try:
            # Open and process the GIF
            with Image.open(input_path) as img:
                frames = []
                
                # Extract all frames
                for frame in ImageSequence.Iterator(img):
                    frame_copy = frame.copy()
                    frames.append(frame_copy)
                
                if not frames:
                    raise ValueError("No frames found in GIF")
                
                # Get original info
                original_size = input_path.stat().st_size
                
                # Create optimized version
                result = self.export_frames_to_gif(frames, output_path, config, overwrite=True)
                
                if result["success"]:
                    # Calculate compression ratio
                    compressed_size = output_path.stat().st_size
                    compression_ratio = (1 - compressed_size / original_size) * 100
                    
                    result.update({
                        "original_size_bytes": original_size,
                        "compressed_size_bytes": compressed_size,
                        "compression_ratio_percent": compression_ratio,
                        "target_size_mb": target_size_mb,
                        "size_under_target": target_size_mb is None or (compressed_size / (1024 * 1024)) <= target_size_mb
                    })
                
                return result
                
        except Exception as e:
            error_msg = f"GIF optimization failed: {e}"
            logger.error(error_msg)
            
            return {
                "success": False,
                "error": error_msg,
                "input_path": str(input_path),
                "output_path": str(output_path)
            }
    
    def get_gif_info(self, gif_path: Path) -> Dict[str, Any]:
        """
        Get information about a GIF file
        
        Args:
            gif_path: Path to GIF file
            
        Returns:
            Dictionary with GIF metadata
        """
        if not gif_path.exists():
            raise FileNotFoundError(f"GIF file not found: {gif_path}")
        
        try:
            with Image.open(gif_path) as img:
                frame_count = 0
                duration_total = 0
                frame_durations = []
                
                # Count frames and calculate total duration
                for frame in ImageSequence.Iterator(img):
                    frame_count += 1
                    duration = frame.info.get('duration', 100)  # Default 100ms
                    duration_total += duration
                    frame_durations.append(duration)
                
                return {
                    "file_path": str(gif_path),
                    "format": img.format,
                    "mode": img.mode,
                    "size": img.size,
                    "width": img.width,
                    "height": img.height,
                    "frame_count": frame_count,
                    "total_duration_ms": duration_total,
                    "total_duration_seconds": duration_total / 1000,
                    "fps_estimated": frame_count / (duration_total / 1000) if duration_total > 0 else 0,
                    "file_size_bytes": gif_path.stat().st_size,
                    "frame_durations": frame_durations,
                    "has_transparency": img.mode == "RGBA" or "transparency" in img.info
                }
                
        except Exception as e:
            raise RuntimeError(f"Failed to get GIF info: {e}")
    
    def extract_frames_from_gif(
        self,
        gif_path: Path,
        output_dir: Path,
        frame_format: str = "PNG"
    ) -> Dict[str, Any]:
        """
        Extract individual frames from a GIF
        
        Args:
            gif_path: Source GIF file
            output_dir: Directory to save extracted frames
            frame_format: Format for extracted frames
            
        Returns:
            Dictionary with extraction results
        """
        if not gif_path.exists():
            raise FileNotFoundError(f"GIF file not found: {gif_path}")
        
        # Create output directory
        output_dir.mkdir(parents=True, exist_ok=True)
        
        extracted_frames = []
        
        try:
            with Image.open(gif_path) as img:
                frame_count = 0
                
                for frame in ImageSequence.Iterator(img):
                    frame_count += 1
                    frame_filename = output_dir / f"frame_{frame_count:04d}.{frame_format.lower()}"
                    
                    # Convert frame if needed
                    if frame_format.upper() == "PNG" and frame.mode == "P":
                        frame = frame.convert("RGBA")
                    
                    # Save frame
                    frame.save(frame_filename, format=frame_format.upper())
                    extracted_frames.append(str(frame_filename))
                
                logger.info(f"Extracted {frame_count} frames to {output_dir}")
                
                return {
                    "success": True,
                    "frame_count": frame_count,
                    "extracted_frames": extracted_frames,
                    "output_directory": str(output_dir),
                    "frame_format": frame_format.upper()
                }
                
        except Exception as e:
            error_msg = f"Frame extraction failed: {e}"
            logger.error(error_msg)
            
            return {
                "success": False,
                "error": error_msg,
                "extracted_frames": extracted_frames
            }
    
    def create_gif_from_images(
        self,
        image_paths: List[Path],
        output_path: Path,
        config: Optional[GIFConfig] = None,
        frame_duration_ms: int = 100
    ) -> Dict[str, Any]:
        """
        Create GIF from a list of image files
        
        Args:
            image_paths: List of image file paths
            output_path: Output GIF path
            config: GIF configuration
            frame_duration_ms: Duration per frame in milliseconds
            
        Returns:
            Dictionary with creation results
        """
        frames = []
        
        for img_path in image_paths:
            if not img_path.exists():
                logger.warning(f"Image file not found: {img_path}")
                continue
            
            try:
                with Image.open(img_path) as img:
                    frames.append(img.copy())
            except Exception as e:
                logger.warning(f"Failed to load image {img_path}: {e}")
                continue
        
        if not frames:
            raise ValueError("No valid images found")
        
        # Update config with frame duration
        if config is None:
            config = GIFConfig()
        
        # Convert frame duration to fps
        if frame_duration_ms > 0:
            config.fps = int(1000 / frame_duration_ms)
        
        return self.export_frames_to_gif(frames, output_path, config, overwrite=True)