"""
Core Event Bus.
Asynchronous message bus compatible with OpenVoiceOS / Mycroft messagebus format.
Supports emit, on, remove, and wait_for_response.
"""

from typing import Dict, List, Callable, Any, Optional
from collections import defaultdict
import threading
import logging
import uuid
import time

logger = logging.getLogger(__name__)


class Message:
    """Represents a messagebus event packet."""
    def __init__(self, msg_type: str, data: Optional[Dict[str, Any]] = None, context: Optional[Dict[str, Any]] = None):
        self.msg_type = msg_type
        self.data = data or {}
        self.context = context or {}
        if "source" not in self.context:
            self.context["source"] = "all-skills-core"

    def reply(self, msg_type: str, data: Optional[Dict[str, Any]] = None) -> "Message":
        """Generate response message inheriting correlation context."""
        ctx = dict(self.context)
        ctx["target"] = self.context.get("source")
        return Message(msg_type, data, ctx)


class EventBus:
    """In-memory event bus with pub/sub messaging."""

    def __init__(self):
        self._handlers: Dict[str, List[Callable[[Message], None]]] = defaultdict(list)
        self._lock = threading.Lock()

    def on(self, msg_type: str, handler: Callable[[Message], None]) -> None:
        """Subscribe to message event."""
        with self._lock:
            self._handlers[msg_type].append(handler)

    def remove(self, msg_type: str, handler: Callable[[Message], None]) -> None:
        """Unsubscribe handler."""
        with self._lock:
            if handler in self._handlers[msg_type]:
                self._handlers[msg_type].remove(handler)

    def emit(self, message: Message) -> None:
        """Dispatch message to all registered listeners."""
        with self._lock:
            listeners = list(self._handlers.get(message.msg_type, []))
            wildcard = list(self._handlers.get("*", []))

        for handler in listeners + wildcard:
            try:
                handler(message)
            except Exception as e:
                logger.error(f"Error handling message '{message.msg_type}': {e}", exc_info=True)
