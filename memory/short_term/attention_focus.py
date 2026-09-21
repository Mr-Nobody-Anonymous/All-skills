"""
Attention Focus - Tracks what the system is currently "focused" on.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional


class AttentionFocus:
    """
    Manages the system's current focus of attention.
    Skills can set focus to guide follow-up intent routing.
    """

    def __init__(self, max_focus_stack: int = 5):
        self._focus: Optional[str] = None
        self._focus_data: Dict[str, Any] = {}
        self._stack: List[Dict] = []
        self._max_stack = max_focus_stack

    def set_focus(self, topic: str, data: Optional[Dict] = None) -> None:
        if self._focus:
            self._push_to_stack()
        self._focus = topic
        self._focus_data = data or {}

    def get_focus(self) -> Optional[str]:
        return self._focus

    def get_focus_data(self) -> Dict[str, Any]:
        return dict(self._focus_data)

    def clear_focus(self) -> None:
        self._focus = None
        self._focus_data = {}

    def pop_focus(self) -> Optional[str]:
        if self._stack:
            prev = self._stack.pop()
            self._focus = prev["topic"]
            self._focus_data = prev["data"]
            return self._focus
        self.clear_focus()
        return None

    def _push_to_stack(self):
        if len(self._stack) >= self._max_stack:
            self._stack.pop(0)
        self._stack.append({"topic": self._focus, "data": self._focus_data})

    def is_focused_on(self, topic: str) -> bool:
        return self._focus == topic if self._focus else False

    def state(self) -> Dict[str, Any]:
        return {
            "current_focus": self._focus,
            "focus_data": self._focus_data,
            "stack_depth": len(self._stack),
        }
