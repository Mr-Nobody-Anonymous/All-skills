"""
Voice Output Adapter.
Prepares dialog utterances, prosody hints, and SSML markup for speech synthesizers.
"""

from typing import Dict, Any

class VoiceOutputAdapter:
    def format_speech(self, text: str, emotion: str = "neutral", speed: float = 1.0) -> Dict[str, Any]:
        ssml = f"<speak><prosody rate='{speed}'>{text}</prosody></speak>"
        return {
            "type": "speech",
            "text": text,
            "ssml": ssml,
            "emotion": emotion
        }
