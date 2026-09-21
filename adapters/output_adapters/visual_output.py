"""
Visual Output Adapter.
Formats charts, images, bounding boxes, and GUI cards for display frontends.
"""

from typing import Dict, Any, List, Optional

class VisualOutputAdapter:
    def format_card(self, title: str, body: str, image_url: Optional[str] = None, buttons: Optional[List[str]] = None) -> Dict[str, Any]:
        return {
            "type": "card",
            "title": title,
            "body": body,
            "image": image_url,
            "actions": buttons or []
        }
