"""Home Assistant REST and WebSocket client."""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)

class HomeAssistantClient:
    def __init__(self, host: str = "http://localhost:8123", token: str = ""):
        self.host = host
        self.token = token

    def get_state(self, entity_id: str) -> Dict[str, Any]:
        return {"entity_id": entity_id, "state": "on", "attributes": {}}

    def call_service(self, domain: str, service: str, service_data: Optional[Dict[str, Any]] = None) -> bool:
        logger.info(f"HA Service Call: {domain}.{service}")
        return True
