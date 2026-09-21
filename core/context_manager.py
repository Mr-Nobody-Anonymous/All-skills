"""
Core Context Manager.
Manages conversational entity context, dialog frame stacks, and slot memories across turns.
"""

from typing import Dict, List, Optional, Any
import time


class DialogFrame:
    """Represents a conversational frame."""
    def __init__(self, skill_name: str, context_type: str, data: Optional[Dict[str, Any]] = None, ttl_seconds: float = 120.0):
        self.skill_name = skill_name
        self.context_type = context_type
        self.data = data or {}
        self.created_at = time.time()
        self.expires_at = self.created_at + ttl_seconds

    def is_expired(self) -> bool:
        return time.time() > self.expires_at


class ContextManager:
    """Maintains active dialogue contexts for intent disambiguation."""

    def __init__(self):
        self._frames: List[DialogFrame] = []

    def set_context(self, skill_name: str, context_type: str, data: Optional[Dict[str, Any]] = None, ttl_seconds: float = 120.0) -> None:
        """Push a context frame onto the stack."""
        self._frames.append(DialogFrame(skill_name, context_type, data, ttl_seconds))

    def get_active_contexts(self) -> List[str]:
        """Return list of active, unexpired context identifiers."""
        self._prune()
        return [f.context_type for f in self._frames]

    def get_context_data(self, context_type: str) -> Optional[Dict[str, Any]]:
        """Retrieve data for the most recent active context frame."""
        self._prune()
        for f in reversed(self._frames):
            if f.context_type == context_type:
                return f.data
        return None

    def clear(self) -> None:
        """Clear all active contexts."""
        self._frames.clear()

    def _prune(self) -> None:
        """Remove expired frames."""
        self._frames = [f for f in self._frames if not f.is_expired()]

    def get_context(self, session_id: str = "default") -> Dict[str, Any]:
        """Retrieve session-level context dictionary."""
        data = self.get_context_data(session_id)
        return dict(data) if data else {}

    def update_context(self, session_id: str, data: Dict[str, Any]) -> None:
        """Update or set session-level context data."""
        current = self.get_context(session_id)
        current.update(data)
        self.set_context("session_manager", session_id, current)
