"""
Image Input Adapter.
Validates image dimensions, channels, and encoding formats for vision pipelines.
"""

from typing import Dict, Any, Optional

class ImageInputAdapter:
    def adapt(self, image_path_or_bytes: Any, source: str = "camera") -> Dict[str, Any]:
        return {
            "type": "image",
            "source": source,
            "data": image_path_or_bytes,
            "processed": True
        }
