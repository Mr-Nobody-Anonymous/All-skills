"""
Text Input Adapter.
Sanitizes, normalizes, and strips noise from keyboard/chat text inputs.
"""

from typing import Dict, Any

class TextInputAdapter:
    def adapt(self, raw_text: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        cleaned = " ".join(raw_text.strip().split())
        return {
            "type": "text",
            "content": cleaned,
            "raw": raw_text,
            "metadata": metadata or {}
        }
