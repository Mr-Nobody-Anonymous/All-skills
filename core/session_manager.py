"""
Core Session Manager.
Tracks user interactions, multi-turn dialogue state, and active sessions.
"""

from typing import Dict, Any, Optional
import uuid
import time


class Session:
    """Encapsulates a client interaction session."""
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.created_at = time.time()
        self.last_activity = time.time()
        self.data: Dict[str, Any] = {}

    def touch(self) -> None:
        self.last_activity = time.time()


class SessionManager:
    """Manages active user sessions."""

    def __init__(self, session_ttl_seconds: float = 3600.0):
        self.session_ttl = session_ttl_seconds
        self._sessions: Dict[str, Session] = {}

    def get_or_create(self, session_id: Optional[str] = None) -> Session:
        """Retrieve existing or create new session."""
        sid = session_id or str(uuid.uuid4())
        if sid not in self._sessions:
            self._sessions[sid] = Session(sid)
        session = self._sessions[sid]
        session.touch()
        return session

    def get(self, session_id: str) -> Optional[Session]:
        """Get session if exists and unexpired."""
        session = self._sessions.get(session_id)
        if session:
            if time.time() - session.last_activity > self.session_ttl:
                del self._sessions[session_id]
                return None
            session.touch()
        return session

    def terminate(self, session_id: str) -> bool:
        """End a session."""
        return self._sessions.pop(session_id, None) is not None
