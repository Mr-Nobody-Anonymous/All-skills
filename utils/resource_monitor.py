"""
Hardware Resource Monitoring Utility (CPU, RAM, GPU).
"""

import os
import shutil
from typing import Dict, Any

class SystemResourceMonitor:
    def __init__(self):
        pass

    def get_stats(self) -> Dict[str, Any]:
        total, used, free = shutil.disk_usage(".")
        return {
            "disk_total_mb": total // (1024 * 1024),
            "disk_used_mb": used // (1024 * 1024),
            "disk_free_mb": free // (1024 * 1024),
            "pid": os.getpid()
        }
