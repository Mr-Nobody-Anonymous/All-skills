"""
Common Execution Decorators (Retry, Timing, Memoize).
"""

import time
import functools
from typing import Callable, Any

def retry(max_attempts: int = 3, delay_sec: float = 0.5):
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_err = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_err = e
                    time.sleep(delay_sec * (attempt + 1))
            raise last_err
        return wrapper
    return decorator

def timing(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = (time.perf_counter() - start) * 1000
        return result
    return wrapper

def memoize(func: Callable) -> Callable:
    cache = {}
    @functools.wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper
