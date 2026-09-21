"""
Recall Engine - Retrieves past events based on semantic or temporal similarity.
"""
from __future__ import annotations
import time
from typing import Any, Dict, List, Optional


class RecallEngine:
    """
    Retrieves relevant past events from episodic memory.
    Supports keyword-based, temporal, and context-based recall.
    """

    def __init__(self, event_log=None, event_memory=None):
        self._log = event_log
        self._memory = event_memory

    def recall_recent(self, n: int = 10) -> List[Dict]:
        """Return n most recent events."""
        if self._log:
            return self._log.tail(n)
        return []

    def recall_by_type(self, event_type: str, limit: int = 20) -> List[Dict]:
        """Return events of a specific type."""
        if self._log:
            return self._log.query(event_type=event_type, limit=limit)
        return []

    def recall_since(self, seconds_ago: float, limit: int = 50) -> List[Dict]:
        """Return events from the last N seconds."""
        cutoff = time.time() - seconds_ago
        if self._log:
            return self._log.query(since=cutoff, limit=limit)
        return []

    def recall_by_keyword(self, keyword: str, limit: int = 20) -> List[Dict]:
        """Return events whose data contains the keyword."""
        if not self._log:
            return []
        results = []
        kw = keyword.lower()
        for event in self._log.tail(1000):
            data_str = str(event.get("data", "")).lower()
            if kw in data_str or kw in event.get("type", "").lower():
                results.append(event)
        return results[-limit:]

    def recall_context(self, context: Dict[str, Any], limit: int = 10) -> List[Dict]:
        """Return events relevant to the current context (heuristic matching)."""
        clues = list(context.values())
        clue_str = " ".join(str(c) for c in clues).lower()
        words = [w for w in clue_str.split() if len(w) > 4]
        results = []
        seen = set()
        for word in words[:5]:
            for event in self.recall_by_keyword(word, limit=5):
                eid = event.get("id")
                if eid not in seen:
                    seen.add(eid)
                    results.append(event)
        return results[:limit]
