"""
Voice Input Adapter.
Normalizes audio streams, extracts acoustic metadata, and structures speech events.
"""

from typing import Dict, Any, Optional

class VoiceInputAdapter:
    def adapt(self, audio_data: Any, sample_rate: int = 16000, transcript: Optional[str] = None) -> Dict[str, Any]:
        return {
            "type": "voice",
            "content": transcript or "",
            "sample_rate": sample_rate,
            "has_audio": audio_data is not None,
            "format": "pcm_16bit"
        }
