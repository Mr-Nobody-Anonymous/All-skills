"""
Priority Queue Engine for All-Skills.
Provides thread-safe, min-heap priority queueing for skill loading and intent scheduling.
"""

import heapq
import threading
from dataclasses import dataclass, field
from typing import Any, Optional, List, Tuple
import itertools

from .priority_levels import PriorityTier


@dataclass(order=True)
class PrioritizedItem:
    priority: int
    count: int
    item: Any = field(compare=False)


class SkillPriorityQueue:
    """Thread-safe priority queue for ordering skill initialization and tasks."""

    def __init__(self):
        self._heap: List[PrioritizedItem] = []
        self._counter = itertools.count()
        self._lock = threading.Lock()

    def put(self, item: Any, priority: int = 40, tier: Optional[PriorityTier] = None) -> None:
        """
        Add an item to the priority queue.
        Lower priority value = dequeued earlier.
        If tier is supplied, it scales the priority value.
        """
        if tier is not None:
            effective_priority = tier.value * 10 + (priority % 10)
        else:
            effective_priority = priority

        with self._lock:
            count = next(self._counter)
            heapq.heappush(self._heap, PrioritizedItem(effective_priority, count, item))

    def get(self) -> Optional[Any]:
        """Pop and return the highest-priority item. Returns None if empty."""
        with self._lock:
            if not self._heap:
                return None
            return heapq.heappop(self._heap).item

    def peek(self) -> Optional[Any]:
        """View the highest-priority item without removing it."""
        with self._lock:
            if not self._heap:
                return None
            return self._heap[0].item

    def qsize(self) -> int:
        """Return number of items in queue."""
        with self._lock:
            return len(self._heap)

    def is_empty(self) -> bool:
        """Check if queue is empty."""
        return self.qsize() == 0

    def clear(self) -> None:
        """Remove all items from queue."""
        with self._lock:
            self._heap.clear()
