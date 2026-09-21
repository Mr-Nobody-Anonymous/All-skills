"""
Web-Based Interface (HTTP / WebSocket).
Provides web dashboard endpoints, skill query handlers, and WebSocket live channels.
"""

from typing import Dict, Any, Optional
from core.pipeline import Pipeline

class WebInterface:
    def __init__(self, pipeline: Optional[Pipeline] = None):
        self.pipeline = pipeline or Pipeline()

    def handle_http_request(self, method: str, path: str, body: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Simulates web request handling for API/dashboard."""
        if path == "/api/query" and method == "POST":
            text = (body or {}).get("text", "")
            return self.pipeline.process(text)
        elif path == "/api/health" and method == "GET":
            return {"status": "ok", "service": "All-Skills Web Engine"}
        return {"status": "error", "code": 404, "message": "Not Found"}
