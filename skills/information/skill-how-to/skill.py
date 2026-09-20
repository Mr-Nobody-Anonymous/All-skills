"""
Implementation of HowToSkill.
"""

import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class HowToSkill:
    """skill-how-to handler compatible with OpenVoiceOS / Mycroft skill interfaces."""

    def __init__(self, bus: Optional[Any] = None):
        self.bus = bus
        self.name = "skill-how-to"
        self.category = "information"
        self.initialized = True
        logger.info(f"Initialized skill: {self.name} [{self.category}]")

    def initialize(self):
        """Register intents and event handlers with the message bus."""
        logger.info(f"Loaded HowToSkill")

    def handle_intent(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Process intent invocation."""
        return {"status": "success", "skill": self.name, "response": "Executed how_to"}

    def shutdown(self):
        """Cleanup skill resources."""
        logger.info(f"Shutdown HowToSkill")
