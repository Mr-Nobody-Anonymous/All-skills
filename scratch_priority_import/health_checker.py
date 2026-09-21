"""
Health Checker - Periodically checks skill liveness and reports degraded skills.
"""
from __future__ import annotations
import time
import threading
from typing import Any, Callable, Dict, List, Optional


class SkillHealthStatus:
    def __init__(self, skill_id: str):
        self.skill_id = skill_id
        self.healthy = True
        self.last_check: float = time.time()
        self.last_error: Optional[str] = None
        self.consecutive_failures = 0


class HealthChecker:
    """
    Periodically calls health_check() on every registered skill.
    Marks skills as degraded after consecutive failures.
    Triggers auto-restart callback if provided.
    """

    def __init__(self, interval_seconds: int = 60, failure_threshold: int = 3):
        self._skills: Dict[str, Any] = {}
        self._statuses: Dict[str, SkillHealthStatus] = {}
        self._interval = interval_seconds
        self._threshold = failure_threshold
        self._restart_cb: Optional[Callable] = None
        self._thread: Optional[threading.Thread] = None
        self._running = False

    def register_skill(self, skill_id: str, skill_instance) -> None:
        self._skills[skill_id] = skill_instance
        self._statuses[skill_id] = SkillHealthStatus(skill_id)

    def set_restart_callback(self, cb: Callable) -> None:
        self._restart_cb = cb

    def check_all(self) -> Dict[str, SkillHealthStatus]:
        for skill_id, skill in self._skills.items():
            status = self._statuses[skill_id]
            try:
                result = skill.health_check() if hasattr(skill, "health_check") else {"healthy": True}
                if result.get("healthy", True):
                    status.healthy = True
                    status.consecutive_failures = 0
                    status.last_error = None
                else:
                    self._handle_failure(skill_id, status, "health_check returned unhealthy")
            except Exception as exc:
                self._handle_failure(skill_id, status, str(exc))
            status.last_check = time.time()
        return self._statuses

    def _handle_failure(self, skill_id: str, status: SkillHealthStatus, error: str):
        status.consecutive_failures += 1
        status.last_error = error
        if status.consecutive_failures >= self._threshold:
            status.healthy = False
            if self._restart_cb:
                try:
                    self._restart_cb(skill_id)
                except Exception:
                    pass

    def start_background(self) -> None:
        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._running = False

    def _loop(self):
        while self._running:
            self.check_all()
            time.sleep(self._interval)

    def report(self) -> List[Dict]:
        return [
            {
                "skill_id": s.skill_id,
                "healthy": s.healthy,
                "consecutive_failures": s.consecutive_failures,
                "last_error": s.last_error,
                "last_check": s.last_check,
            }
            for s in self._statuses.values()
        ]
