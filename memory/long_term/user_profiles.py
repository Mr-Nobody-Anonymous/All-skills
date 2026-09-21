"""
User Profile and Preference Learning System.
Stores long-term user settings, learned behavioral preferences, and custom skill overrides.
"""

from typing import Dict, Any, Optional

class UserProfiles:
    def __init__(self):
        self.profiles: Dict[str, Dict[str, Any]] = {}

    def get_profile(self, user_id: str = "default_user") -> Dict[str, Any]:
        if user_id not in self.profiles:
            self.profiles[user_id] = {
                "user_id": user_id,
                "preferences": {},
                "pinned_skills": {},
                "voice_profile": {}
            }
        return self.profiles[user_id]

    def set_preference(self, user_id: str, key: str, value: Any):
        profile = self.get_profile(user_id)
        profile["preferences"][key] = value

    def get_preference(self, user_id: str, key: str, default: Optional[Any] = None) -> Any:
        profile = self.get_profile(user_id)
        return profile["preferences"].get(key, default)

    def pin_skill(self, user_id: str, intent: str, skill_id: str):
        profile = self.get_profile(user_id)
        profile["pinned_skills"][intent] = skill_id
