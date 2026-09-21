"""
Working Memory for Active Task State.
Stores intermediate goal state, active variables, and execution plans.
"""

from typing import Dict, Any, Optional

class WorkingMemory:
    def __init__(self):
        self.state: Dict[str, Any] = {}

    def set(self, key: str, value: Any):
        self.state[key] = value

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        return self.state.get(key, default)

    def delete(self, key: str):
        if key in self.state:
            del self.state[key]

    def snapshot(self) -> Dict[str, Any]:
        return dict(self.state)

    def reset(self):
        self.state.clear()
