"""Configuration management for URL Shortener API"""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Database
    DATABASE_URL: str
    
    # Redis
    REDIS_URL: str
    
    # API
    API_PORT: int = 8000
    API_HOST: str = "0.0.0.0"
    DEBUG: bool = False
    
    # Base URL for short links
    BASE_URL: str = "http://localhost:8000"
    
    # Cache
    CACHE_TTL: int = 86400  # 24 hours
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """
    Get application settings (cached).
    
    Returns:
        Settings: Configured application settings
    """
    return Settings()
