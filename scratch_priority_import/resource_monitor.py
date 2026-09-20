"""
Resource Monitor for All-Skills.
Monitors memory and CPU metrics to throttle skill loading and prevent system thrashing.
"""

import os
import sys
import time
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False


class ResourceMonitor:
    """Tracks process and host resource consumption during skill imports."""

    def __init__(self, max_memory_mb: float = 2048.0, max_cpu_percent: float = 90.0):
        self.max_memory_mb = max_memory_mb
        self.max_cpu_percent = max_cpu_percent
        self._process = psutil.Process(os.getpid()) if HAS_PSUTIL else None

    def get_memory_usage_mb(self) -> float:
        """Get current process RSS memory in Megabytes."""
        if HAS_PSUTIL and self._process:
            try:
                return self._process.memory_info().rss / (1024 * 1024)
            except Exception:
                pass
        return 50.0  # Safe default estimate

    def get_system_memory_percent(self) -> float:
        """Get total system memory utilization percentage."""
        if HAS_PSUTIL:
            try:
                return psutil.virtual_memory().percent
            except Exception:
                pass
        return 30.0

    def get_cpu_percent(self) -> float:
        """Get process CPU utilization percentage."""
        if HAS_PSUTIL and self._process:
            try:
                return self._process.cpu_percent(interval=None)
            except Exception:
                pass
        return 5.0

    def can_allocate(self, estimated_mb: float = 25.0) -> bool:
        """Check if requested memory buffer can safely be allocated."""
        current = self.get_memory_usage_mb()
        if (current + estimated_mb) > self.max_memory_mb:
            logger.warning(
                f"Resource threshold reached: current {current:.1f}MB + req {estimated_mb:.1f}MB > limit {self.max_memory_mb:.1f}MB"
            )
            return False
        return True

    def get_status(self) -> Dict[str, Any]:
        """Return diagnostic dictionary of resource consumption."""
        return {
            "process_rss_mb": round(self.get_memory_usage_mb(), 2),
            "max_memory_limit_mb": self.max_memory_mb,
            "system_memory_percent": self.get_system_memory_percent(),
            "cpu_percent": self.get_cpu_percent(),
            "has_psutil": HAS_PSUTIL,
        }
