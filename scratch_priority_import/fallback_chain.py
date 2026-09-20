"""
Fallback Chain Manager for All-Skills.
Sequences and orchestrates fallback handlers when primary intent parsers fail.
"""

from typing import List, Callable, Optional, Dict, Any
import logging
import time

logger = logging.getLogger(__name__)


class FallbackHandler:
    """Represents a single fallback provider in the chain."""

    def __init__(self, name: str, priority: int, handler_fn: Callable[[str], Optional[str]], timeout_seconds: float = 3.0):
        self.name = name
        self.priority = priority  # Lower number = higher priority
        self.handler_fn = handler_fn
        self.timeout_seconds = timeout_seconds
        self.enabled = True

    def execute(self, utterance: str) -> Optional[str]:
        """Execute fallback handler with error handling."""
        if not self.enabled:
            return None
        try:
            return self.handler_fn(utterance)
        except Exception as e:
            logger.warning(f"Fallback handler '{self.name}' failed: {e}")
            return None


class FallbackChain:
    """Manages ordered sequence of fallback skills."""

    DEFAULT_ORDER = [
        "skill-fallback-wolfram",
        "skill-fallback-chatgpt",
        "skill-fallback-duckduckgo",
        "skill-fallback-wikipedia",
        "skill-fallback-web-search",
        "skill-fallback-unknown"
    ]

    def __init__(self):
        self._handlers: Dict[str, FallbackHandler] = {}

    def register_handler(
        self,
        name: str,
        priority: int,
        handler_fn: Callable[[str], Optional[str]],
        timeout_seconds: float = 3.0
    ) -> None:
        """Register a fallback handler function."""
        self._handlers[name] = FallbackHandler(name, priority, handler_fn, timeout_seconds)
        logger.info(f"Registered fallback handler '{name}' with priority {priority}")

    def remove_handler(self, name: str) -> None:
        """Remove a fallback handler."""
        self._handlers.pop(name, None)

    def get_ordered_handlers(self) -> List[FallbackHandler]:
        """Return enabled fallback handlers sorted by priority."""
        active = [h for h in self._handlers.values() if h.enabled]
        return sorted(active, key=lambda h: h.priority)

    def dispatch(self, utterance: str) -> Optional[Dict[str, Any]]:
        """
        Iterate through fallback chain until a handler returns a response.
        Returns dict with handler name, response, and elapsed time, or None if all failed.
        """
        ordered = self.get_ordered_handlers()
        for handler in ordered:
            start = time.time()
            res = handler.execute(utterance)
            elapsed = time.time() - start
            if res:
                return {
                    "handler": handler.name,
                    "response": res,
                    "elapsed_seconds": elapsed
                }
        return None
