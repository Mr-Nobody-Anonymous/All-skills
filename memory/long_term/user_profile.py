"""
User Profile - Single user's learned preferences and skill pin settings.
Thin alias that imports from user_profiles.py for backward compatibility.
"""
from .user_profiles import UserProfileStore

# Expose a convenience singleton-style profile class
class UserProfile:
    """Single-user profile wrapper around UserProfileStore."""

    def __init__(self, user_id: str = "default"):
        self._store = UserProfileStore()
        self._user_id = user_id

    def set(self, key: str, value) -> None:
        self._store.set_preference(self._user_id, key, value)

    def get(self, key: str, default=None):
        return self._store.get_preference(self._user_id, key, default)

    def pin_skill(self, skill_id: str) -> None:
        self._store.pin_skill(self._user_id, skill_id)

    def pinned_skills(self):
        return self._store.get_pinned_skills(self._user_id)

    def preferences(self) -> dict:
        return self._store.get_all_preferences(self._user_id)
