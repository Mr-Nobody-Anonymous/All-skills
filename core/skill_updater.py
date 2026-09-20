"""
Core Skill Updater.
Tracks version drift, queries git remotes, and updates local skill instances safely.
"""

import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)


class SkillUpdater:
    """Updates installed skill repositories."""

    def __init__(self, skills_dir: Optional[str] = None):
        self.skills_dir = Path(skills_dir) if skills_dir else Path.cwd() / "skills"

    def check_updates(self, skill_path: Path) -> bool:
        """Check if remote git commits exist for this skill."""
        if not (skill_path / ".git").exists():
            return False
        try:
            subprocess.run(["git", "-C", str(skill_path), "fetch"], capture_output=True, check=True)
            status = subprocess.run(
                ["git", "-C", str(skill_path), "status", "-uno"],
                capture_output=True,
                text=True,
                check=True
            )
            return "Your branch is behind" in status.stdout
        except Exception as e:
            logger.warning(f"Failed to check updates for {skill_path.name}: {e}")
            return False

    def update_skill(self, skill_path: Path) -> Dict[str, Any]:
        """Run git pull on skill directory."""
        if not (skill_path / ".git").exists():
            return {"success": False, "reason": "Not a git repository"}
        try:
            res = subprocess.run(
                ["git", "-C", str(skill_path), "pull"],
                capture_output=True,
                text=True,
                check=True
            )
            return {"success": True, "output": res.stdout}
        except subprocess.CalledProcessError as e:
            return {"success": False, "error": e.stderr}
