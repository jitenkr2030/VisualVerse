"""
Configuration settings for VisualVerse Content Metadata Service.
"""

import os
from typing import List, Optional
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Application settings"""
    
    # Server configuration
    HOST: str = Field(default="0.0.0.0", env="HOST")
    PORT: int = Field(default=8001, env="PORT")
    DEBUG: bool = Field(default=False, env="DEBUG")
    
    # CORS configuration
    ALLOWED_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:5000"],
        env="ALLOWED_ORIGINS"
    )
    
    # Database configuration
    NEO4J_URI: str = Field(default="bolt://localhost:7687", env="NEO4J_URI")
    NEO4J_USERNAME: str = Field(default="neo4j", env="NEO4J_USERNAME")
    NEO4J_PASSWORD: str = Field(default="password", env="NEO4J_PASSWORD")
    NEO4J_DATABASE: str = Field(default="visualverse", env="NEO4J_DATABASE")
    NEO4J_MAX_CONNECTIONS: int = Field(default=100, env="NEO4J_MAX_CONNECTIONS")
    NEO4J_CONNECTION_TIMEOUT: int = Field(default=30, env="NEO4J_CONNECTION_TIMEOUT")
    
    # Cache configuration
    REDIS_URL: Optional[str] = Field(default=None, env="REDIS_URL")
    CACHE_TTL: int = Field(default=3600, env="CACHE_TTL")  # 1 hour
    
    # Logging configuration
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    LOG_FORMAT: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        env="LOG_FORMAT"
    )
    
    # API configuration
    API_VERSION: str = Field(default="1.0.0", env="API_VERSION")
    API_TITLE: str = Field(default="VisualVerse Content Metadata API", env="API_TITLE")
    
    # Security configuration
    SECRET_KEY: str = Field(default="your-secret-key-change-in-production", env="SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    
    # Rate limiting
    RATE_LIMIT_PER_MINUTE: int = Field(default=100, env="RATE_LIMIT_PER_MINUTE")
    RATE_LIMIT_PER_HOUR: int = Field(default=1000, env="RATE_LIMIT_PER_HOUR")
    
    # Content limits
    MAX_CONCEPTS_PER_REQUEST: int = Field(default=50, env="MAX_CONCEPTS_PER_REQUEST")
    MAX_SEARCH_RESULTS: int = Field(default=100, env="MAX_SEARCH_RESULTS")
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
