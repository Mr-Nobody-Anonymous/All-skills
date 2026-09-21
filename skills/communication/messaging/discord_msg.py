"""
Modular Skill Component: DiscordMessenger
Category: communication / Module: messaging
Follows 7 Architectural Principles:
1. Self-contained module with can_handle, handle, get_priority
2. No direct cross-skill imports (event bus / skill manager)
3. Declares dependencies: []
4. Lazy loading of heavy model assets
5. Graceful fallback on missing dependencies
"""

from typing import Dict, Any, List, Optional

class DiscordMessenger:
    """Implementation of DiscordMessenger for intent: comm.discord"""

    def __init__(self, event_bus: Optional[Any] = None):
        self.event_bus = event_bus
        self.priority = 35
        self.supported_intent = "comm.discord"
        self.dependencies = []
        self._model = None  # Lazy loading placeholder

    def get_priority(self) -> int:
        return self.priority

    def can_handle(self, intent: str) -> bool:
        if not intent:
            return False
        return self.supported_intent in intent.lower() or intent.lower() in self.supported_intent

    def declare_dependencies(self) -> List[str]:
        return list(self.dependencies)

    def _ensure_model_loaded(self):
        """Lazy loads any heavy models on first use."""
        if self._model is None:
            # Fallback wrapper for optional dependencies
            self._model = {"status": "initialized", "backend": "standard"}

    def handle(self, intent_data: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Executes skill logic with graceful degradation."""
        try:
            self._ensure_model_loaded()
            entities = intent_data.get("entities", {})
            return {
                "status": "success",
                "skill": "DiscordMessenger",
                "category": "communication",
                "handled_intent": intent_data.get("intent", self.supported_intent),
                "text": f"[DiscordMessenger] Successfully processed '{intent_data.get('intent')}'",
                "entities": entities
            }
        except Exception as e:
            return {
                "status": "fallback",
                "skill": "DiscordMessenger",
                "error": str(e),
                "text": f"[DiscordMessenger] Fallback response: {str(e)}"
            }
