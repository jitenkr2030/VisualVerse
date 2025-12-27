"""
VisualVerse Animation Engine - FFmpeg Exporter

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

Handles the conversion of frame buffers to video formats using FFmpeg.
Supports MP4, WebM, and other common video formats with configurable quality settings.
"""

import subprocess
import os
import tempfile
from pathlib import Path
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class FFmpegConfig:
    """Configuration for FFmpeg video export"""
    framerate: int = 30
    bitrate: str = "2M"
    codec: str = "libx264"
    pixel_format: str = "yuv420p"
    audio_codec: Optional[str] = "aac"
    audio_bitrate: str = "128k"
    quality_preset: str = "medium"  # ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow
    
    def to_ffmpeg_args(self) -> List[str]:
        """Convert config to FFmpeg command line arguments"""
        args = [
            "-r", str(self.framerate),
            "-b:v", self.bitrate,
            "-c:v", self.codec,
            "-pix_fmt", self.pixel_format,
            "-preset", self.quality_preset
        ]
        
        if self.audio_codec:
            args.extend([
                "-c:a", self.audio_codec,
                "-b:a", self.audio_bitrate
            ])
            
        return args

class FFmpegExporter:
    """Exports animation frames to video using FFmpeg"""
    
    def __init__(self, ffmpeg_path: Optional[str] = None):
        """
        Initialize FFmpeg exporter
        
        Args:
            ffmpeg_path: Path to FFmpeg binary. If None, will use system PATH
        """
        self.ffmpeg_path = ffmpeg_path or "ffmpeg"
        self._check_ffmpeg_available()
    
    def _check_ffmpeg_available(self):
        """Verify FFmpeg is available on the system"""
        try:
            result = subprocess.run(
                [self.ffmpeg_path, "-version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode != 0:
                raise RuntimeError("FFmpeg not found or not executable")
        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            raise RuntimeError(f"FFmpeg not available: {e}")
    
    def export_frames_to_video(
        self,
        frame_directory: Path,
        output_path: Path,
        config: Optional[FFmpegConfig] = None,
        overwrite: bool = False,
        verbose: bool = False
    ) -> Dict[str, Any]:
        """
        Export frames to video file
        
        Args:
            frame_directory: Directory containing frame images (frame_0001.png, frame_0002.png, etc.)
            output_path: Path for output video file
            config: FFmpeg configuration options
            overwrite: Whether to overwrite existing output file
            verbose: Whether to show FFmpeg progress
            
        Returns:
            Dictionary with export results and metadata
        """
        if config is None:
            config = FFmpegConfig()
        
        if not frame_directory.exists():
            raise FileNotFoundError(f"Frame directory not found: {frame_directory}")
        
        # Create output directory if it doesn't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Check for overwrite flag
        if output_path.exists() and not overwrite:
            raise FileExistsError(f"Output file already exists: {output_path}")
        
        # Find all frame files and sort them
        frame_files = sorted([
            f for f in frame_directory.glob("frame_*.png")
        ])
        
        if not frame_files:
            raise ValueError(f"No frame files found in {frame_directory}")
        
        logger.info(f"Found {len(frame_files)} frames for video export")
        
        # Build FFmpeg command
        cmd = [
            self.ffmpeg_path,
            "-y" if overwrite else "-n",  # Overwrite/no overwrite
            "-framerate", str(config.framerate),
            "-i", str(frame_directory / "frame_%04d.png"),
            *config.to_ffmpeg_args(),
            str(output_path)
        ]
        
        # Run FFmpeg
        try:
            if verbose:
                result = subprocess.run(cmd, check=True)
            else:
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            logger.info(f"Successfully exported video to {output_path}")
            
            return {
                "success": True,
                "output_path": str(output_path),
                "frame_count": len(frame_files),
                "duration_seconds": len(frame_files) / config.framerate,
                "file_size_bytes": output_path.stat().st_size if output_path.exists() else 0
            }
            
        except subprocess.CalledProcessError as e:
            error_msg = f"FFmpeg export failed: {e}"
            if hasattr(e, 'stderr') and e.stderr:
                error_msg += f"\nFFmpeg stderr: {e.stderr}"
            logger.error(error_msg)
            
            return {
                "success": False,
                "error": error_msg,
                "frame_count": len(frame_files)
            }
    
    def create_video_from_frames(
        self,
        frames: List[bytes],
        output_path: Path,
        config: Optional[FFmpegConfig] = None,
        frame_pattern: str = "frame_%04d.png"
    ) -> Dict[str, Any]:
        """
        Create video from in-memory frame data
        
        Args:
            frames: List of frame data as bytes
            output_path: Path for output video file
            config: FFmpeg configuration options
            frame_pattern: Filename pattern for temporary frames
            
        Returns:
            Dictionary with export results
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Write frames to temporary directory
            for i, frame_data in enumerate(frames):
                frame_file = temp_path / frame_pattern % (i + 1)
                frame_file.write_bytes(frame_data)
            
            return self.export_frames_to_video(
                frame_directory=temp_path,
                output_path=output_path,
                config=config
            )
    
    def get_video_info(self, video_path: Path) -> Dict[str, Any]:
        """
        Get information about a video file
        
        Args:
            video_path: Path to video file
            
        Returns:
            Dictionary with video metadata
        """
        if not video_path.exists():
            raise FileNotFoundError(f"Video file not found: {video_path}")
        
        cmd = [
            self.ffmpeg_path,
            "-i", str(video_path),
            "-f", "null",
            "-"
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            # Parse FFmpeg output for video information
            output_lines = result.stderr.split('\n')
            video_info = {
                "file_path": str(video_path),
                "file_size_bytes": video_path.stat().st_size
            }
            
            for line in output_lines:
                if "Duration:" in line:
                    # Parse duration: Duration: 00:01:23.45
                    duration_part = line.split("Duration:")[1].split(",")[0].strip()
                    video_info["duration_seconds"] = self._parse_duration(duration_part)
                elif "Video:" in line:
                    # Parse video stream info
                    video_info["video_codec"] = line.split("Video:")[1].split(",")[0].strip()
            
            return video_info
            
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to get video info: {e}")
    
    def _parse_duration(self, duration_str: str) -> float:
        """Parse FFmpeg duration string to seconds"""
        try:
            parts = duration_str.split(":")
            hours = int(parts[0])
            minutes = int(parts[1])
            seconds = float(parts[2])
            return hours * 3600 + minutes * 60 + seconds
        except (ValueError, IndexError):
            return 0.0