"""
Config Loader for All-Skills Platform.
Loads configuration from YAML, JSON, and environment variables with fallbacks.
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional
import yaml

class ConfigLoader:
    def __init__(self, base_path: Optional[Path] = None):
        self.base_path = base_path or Path(__file__).resolve().parent.parent

    def load_yaml(self, rel_path: str) -> Dict[str, Any]:
        target = self.base_path / rel_path
        if target.exists():
            with open(target, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        return {}

    def load_json(self, rel_path: str) -> Dict[str, Any]:
        target = self.base_path / rel_path
        if target.exists():
            with open(target, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def get_env(self, key: str, default: Optional[str] = None) -> Optional[str]:
        return os.environ.get(key, default)

    def load_app_config(self) -> Dict[str, Any]:
        """Loads default config with overrides."""
        config = self.load_yaml("config/default_config.yml")
        root_config = self.load_yaml("config.yaml")
        config.update(root_config)
        return config
