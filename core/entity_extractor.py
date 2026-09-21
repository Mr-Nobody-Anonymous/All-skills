"""
Entity Extractor - Pulls named entities from user input.
"""
from __future__ import annotations
import re
from typing import Any, Dict, List


class EntityExtractor:
    """
    Extracts entities (dates, locations, names, numbers, URLs) from text.
    Uses regex patterns as default; can be swapped for NER model.
    """

    PATTERNS = {
        "url": r"https?://[\w./%-]+",
        "email": r"[\w.+-]+@[\w.-]+\.[a-zA-Z]{2,}",
        "date": r"\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|today|tomorrow|yesterday|monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b",
        "time": r"\b(\d{1,2}:\d{2}\s*(?:am|pm)?|\d{1,2}\s*(?:am|pm))\b",
        "number": r"\b\d+(?:\.\d+)?\b",
        "duration": r"\b(\d+)\s*(second|minute|hour|day|week|month|year)s?\b",
    }

    def extract(self, text: str) -> Dict[str, List[str]]:
        """Return a dict of entity_type → list of matched strings."""
        results: Dict[str, List[str]] = {}
        for entity_type, pattern in self.PATTERNS.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                results[entity_type] = [m if isinstance(m, str) else m[0] for m in matches]
        return results

    def extract_flat(self, text: str) -> List[Dict[str, Any]]:
        """Return a flat list of {'type': ..., 'value': ...} dicts."""
        flat = []
        for entity_type, pattern in self.PATTERNS.items():
            for match in re.finditer(pattern, text, re.IGNORECASE):
                flat.append({
                    "type": entity_type,
                    "value": match.group(0),
                    "start": match.start(),
                    "end": match.end(),
                })
        flat.sort(key=lambda x: x["start"])
        return flat
