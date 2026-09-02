"""Skill lifecycle states.

Explicit lifecycle states make importing hundreds of third-party skills
manageable: a skill is discovered, imported, validated, security-scanned,
made ready, enabled, disabled, quarantined, or deprecated. The router only
considers skills whose lifecycle permits activation (``enabled``), and the
validator rejects malformed state transitions.
"""
from __future__ import annotations

from typing import Dict, Set

LIFECYCLE_STATES = [
    "discovered",
    "imported",
    "validated",
    "security_scanned",
    "ready",
    "enabled",
    "disabled",
    "quarantined",
    "deprecated",
]

_ACTIVE_STATES = {"enabled"}

# Permitted forward transitions. Deprecated is terminal; quarantined can be
# re-validated and moved back onto the normal path.
_TRANSITIONS: Dict[str, Set[str]] = {
    "discovered": {"imported", "quarantined", "disabled", "deprecated"},
    "imported": {"validated", "quarantined", "disabled", "deprecated"},
    "validated": {"security_scanned", "ready", "quarantined", "disabled", "deprecated"},
    "security_scanned": {"ready", "quarantined", "disabled", "deprecated"},
    "ready": {"enabled", "disabled", "quarantined", "deprecated"},
    "enabled": {"disabled", "quarantined", "deprecated", "ready"},
    "disabled": {"enabled", "ready", "quarantined", "deprecated"},
    "quarantined": {"disabled", "deprecated", "validated"},
    "deprecated": set(),
}


def valid_states() -> list:
    """Return the ordered list of valid lifecycle states."""
    return list(LIFECYCLE_STATES)


def is_valid(state: str) -> bool:
    """True if ``state`` names a defined lifecycle state."""
    return (state or "").strip().lower() in LIFECYCLE_STATES


def is_active(state: str) -> bool:
    """True if the lifecycle permits active routing/execution."""
    return (state or "").strip().lower() in _ACTIVE_STATES


def can_transition(current: str, target: str) -> bool:
    """Whether a transition from ``current`` to ``target`` is permitted."""
    current = (current or "discovered").strip().lower()
    target = (target or "").strip().lower()
    if not is_valid(current) or not is_valid(target):
        return False
    if current == target:
        return True
    return target in _TRANSITIONS.get(current, set())


def transition(current: str, target: str) -> str:
    """Return the new state after a transition, or raise ``ValueError``."""
    current = (current or "discovered").strip().lower()
    target = (target or "").strip().lower()
    if not is_valid(target):
        raise ValueError(
            f"unknown lifecycle state: {target!r} (valid: {', '.join(LIFECYCLE_STATES)})"
        )
    if target == current:
        return current
    if can_transition(current, target):
        return target
    raise ValueError(
        f"invalid lifecycle transition: {current!r} -> {target!r} "
        f"(allowed from {current!r}: {sorted(_TRANSITIONS.get(current, set())) or 'none'})"
    )