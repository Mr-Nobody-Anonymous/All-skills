"""
Core Authentication and Security Manager.
Validates skill permissions, enforces token authorization, and protects credentials.
"""

from typing import Dict, Set, Optional, Any
import logging

logger = logging.getLogger(__name__)


class AuthManager:
    """Controls access and permission verification for skills."""

    def __init__(self):
        self._skill_permissions: Dict[str, Set[str]] = {}
        self._tokens: Dict[str, str] = {}  # token -> identity

    def grant_permission(self, skill_name: str, permission: str) -> None:
        """Grant a capability permission to a skill."""
        if skill_name not in self._skill_permissions:
            self._skill_permissions[skill_name] = set()
        self._skill_permissions[skill_name].add(permission)

    def has_permission(self, skill_name: str, permission: str) -> bool:
        """Verify if skill has permission."""
        perms = self._skill_permissions.get(skill_name, set())
        return "*" in perms or permission in perms

    def register_token(self, token: str, user: str) -> None:
        """Register an authorization token."""
        self._tokens[token] = user

    def validate_token(self, token: str) -> Optional[str]:
        """Validate bearer token."""
        return self._tokens.get(token)
