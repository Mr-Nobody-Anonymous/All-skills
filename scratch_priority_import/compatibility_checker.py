"""
Compatibility Checker for All-Skills.
Verifies host operating system, Python runtime version, hardware flags, and dependencies.
"""

import sys
import os
import platform
from typing import Dict, List, Optional, Any, Set
import logging

logger = logging.getLogger(__name__)


class CompatibilityChecker:
    """Checks host environment against skill requirements."""

    def __init__(self):
        self.os_type = platform.system().lower()  # 'windows', 'linux', 'darwin'
        self.python_version = (sys.version_info.major, sys.version_info.minor)
        self.arch = platform.machine().lower()

    def is_os_supported(self, supported_platforms: List[str]) -> bool:
        """Check if current OS is supported."""
        if not supported_platforms or "*" in supported_platforms:
            return True
        normalized = [p.strip().lower() for p in supported_platforms]
        return self.os_type in normalized or "all" in normalized

    def is_python_supported(self, min_version: str = "3.8", max_version: Optional[str] = None) -> bool:
        """Check if current Python version is supported."""
        min_parts = tuple(int(x) for x in min_version.split("."))
        if self.python_version < min_parts:
            return False
        if max_version:
            max_parts = tuple(int(x) for x in max_version.split("."))
            if self.python_version > max_parts:
                return False
        return True

    def check_system_tools(self, required_binaries: List[str]) -> Dict[str, bool]:
        """Check if external CLI tools (e.g. git, ffmpeg, pulseaudio) exist in PATH."""
        import shutil
        status = {}
        for binary in required_binaries:
            status[binary] = shutil.which(binary) is not None
        return status

    def evaluate_skill(
        self,
        skill_name: str,
        supported_platforms: Optional[List[str]] = None,
        min_python: str = "3.8",
        required_tools: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Comprehensive compatibility evaluation."""
        os_ok = self.is_os_supported(supported_platforms or ["linux", "windows", "darwin"])
        py_ok = self.is_python_supported(min_python)
        tools_status = self.check_system_tools(required_tools or [])
        all_tools_ok = all(tools_status.values()) if tools_status else True

        compatible = os_ok and py_ok and all_tools_ok
        return {
            "skill": skill_name,
            "compatible": compatible,
            "os_ok": os_ok,
            "os_current": self.os_type,
            "python_ok": py_ok,
            "python_current": f"{self.python_version[0]}.{self.python_version[1]}",
            "tools_ok": all_tools_ok,
            "tools_detail": tools_status,
        }
