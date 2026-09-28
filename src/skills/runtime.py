"""Universal Skill Execution Runtime.

Runs a skill request through the governance pipeline — revocation kill switch,
lifecycle state, capability policy (with enforced human approval), SSRF and
caller-permission checks — and then *honestly* reports what happened:

``simulated``          ``dry_run=True``: every gate was evaluated, nothing ran.
``prepared``           No executor is registered for the skill. The runtime
                       returns the skill's instruction bundle for the calling
                       agent to carry out; it does not claim the task was done.
``completed``          A registered executor ran, returned every declared
                       output, and reported only tool calls it was authorised
                       to make.
``failed``             The executor raised, its result was missing declared
                       outputs, it reported a tool call outside its authorised
                       tools/capabilities, or the skill does not exist.
``approval_required``  The policy verdict is ASK and no matching approval was
                       supplied. Nothing ran.
``blocked`` / ``quarantined`` / ``error``
                       Refused by a security gate, or the security state could
                       not be evaluated (fail closed).

Executors are ordinary callables registered with
:meth:`ExecutionRuntime.register_executor`; they receive a
:class:`SkillInvocation` and return a mapping with an ``outputs`` dict and,
optionally, ``artifacts``, ``tool_calls`` (``{"tool": <name>, ...}``) and
``usage``.

What the gates guarantee, and what they do not: the runtime decides *whether*
an executor may run and checks what it reports. An in-process executor is
trusted code — it runs with this process's privileges, so the tool-call check
detects violations after the fact rather than preventing them. For bounded
execution use :class:`skills.executors.SubprocessExecutor` (separate process,
scratch directory, scrubbed environment, timeout, resource limits); for
untrusted code add OS-level isolation (container/VM) — see docs/LIMITATIONS.md.
"""

from __future__ import annotations

import hashlib
import json
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Mapping, Optional

from .lifecycle import is_valid, permits_activation
from .loader import load_skill
from .policy import UNCLASSIFIED_CAPABILITY, PolicyEngine, PolicyEvaluationResult, PolicyVerdict, capabilities_for_tool
from .registry import SkillEntry, load_registry
from .revocations import LEGACY_RELPATH, RevocationError, load_revocations


@dataclass
class ExecutionResult:
    """Structured result returned by ExecutionRuntime.execute()."""

    # simulated | prepared | completed | failed | approval_required | blocked | quarantined | error
    status: str
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
    executed: bool = False
    approval_request: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status,
            "skill": self.skill,
            "executed": self.executed,
            "outputs": self.outputs,
            "artifacts": self.artifacts,
            "tool_calls": self.tool_calls,
            "verification": self.verification,
            "cost": self.cost,
            "duration_ms": round(self.duration_ms, 2),
            "audit_id": self.audit_id,
            "error": self.error,
            "recovery": self.recovery,
            "approval_request": self.approval_request,
        }


@dataclass(frozen=True)
class SkillInvocation:
    """What an executor receives."""

    skill: SkillEntry
    inputs: Dict[str, Any]
    instructions: str
    authorized_capabilities: List[str]
    session_id: Optional[str]
    audit_id: str


Executor = Callable[[SkillInvocation], Mapping[str, Any]]


SUCCESS_STATUSES = frozenset({"completed", "prepared", "simulated"})


def tool_call_violations(tool_calls: List[Dict[str, Any]], authorized_tools: List[str],
                         authorized_capabilities: List[str]) -> List[str]:
    """Reported tool calls the invocation was not authorised to make (fail closed).

    A call is allowed when its tool is one the skill was evaluated with, or when
    every capability it needs was authorised. Unclassified capabilities only
    count through the tool's own name, so approving one unknown tool never
    authorises another; a call that does not name its tool is a violation.
    """
    tools = {str(t).strip().lower() for t in authorized_tools}
    caps = set(authorized_capabilities) - {UNCLASSIFIED_CAPABILITY}
    violations: List[str] = []
    for call in tool_calls:
        name = str(call.get("tool") or call.get("name") or "").strip()
        if not name:
            violations.append("a tool call that does not name its tool")
            continue
        if name.lower() in tools:
            continue
        missing = [cap for cap in capabilities_for_tool(name) if cap not in caps]
        if missing:
            violations.append(f"{name} (needs {', '.join(missing)})")
    return violations


def exit_code_for(status: str) -> int:
    """CLI exit code: 0 success, 2 approval required, 1 refused/failed."""
    if status in SUCCESS_STATUSES:
        return 0
    return 2 if status == "approval_required" else 1


def approval_from_args(approval_id: Optional[str], approved_by: Optional[str]) -> Optional[Dict[str, str]]:
    """Build an ``approval`` mapping from CLI flags (None if not supplied)."""
    if not approval_id:
        return None
    return {"request_id": approval_id, "approved_by": approved_by or ""}


def approval_request_id(skill: str, capabilities: List[str], inputs: Mapping[str, Any]) -> str:
    """Deterministic id binding an approval to one skill, capability set and input."""
    payload = json.dumps(
        {"skill": skill, "capabilities": sorted(capabilities), "inputs": dict(inputs)},
        sort_keys=True,
        default=str,
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:32]


class ExecutionRuntime:
    """Universal execution runtime for Agent Skills."""

    def __init__(
        self,
        workspace_root: Optional[Path] = None,
        policy_engine: Optional[PolicyEngine] = None,
        audit_log_path: Optional[Path] = None,
        executors: Optional[Dict[str, Executor]] = None,
    ) -> None:
        self.workspace_root = workspace_root or Path(__file__).resolve().parents[2]
        self.policy_engine = policy_engine or PolicyEngine(self.workspace_root)
        self.audit_log_path = audit_log_path or (self.workspace_root / ".agents" / "audit_log.jsonl")
        self._revocations_path = self.workspace_root / "registry" / "revocations.json"
        self._legacy_revocations_path = self.workspace_root / LEGACY_RELPATH
        self._executors: Dict[str, Executor] = dict(executors or {})

    # ── Executors ────────────────────────────────────────────────────────────

    def register_executor(self, skill_id: str, executor: Executor) -> None:
        """Register the callable that actually performs ``skill_id``."""
        self._executors[skill_id] = executor

    # ── Gates ────────────────────────────────────────────────────────────────

    def _is_revoked(self, skill_id: str) -> Optional[str]:
        """Reason if ``skill_id`` is revoked. Raises RevocationError if the registry is invalid."""
        revoked = load_revocations(self._legacy_revocations_path)
        revoked.update(load_revocations(self._revocations_path))
        entry = revoked.get(skill_id)
        return entry.reason if entry else None

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
        approved_by: Optional[str] = None,
    ) -> None:
        """Record an immutable execution entry to the audit log."""
        try:
            self.audit_log_path.parent.mkdir(parents=True, exist_ok=True)
            safe_error = error
            if safe_error and any(pat in safe_error for pat in ("AKIA", "ASIA", "PRIVATE KEY", "Bearer ")):
                import re
                safe_error = re.sub(r"(AKIA|ASIA)[0-9A-Z]{16}", "[REDACTED_AWS_KEY]", safe_error)
                safe_error = re.sub(r"Bearer\s+[A-Za-z0-9._~+/-]+", "Bearer [REDACTED_TOKEN]", safe_error)

            entry = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "audit_id": audit_id,
                "session_id": session_id or "default-session",
                "skill": skill,
                "status": status,
                "duration_ms": round(duration_ms, 2),
                "policy_verdict": policy_verdict,
                "tool_calls_count": len(tool_calls),
                "approved_by": approved_by,
                "error": safe_error,
            }
            with open(self.audit_log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as exc:
            import sys
            print(f"[AUDIT ERROR] Failed writing audit log to {self.audit_log_path}: {exc}", file=sys.stderr)
            if status in {"blocked", "quarantined", "approval_required", "error"}:
                raise RuntimeError(f"Audit log failure during security boundary event: {exc}") from exc

    def _refuse(
        self,
        status: str,
        skill: str,
        t0: float,
        audit_id: str,
        session_id: Optional[str],
        verdict: str,
        err_msg: str,
    ) -> ExecutionResult:
        duration_ms = (time.perf_counter() - t0) * 1000
        self._log_audit(audit_id, skill, status, duration_ms, session_id, verdict, [], err_msg)
        return ExecutionResult(status=status, skill=skill, duration_ms=duration_ms, audit_id=audit_id, error=err_msg)

    # ── Pipeline ─────────────────────────────────────────────────────────────

    def execute(
        self,
        skill: str,
        input: Optional[Dict[str, Any]] = None,
        permissions: Optional[Dict[str, str]] = None,
        tools: Optional[List[str]] = None,
        dry_run: bool = False,
        session_id: Optional[str] = None,
        approval: Optional[Mapping[str, str]] = None,
    ) -> ExecutionResult:
        """Run ``skill`` through the governed pipeline (see module docstring).

        ``approval`` authorises capabilities whose policy verdict is ASK. It
        must be ``{"request_id": <id from the approval_required result>,
        "approved_by": <who approved>}``; an approval for a different skill,
        capability set or input does not match.
        """
        t0 = time.perf_counter()
        audit_id = str(uuid.uuid4())
        context = dict(input or {})
        active_tools = list(tools or [])

        # ── 1. Kill-switch revocation gate (fail closed) ─────────────────────
        try:
            revocation_reason = self._is_revoked(skill)
        except RevocationError as exc:
            return self._refuse("error", skill, t0, audit_id, session_id, "DENY",
                                f"Refusing to execute '{skill}': revocation registry is invalid ({exc})")
        if revocation_reason:
            return self._refuse("blocked", skill, t0, audit_id, session_id, "DENY",
                                f"Skill '{skill}' is blocked by active security kill-switch: {revocation_reason}")

        # ── 2. Registry & lifecycle gate ─────────────────────────────────────
        reg = load_registry(self.workspace_root)
        entry = reg.get(skill)
        if entry is None:
            return self._refuse("failed", skill, t0, audit_id, session_id, "UNKNOWN",
                                f"Skill '{skill}' not found in registry")

        lifecycle = (entry.lifecycle or "").strip().lower()
        if lifecycle == "quarantined":
            return self._refuse("quarantined", skill, t0, audit_id, session_id, "DENY",
                                f"Skill '{skill}' is in quarantined lifecycle state")
        if not is_valid(lifecycle):
            return self._refuse("blocked", skill, t0, audit_id, session_id, "DENY",
                                f"Skill '{skill}' has an invalid lifecycle state '{entry.lifecycle}'")
        if not permits_activation(lifecycle, entry.enabled):
            return self._refuse("blocked", skill, t0, audit_id, session_id, "DENY",
                                f"Skill lifecycle state '{lifecycle}' (enabled={entry.enabled}) does not permit execution")

        # ── 3. Capability policy, approval, SSRF & caller permissions ────────
        pol_eval = self.policy_engine.evaluate_skill(skill, declared_tools=active_tools)
        if pol_eval.overall_verdict == PolicyVerdict.DENY:
            reasons_str = "; ".join(pol_eval.reasons) or "Restricted by capability security policy"
            return self._refuse("blocked", skill, t0, audit_id, session_id, "DENY",
                                f"Policy evaluation denied execution for '{skill}': {reasons_str}")

        for key, val in context.items():
            if isinstance(val, str) and (val.startswith("http://") or val.startswith("https://")):
                from .policy import validate_network_target
                is_safe, ssrf_reason = validate_network_target(val)
                if not is_safe:
                    return self._refuse("blocked", skill, t0, audit_id, session_id, "DENY",
                                        f"SSRF boundary violation in input parameter '{key}': {ssrf_reason}")

        if permissions:
            for cap in pol_eval.capabilities_requested:
                perm_setting = str(permissions.get(cap, "allow")).strip().lower()
                if perm_setting in {"deny", "blocked", "false", "0"}:
                    return self._refuse("blocked", skill, t0, audit_id, session_id, "DENY",
                                        f"Caller policy explicitly denied required capability '{cap}' for '{skill}'")

        approved_by: Optional[str] = None
        if pol_eval.overall_verdict == PolicyVerdict.ASK:
            request_id = approval_request_id(skill, pol_eval.capabilities_requested, context)
            granted = (
                approval is not None
                and approval.get("request_id") == request_id
                and bool(str(approval.get("approved_by") or "").strip())
            )
            if not granted:
                return self._approval_required(skill, pol_eval, request_id, t0, audit_id, session_id)
            approved_by = str(approval.get("approved_by")) if approval else None

        authorized = [
            {"tool": tool_name, "status": "authorized", "capabilities": capabilities_for_tool(tool_name)}
            for tool_name in active_tools
        ]
        gates = ["revocation_check", "lifecycle_state", "security_policy", "ssrf_check", "caller_permissions"]
        if approved_by:
            gates.append("human_approval")
        verification: Dict[str, Any] = {
            "gates_passed": gates,
            "policy_verdict": pol_eval.overall_verdict.value,
            "max_risk": pol_eval.max_risk.value,
            "capabilities_evaluated": pol_eval.capabilities_requested,
            "tools_authorized": authorized,
            "approved_by": approved_by,
            "postconditions": "not_evaluated",
            "verified": False,
        }

        loaded = load_skill(self.workspace_root / "skills", skill)
        instructions = (getattr(loaded, "body", "") or "") if loaded else ""
        cost: Dict[str, Any] = {
            "instruction_chars": len(instructions),
            "estimated_tokens": -(-len(instructions) // 4),
            "tokens_are_estimate": True,
            "tool_calls": 0,
        }

        # ── 4a. Dry run: evaluate gates only ─────────────────────────────────
        if dry_run:
            duration_ms = (time.perf_counter() - t0) * 1000
            self._log_audit(audit_id, skill, "simulated", duration_ms, session_id,
                            pol_eval.overall_verdict.value, [], approved_by=approved_by)
            return ExecutionResult(
                status="simulated",
                skill=skill,
                outputs={
                    "plan": {
                        "would_execute_with": "executor" if skill in self._executors else "agent_instructions",
                        "declared_outputs": list(entry.outputs),
                        "capabilities": pol_eval.capabilities_requested,
                    }
                },
                verification=verification,
                cost=cost,
                duration_ms=duration_ms,
                audit_id=audit_id,
            )

        executor = self._executors.get(skill)

        # ── 4b. No executor: hand the instruction bundle to the calling agent ─
        if executor is None:
            duration_ms = (time.perf_counter() - t0) * 1000
            self._log_audit(audit_id, skill, "prepared", duration_ms, session_id,
                            pol_eval.overall_verdict.value, [], approved_by=approved_by)
            return ExecutionResult(
                status="prepared",
                skill=skill,
                outputs={
                    "instructions": instructions,
                    "skill_path": entry.path,
                    "inputs": context,
                    "declared_outputs": list(entry.outputs),
                    "note": "No executor is registered for this skill; the calling agent must carry out these instructions.",
                },
                artifacts=[],
                verification=verification,
                cost=cost,
                duration_ms=duration_ms,
                audit_id=audit_id,
            )

        # ── 4c. Real execution through the registered executor ───────────────
        invocation = SkillInvocation(
            skill=entry,
            inputs=context,
            instructions=instructions,
            authorized_capabilities=list(pol_eval.capabilities_requested),
            session_id=session_id,
            audit_id=audit_id,
        )
        try:
            raw_result = executor(invocation)
        except Exception as exc:
            duration_ms = (time.perf_counter() - t0) * 1000
            err_msg = f"Executor for '{skill}' raised {type(exc).__name__}: {exc}"
            self._log_audit(audit_id, skill, "failed", duration_ms, session_id,
                            pol_eval.overall_verdict.value, [], err_msg, approved_by)
            return ExecutionResult(status="failed", skill=skill, verification=verification, cost=cost,
                                   duration_ms=duration_ms, audit_id=audit_id, error=err_msg, executed=True)

        result_map = dict(raw_result or {})
        outputs = result_map.get("outputs")
        outputs = dict(outputs) if isinstance(outputs, Mapping) else {}
        tool_calls = [dict(tc) for tc in result_map.get("tool_calls", []) if isinstance(tc, Mapping)]
        artifacts = [dict(a) for a in result_map.get("artifacts", []) if isinstance(a, Mapping)]
        usage = result_map.get("usage")
        cost.update({"tool_calls": len(tool_calls)})
        if isinstance(usage, Mapping):
            cost["executor_usage"] = dict(usage)

        missing = [name for name in entry.outputs if isinstance(name, str) and name not in outputs]
        violations = tool_call_violations(tool_calls, pol_eval.tools or active_tools, pol_eval.capabilities_requested)
        verification["postconditions"] = "failed" if missing or violations else "passed"
        verification["verified"] = not missing and not violations
        verification["missing_outputs"] = missing
        verification["capability_violations"] = violations
        status = "failed" if missing or violations else "completed"
        problems = []
        if violations:
            problems.append(f"reported tool calls outside its authorisation: {'; '.join(violations)}")
        if missing:
            problems.append(f"did not return declared outputs: {', '.join(missing)}")
        err = f"Executor for '{skill}' " + " and ".join(problems) if problems else None

        duration_ms = (time.perf_counter() - t0) * 1000
        self._log_audit(audit_id, skill, status, duration_ms, session_id,
                        pol_eval.overall_verdict.value, tool_calls, err, approved_by)
        return ExecutionResult(
            status=status,
            skill=skill,
            outputs=outputs,
            artifacts=artifacts,
            tool_calls=tool_calls,
            verification=verification,
            cost=cost,
            duration_ms=duration_ms,
            audit_id=audit_id,
            error=err,
            executed=True,
        )

    def _approval_required(
        self,
        skill: str,
        pol_eval: PolicyEvaluationResult,
        request_id: str,
        t0: float,
        audit_id: str,
        session_id: Optional[str],
    ) -> ExecutionResult:
        ask_caps = [cap for cap, info in pol_eval.breakdown.items() if info.get("verdict") == PolicyVerdict.ASK.value]
        err_msg = (
            f"Skill '{skill}' requires human approval for: {', '.join(ask_caps) or 'unclassified capabilities'}. "
            f"Re-run with approval request_id={request_id} and approved_by=<name>."
        )
        duration_ms = (time.perf_counter() - t0) * 1000
        self._log_audit(audit_id, skill, "approval_required", duration_ms, session_id, "ASK", [], err_msg)
        return ExecutionResult(
            status="approval_required",
            skill=skill,
            duration_ms=duration_ms,
            audit_id=audit_id,
            error=err_msg,
            approval_request={
                "request_id": request_id,
                "capabilities": ask_caps,
                "reasons": list(pol_eval.reasons),
            },
        )

    def simulate(
        self,
        skill: str,
        input: Optional[Dict[str, Any]] = None,
        permissions: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """Evaluate every gate for ``skill`` without executing anything."""
        res = self.execute(skill=skill, input=input, permissions=permissions, dry_run=True)
        policy_eval = self.policy_engine.evaluate_skill(skill)
        return {
            "skill": skill,
            "simulation_status": "would_succeed" if res.status == "simulated" else (
                "needs_approval" if res.status == "approval_required" else "would_fail"
            ),
            "execution_status": res.status,
            "error": res.error,
            "verdict": policy_eval.overall_verdict.value,
            "max_risk": policy_eval.max_risk.value,
            "capabilities_required": policy_eval.capabilities_requested,
            "reasons": policy_eval.reasons,
            "approval_request": res.approval_request,
        }
