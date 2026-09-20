"""
Core Metrics Collector.
Aggregates invocation latency, error counts, and operational throughput statistics.
"""

from typing import Dict, Any, List
import time
import threading
from collections import defaultdict


class MetricsCollector:
    """Collects runtime telemetry metrics."""

    def __init__(self):
        self._invocations = defaultdict(int)
        self._errors = defaultdict(int)
        self._latencies = defaultdict(list)
        self._lock = threading.Lock()

    def record_invocation(self, skill_name: str, latency_seconds: float, success: bool = True) -> None:
        with self._lock:
            self._invocations[skill_name] += 1
            if not success:
                self._errors[skill_name] += 1
            self._latencies[skill_name].append(latency_seconds)
            # Keep sliding window of last 100 samples
            if len(self._latencies[skill_name]) > 100:
                self._latencies[skill_name].pop(0)

    def get_summary(self) -> Dict[str, Any]:
        with self._lock:
            summary = {}
            for name, count in self._invocations.items():
                lats = self._latencies.get(name, [])
                avg_lat = sum(lats) / len(lats) if lats else 0.0
                summary[name] = {
                    "total_invocations": count,
                    "errors": self._errors[name],
                    "average_latency_ms": round(avg_lat * 1000, 2),
                }
            return summary
