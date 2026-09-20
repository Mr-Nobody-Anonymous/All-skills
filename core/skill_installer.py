"""
Core Skill Installer.
Handles safe cloning and installation of external voice assistant skill repositories.
"""

import subprocess
import shutil
from pathlib import Path
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class SkillInstaller:
    """Manages cloning, requirements installation, and setup of skills."""

    def __init__(self, target_base_dir: Optional[str] = None):
        self.base_dir = Path(target_base_dir) if target_base_dir else Path.cwd() / "skills"

    def install_from_git(self, repo_url: str, category: str, skill_name: Optional[str] = None, depth: int = 1) -> Dict[str, Any]:
        """Clone external repository into appropriate category directory."""
        if not skill_name:
            skill_name = repo_url.rstrip("/").split("/")[-1]
            if skill_name.endswith(".git"):
                skill_name = skill_name[:-4]

        dest_dir = self.base_dir / category / skill_name
        dest_dir.parent.mkdir(parents=True, exist_ok=True)

        if dest_dir.exists():
            return {
                "success": True,
                "action": "already_installed",
                "destination": str(dest_dir),
                "skill_name": skill_name
            }

        cmd = ["git", "clone", "--depth", str(depth), "--single-branch", repo_url, str(dest_dir)]
        try:
            logger.info(f"Cloning {repo_url} -> {dest_dir}...")
            res = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return {
                "success": True,
                "action": "cloned",
                "destination": str(dest_dir),
                "skill_name": skill_name
            }
        except subprocess.CalledProcessError as e:
            logger.error(f"Git clone failed for {repo_url}: {e.stderr}")
            return {
                "success": False,
                "action": "failed",
                "error": e.stderr,
                "skill_name": skill_name
            }
