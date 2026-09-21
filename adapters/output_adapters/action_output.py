"""
Action Output Adapter.
Dispatches executable system commands, smart home operations, and hardware pin toggles.
"""

from typing import Dict, Any

class ActionOutputAdapter:
    def format_action(self, action_name: str, parameters: Dict[str, Any], requires_confirmation: bool = False) -> Dict[str, Any]:
        return {
            "type": "action",
            "action": action_name,
            "params": parameters,
            "requires_confirmation": requires_confirmation,
            "status": "pending"
        }
