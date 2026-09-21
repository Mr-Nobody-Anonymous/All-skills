"""
Knowledge Graph - Structured factual memory as a typed triple store.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional, Tuple


class KnowledgeGraph:
    """
    Stores (subject, predicate, object) triples for structured reasoning.
    Provides lookup, update, and traversal operations.
    """

    def __init__(self):
        self._triples: List[Tuple[str, str, Any]] = []
        self._index: Dict[str, List[int]] = {}

    def assert_fact(self, subject: str, predicate: str, obj: Any) -> None:
        idx = len(self._triples)
        self._triples.append((subject, predicate, obj))
        self._index.setdefault(subject.lower(), []).append(idx)
        self._index.setdefault(predicate.lower(), []).append(idx)

    def query(self, subject: Optional[str] = None, predicate: Optional[str] = None) -> List[Tuple]:
        results = []
        for s, p, o in self._triples:
            if subject and s.lower() != subject.lower():
                continue
            if predicate and p.lower() != predicate.lower():
                continue
            results.append((s, p, o))
        return results

    def retract(self, subject: str, predicate: str) -> int:
        before = len(self._triples)
        self._triples = [
            (s, p, o) for s, p, o in self._triples
            if not (s.lower() == subject.lower() and p.lower() == predicate.lower())
        ]
        self._rebuild_index()
        return before - len(self._triples)

    def _rebuild_index(self):
        self._index = {}
        for i, (s, p, _) in enumerate(self._triples):
            self._index.setdefault(s.lower(), []).append(i)
            self._index.setdefault(p.lower(), []).append(i)

    def size(self) -> int:
        return len(self._triples)

    def entities(self) -> List[str]:
        return list({s for s, _, _ in self._triples})
