"""
Core Plugin System.
Plugin architecture supporting STT, TTS, Wake Word, Audio, Solver, and PHAL hardware abstraction layers.
"""

from typing import Dict, Any, Optional, List
import logging

logger = logging.getLogger(__name__)


class PluginType:
    STT = "stt"
    TTS = "tts"
    WAKEWORD = "wakeword"
    INTENT = "intent"
    AUDIO = "audio"
    SOLVER = "solver"
    PHAL = "phal"


class PluginSystem:
    """Manages discoverable plugins for voice pipelines."""

    def __init__(self):
        self._plugins: Dict[str, Dict[str, Any]] = {
            PluginType.STT: {},
            PluginType.TTS: {},
            PluginType.WAKEWORD: {},
            PluginType.INTENT: {},
            PluginType.AUDIO: {},
            PluginType.SOLVER: {},
            PluginType.PHAL: {},
        }

    def register_plugin(self, plugin_type: str, plugin_name: str, instance: Any) -> None:
        """Register a plugin instance under its category."""
        if plugin_type not in self._plugins:
            self._plugins[plugin_type] = {}
        self._plugins[plugin_type][plugin_name] = instance
        logger.info(f"Registered {plugin_type} plugin: {plugin_name}")

    def get_plugin(self, plugin_type: str, plugin_name: str) -> Optional[Any]:
        """Retrieve plugin instance."""
        return self._plugins.get(plugin_type, {}).get(plugin_name)

    def list_plugins(self, plugin_type: Optional[str] = None) -> Dict[str, List[str]]:
        """List all registered plugins."""
        if plugin_type:
            return {plugin_type: list(self._plugins.get(plugin_type, {}).keys())}
        return {pt: list(instances.keys()) for pt, instances in self._plugins.items()}
