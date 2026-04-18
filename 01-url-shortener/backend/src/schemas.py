"""Pydantic schemas for request/response validation"""

from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional


class ShortenRequest(BaseModel):
    """
    Request schema for POST /api/shorten endpoint.
    
    Example:
        {
            "long_url": "https://www.example.com/very/long/path"
        }
    """
    long_url: str = Field(..., description="Original URL to shorten", min_length=1, max_length=2048)
    
    @field_validator('long_url')
    @classmethod
    def validate_url(cls, v):
        """Validate URL format - must start with http:// or https://"""
        if not v or not isinstance(v, str):
            raise ValueError("URL must be a non-empty string")
        if not (v.startswith('http://') or v.startswith('https://')):
            raise ValueError("URL must start with http:// or https://")
        return v


class ShortenResponse(BaseModel):
    """
    Response schema for POST /api/shorten endpoint.
    
    Example:
        {
            "short_code": "abc123",
            "short_url": "http://short.ly/abc123",
            "created_at": "2026-04-17T10:30:00"
        }
    """
    short_code: str = Field(..., description="Generated short code")
    short_url: str = Field(..., description="Full short URL")
    created_at: datetime = Field(..., description="Timestamp when URL was created")


class StatsResponse(BaseModel):
    """
    Response schema for GET /api/stats/:short_code endpoint.
    
    Example:
        {
            "short_code": "abc123",
            "long_url": "https://www.example.com/very/long/path",
            "created_at": "2026-04-17T10:30:00",
            "click_count": 42
        }
    """
    short_code: str = Field(..., description="Short code")
    long_url: str = Field(..., description="Original long URL")
    created_at: datetime = Field(..., description="Timestamp when URL was created")
    click_count: int = Field(..., description="Number of times URL was accessed")


class ErrorResponse(BaseModel):
    """
    Generic error response schema.
    
    Example:
        {
            "error": "Invalid URL format",
            "details": "URL must start with http:// or https://"
        }
    """
    error: str = Field(..., description="Error message")
    details: Optional[str] = Field(None, description="Additional error details")
