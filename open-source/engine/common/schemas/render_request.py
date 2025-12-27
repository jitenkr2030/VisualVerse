"""
Render Request Schema for VisualVerse Engine

Pydantic model defining the inputs required to trigger a render job
including script ID, resolution, format, and rendering options.
"""

from typing import Optional, Dict, Any, List, Union
from enum import Enum
from datetime import datetime
from pathlib import Path
from pydantic import BaseModel, Field, validator, root_validator
import uuid

class RenderFormat(Enum):
    """Supported render output formats"""
    MP4 = "mp4"
    WEBM = "webm"
    AVI = "avi"
    MOV = "mov"
    GIF = "gif"
    PNG = "png"
    JPEG = "jpeg"
    SVG = "svg"

class RenderQuality(Enum):
    """Render quality presets"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    ULTRA = "ultra"
    CUSTOM = "custom"

class RenderEngine(Enum):
    """Available render engines"""
    MANIM = "manim"
    BLENDER = "blender"
    INTERNAL = "internal"

class RenderStatus(Enum):
    """Render job status"""
    PENDING = "pending"
    QUEUED = "queued"
    RENDERING = "rendering"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class AudioSettings(BaseModel):
    """Audio configuration for render"""
    enabled: bool = False
    sample_rate: int = 44100
    bitrate: int = 128
    format: str = "mp3"
    volume: float = 1.0
    fade_in: float = 0.0
    fade_out: float = 0.0

class VideoSettings(BaseModel):
    """Video configuration for render"""
    fps: int = 30
    codec: str = "libx264"
    bitrate: str = "2M"
    quality: RenderQuality = RenderQuality.MEDIUM
    pixel_format: str = "yuv420p"
    color_profile: str = "bt709"
    
    @validator('fps')
    def validate_fps(cls, v):
        if v < 1 or v > 120:
            raise ValueError('FPS must be between 1 and 120')
        return v

class ImageSettings(BaseModel):
    """Image configuration for render"""
    format: RenderFormat = RenderFormat.PNG
    quality: int = 95
    dpi: int = 300
    color_depth: int = 8
    compression: bool = True

class RenderOptions(BaseModel):
    """Additional render options"""
    parallel_rendering: bool = True
    max_threads: int = 4
    memory_limit_gb: int = 8
    cache_enabled: bool = True
    cache_duration_hours: int = 24
    preview_enabled: bool = False
    watermark_enabled: bool = False
    watermark_text: Optional[str] = None
    watermark_position: str = "bottom-right"
    background_transparent: bool = False

class SceneProperties(BaseModel):
    """Scene-level properties"""
    width: int = 1920
    height: int = 1080
    background_color: str = "#FFFFFF"
    frame_rate: int = 30
    duration: Optional[float] = None  # If None, auto-calculate from animations
    aspect_ratio: Optional[str] = None
    
    @validator('width', 'height')
    def validate_dimensions(cls, v):
        if v < 64 or v > 7680:
            raise ValueError('Dimension must be between 64 and 7680 pixels')
        return v
    
    @validator('background_color')
    def validate_color(cls, v):
        if not v.startswith('#') or len(v) not in [4, 7, 9]:
            raise ValueError('Background color must be a valid hex color')
        return v

class RenderRequest(BaseModel):
    """Main render request model"""
    # Required fields
    job_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    script_id: str = Field(..., description="ID of the animation script to render")
    output_format: RenderFormat = Field(..., description="Output file format")
    
    # Scene configuration
    scene: SceneProperties = Field(default_factory=SceneProperties)
    
    # Engine configuration
    engine: RenderEngine = Field(default=RenderEngine.MANIM, description="Render engine to use")
    
    # Output configuration
    output_path: Optional[str] = Field(None, description="Custom output path (auto-generated if None)")
    filename: Optional[str] = Field(None, description="Custom filename (auto-generated if None)")
    
    # Quality and settings
    video_settings: Optional[VideoSettings] = Field(None, description="Video-specific settings")
    image_settings: Optional[ImageSettings] = Field(None, description="Image-specific settings")
    audio_settings: AudioSettings = Field(default_factory=AudioSettings)
    options: RenderOptions = Field(default_factory=RenderOptions)
    
    # Metadata
    user_id: Optional[str] = Field(None, description="User who initiated the render")
    project_id: Optional[str] = Field(None, description="Project context")
    priority: int = Field(default=5, ge=1, le=10, description="Render priority (1=highest, 10=lowest)")
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        use_enum_values = True
    
    @root_validator
    def validate_settings(cls, values):
        """Validate settings based on output format"""
        output_format = values.get('output_format')
        video_settings = values.get('video_settings')
        image_settings = values.get('image_settings')
        
        if output_format in [RenderFormat.MP4, RenderFormat.WEBM, RenderFormat.AVI, RenderFormat.MOV]:
            if video_settings is None:
                values['video_settings'] = VideoSettings()
        elif output_format in [RenderFormat.PNG, RenderFormat.JPEG]:
            if image_settings is None:
                values['image_settings'] = ImageSettings()
        
        return values
    
    @validator('output_path')
    def validate_output_path(cls, v, values):
        """Validate output path"""
        if v:
            try:
                path = Path(v)
                # Ensure parent directory exists or can be created
                path.parent.mkdir(parents=True, exist_ok=True)
            except (OSError, PermissionError) as e:
                raise ValueError(f'Invalid output path: {e}')
        return v
    
    @validator('filename')
    def validate_filename(cls, v):
        """Validate filename"""
        if v:
            # Check for invalid characters
            invalid_chars = '<>:"/\\|?*'
            if any(char in v for char in invalid_chars):
                raise ValueError(f'Filename contains invalid characters: {invalid_chars}')
            
            # Check length
            if len(v) > 255:
                raise ValueError('Filename too long (max 255 characters)')
        return v
    
    def generate_output_path(self) -> str:
        """Generate output path based on request parameters"""
        if self.output_path:
            return self.output_path
        
        # Generate path based on script_id and format
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.filename or f"{self.script_id}_{timestamp}"
        
        # Ensure proper extension
        extension = self.output_format.value
        if not filename.endswith(f".{extension}"):
            filename = f"{filename}.{extension}"
        
        # Default output directory
        default_dir = Path("renders") / self.script_id
        return str(default_dir / filename)
    
    def get_file_size_estimate(self) -> int:
        """Estimate output file size in bytes"""
        if self.output_format in [RenderFormat.MP4, RenderFormat.WEBM, RenderFormat.AVI, RenderFormat.MOV]:
            # Video size estimation
            fps = self.scene.frame_rate
            duration = self.scene.duration or 10.0  # Default 10 seconds
            bitrate_str = self.video_settings.bitrate if self.video_settings else "2M"
            
            # Parse bitrate (e.g., "2M" -> 2000000)
            bitrate = int(bitrate_str.replace('M', '000000').replace('K', '000'))
            
            # Estimate size (rough calculation)
            size_bytes = (bitrate * duration) // 8
            return size_bytes
        
        elif self.output_format in [RenderFormat.PNG, RenderFormat.JPEG]:
            # Image size estimation
            width = self.scene.width
            height = self.scene.height
            
            if self.output_format == RenderFormat.PNG:
                # PNG is roughly width * height * 3-4 bytes
                estimated_size = width * height * 4
            else:  # JPEG
                # JPEG is roughly width * height * 0.8-1.2 bytes (depends on quality)
                quality = self.image_settings.quality if self.image_settings else 95
                compression_ratio = quality / 100.0
                estimated_size = int(width * height * compression_ratio)
            
            return estimated_size
        
        else:
            # GIF and other formats
            return 1024 * 1024  # Default 1MB estimate
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert request to dictionary"""
        return self.dict(by_alias=True, exclude_none=True)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'RenderRequest':
        """Create request from dictionary"""
        return cls(**data)

class RenderJob(BaseModel):
    """Extended render job model with status tracking"""
    request: RenderRequest
    status: RenderStatus = RenderStatus.PENDING
    progress: float = 0.0
    current_frame: int = 0
    total_frames: int = 0
    
    # Timing
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    estimated_completion: Optional[datetime] = None
    
    # Results
    output_file: Optional[str] = None
    file_size: Optional[int] = None
    error_message: Optional[str] = None
    logs: List[str] = Field(default_factory=list)
    
    # Performance metrics
    render_time_seconds: Optional[float] = None
    frames_per_second: Optional[float] = None
    memory_peak_mb: Optional[float] = None
    
    class Config:
        use_enum_values = True
    
    def update_progress(self, current_frame: int, total_frames: int):
        """Update render progress"""
        self.current_frame = current_frame
        self.total_frames = total_frames
        self.progress = (current_frame / total_frames) * 100 if total_frames > 0 else 0
    
    def mark_completed(self, output_file: str, file_size: int):
        """Mark render as completed"""
        self.status = RenderStatus.COMPLETED
        self.completed_at = datetime.utcnow()
        self.output_file = output_file
        self.file_size = file_size
        self.progress = 100.0
    
    def mark_failed(self, error_message: str):
        """Mark render as failed"""
        self.status = RenderStatus.FAILED
        self.completed_at = datetime.utcnow()
        self.error_message = error_message
    
    def get_duration(self) -> Optional[float]:
        """Get render duration in seconds"""
        if self.started_at and self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        return None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert job to dictionary"""
        data = self.dict(by_alias=True, exclude_none=True)
        
        # Handle datetime serialization
        for field_name, field_value in data.items():
            if isinstance(field_value, datetime):
                data[field_name] = field_value.isoformat() + "Z"
        
        return data
    
    @classmethod
    def from_request(cls, request: RenderRequest) -> 'RenderJob':
        """Create job from request"""
        return cls(request=request)

class RenderQueueStatus(BaseModel):
    """Status of the render queue"""
    total_jobs: int = 0
    pending_jobs: int = 0
    rendering_jobs: int = 0
    completed_jobs: int = 0
    failed_jobs: int = 0
    
    average_wait_time_minutes: float = 0.0
    estimated_throughput_jobs_per_hour: float = 0.0
    
    active_jobs: List[RenderJob] = Field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert queue status to dictionary"""
        return self.dict()

# Utility functions
def create_render_request(
    script_id: str,
    output_format: RenderFormat,
    width: int = 1920,
    height: int = 1080,
    **kwargs
) -> RenderRequest:
    """Create a basic render request"""
    scene = SceneProperties(width=width, height=height)
    return RenderRequest(
        script_id=script_id,
        output_format=output_format,
        scene=scene,
        **kwargs
    )

def validate_render_request(request_data: Dict[str, Any]) -> List[str]:
    """Validate render request data and return error messages"""
    errors = []
    
    try:
        RenderRequest(**request_data)
    except Exception as e:
        errors.append(str(e))
    
    return errors