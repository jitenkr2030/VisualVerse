"""
Logging utilities for VisualVerse engine.
Centralized logging configuration and utilities.
"""

import logging
import sys
from typing import Optional, Dict, Any
from datetime import datetime
import json
import structlog
from pathlib import Path


class VisualVerseFormatter(logging.Formatter):
    """Custom formatter for VisualVerse logs"""
    
    def __init__(self):
        super().__init__()
        self.service_name = "visualverse"
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record with structured data"""
        # Create base log entry
        log_entry = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "service": self.service_name,
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        # Add exception info if present
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        
        # Add extra fields
        if hasattr(record, 'user_id'):
            log_entry["user_id"] = record.user_id
        if hasattr(record, 'request_id'):
            log_entry["request_id"] = record.request_id
        if hasattr(record, 'session_id'):
            log_entry["session_id"] = record.session_id
        
        # Add custom fields
        for key, value in record.__dict__.items():
            if key not in ['name', 'msg', 'args', 'levelname', 'levelno', 
                          'pathname', 'filename', 'module', 'lineno', 'funcName',
                          'created', 'msecs', 'relativeCreated', 'thread',
                          'threadName', 'processName', 'process', 'getMessage',
                          'exc_info', 'exc_text', 'stack_info']:
                log_entry[key] = value
        
        return json.dumps(log_entry, default=str)


class ContextFilter(logging.Filter):
    """Filter to add context information to logs"""
    
    def __init__(self, service_name: str = "visualverse"):
        super().__init__()
        self.service_name = service_name
    
    def filter(self, record: logging.LogRecord) -> bool:
        """Add context to log record"""
        record.service = self.service_name
        return True


def setup_logging(
    level: str = "INFO",
    format_type: str = "json",
    output_file: Optional[str] = None,
    service_name: str = "visualverse"
) -> None:
    """
    Setup logging configuration for VisualVerse
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format_type: Format type ('json' or 'text')
        output_file: Optional file path for log output
        service_name: Name of the service for log context
    """
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, level.upper()))
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # Create formatter
    if format_type == "json":
        formatter = VisualVerseFormatter()
    else:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    # Create context filter
    context_filter = ContextFilter(service_name)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, level.upper()))
    console_handler.setFormatter(formatter)
    console_handler.addFilter(context_filter)
    root_logger.addHandler(console_handler)
    
    # File handler (if specified)
    if output_file:
        # Ensure log directory exists
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(output_file)
        file_handler.setLevel(getattr(logging, level.upper()))
        file_handler.setFormatter(formatter)
        file_handler.addFilter(context_filter)
        root_logger.addHandler(file_handler)
    
    # Configure structlog for structured logging
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


def get_logger(name: str) -> structlog.BoundLogger:
    """
    Get a structured logger instance
    
    Args:
        name: Logger name (typically __name__)
    
    Returns:
        Configured structlog logger
    """
    return structlog.get_logger(name)


class LoggingContext:
    """Context manager for adding logging context"""
    
    def __init__(self, **context):
        self.context = context
        self.logger = None
    
    def __enter__(self):
        self.logger = get_logger(self.__class__.__name__)
        # Bind context to logger
        for key, value in self.context.items():
            self.logger = self.logger.bind(**{key: value})
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # Unbind context
        if self.logger and self.context:
            self.logger = self.logger.unbind(*self.context.keys())


class PerformanceLogger:
    """Logger for performance metrics"""
    
    def __init__(self, operation: str, logger_name: str = "performance"):
        self.operation = operation
        self.logger = get_logger(logger_name)
        self.start_time = None
    
    def __enter__(self):
        self.start_time = datetime.now()
        self.logger.info("Operation started", operation=self.operation)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.start_time:
            duration = (datetime.now() - self.start_time).total_seconds()
            
            if exc_type:
                self.logger.error(
                    "Operation failed",
                    operation=self.operation,
                    duration=duration,
                    error=str(exc_val)
                )
            else:
                self.logger.info(
                    "Operation completed",
                    operation=self.operation,
                    duration=duration
                )


# Pre-configured loggers for common use cases
def get_animation_logger() -> structlog.BoundLogger:
    """Get logger for animation operations"""
    return get_logger("visualverse.animation")


def get_api_logger() -> structlog.BoundLogger:
    """Get logger for API operations"""
    return get_logger("visualverse.api")


def get_recommendation_logger() -> structlog.BoundLogger:
    """Get logger for recommendation operations"""
    return get_logger("visualverse.recommendation")


def get_database_logger() -> structlog.BoundLogger:
    """Get logger for database operations"""
    return get_logger("visualverse.database")


def get_auth_logger() -> structlog.BoundLogger:
    """Get logger for authentication operations"""
    return get_logger("visualverse.auth")


# Log level constants
LOG_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "WARN": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL
}


def get_log_level(level_str: str) -> int:
    """Convert log level string to logging constant"""
    return LOG_LEVELS.get(level_str.upper(), logging.INFO)


# Default configuration
DEFAULT_LOG_CONFIG = {
    "level": "INFO",
    "format": "json",
    "output_file": None,
    "service_name": "visualverse"
}


def configure_default_logging(**overrides):
    """Configure logging with default settings and overrides"""
    config = {**DEFAULT_LOG_CONFIG, **overrides}
    setup_logging(**config)


# Initialize default logging
configure_default_logging()
