"""
Text Output Adapter.
Formats skill outputs into Markdown, terminal color text, or plain text strings.
"""

from typing import Dict, Any

class TextOutputAdapter:
    def format(self, payload: Dict[str, Any], format_type: str = "plain") -> str:
        text = payload.get("dialog") or payload.get("text") or str(payload)
        if format_type == "markdown":
            return f"**Output**: {text}"
        return text
