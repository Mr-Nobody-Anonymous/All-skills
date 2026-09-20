"""
Core Rate Limiter.
Token bucket rate limiter to prevent API quota exhaustion and host overload.
"""

import time
import threading
from typing import Dict


class TokenBucket:
    def __init__(self, rate: float, capacity: float):
        self.rate = rate  # tokens added per second
        self.capacity = capacity
        self.tokens = capacity
        self.last_update = time.time()
        self.lock = threading.Lock()

    def consume(self, tokens: float = 1.0) -> bool:
        with self.lock:
            now = time.time()
            elapsed = now - self.last_update
            self.last_update = now
            self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)

            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False


class RateLimiter:
    """Manages token buckets for skills, endpoints, and callers."""

    def __init__(self, default_rate: float = 10.0, default_capacity: float = 20.0):
        self.default_rate = default_rate
        self.default_capacity = default_capacity
        self._buckets: Dict[str, TokenBucket] = {}
        self._lock = threading.Lock()

    def check(self, key: str, tokens: float = 1.0) -> bool:
        """Check and consume rate limit quota."""
        with self._lock:
            if key not in self._buckets:
                self._buckets[key] = TokenBucket(self.default_rate, self.default_capacity)
            bucket = self._buckets[key]
        return bucket.consume(tokens)
