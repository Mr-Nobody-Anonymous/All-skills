"""
Core Cache Manager.
In-memory and disk TTL cache for voice assistant queries and expensive computations.
"""

from typing import Dict, Any, Optional
import time
import threading


class CacheItem:
    def __init__(self, value: Any, ttl_seconds: float):
        self.value = value
        self.expires_at = time.time() + ttl_seconds if ttl_seconds > 0 else float("inf")

    def is_expired(self) -> bool:
        return time.time() > self.expires_at


class CacheManager:
    """Multi-tiered memory cache."""

    def __init__(self):
        self._store: Dict[str, CacheItem] = {}
        self._lock = threading.Lock()

    def set(self, key: str, value: Any, ttl_seconds: float = 300.0) -> None:
        """Store value in cache with TTL."""
        with self._lock:
            self._store[key] = CacheItem(value, ttl_seconds)

    def get(self, key: str) -> Optional[Any]:
        """Retrieve value if unexpired."""
        with self._lock:
            item = self._store.get(key)
            if item:
                if item.is_expired():
                    del self._store[key]
                    return None
                return item.value
            return None

    def delete(self, key: str) -> bool:
        with self._lock:
            return self._store.pop(key, None) is not None

    def clear(self) -> None:
        with self._lock:
            self._store.clear()
