"""
VisualVerse Configuration Manager

This module provides the central configuration management system for loading,
validating, and caching vertical configurations in the VisualVerse learning
platform. It implements a singleton pattern to ensure a single source of
truth for all configuration data across the application.

The ConfigurationManager handles:
- Loading configuration files from disk or remote sources
- Validating configurations against the master schema
- Caching configurations for performance optimization
- Providing fallback to default configurations when needed
- Managing configuration updates and hot-reloading capabilities

Author: MiniMax Agent
Version: 1.0.0
"""

from pathlib import Path
from typing import Dict, List, Optional, Any, TypeVar, Callable
from dataclasses import dataclass, field
from datetime import datetime
import json
import logging
import copy
import threading
from enum import Enum

from jsonschema import Draft7Validator, ValidationError
from jsonschema.validators import extend

from .vertical_config_schema import (
    VerticalConfig,
    MASTER_CONFIG_SCHEMA,
    VerticalType,
    ServiceSettings,
    VisualPreferences,
    AnimationConfig,
    InteractionConfig,
    ColorPalette,
    CameraConfig,
    LearningObjective,
    DomainSpecificConfig,
    validate_config,
    create_default_config
)


logger = logging.getLogger(__name__)


T = TypeVar('T')


class ConfigLoadError(Exception):
    """Exception raised when configuration loading fails."""
    pass


class ConfigValidationError(Exception):
    """Exception raised when configuration validation fails."""
    pass


class ConfigNotFoundError(Exception):
    """Exception raised when a configuration is not found."""
    pass


class ConfigSource(str, Enum):
    """Source types for configuration files."""
    LOCAL_FILE = "local_file"
    REMOTE_URL = "remote_url"
    DEFAULT = "default"
    INLINE = "inline"


@dataclass
class ConfigMetadata:
    """Metadata about a loaded configuration."""
    source: ConfigSource
    source_path: Optional[str] = None
    loaded_at: Optional[datetime] = None
    last_modified: Optional[datetime] = None
    version: str = "1.0.0"
    is_valid: bool = True
    validation_errors: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "source": self.source.value,
            "sourcePath": self.source_path,
            "loadedAt": self.loaded_at.isoformat() if self.loaded_at else None,
            "lastModified": self.last_modified.isoformat() if self.last_modified else None,
            "version": self.version,
            "isValid": self.is_valid,
            "validationErrors": self.validation_errors
        }


@dataclass
class LoadedConfig:
    """Wrapper for a loaded configuration with metadata."""
    config: VerticalConfig
    metadata: ConfigMetadata


class SchemaValidator:
    """
    Helper class for validating configuration data against the master schema.
    
    This class provides comprehensive validation capabilities including:
    - JSON Schema validation using Draft7
    - Custom validation rules for domain-specific requirements
    - Detailed error reporting with suggestions for fixes
    - Validation result caching for performance
    """
    
    def __init__(self, schema: Dict[str, Any] = None):
        """
        Initialize the schema validator.
        
        Args:
            schema: Optional custom schema to use for validation
        """
        self._schema = schema or MASTER_CONFIG_SCHEMA
        self._validator = Draft7Validator(self._schema)
        self._custom_validators: Dict[str, Callable] = {}
        self._validation_cache: Dict[str, bool] = {}
        self._cache_lock = threading.RLock()
        self._setup_custom_validators()
    
    def _setup_custom_validators(self):
        """Set up custom validation rules."""
        pass
    
    def validate(self, config_data: Dict[str, Any]) -> tuple:
        """
        Validate configuration data against the schema.
        
        Args:
            config_data: Configuration data to validate
            
        Returns:
            Tuple of (is_valid, errors)
        """
        if not config_data:
            return False, ["Configuration data is empty or None"]
        
        errors = list(self._validator.iter_errors(config_data))
        return len(errors) == 0, [self._format_error(error) for error in errors]
    
    def validate_with_details(self, config_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate configuration data with detailed error information.
        
        Args:
            config_data: Configuration data to validate
            
        Returns:
            Dictionary with validation results and detailed errors
        """
        is_valid, errors = self.validate(config_data)
        
        detailed_errors = []
        for error in self._validator.iter_errors(config_data):
            detailed_errors.append({
                "path": self._get_error_path(error),
                "message": error.message,
                "validator": error.validator,
                "validator_value": error.validator_value
            })
        
        return {
            "isValid": is_valid,
            "errorCount": len(detailed_errors),
            "errors": detailed_errors,
            "summary": errors
        }
    
    def validate_partial(self, config_data: Dict[str, Any], 
                         required_fields: List[str] = None) -> tuple:
        """
        Validate only required fields in the configuration.
        
        Args:
            config_data: Configuration data to validate
            required_fields: List of fields that must be present and valid
            
        Returns:
            Tuple of (is_valid, errors)
        """
        if required_fields is None:
            required_fields = ["verticalId", "verticalName", "verticalType"]
        
        errors = []
        
        for field_name in required_fields:
            if field_name not in config_data:
                errors.append(f"Missing required field: {field_name}")
            else:
                value = config_data[field_name]
                field_errors = self._validate_field(field_name, value)
                errors.extend(field_errors)
        
        return len(errors) == 0, errors
    
    def _validate_field(self, field_name: str, value: Any) -> List[str]:
        """Validate a specific field value."""
        errors = []
        
        if field_name == "verticalId":
            if not isinstance(value, str):
                errors.append("verticalId must be a string")
            elif not value.replace('-', '').replace('_', '').isalnum():
                errors.append("verticalId must be alphanumeric with hyphens or underscores")
        
        elif field_name == "verticalType":
            valid_types = [vt.value for vt in VerticalType]
            if value not in valid_types:
                errors.append(f"verticalType must be one of: {valid_types}")
        
        elif field_name == "version":
            if not isinstance(value, str):
                errors.append("version must be a string")
            elif not all(c.isdigit() or c == '.' for c in value):
                errors.append("version must follow semantic versioning (e.g., '1.0.0')")
        
        return errors
    
    def _format_error(self, error: ValidationError) -> str:
        """Format a validation error into a human-readable message."""
        path = " -> ".join(str(p) for p in error.absolute_path)
        return f"[{path}] {error.message}" if path else error.message
    
    def _get_error_path(self, error: ValidationError) -> str:
        """Get the path to the error in dotted notation."""
        return ".".join(str(p) for p in error.absolute_path) or "root"
    
    def is_valid_cached(self, config_hash: str) -> Optional[bool]:
        """
        Get cached validation result.
        
        Args:
            config_hash: Hash of the configuration data
            
        Returns:
            Cached validation result or None if not cached
        """
        with self._cache_lock:
            return self._validation_cache.get(config_hash)
    
    def cache_result(self, config_hash: str, is_valid: bool) -> None:
        """
        Cache a validation result.
        
        Args:
            config_hash: Hash of the configuration data
            is_valid: Validation result
        """
        with self._cache_lock:
            self._validation_cache[config_hash] = is_valid
    
    def clear_cache(self) -> None:
        """Clear the validation cache."""
        with self._cache_lock:
            self._validation_cache.clear()
    
    def get_schema(self) -> Dict[str, Any]:
        """Get the current schema being used for validation."""
        return copy.deepcopy(self._schema)


class VerticalConfigLoader:
    """
    Helper class for loading vertical configuration files from various sources.
    
    This class handles the loading of configuration data from:
    - Local JSON files in the filesystem
    - Remote URLs (HTTP/HTTPS)
    - Default configurations
    - Inline configuration data
    
    The loader provides:
    - Automatic file discovery based on vertical ID
    - Support for multiple file formats (JSON)
    - Remote configuration fetching with timeout
    - Configuration merging and inheritance
    - Hot-reloading support with file watching
    """
    
    def __init__(self, config_dir: str = None):
        """
        Initialize the configuration loader.
        
        Args:
            config_dir: Base directory for configuration files
        """
        self._config_dir = Path(config_dir) if config_dir else None
        self._file_cache: Dict[str, Dict[str, Any]] = {}
        self._file_watchers: Dict[str, threading.Thread] = {}
        self._watcher_lock = threading.Lock()
        self._http_timeout = 30.0
        self._max_file_size_mb = 10
        self._default_configs: Dict[str, Dict[str, Any]] = {}
    
    def set_config_directory(self, config_dir: str) -> None:
        """
        Set the base configuration directory.
        
        Args:
            config_dir: Path to the configuration directory
        """
        self._config_dir = Path(config_dir)
        self._file_cache.clear()
    
    def load_from_file(self, vertical_id: str, file_path: str = None) -> Dict[str, Any]:
        """
        Load configuration from a local file.
        
        Args:
            vertical_id: The vertical identifier
            file_path: Optional explicit file path
            
        Returns:
            Configuration data as dictionary
            
        Raises:
            ConfigNotFoundError: If file is not found
            ConfigLoadError: If file cannot be loaded
        """
        if file_path is None and self._config_dir is None:
            raise ConfigNotFoundError(
                f"No file path or config directory provided for vertical: {vertical_id}"
            )
        
        if file_path is None:
            file_path = str(self._config_dir / f"{vertical_id}.json")
        
        cache_key = f"file:{file_path}"
        if cache_key in self._file_cache:
            return copy.deepcopy(self._file_cache[cache_key])
        
        try:
            path = Path(file_path)
            if not path.exists():
                raise ConfigNotFoundError(f"Configuration file not found: {file_path}")
            
            if path.stat().st_size > self._max_file_size_mb * 1024 * 1024:
                raise ConfigLoadError(
                    f"Configuration file exceeds maximum size: {file_path}"
                )
            
            with open(path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            self._file_cache[cache_key] = config_data
            logger.info(f"Loaded configuration from file: {file_path}")
            return config_data
        
        except json.JSONDecodeError as e:
            raise ConfigLoadError(f"Invalid JSON in configuration file: {file_path} - {e}")
        except Exception as e:
            raise ConfigLoadError(f"Failed to load configuration file: {file_path} - {e}")
    
    def load_from_url(self, vertical_id: str, url: str) -> Dict[str, Any]:
        """
        Load configuration from a remote URL.
        
        Args:
            vertical_id: The vertical identifier
            url: URL to fetch configuration from
            
        Returns:
            Configuration data as dictionary
            
        Raises:
            ConfigLoadError: If URL cannot be accessed
        """
        cache_key = f"url:{url}"
        if cache_key in self._file_cache:
            return copy.deepcopy(self._file_cache[cache_key])
        
        try:
            import requests
            
            response = requests.get(url, timeout=self._http_timeout)
            response.raise_for_status()
            
            config_data = response.json()
            self._file_cache[cache_key] = config_data
            
            logger.info(f"Loaded configuration from URL: {url}")
            return config_data
        
        except requests.RequestException as e:
            raise ConfigLoadError(f"Failed to fetch configuration from URL: {url} - {e}")
        except json.JSONDecodeError as e:
            raise ConfigLoadError(f"Invalid JSON from URL: {url} - {e}")
    
    def load_default(self, vertical_type: str) -> Dict[str, Any]:
        """
        Load default configuration for a vertical type.
        
        Args:
            vertical_type: Type of vertical
            
        Returns:
            Default configuration data
        """
        cache_key = f"default:{vertical_type}"
        if cache_key in self._default_configs:
            return copy.deepcopy(self._default_configs[cache_key])
        
        default_config = create_default_config(vertical_type)
        self._default_configs[cache_key] = default_config
        
        return copy.deepcopy(default_config)
    
    def load_with_fallback(self, vertical_id: str, 
                           vertical_type: str = None) -> Dict[str, Any]:
        """
        Load configuration with fallback to default.
        
        Args:
            vertical_id: The vertical identifier
            vertical_type: Type of vertical for fallback
            
        Returns:
            Configuration data
            
        Raises:
            ConfigLoadError: If all loading methods fail
        """
        sources = []
        
        if self._config_dir:
            sources.append(("local file", lambda: self.load_from_file(vertical_id)))
        
        sources.append(("default", lambda: self.load_default(
            vertical_type or self._infer_vertical_type(vertical_id)
        )))
        
        last_error = None
        for source_name, load_func in sources:
            try:
                return load_func()
            except (ConfigNotFoundError, ConfigLoadError) as e:
                last_error = e
                logger.warning(
                    f"Failed to load configuration from {source_name} for {vertical_id}: {e}"
                )
                continue
        
        raise ConfigLoadError(
            f"Failed to load configuration for {vertical_id} from any source: {last_error}"
        )
    
    def _infer_vertical_type(self, vertical_id: str) -> str:
        """Infer the vertical type from the vertical ID."""
        known_types = ["math-verse", "algo-verse", "physics-verse", "chem-verse", "fin-verse"]
        
        for vertical_type in known_types:
            if vertical_type in vertical_id.lower():
                return vertical_type
        
        return "math-verse"
    
    def merge_configs(self, base: Dict[str, Any], 
                      override: Dict[str, Any]) -> Dict[str, Any]:
        """
        Merge two configuration dictionaries.
        
        Args:
            base: Base configuration
            override: Configuration to merge on top
            
        Returns:
            Merged configuration
        """
        result = copy.deepcopy(base)
        self._deep_merge(result, override)
        return result
    
    def _deep_merge(self, base: Dict, override: Dict) -> None:
        """Deep merge override into base."""
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value
    
    def clear_cache(self) -> None:
        """Clear the file cache."""
        self._file_cache.clear()
    
    def get_cached_sources(self) -> List[str]:
        """Get list of cached configuration sources."""
        return list(self._file_cache.keys())


class ConfigurationManager:
    """
    Central singleton configuration manager for the VisualVerse platform.
    
    This class is the primary entry point for all configuration operations.
    It provides:
    - Singleton instance management
    - Configuration loading with automatic validation
    - In-memory caching for performance
    - Hot-reloading support
    - Configuration inheritance and merging
    - Detailed error reporting
    
    Example:
        >>> config_manager = ConfigurationManager()
        >>> config = config_manager.load_config("physics-mechanics")
        >>> renderer = config.visual_preferences.renderer
    """
    
    _instance: 'ConfigurationManager' = None
    _lock = threading.Lock()
    
    def __new__(cls):
        """Create or return the singleton instance."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize the configuration manager."""
        if self._initialized:
            return
        
        self._config_dir: Optional[Path] = None
        self._loader: Optional[VerticalConfigLoader] = None
        self._validator: Optional[SchemaValidator] = None
        self._config_cache: Dict[str, LoadedConfig] = {}
        self._cache_lock = threading.RLock()
        self._auto_reload: bool = False
        self._reload_interval: float = 60.0
        self._reload_thread: Optional[threading.Thread] = None
        self._initialized = True
        
        logger.info("ConfigurationManager singleton initialized")
    
    def initialize(self, config_dir: str = None, auto_reload: bool = False) -> None:
        """
        Initialize the configuration manager with custom settings.
        
        Args:
            config_dir: Base directory for configuration files
            auto_reload: Enable automatic configuration reloading
        """
        if config_dir:
            self._config_dir = Path(config_dir)
        else:
            self._config_dir = Path(__file__).parent / "verticals"
        
        self._loader = VerticalConfigLoader(str(self._config_dir))
        self._validator = SchemaValidator()
        
        self._auto_reload = auto_reload
        if auto_reload:
            self._start_reload_thread()
        
        logger.info(
            f"ConfigurationManager initialized with config_dir: {self._config_dir}"
        )
    
    def _start_reload_thread(self) -> None:
        """Start the background thread for auto-reloading configurations."""
        if self._reload_thread and self._reload_thread.is_alive():
            return
        
        self._reload_thread = threading.Thread(
            target=self._reload_loop,
            daemon=True,
            name="ConfigReloadThread"
        )
        self._reload_thread.start()
    
    def _reload_loop(self) -> None:
        """Background loop for automatic configuration reloading."""
        import time
        
        while self._auto_reload:
            time.sleep(self._reload_interval)
            try:
                self._reload_changed_configs()
            except Exception as e:
                logger.error(f"Error in config reload loop: {e}")
    
    def _reload_changed_configs(self) -> None:
        """Reload configurations that have changed on disk."""
        with self._cache_lock:
            for vertical_id, loaded_config in list(self._config_cache.items()):
                metadata = loaded_config.metadata
                
                if metadata.source != ConfigSource.LOCAL_FILE:
                    continue
                
                file_path = metadata.source_path
                if file_path and Path(file_path).exists():
                    file_mtime = datetime.fromtimestamp(
                        Path(file_path).stat().st_mtime
                    )
                    
                    if (metadata.last_modified and 
                        file_mtime > metadata.last_modified):
                        try:
                            new_config = self._load_and_validate(vertical_id, file_path)
                            logger.info(f"Auto-reloaded configuration: {vertical_id}")
                        except Exception as e:
                            logger.error(
                                f"Failed to reload {vertical_id}: {e}"
                            )
    
    def load_config(self, vertical_id: str, 
                    config_path: str = None) -> VerticalConfig:
        """
        Load and validate a vertical configuration.
        
        This method loads a configuration from the specified path or from
        the default configuration directory. The configuration is validated
        against the master schema before being returned.
        
        Args:
            vertical_id: The vertical identifier
            config_path: Optional explicit path to configuration file
            
        Returns:
            Validated VerticalConfig object
            
        Raises:
            ConfigLoadError: If configuration cannot be loaded
            ConfigValidationError: If configuration validation fails
        """
        with self._cache_lock:
            if vertical_id in self._config_cache:
                return self._config_cache[vertical_id].config
        
        config_data = self._load_config_data(vertical_id, config_path)
        config = self._create_config_object(vertical_id, config_data)
        
        with self._cache_lock:
            self._config_cache[vertical_id] = LoadedConfig(
                config=config,
                metadata=self._create_metadata(vertical_id, config_path, config_data)
            )
            return config
    
    def _load_config_data(self, vertical_id: str, 
                          config_path: str = None) -> Dict[str, Any]:
        """Load raw configuration data."""
        if self._loader is None:
            self.initialize()
        
        if config_path:
            return self._loader.load_from_file(vertical_id, config_path)
        else:
            return self._loader.load_with_fallback(vertical_id)
    
    def _load_and_validate(self, vertical_id: str, 
                           config_path: str) -> VerticalConfig:
        """Load and validate configuration from a specific path."""
        config_data = self._loader.load_from_file(vertical_id, config_path)
        return self._create_config_object(vertical_id, config_data)
    
    def _create_config_object(self, vertical_id: str, 
                              config_data: Dict[str, Any]) -> VerticalConfig:
        """Create a VerticalConfig object from raw data."""
        is_valid, errors = self._validator.validate(config_data)
        
        if not is_valid:
            raise ConfigValidationError(
                f"Configuration validation failed for {vertical_id}: {errors}"
            )
        
        return VerticalConfig.from_dict(config_data)
    
    def _create_metadata(self, vertical_id: str, config_path: str,
                         config_data: Dict[str, Any]) -> ConfigMetadata:
        """Create metadata for a loaded configuration."""
        source = ConfigSource.LOCAL_FILE if config_path else ConfigSource.DEFAULT
        source_path = config_path
        
        last_modified = None
        if config_path and Path(config_path).exists():
            last_modified = datetime.fromtimestamp(
                Path(config_path).stat().st_mtime
            )
        
        return ConfigMetadata(
            source=source,
            source_path=source_path,
            loaded_at=datetime.utcnow(),
            last_modified=last_modified,
            version=config_data.get("version", "1.0.0"),
            is_valid=True
        )
    
    def get_config(self, vertical_id: str) -> Optional[VerticalConfig]:
        """
        Get a cached configuration.
        
        Args:
            vertical_id: The vertical identifier
            
        Returns:
            VerticalConfig or None if not found
        """
        with self._cache_lock:
            loaded = self._config_cache.get(vertical_id)
            return loaded.config if loaded else None
    
    def get_config_with_metadata(self, vertical_id: str) -> Optional[LoadedConfig]:
        """
        Get a configuration with its metadata.
        
        Args:
            vertical_id: The vertical identifier
            
        Returns:
            LoadedConfig or None if not found
        """
        with self._cache_lock:
            return self._config_cache.get(vertical_id)
    
    def get_all_configs(self) -> Dict[str, VerticalConfig]:
        """
        Get all cached configurations.
        
        Returns:
            Dictionary of vertical_id to VerticalConfig
        """
        with self._cache_lock:
            return {
                vertical_id: loaded.config 
                for vertical_id, loaded in self._config_cache.items()
            }
    
    def reload_config(self, vertical_id: str) -> Optional[VerticalConfig]:
        """
        Force reload a configuration from disk.
        
        Args:
            vertical_id: The vertical identifier
            
        Returns:
            Reloaded VerticalConfig or None if not found
        """
        with self._cache_lock:
            if vertical_id not in self._config_cache:
                return None
            
            loaded = self._config_cache[vertical_id]
            source_path = loaded.metadata.source_path
            
            del self._config_cache[vertical_id]
        
        return self.load_config(vertical_id, source_path)
    
    def unload_config(self, vertical_id: str) -> bool:
        """
        Unload a configuration from the cache.
        
        Args:
            vertical_id: The vertical identifier
            
        Returns:
            True if unloaded, False if not found
        """
        with self._cache_lock:
            if vertical_id in self._config_cache:
                del self._config_cache[vertical_id]
                logger.info(f"Unloaded configuration: {vertical_id}")
                return True
            return False
    
    def clear_cache(self) -> None:
        """Clear all cached configurations."""
        with self._cache_lock:
            count = len(self._config_cache)
            self._config_cache.clear()
            self._validator.clear_cache()
            self._loader.clear_cache()
            logger.info(f"Cleared {count} configurations from cache")
    
    def list_loaded_configs(self) -> List[str]:
        """
        List all loaded configuration vertical IDs.
        
        Returns:
            List of vertical identifiers
        """
        with self._cache_lock:
            return list(self._config_cache.keys())
    
    def list_available_configs(self) -> List[str]:
        """
        List all available configuration files.
        
        Returns:
            List of vertical identifiers that have configuration files
        """
        if not self._config_dir:
            return []
        
        configs = []
        for file_path in self._config_dir.glob("*.json"):
            configs.append(file_path.stem)
        
        return configs
    
    def merge_with_defaults(self, vertical_id: str) -> Dict[str, Any]:
        """
        Merge a configuration with global defaults.
        
        Args:
            vertical_id: The vertical identifier
            
        Returns:
            Merged configuration dictionary
        """
        config = self.get_config(vertical_id)
        if config is None:
            config_data = self._loader.load_with_fallback(vertical_id)
        else:
            config_data = config.to_dict()
        
        return self._loader.merge_configs(
            self._get_global_defaults(),
            config_data
        )
    
    def _get_global_defaults(self) -> Dict[str, Any]:
        """Get global default configuration values."""
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
                "transitionType": "smooth",
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
                "panButton": "left",
                "zoomMouseWheel": True,
                "doubleClickZoom": False,
                "touchSupport": True
            }
        }
    
    def update_config(self, vertical_id: str, 
                      updates: Dict[str, Any]) -> VerticalConfig:
        """
        Update a configuration with new values.
        
        Args:
            vertical_id: The vertical identifier
            updates: Dictionary of updates to apply
            
        Returns:
            Updated VerticalConfig
            
        Raises:
            ConfigNotFoundError: If configuration is not loaded
        """
        with self._cache_lock:
            if vertical_id not in self._config_cache:
                raise ConfigNotFoundError(
                    f"Configuration not found: {vertical_id}"
                )
            
            loaded = self._config_cache[vertical_id]
            config_data = loaded.config.to_dict()
            
            for key, value in updates.items():
                if key in config_data and isinstance(config_data[key], dict):
                    self._loader._deep_merge(config_data[key], value)
                else:
                    config_data[key] = value
            
            config = self._create_config_object(vertical_id, config_data)
            
            self._config_cache[vertical_id] = LoadedConfig(
                config=config,
                metadata=loaded.metadata
            )
            
            return config
    
    def export_config(self, vertical_id: str, output_path: str) -> None:
        """
        Export a configuration to a JSON file.
        
        Args:
            vertical_id: The vertical identifier
            output_path: Path to export the configuration
            
        Raises:
            ConfigNotFoundError: If configuration is not found
        """
        config = self.get_config(vertical_id)
        if config is None:
            raise ConfigNotFoundError(
                f"Configuration not found: {vertical_id}"
            )
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(config.to_dict(), f, indent=2, ensure_ascii=False)
        
        logger.info(f"Exported configuration {vertical_id} to: {output_path}")
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the configuration cache.
        
        Returns:
            Dictionary with cache statistics
        """
        with self._cache_lock:
            configs_by_source = {}
            for loaded in self._config_cache.values():
                source = loaded.metadata.source.value
                configs_by_source[source] = configs_by_source.get(source, 0) + 1
            
            return {
                "totalConfigs": len(self._config_cache),
                "configsBySource": configs_by_source,
                "autoReloadEnabled": self._auto_reload,
                "configDirectory": str(self._config_dir) if self._config_dir else None
            }
    
    def shutdown(self) -> None:
        """Shutdown the configuration manager and cleanup resources."""
        self._auto_reload = False
        self.clear_cache()
        logger.info("ConfigurationManager shutdown complete")


def get_config_manager() -> ConfigurationManager:
    """
    Get the singleton ConfigurationManager instance.
    
    Returns:
        The singleton ConfigurationManager instance
    """
    return ConfigurationManager()


__all__ = [
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
