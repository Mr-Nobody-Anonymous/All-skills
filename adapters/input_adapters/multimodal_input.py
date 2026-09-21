"""
Multimodal Input Adapter.
Fuses simultaneous text, speech, vision, and sensor signals into a unified context payload.
"""

from typing import Dict, Any, Optional

class MultimodalInputAdapter:
    def adapt(self,
              text: Optional[str] = None,
              audio: Optional[Any] = None,
              image: Optional[Any] = None,
              sensors: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return {
            "type": "multimodal",
            "text": text,
            "has_audio": audio is not None,
            "has_image": image is not None,
            "sensors": sensors or {},
            "signals": [s for s, val in [("text", text), ("audio", audio), ("image", image), ("sensors", sensors)] if val is not None]
        }
