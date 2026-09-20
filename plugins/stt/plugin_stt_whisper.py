"""Plugin implementation for stt-whisper."""

from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class PluginWhisper:
    """STT plugin using whisper."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.name = "whisper"
        self.plugin_type = "stt"
        self.initialized = True
        logger.info(f"Initialized stt plugin: {self.name}")

    def execute(self, *args, **kwargs) -> Any:
        return {"status": "ok", "plugin": self.name, "type": self.plugin_type}
