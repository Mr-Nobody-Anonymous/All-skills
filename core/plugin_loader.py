"""
Plugin Loader for All-Skills Platform.
Dynamically discovers, validates, and loads plugins and skills across categories.
"""

import os
import sys
import importlib.util
from pathlib import Path
from typing import Dict, Any, List, Optional
from .plugin_system import PluginSystem

class PluginLoader:
    def __init__(self, plugin_system: Optional[PluginSystem] = None):
        self.system = plugin_system or PluginSystem()
        self.loaded_plugins: Dict[str, Any] = {}

    def discover_and_load(self, base_dir: Path) -> Dict[str, Any]:
        """Scans base_dir for plugin manifests and modules."""
        if not base_dir.exists():
            return {}

        for item in base_dir.iterdir():
            if item.is_dir() and not item.name.startswith((".", "_")):
                init_file = item / "__init__.py"
                if init_file.exists():
                    plugin_name = item.name
                    try:
                        spec = importlib.util.spec_from_file_location(plugin_name, init_file)
                        if spec and spec.loader:
                            module = importlib.util.module_from_spec(spec)
                            sys.modules[plugin_name] = module
                            spec.loader.exec_module(module)
                            self.loaded_plugins[plugin_name] = module
                    except Exception as e:
                        print(f"[PluginLoader] Failed to load {plugin_name}: {e}")
        return self.loaded_plugins

    def get_plugin(self, name: str) -> Optional[Any]:
        return self.loaded_plugins.get(name)
