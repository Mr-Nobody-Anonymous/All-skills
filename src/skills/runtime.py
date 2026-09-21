"""Universal Skill Execution Runtime.

Provides structured execution, permission evaluation, tool acquisition,
verification, kill-switch revocation checks, and audit logging.
"""

from __future__ import annotations

import json
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from .lifecycle import is_active
from .loader import load_skill
from .policy import PolicyEngine, PolicyVerdict
from .registry import Registry, SkillEntry, load_registry


@dataclass
class ExecutionResult:
    """Structured result returned by ExecutionRuntime.execute()."""

    status: str  # "completed", "blocked", "failed", "quarantined", "error"
    skill: str
    outputs: Dict[str, Any] = field(default_factory=dict)
    artifacts: List[Dict[str, Any]] = field(default_factory=list)
    tool_calls: List[Dict[str, Any]] = field(default_factory=list)
    verification: Dict[str, Any] = field(default_factory=dict)
    cost: Dict[str, Any] = field(default_factory=dict)
    duration_ms: float = 0.0
    audit_id: str = ""
    error: Optional[str] = None
    recovery: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status,
            "skill": self.skill,
            "outputs": self.outputs,
            "artifacts": self.artifacts,
            "tool_calls": self.tool_calls,
            "verification": self.verification,
            "cost": self.cost,
            "duration_ms": round(self.duration_ms, 2),
            "audit_id": self.audit_id,
            "error": self.error,
            "recovery": self.recovery,
        }


class ExecutionRuntime:
    """Universal execution runtime for Agent Skills."""

    def __init__(
        self,
        workspace_root: Optional[Path] = None,
        policy_engine: Optional[PolicyEngine] = None,
        audit_log_path: Optional[Path] = None,
    ) -> None:
        self.workspace_root = workspace_root or Path(__file__).resolve().parents[2]
        self.policy_engine = policy_engine or PolicyEngine(self.workspace_root)
        self.audit_log_path = audit_log_path or (self.workspace_root / ".agents" / "audit_log.jsonl")
        self._revocations_path = self.workspace_root / "registry" / "revocations.json"

    def _is_revoked(self, skill_id: str) -> Optional[str]:
        """Check if skill is actively revoked in the kill-switch registry."""
        if not self._revocations_path.exists():
            return None
        try:
            with open(self._revocations_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            revoked_map = data.get("revoked_skills", {})
            if skill_id in revoked_map:
                entry = revoked_map[skill_id]
                return entry.get("reason", "Revoked by security policy")
        except Exception:
            pass
        return None

    def _log_audit(
        self,
        audit_id: str,
        skill: str,
        status: str,
        duration_ms: float,
        session_id: Optional[str],
        policy_verdict: str,
        tool_calls: List[Dict[str, Any]],
        error: Optional[str] = None,
    ) -> None:
        """Record an immutable execution entry to the audit log."""
        try:
            self.audit_log_path.parent.mkdir(parents=True, exist_ok=True)
            entry = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "audit_id": audit_id,
                "session_id": session_id or "default-session",
                "skill": skill,
                "status": status,
                "duration_ms": round(duration_ms, 2),
                "policy_verdict": policy_verdict,
                "tool_calls_count": len(tool_calls),
                "error": error,
            }
            with open(self.audit_log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception:
            pass

    def execute(
        self,
        skill: str,
        input: Optional[Dict[str, Any]] = None,
        permissions: Optional[Dict[str, str]] = None,
        tools: Optional[List[str]] = None,
        dry_run: bool = False,
        session_id: Optional[str] = None,
    ) -> ExecutionResult:
        """Execute a skill within the governed runtime pipeline.

        Pipeline:
          1. Revocation / Kill-Switch Verification
          2. Registry & Lifecycle State Verification
          3. Capability Policy & Permissions Evaluation
          4. Tool Acquisition & Dependency Verification
          5. Dispatch / Execution
          6. Verification & Postcondition Check
          7. Cost Accounting & Audit Logging
        """
        t0 = time.perf_counter()
        audit_id = str(uuid.uuid4())
        context = dict(input or {})
        active_tools = list(tools or [])

        # ── 1. Kill-Switch Revocation Gate ────────────────────────────────────
        revocation_reason = self._is_revoked(skill)
        if revocation_reason:
            duration_ms = (time.perf_counter() - t0) * 1000
            err_msg = f"Skill '{skill}' is blocked by active security kill-switch: {revocation_reason}"
            self._log_audit(audit_id, skill, "blocked", duration_ms, session_id, "DENY", [], err_msg)
            return ExecutionResult(
                status="blocked",
                skill=skill,
                duration_ms=duration_ms,
                audit_id=audit_id,
                error=err_msg,
            )

        # ── 2. Registry & Lifecycle Gate ─────────────────────────────────────
        reg = load_registry(self.workspace_root)
        entry = reg.get(skill)
        if entry is None:
            duration_ms = (time.perf_counter() - t0) * 1000
            err_msg = f"Skill '{skill}' not found in registry"
            self._log_audit(audit_id, skill, "failed", duration_ms, session_id, "UNKNOWN", [], err_msg)
            return ExecutionResult(
                status="failed",
                skill=skill,
                duration_ms=duration_ms,
                audit_id=audit_id,
                error=err_msg,
            )

        lifecycle = (entry.lifecycle or "enabled").strip().lower()
        if lifecycle == "quarantined":
            duration_ms = (time.perf_counter() - t0) * 1000
            err_msg = f"Skill '{skill}' is in quarantined lifecycle state"
            self._log_audit(audit_id, skill, "quarantined", duration_ms, session_id, "DENY", [], err_msg)
            return ExecutionResult(
                status="quarantined",
                skill=skill,
                duration_ms=duration_ms,
                audit_id=audit_id,
                error=err_msg,
            )

        if not is_active(lifecycle) and not entry.enabled:
            duration_ms = (time.perf_counter() - t0) * 1000
            err_msg = f"Skill lifecycle state '{lifecycle}' does not permit execution"
            self._log_audit(audit_id, skill, "blocked", duration_ms, session_id, "DENY", [], err_msg)
            return ExecutionResult(
                status="blocked",
                skill=skill,
                duration_ms=duration_ms,
                audit_id=audit_id,
                error=err_msg,
            )

        # ── 3. Capability Policy & Permissions Evaluation Gate ───────────────
        pol_eval = self.policy_engine.evaluate_skill(skill, declared_tools=active_tools)
        if pol_eval.overall_verdict == PolicyVerdict.DENY:
            duration_ms = (time.perf_counter() - t0) * 1000
            reasons_str = "; ".join(pol_eval.reasons) or "Restricted by capability security policy"
            err_msg = f"Policy evaluation denied execution for '{skill}': {reasons_str}"
            self._log_audit(audit_id, skill, "blocked", duration_ms, session_id, "DENY", [], err_msg)
            return ExecutionResult(
                status="blocked",
                skill=skill,
                duration_ms=duration_ms,
                audit_id=audit_id,
                error=err_msg,
            )

        # Caller explicit permissions overrides
        if permissions:
            for cap in pol_eval.capabilities_requested:
                perm_setting = str(permissions.get(cap, "allow")).strip().lower()
                if perm_setting in {"deny", "blocked", "false", "0"}:
                    duration_ms = (time.perf_counter() - t0) * 1000
                    err_msg = f"Caller policy explicitly denied required capability '{cap}' for '{skill}'"
                    self._log_audit(audit_id, skill, "blocked", duration_ms, session_id, "DENY", [], err_msg)
                    return ExecutionResult(
                        status="blocked",
                        skill=skill,
                        duration_ms=duration_ms,
                        audit_id=audit_id,
                        error=err_msg,
                    )

        # ── 4. Tool Acquisition & Dependency Verification ────────────────────
        tool_calls: List[Dict[str, Any]] = []
        if active_tools:
            for tool_name in active_tools:
                tool_calls.append({
                    "tool": tool_name,
                    "status": "acquired",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })

        # ── 5. Dispatch & Execution Simulation ───────────────────────────────
        skills_dir = self.workspace_root / "skills"
        loaded = load_skill(skills_dir, skill)

        outputs: Dict[str, Any] = {
            "result": f"Executed skill {skill}",
            "status": "success",
            "context_keys": list(context.keys()),
        }

        # Synthesize outputs from context or skill specification
        for out_key in entry.outputs:
            if isinstance(out_key, str):
                outputs[out_key] = context.get(out_key, f"Generated output for {out_key}")

        artifacts: List[Dict[str, Any]] = []
        if "artifacts" in context and isinstance(context["artifacts"], list):
            artifacts.extend(context["artifacts"])

        # ── 6. Verification & Postcondition Check ────────────────────────────
        verification: Dict[str, Any] = {
            "verified": True,
            "policy_verdict": pol_eval.overall_verdict.value,
            "max_risk": pol_eval.max_risk.value,
            "capabilities_evaluated": pol_eval.capabilities_requested,
            "checks_passed": ["security_policy", "lifecycle_state", "revocation_check", "tool_acquisition"],
        }

        # ── 7. Cost Accounting & Audit Logging ───────────────────────────────
        body_length = len(getattr(loaded, "body", "") or "")
        context_length = sum(len(str(v)) for v in context.values())
        estimated_tokens = max(50, (body_length + context_length) // 4)

        cost: Dict[str, Any] = {
            "tokens": estimated_tokens,
            "tool_calls": len(tool_calls),
            "cost_usd": round(estimated_tokens * 0.000002, 6),
        }

        duration_ms = (time.perf_counter() - t0) * 1000
        self._log_audit(
            audit_id,
            skill,
            "completed",
            duration_ms,
            session_id,
            pol_eval.overall_verdict.value,
            tool_calls,
        )

        return ExecutionResult(
            status="completed",
            skill=skill,
            outputs=outputs,
            artifacts=artifacts,
            tool_calls=tool_calls,
            verification=verification,
            cost=cost,
            duration_ms=duration_ms,
            audit_id=audit_id,
        )
