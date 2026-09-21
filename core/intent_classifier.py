"""
Intent Classifier - Classifies raw user input into structured intent objects.
"""
from __future__ import annotations
import re
from typing import Any, Dict, List, Optional


class IntentClassifier:
    """
    Classifies user input text into intent + confidence score.
    Uses regex rules as primary, falls back to keyword matching.
    """

    def __init__(self):
        self._rules: List[Dict] = []
        self._default_intent = "general_query"
        self._load_default_rules()

    def _load_default_rules(self):
        patterns = [
            ("search_web", [r"search for", r"look up", r"find info"]),
            ("play_music", [r"play (some )?music", r"play (the )?song"]),
            ("set_timer", [r"set (a )?timer", r"remind me in"]),
            ("send_email", [r"send (an )?email", r"email to"]),
            ("translate", [r"translate .+ to", r"how (do you|to) say"]),
            ("get_weather", [r"weather (in|for|today)", r"will it rain"]),
            ("write_code", [r"write (a )?function", r"generate (some )?code"]),
        ]
        for intent, pats in patterns:
            for pat in pats:
                self._rules.append({
                    "intent": intent,
                    "pattern": re.compile(pat, re.IGNORECASE),
                })

    def classify(self, text: str) -> Dict[str, Any]:
        """Return {'intent': str, 'confidence': float, 'entities': dict}"""
        text = text.strip()
        for rule in self._rules:
            if rule["pattern"].search(text):
                return {
                    "intent": rule["intent"],
                    "confidence": 0.85,
                    "entities": {},
                    "raw": text,
                }
        return {
            "intent": self._default_intent,
            "confidence": 0.40,
            "entities": {},
            "raw": text,
        }

    def add_rule(self, intent: str, pattern: str):
        self._rules.append({
            "intent": intent,
            "pattern": re.compile(pattern, re.IGNORECASE),
        })
