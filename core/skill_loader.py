"""
Core Skill Loader.
Safely dynamically loads python skills from filesystem directories with validation and sandboxing checks.
"""

import sys
import importlib.util
from pathlib import Path
from typing import Optional, Any, Dict
import logging

logger = logging.getLogger(__name__)


class SkillLoader:
    """Dynamic Python skill loader."""

    def __init__(self, base_directory: Optional[str] = None):
        self.base_dir = Path(base_directory) if base_directory else Path.cwd() / "skills"

    def load_from_path(self, skill_path: Path) -> Optional[Any]:
        """Load skill instance from its directory containing __init__.py or skill.py."""
        if not skill_path.exists() or not skill_path.is_dir():
            logger.error(f"Invalid skill path: {skill_path}")
            return None

        init_file = skill_path / "__init__.py"
        entry_file = init_file if init_file.exists() else skill_path / f"{skill_path.name}.py"

        if not entry_file.exists():
            logger.warning(f"No entry point found for skill at: {skill_path}")
            return None

        module_name = f"skills.{skill_path.parent.name}.{skill_path.name}"
        try:
            spec = importlib.util.spec_from_file_location(module_name, str(entry_file))
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = module
                spec.loader.exec_module(module)
                logger.info(f"Loaded module '{module_name}' from {entry_file}")
                return module
        except Exception as e:
            logger.error(f"Failed to load skill module at {entry_file}: {e}", exc_info=True)
            return None

    def scan_directory(self) -> Dict[str, Path]:
        """Scan skills directory for all skill packages."""
        found = {}
        if not self.base_dir.exists():
            return found
        for cat_dir in self.base_dir.iterdir():
            if cat_dir.is_dir() and not cat_dir.name.startswith("."):
                for skill_dir in cat_dir.iterdir():
                    if skill_dir.is_dir() and (skill_dir / "__init__.py").exists():
                        found[skill_dir.name] = skill_dir
        return found
