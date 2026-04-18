"""Database models for URL Shortener"""

from sqlalchemy import Column, Integer, String, Text, DateTime, BigInteger
from sqlalchemy.sql import func
from datetime import datetime

from src.database import Base


class URLRecord(Base):
    """
    SQLAlchemy model for storing shortened URLs.
    
    Maps to 'urls' table in PostgreSQL.
    """
    __tablename__ = "urls"
    
    # Primary Key
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    
    # Short Code (unique identifier for the short URL)
    short_code = Column(String(10), unique=True, nullable=False, index=True)
    
    # Original Long URL
    long_url = Column(Text, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    expires_at = Column(DateTime, nullable=True, index=True)
    
    # Analytics
    click_count = Column(Integer, default=0, nullable=False)
    
    # Future: Multi-user support
    user_id = Column(String(255), nullable=True, index=True)
    
    def __repr__(self):
        """String representation of URLRecord"""
        # TODO: Implement this function
        # Hint: return f"<URLRecord(id={self.id}, short_code={self.short_code})>"
        pass
    
    def to_dict(self) -> dict:
        """
        Convert URLRecord to dictionary.
        
        Returns:
            dict: Record as dictionary
            
        Example:
            {
                'short_code': 'abc123',
                'long_url': 'https://example.com/...',
                'created_at': '2026-04-17T10:30:00',
                'click_count': 42
            }
        """
        # TODO: Implement this function
        pass
