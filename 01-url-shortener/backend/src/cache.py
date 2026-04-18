"""Redis cache wrapper for URL Shortener"""

import redis
from typing import Optional
import json


class CacheManager:
    """Manages Redis caching operations"""
    
    def __init__(self, redis_url: str):
        """
        Initialize Redis connection.
        
        Args:
            redis_url: Redis connection string (e.g., 'redis://localhost:6379/0')
        """
        self.client = redis.from_url(redis_url, decode_responses=True)
    
    async def get(self, key: str) -> Optional[str]:
        """
        Get value from cache.
        
        Args:
            key: Cache key (short code)
            
        Returns:
            Optional[str]: Cached value or None if not found
            
        Example:
            url = await cache.get('abc123')
            # Returns: 'https://example.com/...' or None
        """
        return self.client.get(key)
    
    async def set(self, key: str, value: str, ttl: int = 86400) -> bool:
        """
        Set value in cache with TTL.
        
        Args:
            key: Cache key (short code)
            value: Value to cache (long URL)
            ttl: Time-to-live in seconds (default: 24 hours)
            
        Returns:
            bool: True if successful
            
        Example:
            success = await cache.set('abc123', 'https://example.com/...', ttl=86400)
        """
        return self.client.set(key, value, ex=ttl)
    
    async def delete(self, key: str) -> bool:
        """
        Delete value from cache.
        
        Args:
            key: Cache key (short code)
            
        Returns:
            bool: True if key existed and was deleted
            
        Example:
            deleted = await cache.delete('abc123')
        """
        return self.client.delete(key) > 0
    
    async def exists(self, key: str) -> bool:
        """
        Check if key exists in cache.
        
        Args:
            key: Cache key (short code)
            
        Returns:
            bool: True if key exists
            
        Example:
            if await cache.exists('abc123'):
                # Key is in cache
        """
        return self.client.exists(key) > 0
    
    async def clear_all(self):
        """
        Clear all cache (use with caution!).
        
        Warning: This clears all Redis data, not just our cache.
        Only use for testing.
        """
        self.client.flushall()
    
    async def health_check(self) -> bool:
        """
        Check Redis connection health.
        
        Returns:
            bool: True if Redis is healthy
            
        Example:
            if await cache.health_check():
                # Redis is up
        """
        try:
            return self.client.ping()
        except redis.ConnectionError:
            return False


# Global cache instance
_cache_instance: Optional[CacheManager] = None


def get_cache(redis_url: str) -> CacheManager:
    """
    Get or create global cache instance.
    
    Args:
        redis_url: Redis connection string
        
    Returns:
        CacheManager: Configured cache manager
    """
    global _cache_instance
    if _cache_instance is None:
        _cache_instance = CacheManager(redis_url)
    return _cache_instance
