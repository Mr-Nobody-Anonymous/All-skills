"""Plugin implementation for stt-azure."""

from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class PluginAzure:
    """STT plugin using azure."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.name = "azure"
        self.plugin_type = "stt"
        self.initialized = True
        logger.info(f"Initialized stt plugin: {self.name}")

    def execute(self, *args, **kwargs) -> Any:
        return {"status": "ok", "plugin": self.name, "type": self.plugin_type}
