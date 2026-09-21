"""
Event Log - Timestamped persistent event storage (append-only log).
Complements event_memory.py with a structured log format.
"""
from __future__ import annotations
import time
from typing import Any, Dict, List, Optional


class EventLog:
    """
    Append-only timestamped log of system events.
    Supports querying by time range, event type, and actor.
    """

    def __init__(self, max_size: int = 10000):
        self._log: List[Dict[str, Any]] = []
        self._max_size = max_size

    def append(self, event_type: str, data: Dict[str, Any], actor: str = "system") -> str:
        event_id = f"evt-{int(time.time() * 1000)}-{len(self._log)}"
        entry = {
            "id": event_id,
            "type": event_type,
            "actor": actor,
            "data": data,
            "timestamp": time.time(),
        }
        if len(self._log) >= self._max_size:
            self._log.pop(0)
        self._log.append(entry)
        return event_id

    def query(
        self,
        event_type: Optional[str] = None,
        actor: Optional[str] = None,
        since: Optional[float] = None,
        limit: int = 100,
    ) -> List[Dict]:
        results = self._log
        if event_type:
            results = [e for e in results if e["type"] == event_type]
        if actor:
            results = [e for e in results if e["actor"] == actor]
        if since:
            results = [e for e in results if e["timestamp"] >= since]
        return results[-limit:]

    def tail(self, n: int = 20) -> List[Dict]:
        return self._log[-n:]

    def size(self) -> int:
        return len(self._log)

    def clear(self) -> None:
        self._log.clear()
