"""
REST API Router for External System Integration.
Exposes standard RESTful routes for skill invocation, status telemetry, and session contexts.
"""

from typing import Dict, Any, Optional
from core.pipeline import Pipeline
from core.health_checker import HealthChecker

class RestApi:
    def __init__(self, pipeline: Optional[Pipeline] = None, health_checker: Optional[HealthChecker] = None):
        self.pipeline = pipeline or Pipeline()
        self.health = health_checker or HealthChecker()

    def route_request(self, endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        if endpoint == "/v1/skills/execute":
            prompt = payload.get("prompt", "")
            session_id = payload.get("session_id", "default")
            return self.pipeline.process(prompt, session_id=session_id)
        elif endpoint == "/v1/health":
            return self.health.check()
        return {"error": "Endpoint not supported", "status": 404}
