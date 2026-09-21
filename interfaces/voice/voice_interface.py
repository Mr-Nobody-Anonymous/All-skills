"""
Voice-Based Interaction Loop.
Connects Wake Word detection, Speech-to-Text, Pipeline routing, and Text-to-Speech output.
"""

from typing import Optional, Dict, Any
from core.pipeline import Pipeline
from core.event_bus import EventBus

class VoiceInterface:
    def __init__(self, pipeline: Optional[Pipeline] = None, event_bus: Optional[EventBus] = None):
        self.pipeline = pipeline or Pipeline()
        self.event_bus = event_bus or EventBus()
        self.listening = False

    def on_wake_word_detected(self, wakeword: str = "hey assistant"):
        self.listening = True
        self.event_bus.publish("voice:wake_word", {"wakeword": wakeword})
        return f"Awake: {wakeword}"

    def process_spoken_utterance(self, audio_transcript: str) -> Dict[str, Any]:
        """Processes transcribed audio through the cognitive pipeline."""
        if not audio_transcript.strip():
            return {"status": "ignored", "message": "Empty audio transcript"}

        self.event_bus.publish("voice:utterance_received", {"transcript": audio_transcript})
        response = self.pipeline.process(audio_transcript)

        # Prepare speech response
        spoken_text = ""
        if response.get("status") == "success":
            res = response.get("result", {})
            spoken_text = res.get("dialog") or res.get("text") or "Done."
        else:
            spoken_text = "I encountered an error processing that request."

        self.event_bus.publish("voice:speak", {"text": spoken_text})
        return {"response": response, "spoken_text": spoken_text}
