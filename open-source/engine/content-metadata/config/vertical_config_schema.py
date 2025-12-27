"""
VisualVerse Configuration Schema and Templates

This module provides the configuration system for all verticals including
JSON schemas, templates, and validation utilities for the VisualVerse
learning platform.

Author: MiniMax Agent
Version: 1.0.0
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Union
from enum import Enum
from pathlib import Path
import json
import jsonschema
from jsonschema import Draft7Validator
import copy


class VerticalType(str, Enum):
    """Types of verticals supported in the platform."""
    MATH_VERSE = "math-verse"
    ALGO_VERSE = "algo-verse"
    PHYSICS_VERSE = "physics-verse"
    CHEM_VERSE = "chem-verse"
    FIN_VERSE = "fin-verse"


class RendererType(str, Enum):
    """Types of rendering engines supported."""
    CANVAS = "canvas"
    WEBGL = "webgl"
    SVG = "svg"
    MANIM = "manim"
    HYBRID = "hybrid"


class CachingStrategy(str, Enum):
    """Caching strategies for service data."""
    LRU = "lru"
    FIFO = "fifo"
    TTL = "ttl"
    NONE = "none"


class DifficultyLevel(str, Enum):
    """Difficulty levels for learning content."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


@dataclass
class ColorPalette:
    """Color palette configuration for a vertical."""
    primary: str = "#3B82F6"
    secondary: str = "#8B5CF6"
    success: str = "#10B981"
    warning: str = "#F59E0B"
    error: str = "#EF4444"
    neutral: str = "#6B7280"
    background: str = "#FFFFFF"
    text: str = "#1F2937"
    
    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary."""
        return {
            "primary": self.primary,
            "secondary": self.secondary,
            "success": self.success,
            "warning": self.warning,
            "error": self.error,
            "neutral": self.neutral,
            "background": self.background,
            "text": self.text
        }


@dataclass
class CameraConfig:
    """Camera position and settings configuration."""
    position: Dict[str, float] = field(default_factory=lambda: {"x": 0, "y": 0, "z": 10})
    target: Dict[str, float] = field(default_factory=lambda: {"x": 0, "y": 0, "z": 0})
    fov: float = 45.0
    near: float = 0.1
    far: float = 1000.0
    zoom_min: float = 0.1
    zoom_max: float = 10.0
    default_zoom: float = 1.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "position": self.position,
            "target": self.target,
            "fov": self.fov,
            "near": self.near,
            "far": self.far,
            "zoomMin": self.zoom_min,
            "zoomMax": self.zoom_max,
            "defaultZoom": self.default_zoom
        }


@dataclass
class AnimationConfig:
    """Animation parameters configuration."""
    default_duration_ms: int = 1000
    easing_function: str = "ease-in-out"
    step_delay_ms: int = 100
    transition_type: str = "smooth"
    auto_play: bool = True
    loop_animation: bool = False
    show_controls: bool = True
    speed_multiplier: float = 1.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "defaultDurationMs": self.default_duration_ms,
            "easingFunction": self.easing_function,
            "stepDelayMs": self.step_delay_ms,
            "transitionType": self.transition_type,
            "autoPlay": self.auto_play,
            "loopAnimation": self.loop_animation,
            "showControls": self.show_controls,
            "speedMultiplier": self.speed_multiplier
        }


@dataclass
class InteractionConfig:
    """User interaction configuration."""
    enable_pan: bool = True
    enable_zoom: bool = True
    enable_rotate: bool = True
    enable_click: bool = True
    enable_drag: bool = True
    pan_button: str = "left"
    zoom_mouse_wheel: bool = True
    double_click_zoom: bool = False
    touch_support: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "enablePan": self.enable_pan,
            "enableZoom": self.enable_zoom,
            "enableRotate": self.enable_rotate,
            "enableClick": self.enable_click,
            "enableDrag": self.enable_drag,
            "panButton": self.pan_button,
            "zoomMouseWheel": self.zoom_mouse_wheel,
            "doubleClickZoom": double_click_zoom,
            "touchSupport": self.touch_support
        }


@dataclass
class LearningObjective:
    """Learning objective configuration."""
    id: str
    title: str
    description: str
    difficulty: DifficultyLevel
    prerequisites: List[str] = field(default_factory=list)
    estimated_minutes: int = 15
    skills: List[str] = field(default_factory=list)
    assessment_type: str = "quiz"
    mastery_threshold: float = 0.8
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "difficulty": self.difficulty.value,
            "prerequisites": self.prerequisites,
            "estimatedMinutes": self.estimated_minutes,
            "skills": self.skills,
            "assessmentType": self.assessment_type,
            "masteryThreshold": self.mastery_threshold
        }


@dataclass
class ServiceSettings:
    """Service-level configuration."""
    api_endpoint: str = ""
    update_frequency_ms: int = 5000
    caching_strategy: CachingStrategy = CachingStrategy.LRU
    cache_ttl_seconds: int = 300
    max_retries: int = 3
    timeout_seconds: int = 30
    enable_logging: bool = True
    log_level: str = "info"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "apiEndpoint": self.api_endpoint,
            "updateFrequencyMs": self.update_frequency_ms,
            "cachingStrategy": self.caching_strategy.value,
            "cacheTtlSeconds": self.cache_ttl_seconds,
            "maxRetries": self.max_retries,
            "timeoutSeconds": self.timeout_seconds,
            "enableLogging": self.enable_logging,
            "logLevel": self.log_level
        }


@dataclass
class VisualPreferences:
    """Visual rendering preferences."""
    renderer: RendererType = RendererType.WEBGL
    color_palette: ColorPalette = field(default_factory=ColorPalette)
    camera: CameraConfig = field(default_factory=CameraConfig)
    antialiasing: bool = True
    shadows_enabled: bool = False
    ambient_occlusion: bool = False
    particle_quality: str = "medium"
    texture_quality: str = "medium"
    resolution_scale: float = 1.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "renderer": self.renderer.value,
            "colorPalette": self.color_palette.to_dict(),
            "camera": self.camera.to_dict(),
            "antialiasing": self.antialiasing,
            "shadowsEnabled": self.shadows_enabled,
            "ambientOcclusion": self.ambient_occlusion,
            "particleQuality": self.particle_quality,
            "textureQuality": self.texture_quality,
            "resolutionScale": self.resolution_scale
        }


@dataclass
class DomainSpecificConfig:
    """Domain-specific configuration container."""
    math_config: Dict[str, Any] = field(default_factory=dict)
    algo_config: Dict[str, Any] = field(default_factory=dict)
    physics_config: Dict[str, Any] = field(default_factory=dict)
    chemistry_config: Dict[str, Any] = field(default_factory=dict)
    finance_config: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "math": self.math_config,
            "algo": self.algo_config,
            "physics": self.physics_config,
            "chemistry": self.chemistry_config,
            "finance": self.finance_config
        }


@dataclass
class VerticalConfig:
    """Complete vertical configuration."""
    vertical_id: str
    vertical_name: str
    vertical_type: VerticalType
    version: str = "1.0.0"
    description: str = ""
    
    # Service configuration
    service_settings: ServiceSettings = field(default_factory=ServiceSettings)
    
    # Visual configuration
    visual_preferences: VisualPreferences = field(default_factory=VisualPreferences)
    
    # Animation configuration
    animation: AnimationConfig = field(default_factory=AnimationConfig)
    
    # Interaction configuration
    interaction: InteractionConfig = field(default_factory=InteractionConfig)
    
    # Learning objectives
    learning_objectives: List[LearningObjective] = field(default_factory=list)
    
    # Domain-specific configuration
    domain_specific: DomainSpecificConfig = field(default_factory=DomainSpecificConfig)
    
    # Feature flags
    features: Dict[str, bool] = field(default_factory=lambda: {
        "interactive_mode": True,
        "animation_support": True,
        "export_enabled": True,
        "collaboration": False,
        "accessibility": True
    })
    
    # Metadata
    author: str = "MiniMax Agent"
    created_at: str = ""
    updated_at: str = ""
    tags: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "verticalId": self.vertical_id,
            "verticalName": self.vertical_name,
            "verticalType": self.vertical_type.value,
            "version": self.version,
            "description": self.description,
            "serviceSettings": self.service_settings.to_dict(),
            "visualPreferences": self.visual_preferences.to_dict(),
            "animation": self.animation.to_dict(),
            "interaction": self.interaction.to_dict(),
            "learningObjectives": [obj.to_dict() for obj in self.learning_objectives],
            "domainSpecific": self.domain_specific.to_dict(),
            "features": self.features,
            "author": self.author,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at,
            "tags": self.tags
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'VerticalConfig':
        """Create from dictionary."""
        config = cls(
            vertical_id=data.get("verticalId", ""),
            vertical_name=data.get("verticalName", ""),
            vertical_type=VerticalType(data.get("verticalType", "math-verse")),
            version=data.get("version", "1.0.0"),
            description=data.get("description", "")
        )
        
        if "serviceSettings" in data:
            ss_data = data["serviceSettings"]
            config.service_settings = ServiceSettings(
                api_endpoint=ss_data.get("apiEndpoint", ""),
                update_frequency_ms=ss_data.get("updateFrequencyMs", 5000),
                caching_strategy=CachingStrategy(ss_data.get("cachingStrategy", "lru")),
                cache_ttl_seconds=ss_data.get("cacheTtlSeconds", 300),
                max_retries=ss_data.get("maxRetries", 3),
                timeout_seconds=ss_data.get("timeoutSeconds", 30),
                enable_logging=ss_data.get("enableLogging", True),
                log_level=ss_data.get("logLevel", "info")
            )
        
        return config


# Master JSON Schema for Configuration Validation
MASTER_CONFIG_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "VisualVerse Vertical Configuration Schema",
    "description": "Master schema for validating vertical configuration files",
    "type": "object",
    "required": ["verticalId", "verticalName", "verticalType"],
    "properties": {
        "verticalId": {
            "type": "string",
            "pattern": "^[a-z]+-[a-z]+$",
            "description": "Unique identifier for the vertical (e.g., 'physics-mechanics')"
        },
        "verticalName": {
            "type": "string",
            "minLength": 1,
            "maxLength": 100,
            "description": "Human-readable name of the vertical"
        },
        "verticalType": {
            "type": "string",
            "enum": ["math-verse", "algo-verse", "physics-verse", "chem-verse", "fin-verse"],
            "description": "Type of vertical"
        },
        "version": {
            "type": "string",
            "pattern": "^[0-9]+\\.[0-9]+\\.[0-9]+$",
            "description": "Semantic version of the configuration"
        },
        "description": {
            "type": "string",
            "maxLength": 500,
            "description": "Brief description of the vertical"
        },
        "serviceSettings": {
            "type": "object",
            "properties": {
                "apiEndpoint": {"type": "string", "format": "uri"},
                "updateFrequencyMs": {"type": "integer", "minimum": 100},
                "cachingStrategy": {"type": "string", "enum": ["lru", "fifo", "ttl", "none"]},
                "cacheTtlSeconds": {"type": "integer", "minimum": 0},
                "maxRetries": {"type": "integer", "minimum": 0},
                "timeoutSeconds": {"type": "integer", "minimum": 1},
                "enableLogging": {"type": "boolean"},
                "logLevel": {"type": "string", "enum": ["debug", "info", "warning", "error"]}
            }
        },
        "visualPreferences": {
            "type": "object",
            "properties": {
                "renderer": {"type": "string", "enum": ["canvas", "webgl", "svg", "manim", "hybrid"]},
                "colorPalette": {
                    "type": "object",
                    "properties": {
                        "primary": {"type": "string", "pattern": "^#[0-9A-Fa-f]{6}$"},
                        "secondary": {"type": "string", "pattern": "^#[0-9A-Fa-f]{6}$"},
                        "success": {"type": "string", "pattern": "^#[0-9A-Fa-f]{6}$"},
                        "warning": {"type": "string", "pattern": "^#[0-9A-Fa-f]{6}$"},
                        "error": {"type": "string", "pattern": "^#[0-9A-Fa-f]{6}$"},
                        "neutral": {"type": "string", "pattern": "^#[0-9A-Fa-f]{6}$"},
                        "background": {"type": "string", "pattern": "^#[0-9A-Fa-f]{6}$"},
                        "text": {"type": "string", "pattern": "^#[0-9A-Fa-f]{6}$"}
                    }
                },
                "camera": {
                    "type": "object",
                    "properties": {
                        "position": {
                            "type": "object",
                            "properties": {
                                "x": {"type": "number"},
                                "y": {"type": "number"},
                                "z": {"type": "number"}
                            }
                        },
                        "target": {
                            "type": "object",
                            "properties": {
                                "x": {"type": "number"},
                                "y": {"type": "number"},
                                "z": {"type": "number"}
                            }
                        },
                        "fov": {"type": "number", "minimum": 1, "maximum": 179},
                        "near": {"type": "number", "minimum": 0},
                        "far": {"type": "number", "minimum": 0},
                        "zoomMin": {"type": "number", "minimum": 0},
                        "zoomMax": {"type": "number", "minimum": 0},
                        "defaultZoom": {"type": "number", "minimum": 0}
                    }
                },
                "antialiasing": {"type": "boolean"},
                "shadowsEnabled": {"type": "boolean"},
                "ambientOcclusion": {"type": "boolean"},
                "particleQuality": {"type": "string", "enum": ["low", "medium", "high"]},
                "textureQuality": {"type": "string", "enum": ["low", "medium", "high"]},
                "resolutionScale": {"type": "number", "minimum": 0.5, "maximum": 2.0}
            }
        },
        "animation": {
            "type": "object",
            "properties": {
                "defaultDurationMs": {"type": "integer", "minimum": 100},
                "easingFunction": {"type": "string"},
                "stepDelayMs": {"type": "integer", "minimum": 0},
                "transitionType": {"type": "string"},
                "autoPlay": {"type": "boolean"},
                "loopAnimation": {"type": "boolean"},
                "showControls": {"type": "boolean"},
                "speedMultiplier": {"type": "number", "minimum": 0.1, "maximum": 5.0}
            }
        },
        "interaction": {
            "type": "object",
            "properties": {
                "enablePan": {"type": "boolean"},
                "enableZoom": {"type": "boolean"},
                "enableRotate": {"type": "boolean"},
                "enableClick": {"type": "boolean"},
                "enableDrag": {"type": "boolean"},
                "panButton": {"type": "string", "enum": ["left", "middle", "right"]},
                "zoomMouseWheel": {"type": "boolean"},
                "doubleClickZoom": {"type": "boolean"},
                "touchSupport": {"type": "boolean"}
            }
        },
        "learningObjectives": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["id", "title", "description", "difficulty"],
                "properties": {
                    "id": {"type": "string"},
                    "title": {"type": "string"},
                    "description": {"type": "string"},
                    "difficulty": {"type": "string", "enum": ["beginner", "intermediate", "advanced", "expert"]},
                    "prerequisites": {"type": "array", "items": {"type": "string"}},
                    "estimatedMinutes": {"type": "integer", "minimum": 1},
                    "skills": {"type": "array", "items": {"type": "string"}},
                    "assessmentType": {"type": "string"},
                    "masteryThreshold": {"type": "number", "minimum": 0, "maximum": 1}
                }
            }
        },
        "domainSpecific": {
            "type": "object",
            "properties": {
                "math": {"type": "object"},
                "algo": {"type": "object"},
                "physics": {"type": "object"},
                "chemistry": {"type": "object"},
                "finance": {"type": "object"}
            }
        },
        "features": {
            "type": "object",
            "properties": {
                "interactiveMode": {"type": "boolean"},
                "animationSupport": {"type": "boolean"},
                "exportEnabled": {"type": "boolean"},
                "collaboration": {"type": "boolean"},
                "accessibility": {"type": "boolean"}
            }
        },
        "author": {"type": "string"},
        "createdAt": {"type": "string", "format": "date-time"},
        "updatedAt": {"type": "string", "format": "date-time"},
        "tags": {"type": "array", "items": {"type": "string"}}
    }
}


class ConfigurationManager:
    """
    Central configuration manager for loading, validating, and caching
    vertical configurations.
    """
    
    _instance = None
    _config_cache: Dict[str, VerticalConfig] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._config_dir = Path(__file__).parent / "verticals"
            self._validator = Draft7Validator(MASTER_CONFIG_SCHEMA)
            self._initialized = True
    
    def load_config(self, vertical_id: str, config_path: str = None) -> VerticalConfig:
        """
        Load and validate a vertical configuration.
        
        Args:
            vertical_id: The vertical identifier
            config_path: Optional path to config file
            
        Returns:
            Validated VerticalConfig object
        """
        # Check cache first
        if vertical_id in self._config_cache:
            return self._config_cache[vertical_id]
        
        # Load config file
        if config_path is None:
            config_path = str(self._config_dir / f"{vertical_id}.json")
        
        with open(config_path, 'r') as f:
            config_data = json.load(f)
        
        # Validate against schema
        errors = list(self._validator.iter_errors(config_data))
        if errors:
            raise ValueError(f"Configuration validation errors: {errors}")
        
        # Create config object
        config = VerticalConfig.from_dict(config_data)
        
        # Cache and return
        self._config_cache[vertical_id] = config
        return config
    
    def get_config(self, vertical_id: str) -> Optional[VerticalConfig]:
        """
        Get a cached configuration.
        
        Args:
            vertical_id: The vertical identifier
            
        Returns:
            VerticalConfig or None if not found
        """
        return self._config_cache.get(vertical_id)
    
    def reload_config(self, vertical_id: str) -> Optional[VerticalConfig]:
        """
        Reload a configuration from disk.
        
        Args:
            vertical_id: The vertical identifier
            
        Returns:
            Reloaded VerticalConfig or None
        """
        if vertical_id in self._config_cache:
            del self._config_cache[vertical_id]
        return self.load_config(vertical_id)
    
    def list_configs(self) -> List[str]:
        """
        List all available configurations.
        
        Returns:
            List of vertical IDs
        """
        return list(self._config_cache.keys())
    
    def merge_with_defaults(self, config_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Merge configuration with global defaults.
        
        Args:
            config_data: Configuration data to merge
            
        Returns:
            Merged configuration
        """
        defaults = self._get_default_config()
        merged = copy.deepcopy(defaults)
        self._deep_merge(merged, config_data)
        return merged
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration values."""
        return {
            "serviceSettings": {
                "updateFrequencyMs": 5000,
                "cachingStrategy": "lru",
                "cacheTtlSeconds": 300,
                "maxRetries": 3,
                "timeoutSeconds": 30,
                "enableLogging": True,
                "logLevel": "info"
            },
            "visualPreferences": {
                "renderer": "webgl",
                "antialiasing": True,
                "shadowsEnabled": False,
                "ambientOcclusion": False,
                "particleQuality": "medium",
                "textureQuality": "medium",
                "resolutionScale": 1.0
            },
            "animation": {
                "defaultDurationMs": 1000,
                "easingFunction": "ease-in-out",
                "stepDelayMs": 100,
                "autoPlay": True,
                "loopAnimation": False,
                "showControls": True,
                "speedMultiplier": 1.0
            },
            "interaction": {
                "enablePan": True,
                "enableZoom": True,
                "enableRotate": True,
                "enableClick": True,
                "enableDrag": True,
                "touchSupport": True
            }
        }
    
    def _deep_merge(self, base: Dict, override: Dict) -> None:
        """Deep merge override into base."""
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value


class TemplateGenerator:
    """
    Generator for creating vertical configuration templates.
    """
    
    @staticmethod
    def create_math_verse_template() -> Dict[str, Any]:
        """Create MathVerse configuration template."""
        return {
            "verticalId": "math-verse",
            "verticalName": "Mathematical Visualization",
            "verticalType": "math-verse",
            "version": "1.0.0",
            "description": "Mathematical concepts and formula visualization",
            "serviceSettings": {
                "apiEndpoint": "/api/math-verse"
            },
            "visualPreferences": {
                "renderer": "webgl",
                "colorPalette": {
                    "primary": "#3B82F6",
                    "secondary": "#8B5CF6",
                    "success": "#10B981",
                    "warning": "#F59E0B",
                    "error": "#EF4444"
                }
            },
            "domainSpecific": {
                "math": {
                    "supportedGraphTypes": ["2d", "3d", "parametric", "implicit"],
                    "equationRendering": "latex",
                    "animationTypes": ["plot", "transform", "rotate"]
                }
            },
            "learningObjectives": [
                {
                    "id": "math-calc-intro",
                    "title": "Introduction to Calculus",
                    "description": "Understand basic calculus concepts",
                    "difficulty": "beginner",
                    "prerequisites": [],
                    "estimatedMinutes": 30
                }
            ]
        }
    
    @staticmethod
    def create_physics_verse_template() -> Dict[str, Any]:
        """Create PhysicsVerse configuration template."""
        return {
            "verticalId": "physics-verse",
            "verticalName": "Physics Simulation",
            "verticalType": "physics-verse",
            "version": "1.0.0",
            "description": "Physics simulations and mechanics visualization",
            "serviceSettings": {
                "apiEndpoint": "/api/physics-verse"
            },
            "visualPreferences": {
                "renderer": "webgl",
                "camera": {
                    "position": {"x": 0, "y": 5, "z": 15},
                    "target": {"x": 0, "y": 0, "z": 0}
                }
            },
            "domainSpecific": {
                "physics": {
                    "supportedSimulations": ["mechanics", "optics", "electromagnetism"],
                    "physicsEngine": "custom",
                    "gravity": -9.81,
                    "collisionDetection": true,
                    "maxParticles": 1000
                }
            }
        }
    
    @staticmethod
    def create_chem_verse_template() -> Dict[str, Any]:
        """Create ChemVerse configuration template."""
        return {
            "verticalId": "chem-verse",
            "verticalName": "Chemistry Visualization",
            "verticalType": "chem-verse",
            "version": "1.0.0",
            "description": "Molecular structures and chemical reactions",
            "serviceSettings": {
                "apiEndpoint": "/api/chem-verse"
            },
            "visualPreferences": {
                "renderer": "webgl",
                "colorPalette": {
                    "primary": "#10B981",
                    "secondary": "#3B82F6"
                }
            },
            "domainSpecific": {
                "chemistry": {
                    "renderStyles": ["ball-and-stick", "space-filling", "wireframe"],
                    "animationTypes": ["reaction", "bond-formation", "orbitals"],
                    "supportedElements": ["H", "C", "N", "O", "F", "P", "S", "Cl"]
                }
            }
        }
    
    @staticmethod
    def create_algo_verse_template() -> Dict[str, Any]:
        """Create AlgoVerse configuration template."""
        return {
            "verticalId": "algo-verse",
            "verticalName": "Algorithm Visualization",
            "verticalType": "algo-verse",
            "version": "1.0.0",
            "description": "Algorithm steps and data structure visualization",
            "serviceSettings": {
                "apiEndpoint": "/api/algo-verse"
            },
            "domainSpecific": {
                "algo": {
                    "supportedStructures": ["array", "linked-list", "tree", "graph", "heap"],
                    "animationSpeed": 1.0,
                    "stepByStep": True,
                    "codeHighlighting": True
                }
            }
        }
    
    @staticmethod
    def create_fin_verse_template() -> Dict[str, Any]:
        """Create FinVerse configuration template."""
        return {
            "verticalId": "fin-verse",
            "verticalName": "Financial Visualization",
            "verticalType": "fin-verse",
            "version": "1.0.0",
            "description": "Financial charts and portfolio analysis",
            "serviceSettings": {
                "apiEndpoint": "/api/fin-verse"
            },
            "domainSpecific": {
                "finance": {
                    "chartTypes": ["line", "candlestick", "bar", "pie"],
                    "supportedIndicators": ["SMA", "EMA", "RSI", "MACD"],
                    "timeframes": ["1D", "1W", "1M", "1Y", "5Y", "ALL"]
                }
            }
        }


def validate_config(config_data: Dict[str, Any]) -> tuple:
    """
    Validate configuration data against the master schema.
    
    Args:
        config_data: Configuration data to validate
        
    Returns:
        Tuple of (is_valid, errors)
    """
    validator = Draft7Validator(MASTER_CONFIG_SCHEMA)
    errors = list(validator.iter_errors(config_data))
    return (len(errors) == 0), [str(e) for e in errors]


def create_default_config(vertical_type: str) -> Dict[str, Any]:
    """
    Create a default configuration for a vertical type.
    
    Args:
        vertical_type: Type of vertical
        
    Returns:
        Default configuration dictionary
    """
    generator = TemplateGenerator()
    
    templates = {
        "math-verse": generator.create_math_verse_template,
        "physics-verse": generator.create_physics_verse_template,
        "chem-verse": generator.create_chem_verse_template,
        "algo-verse": generator.create_algo_verse_template,
        "fin-verse": generator.create_fin_verse_template
    }
    
    if vertical_type in templates:
        return templates[vertical_type]()
    else:
        raise ValueError(f"Unknown vertical type: {vertical_type}")


__all__ = [
    "VerticalType",
    "RendererType",
    "CachingStrategy",
    "DifficultyLevel",
    "ColorPalette",
    "CameraConfig",
    "AnimationConfig",
    "InteractionConfig",
    "LearningObjective",
    "ServiceSettings",
    "VisualPreferences",
    "DomainSpecificConfig",
    "VerticalConfig",
    "MASTER_CONFIG_SCHEMA",
    "ConfigurationManager",
    "TemplateGenerator",
    "validate_config",
    "create_default_config"
]
