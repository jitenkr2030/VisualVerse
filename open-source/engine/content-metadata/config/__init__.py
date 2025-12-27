"""
VisualVerse Configuration Package

This package provides the configuration management system for the VisualVerse
learning platform, including schema definitions, validation utilities, and
the central configuration manager.

Modules:
    vertical_config_schema: Core configuration schema and data classes
    config_manager: Configuration loading, validation, and caching

Author: MiniMax Agent
Version: 1.0.0
"""

from .vertical_config_schema import (
    VerticalType,
    RendererType,
    CachingStrategy,
    DifficultyLevel,
    ColorPalette,
    CameraConfig,
    AnimationConfig,
    InteractionConfig,
    LearningObjective,
    ServiceSettings,
    VisualPreferences,
    DomainSpecificConfig,
    VerticalConfig,
    MASTER_CONFIG_SCHEMA,
    TemplateGenerator,
    validate_config,
    create_default_config
)

from .config_manager import (
    ConfigLoadError,
    ConfigValidationError,
    ConfigNotFoundError,
    ConfigSource,
    ConfigMetadata,
    LoadedConfig,
    SchemaValidator,
    VerticalConfigLoader,
    ConfigurationManager,
    get_config_manager
)


__all__ = [
    # Enums
    "VerticalType",
    "RendererType",
    "CachingStrategy",
    "DifficultyLevel",
    
    # Data classes
    "ColorPalette",
    "CameraConfig",
    "AnimationConfig",
    "InteractionConfig",
    "LearningObjective",
    "ServiceSettings",
    "VisualPreferences",
    "DomainSpecificConfig",
    "VerticalConfig",
    
    # Schema
    "MASTER_CONFIG_SCHEMA",
    "TemplateGenerator",
    "validate_config",
    "create_default_config",
    
    # Configuration Manager
    "ConfigLoadError",
    "ConfigValidationError",
    "ConfigNotFoundError",
    "ConfigSource",
    "ConfigMetadata",
    "LoadedConfig",
    "SchemaValidator",
    "VerticalConfigLoader",
    "ConfigurationManager",
    "get_config_manager"
]


__version__ = "1.0.0"
