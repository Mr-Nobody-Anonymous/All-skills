"""
Chat Widget Interface.
Provides multi-turn conversational chat sessions, streaming tokens, and rich card messaging.
"""

from typing import List, Dict, Any, Optional
from core.pipeline import Pipeline

class ChatInterface:
    def __init__(self, pipeline: Optional[Pipeline] = None):
        self.pipeline = pipeline or Pipeline()
        self.sessions: Dict[str, List[Dict[str, Any]]] = {}

    def send_message(self, session_id: str, message: str) -> Dict[str, Any]:
        if session_id not in self.sessions:
            self.sessions[session_id] = []

        self.sessions[session_id].append({"sender": "user", "text": message})
        res = self.pipeline.process(message, session_id=session_id)

        bot_reply = "Understood."
        if res.get("status") == "success":
            r = res.get("result", {})
            bot_reply = r.get("dialog") or r.get("text") or "Request fulfilled."

        self.sessions[session_id].append({"sender": "bot", "text": bot_reply})
        return {
            "reply": bot_reply,
            "session_id": session_id,
            "pipeline_status": res.get("status")
        }
