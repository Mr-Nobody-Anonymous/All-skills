"""
Intent Engine for All-Skills Platform.
Handles natural language intent parsing, keyword extraction, and skill routing.
"""

from typing import Dict, Any, List, Optional
import re
from .intent_router import IntentRouter

class IntentEngine:
    def __init__(self, router: Optional[IntentRouter] = None):
        self.router = router or IntentRouter()
        self.rules: List[Dict[str, Any]] = []

    def register_intent_rule(self, intent_name: str, patterns: List[str], skill_id: str, priority: int = 50):
        self.rules.append({
            "intent": intent_name,
            "patterns": [re.compile(p, re.IGNORECASE) for p in patterns],
            "skill_id": skill_id,
            "priority": priority
        })

    def classify(self, text: str) -> Dict[str, Any]:
        """Classifies text into intent matches, ranking by priority and confidence."""
        matches = []
        for rule in self.rules:
            for pattern in rule["patterns"]:
                match = pattern.search(text)
                if match:
                    entities = match.groupdict() if match.groupdict() else {}
                    matches.append({
                        "intent": rule["intent"],
                        "skill_id": rule["skill_id"],
                        "priority": rule["priority"],
                        "confidence": 0.95,
                        "entities": entities
                    })
                    break

        if matches:
            matches.sort(key=lambda x: (-x["confidence"], x["priority"]))
            return matches[0]

        # Fallback to router
        routed = self.router.route(text) if self.router else None
        if isinstance(routed, dict):
            return {
                "intent": routed.get("intent", "general_query"),
                "skill_id": routed.get("skill_id", "skill-fallback-unknown"),
                "priority": routed.get("priority", 100),
                "confidence": routed.get("confidence", 0.5),
                "entities": routed.get("entities", {})
            }

        return {
            "intent": "general_query",
            "skill_id": str(routed) if routed else "skill-fallback-unknown",
            "priority": 100,
            "confidence": 0.5,
            "entities": {}
        }
