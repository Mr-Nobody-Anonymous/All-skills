"""Home Assistant Entity Models."""
from typing import Dict, Any

class HAEntity:
    def __init__(self, entity_id: str, state: str, attributes: Dict[str, Any]):
        self.entity_id = entity_id
        self.state = state
        self.attributes = attributes
