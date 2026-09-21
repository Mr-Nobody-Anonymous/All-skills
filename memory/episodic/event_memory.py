"""
Episodic Event Memory.
Stores and queries time-stamped events, agent actions, user milestones, and system state transitions.
"""

from typing import List, Dict, Any, Optional
import time

class EventMemory:
    def __init__(self):
        self.events: List[Dict[str, Any]] = []

    def record_event(self, event_type: str, description: str, metadata: Optional[Dict[str, Any]] = None):
        entry = {
            "id": f"event_{len(self.events)+1}",
            "type": event_type,
            "description": description,
            "timestamp": time.time(),
            "metadata": metadata or {}
        }
        self.events.append(entry)
        return entry

    def query_events(self,
                     event_type: Optional[str] = None,
                     since: Optional[float] = None,
                     limit: int = 50) -> List[Dict[str, Any]]:
        results = self.events
        if event_type:
            results = [e for e in results if e["type"].lower() == event_type.lower()]
        if since is not None:
            results = [e for e in results if e["timestamp"] >= since]
        return results[-limit:]
