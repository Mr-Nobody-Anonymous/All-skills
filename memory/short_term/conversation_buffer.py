"""
Conversation Buffer for All-Skills Memory.
Maintains recent turns, messages, and token-bounded conversation history.
"""

from typing import List, Dict, Any, Optional
import time

class ConversationBuffer:
    def __init__(self, max_turns: int = 20):
        self.max_turns = max_turns
        self.history: List[Dict[str, Any]] = []

    def add_turn(self, role: str, message: str, metadata: Optional[Dict[str, Any]] = None):
        turn = {
            "role": role,
            "message": message,
            "timestamp": time.time(),
            "metadata": metadata or {}
        }
        self.history.append(turn)
        if len(self.history) > self.max_turns:
            self.history.pop(0)

    def get_recent_history(self, count: Optional[int] = None) -> List[Dict[str, Any]]:
        if count is None:
            return list(self.history)
        return self.history[-count:]

    def clear(self):
        self.history.clear()
