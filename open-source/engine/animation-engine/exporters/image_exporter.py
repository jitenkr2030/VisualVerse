"""
VisualVerse Animation Engine - Image Exporter

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

Handles single-frame export functionality supporting PNG, JPEG, SVG formats.
Includes anti-aliasing and resolution scaling options.
"""

import io
import base64
from pathlib import Path
from typing import Union, Optional, Dict, Any, Tuple
from dataclasses import dataclass
from PIL import Image, ImageDraw, ImageFont
import logging

logger = logging.getLogger(__name__)

@dataclass
class ImageConfig:
    """Configuration for image export"""
    width: int = 1920
    height: int = 1080
    dpi: int = 300
    format: str = "PNG"  # PNG, JPEG, SVG
    quality: int = 95  # For JPEG (1-100)
    optimize: bool = True
    background_color: Tuple[int, int, int] = (255, 255, 255)  # RGB
    antialias: bool = True
    
    def validate(self):
        """Validate image configuration"""
        if self.width <= 0 or self.height <= 0:
            raise ValueError("Width and height must be positive")
        if self.format.upper() not in ["PNG", "JPEG", "JPG", "SVG"]:
            raise ValueError(f"Unsupported format: {self.format}")
        if self.format.upper() == "JPEG" and not (1 <= self.quality <= 100):
            raise ValueError("JPEG quality must be between 1 and 100")

class ImageExporter:
    """Exports animation frames to various image formats"""
    
    def __init__(self):
        """Initialize image exporter"""
        self.supported_formats = ["PNG", "JPEG", "JPG", "SVG"]
    
    def export_frame(
        self,
        image_data: Union[Image.Image, bytes],
        output_path: Path,
        config: Optional[ImageConfig] = None,
        overwrite: bool = False
    ) -> Dict[str, Any]:
        """
        Export a single frame to image file
        
        Args:
            image_data: PIL Image object or image bytes
            output_path: Path for output image file
            config: Image configuration options
            overwrite: Whether to overwrite existing file
            
        Returns:
            Dictionary with export results
        """
        if config is None:
            config = ImageConfig()
        
        config.validate()
        
        # Create output directory if it doesn't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Check for overwrite
        if output_path.exists() and not overwrite:
            raise FileExistsError(f"Output file already exists: {output_path}")
        
        try:
            # Handle PIL Image object
            if isinstance(image_data, Image.Image):
                pil_image = self._process_pil_image(image_data, config)
            else:
                # Handle image bytes
                pil_image = Image.open(io.BytesIO(image_data))
                pil_image = self._process_pil_image(pil_image, config)
            
            # Save image
            save_kwargs = self._get_save_kwargs(config)
            pil_image.save(output_path, **save_kwargs)
            
            logger.info(f"Successfully exported image to {output_path}")
            
            return {
                "success": True,
                "output_path": str(output_path),
                "format": config.format.upper(),
                "width": config.width,
                "height": config.height,
                "dpi": config.dpi,
                "file_size_bytes": output_path.stat().st_size,
                "original_size": pil_image.size
            }
            
        except Exception as e:
            error_msg = f"Image export failed: {e}"
            logger.error(error_msg)
            
            return {
                "success": False,
                "error": error_msg,
                "output_path": str(output_path)
            }
    
    def _process_pil_image(self, image: Image.Image, config: ImageConfig) -> Image.Image:
        """Process PIL image according to configuration"""
        # Convert to RGB if necessary
        if image.mode not in ["RGB", "RGBA"]:
            image = image.convert("RGB")
        
        # Resize if needed
        if image.size != (config.width, config.height):
            resampling = Image.LANCZOS if config.antialias else Image.NEAREST
            image = image.resize((config.width, config.height), resampling)
        
        # Create background if needed
        if config.background_color and config.background_color != (255, 255, 255):
            background = Image.new("RGB", (config.width, config.height), config.background_color)
            if image.mode == "RGBA":
                background.paste(image, (0, 0), image)
            else:
                background.paste(image, (0, 0))
            image = background
        
        return image
    
    def _get_save_kwargs(self, config: ImageConfig) -> Dict[str, Any]:
        """Get save parameters based on format"""
        save_kwargs = {"format": config.format.upper()}
        
        if config.format.upper() == "JPEG":
            save_kwargs.update({
                "quality": config.quality,
                "optimize": config.optimize
            })
        elif config.format.upper() == "PNG":
            save_kwargs.update({
                "optimize": config.optimize,
                "dpi": (config.dpi, config.dpi)
            })
        
        return save_kwargs
    
    def create_thumbnail(
        self,
        image_data: Union[Image.Image, bytes],
        output_path: Path,
        size: Tuple[int, int] = (200, 200),
        format: str = "PNG"
    ) -> Dict[str, Any]:
        """
        Create a thumbnail from an image
        
        Args:
            image_data: Source image data
            output_path: Path for thumbnail output
            size: Thumbnail dimensions (width, height)
            format: Output format
            
        Returns:
            Dictionary with thumbnail creation results
        """
        try:
            # Open source image
            if isinstance(image_data, Image.Image):
                pil_image = image_data
            else:
                pil_image = Image.open(io.BytesIO(image_data))
            
            # Create thumbnail
            pil_image.thumbnail(size, Image.LANCZOS)
            
            # Save thumbnail
            save_kwargs = {"format": format.upper()}
            if format.upper() == "JPEG":
                save_kwargs["quality"] = 85
            
            pil_image.save(output_path, **save_kwargs)
            
            return {
                "success": True,
                "output_path": str(output_path),
                "thumbnail_size": pil_image.size,
                "format": format.upper()
            }
            
        except Exception as e:
            error_msg = f"Thumbnail creation failed: {e}"
            logger.error(error_msg)
            
            return {
                "success": False,
                "error": error_msg
            }
    
    def get_image_info(self, image_path: Path) -> Dict[str, Any]:
        """
        Get information about an image file
        
        Args:
            image_path: Path to image file
            
        Returns:
            Dictionary with image metadata
        """
        if not image_path.exists():
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        try:
            with Image.open(image_path) as img:
                return {
                    "file_path": str(image_path),
                    "format": img.format,
                    "mode": img.mode,
                    "size": img.size,
                    "width": img.width,
                    "height": img.height,
                    "file_size_bytes": image_path.stat().st_size,
                    "has_transparency": img.mode in ("RGBA", "LA") or "transparency" in img.info
                }
        except Exception as e:
            raise RuntimeError(f"Failed to get image info: {e}")
    
    def convert_format(
        self,
        input_path: Path,
        output_path: Path,
        target_format: str,
        config: Optional[ImageConfig] = None
    ) -> Dict[str, Any]:
        """
        Convert image from one format to another
        
        Args:
            input_path: Source image file
            output_path: Output image file
            target_format: Target format (PNG, JPEG, etc.)
            config: Image configuration for output
            
        Returns:
            Dictionary with conversion results
        """
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")
        
        if config is None:
            config = ImageConfig(format=target_format)
        else:
            config.format = target_format
        
        try:
            with Image.open(input_path) as img:
                return self.export_frame(img, output_path, config, overwrite=True)
                
        except Exception as e:
            error_msg = f"Image conversion failed: {e}"
            logger.error(error_msg)
            
            return {
                "success": False,
                "error": error_msg,
                "input_path": str(input_path),
                "output_path": str(output_path)
            }
    
    def encode_image_to_base64(self, image_path: Path, format: str = "PNG") -> str:
        """
        Encode image as base64 string
        
        Args:
            image_path: Path to image file
            format: Image format for encoding
            
        Returns:
            Base64 encoded image string
        """
        if not image_path.exists():
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        try:
            with open(image_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode('utf-8')
        except Exception as e:
            raise RuntimeError(f"Failed to encode image: {e}")
    
    def create_placeholder_image(
        self,
        output_path: Path,
        text: str = "VisualVerse",
        config: Optional[ImageConfig] = None
    ) -> Dict[str, Any]:
        """
        Create a placeholder image with text
        
        Args:
            output_path: Path for placeholder image
            text: Text to display on placeholder
            config: Image configuration
            
        Returns:
            Dictionary with creation results
        """
        if config is None:
            config = ImageConfig()
        
        config.validate()
        
        try:
            # Create image with background
            image = Image.new("RGB", (config.width, config.height), config.background_color)
            draw = ImageDraw.Draw(image)
            
            # Try to use a nice font, fall back to default
            try:
                font_size = min(config.width, config.height) // 10
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
            except (OSError, IOError):
                font = ImageFont.load_default()
            
            # Calculate text position (center)
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            
            x = (config.width - text_width) // 2
            y = (config.height - text_height) // 2
            
            # Draw text
            draw.text((x, y), text, fill=(0, 0, 0), font=font)
            
            # Save image
            return self.export_frame(image, output_path, config, overwrite=True)
            
        except Exception as e:
            error_msg = f"Placeholder creation failed: {e}"
            logger.error(error_msg)
            
            return {
                "success": False,
                "error": error_msg
            }