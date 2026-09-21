"""
Discord bot messaging via discord.py
Category: communication
"""
from __future__ import annotations
from typing import Any, Dict

try:
    import discord
    _LIB_AVAILABLE = True
except ImportError:
    _LIB_AVAILABLE = False


class DiscordSkill(BaseSkill):
    """
    Discord bot messaging via discord.py
    """

    def __init__(self):
        self._model = None
        self._lib_available = _LIB_AVAILABLE

    def can_handle(self, intent: str, context: Dict[str, Any]) -> bool:
        """Return True if this skill can handle the given intent."""
        keywords = self._get_keywords()
        return any(k in intent.lower() for k in keywords)

    def handle(self, intent: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the skill and return a result dictionary."""
        if not self._lib_available:
            return {
                "status": "degraded",
                "error": "Required library not installed. Run: pip install -r requirements.txt",
                "intent": intent,
            }
        try:
            result = self._execute(intent, context)
            return {"status": "ok", "result": result, "intent": intent}
        except Exception as exc:
            return {"status": "error", "error": str(exc), "intent": intent}

    def get_priority(self) -> int:
        return 50

    def load_model(self):
        """Lazy-load the heavy model on first use."""
        pass

    def unload_model(self):
        """Release model from memory."""
        self._model = None

    def health_check(self) -> Dict[str, Any]:
        return {"healthy": self._lib_available, "model_loaded": self._model is not None}

    def _get_keywords(self):
        return ["discordskill"]

    def _execute(self, intent: str, context: Dict[str, Any]) -> Any:
        return f"{self.__class__.__name__} executed for: {intent}"


try:
    from skills.base_skill import BaseSkill
except ImportError:
    class BaseSkill:
        def can_handle(self, intent, context): return False
        def handle(self, intent, context): return {}
        def get_priority(self): return 50
        def load_model(self): pass
        def unload_model(self): pass
        def health_check(self): return {}
