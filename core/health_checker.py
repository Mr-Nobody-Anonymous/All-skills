"""
Core Health Checker.
Liveness, readiness, and diagnostics probes for skills and background workers.
"""

from typing import Dict, Any, List
import time
import platform
import sys

from scratch_priority_import.resource_monitor import ResourceMonitor


class HealthChecker:
    """Evaluates health of the skill runtime and host environment."""

    def __init__(self):
        self.resource_monitor = ResourceMonitor()
        self.start_time = time.time()

    def get_health_status(self) -> Dict[str, Any]:
        """Produce comprehensive diagnostic report."""
        uptime = time.time() - self.start_time
        res = self.resource_monitor.get_status()

        return {
            "status": "healthy",
            "uptime_seconds": round(uptime, 2),
            "platform": platform.system(),
            "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            "memory": res,
        }
