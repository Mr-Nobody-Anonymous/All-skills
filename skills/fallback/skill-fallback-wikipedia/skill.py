"""
Implementation of FallbackWikipediaSkill.
"""

import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class FallbackWikipediaSkill:
    """skill-fallback-wikipedia handler compatible with OpenVoiceOS / Mycroft skill interfaces."""

    def __init__(self, bus: Optional[Any] = None):
        self.bus = bus
        self.name = "skill-fallback-wikipedia"
        self.category = "fallback"
        self.initialized = True
        logger.info(f"Initialized skill: {self.name} [{self.category}]")

    def initialize(self):
        """Register intents and event handlers with the message bus."""
        logger.info(f"Loaded FallbackWikipediaSkill")

    def handle_intent(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Process intent invocation."""
        return {"status": "success", "skill": self.name, "response": "Executed fallback_wikipedia"}

    def shutdown(self):
        """Cleanup skill resources."""
        logger.info(f"Shutdown FallbackWikipediaSkill")
