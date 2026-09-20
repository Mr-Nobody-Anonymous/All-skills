"""Plugin implementation for wakeword-vosk."""

from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class PluginVosk:
    """WAKEWORD plugin using vosk."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.name = "vosk"
        self.plugin_type = "wakeword"
        self.initialized = True
        logger.info(f"Initialized wakeword plugin: {self.name}")

    def execute(self, *args, **kwargs) -> Any:
        return {"status": "ok", "plugin": self.name, "type": self.plugin_type}
