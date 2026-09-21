"""Capability-based execution policy engine for AI agent skills.

Evaluates requested tool and system capabilities against declared security policies,
returning deterministic execution verdicts: ALLOW, ASK, or DENY.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Set


class PolicyVerdict(str, Enum):
    ALLOW = "ALLOW"
    ASK = "ASK"
    DENY = "DENY"


class RiskLevel(str, Enum):
    SAFE = "SAFE"
    LOW_RISK = "LOW_RISK"
    MEDIUM_RISK = "MEDIUM_RISK"
    HIGH_RISK = "HIGH_RISK"
    CRITICAL = "CRITICAL"


# Default capability classifications and baseline policies
DEFAULT_CAPABILITY_POLICIES: Dict[str, dict] = {
    "filesystem.read": {
        "verdict": PolicyVerdict.ALLOW,
        "risk": RiskLevel.SAFE,
        "description": "Read workspace source files, documentation, and metadata."
    },
    "filesystem.write": {
        "verdict": PolicyVerdict.ALLOW,
        "risk": RiskLevel.LOW_RISK,
        "description": "Modify or create workspace files within workspace boundaries."
    },
    "git.read": {
        "verdict": PolicyVerdict.ALLOW,
        "risk": RiskLevel.SAFE,
        "description": "Inspect git status, log, diff, and branches."
    },
    "git.write": {
        "verdict": PolicyVerdict.ALLOW,
        "risk": RiskLevel.LOW_RISK,
        "description": "Create commits, branches, or stage changes."
    },
    "shell.execute": {
        "verdict": PolicyVerdict.ALLOW,
        "risk": RiskLevel.MEDIUM_RISK,
        "description": "Execute non-destructive development commands (tests, linters, builds)."
    },
    "network.request": {
        "verdict": PolicyVerdict.ALLOW,
        "risk": RiskLevel.MEDIUM_RISK,
        "description": "Issue external HTTP/API requests for docs or package info."
    },
    "credentials.read": {
        "verdict": PolicyVerdict.DENY,
        "risk": RiskLevel.HIGH_RISK,
        "description": "Read raw environment secrets, SSH keys, or cloud credentials."
    },
    "cloud.modify": {
        "verdict": PolicyVerdict.ASK,
        "risk": RiskLevel.HIGH_RISK,
        "description": "Provision, modify, or tear down cloud resources."
    },
    "production.deploy": {
        "verdict": PolicyVerdict.ASK,
        "risk": RiskLevel.CRITICAL,
        "description": "Trigger deployments to production environments."
    },
    "database.delete": {
        "verdict": PolicyVerdict.DENY,
        "risk": RiskLevel.CRITICAL,
        "description": "Drop tables, truncate databases, or execute irreversible data purges."
    }
}

# Map harness tools to capability sets
TOOL_TO_CAPABILITIES: Dict[str, List[str]] = {
    "file_read": ["filesystem.read"],
    "file_write": ["filesystem.write"],
    "file_edit": ["filesystem.write"],
    "ast_grep": ["filesystem.read"],
    "read_url": ["network.request"],
    "browser": ["network.request"],
    "generate_image": ["filesystem.write"],
    "bash": ["shell.execute"],
    "terminal": ["shell.execute"],
    "mcp_call": ["network.request"],
    "manage_task": ["shell.execute"],
    "git": ["git.read", "git.write"],
    "docker": ["shell.execute"],
    "deploy": ["production.deploy"],
    "credentials": ["credentials.read"]
}


@dataclass
class PolicyEvaluationResult:
    skill_id: str
    overall_verdict: PolicyVerdict
    max_risk: RiskLevel
    capabilities_requested: List[str]
    breakdown: Dict[str, dict] = field(default_factory=dict)
    reasons: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "skill_id": self.skill_id,
            "overall_verdict": self.overall_verdict.value,
            "max_risk": self.max_risk.value,
            "capabilities_requested": self.capabilities_requested,
            "breakdown": self.breakdown,
            "reasons": self.reasons
        }


class PolicyEngine:
    """Enforces capability security policies at execution time."""

    def __init__(self, workspace_root: Optional[Path] = None) -> None:
        self.workspace_root = workspace_root or Path.cwd()
        self.policies = dict(DEFAULT_CAPABILITY_POLICIES)
        self._load_custom_policy()

    def _load_custom_policy(self) -> None:
        policy_file = self.workspace_root / "skills" / "policy.json"
        if policy_file.exists():
            try:
                data = json.loads(policy_file.read_text(encoding="utf-8"))
                for cap, pdata in data.get("capabilities", {}).items():
                    verdict_str = pdata.get("verdict", "ALLOW").upper()
                    verdict = getattr(PolicyVerdict, verdict_str, PolicyVerdict.ASK)
                    risk_str = pdata.get("risk", "MEDIUM_RISK").upper()
                    risk = getattr(RiskLevel, risk_str, RiskLevel.MEDIUM_RISK)
                    self.policies[cap] = {
                        "verdict": verdict,
                        "risk": risk,
                        "description": pdata.get("description", "")
                    }
            except Exception:
                pass

    def evaluate_skill(self, skill_id: str, declared_tools: Optional[List[str]] = None) -> PolicyEvaluationResult:
        """Evaluate permissions required for a skill."""
        # 1. Discover declared tools if not passed
        tools = list(declared_tools or [])
        if not tools:
            # Check manifest.json
            manifest_file = self.workspace_root / "manifest.json"
            if manifest_file.exists():
                try:
                    m = json.loads(manifest_file.read_text(encoding="utf-8"))
                    skill_info = m.get("skills", {}).get(skill_id, {})
                    tools.extend(skill_info.get("tools", []))
                except Exception:
                    pass

        # Check frontmatter if still empty
        if not tools:
            skill_md = self.workspace_root / ".agents" / "skills" / skill_id / "SKILL.md"
            if not skill_md.exists():
                skill_md = self.workspace_root / "skills" / skill_id.replace(".", "/") / "SKILL.md"
            if skill_md.exists():
                try:
                    from .frontmatter import parse_frontmatter
                    meta, _ = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
                    tools.extend(meta.get("tools", []))
                except Exception:
                    pass

        # If still empty, default to read/edit capabilities
        if not tools:
            tools = ["file_read", "file_edit"]

        # 2. Derive requested capabilities
        caps_requested: Set[str] = set()
        for t in tools:
            tl = t.lower()
            if tl in TOOL_TO_CAPABILITIES:
                caps_requested.update(TOOL_TO_CAPABILITIES[tl])
            elif "deploy" in tl or "production" in tl:
                caps_requested.add("production.deploy")
            elif "credential" in tl or "secret" in tl:
                caps_requested.add("credentials.read")
            else:
                caps_requested.add("shell.execute")

        # Check specific sensitive skills
        if "deploy" in skill_id or "production" in skill_id:
            caps_requested.add("production.deploy")
        if "secrets" in skill_id or "credential" in skill_id:
            caps_requested.add("credentials.read")

        # 3. Evaluate each capability
        overall = PolicyVerdict.ALLOW
        max_risk = RiskLevel.SAFE
        breakdown: Dict[str, dict] = {}
        reasons: List[str] = []

        risk_order = [
            RiskLevel.SAFE,
            RiskLevel.LOW_RISK,
            RiskLevel.MEDIUM_RISK,
            RiskLevel.HIGH_RISK,
            RiskLevel.CRITICAL
        ]

        for cap in sorted(caps_requested):
            policy = self.policies.get(cap, {
                "verdict": PolicyVerdict.ASK,
                "risk": RiskLevel.MEDIUM_RISK,
                "description": "Unclassified capability"
            })
            verdict = policy["verdict"]
            risk = policy["risk"]

            breakdown[cap] = {
                "verdict": verdict.value if isinstance(verdict, PolicyVerdict) else str(verdict),
                "risk": risk.value if isinstance(risk, RiskLevel) else str(risk),
                "description": policy["description"]
            }

            # Update highest risk
            if risk_order.index(risk) > risk_order.index(max_risk):
                max_risk = risk

            # Policy verdict precedence: DENY > ASK > ALLOW
            if verdict == PolicyVerdict.DENY:
                overall = PolicyVerdict.DENY
                reasons.append(f"Capability '{cap}' is strictly DENIED by security policy.")
            elif verdict == PolicyVerdict.ASK and overall != PolicyVerdict.DENY:
                overall = PolicyVerdict.ASK
                reasons.append(f"Capability '{cap}' requires explicit USER confirmation.")

        if not reasons:
            reasons.append("All requested capabilities are pre-authorized (ALLOW).")

        return PolicyEvaluationResult(
            skill_id=skill_id,
            overall_verdict=overall,
            max_risk=max_risk,
            capabilities_requested=sorted(caps_requested),
            breakdown=breakdown,
            reasons=reasons
        )

    def explain_policy(self, skill_id: str) -> dict:
        """Structured policy simulation explaining permission and risk boundaries."""
        res = self.evaluate_skill(skill_id)
        return {
            "skill_id": skill_id,
            "overall_verdict": res.overall_verdict.value,
            "max_risk": res.max_risk.value,
            "capabilities": res.breakdown,
            "reasons": res.reasons,
        }


import ipaddress
import os
import urllib.parse


def validate_network_target(url_or_host: str) -> tuple[bool, str]:
    """Inspect destination host for SSRF hazards, loopback, link-local, and cloud metadata."""
    target = url_or_host.strip()
    if "://" in target:
        parsed = urllib.parse.urlparse(target)
        host = parsed.hostname or ""
    else:
        host = target.split(":")[0]

    host_lower = host.lower()
    if host_lower in {"localhost", "metadata.google.internal", "169.254.169.254", "0.0.0.0"}:
        return False, f"SSRF blocked: access to '{host}' is forbidden"

    try:
        ip = ipaddress.ip_address(host_lower)
        if ip.is_loopback or ip.is_private or ip.is_link_local or ip.is_reserved or ip.is_multicast:
            return False, f"SSRF blocked: '{host}' is a non-routable or private IP address"
    except ValueError:
        pass

    return True, "valid"


def broker_secrets(skill_id: str, declared_secrets: Optional[List[str]] = None) -> Dict[str, str]:
    """Brokers ONLY explicitly declared credentials for a skill, isolating the environment."""
    brokered: Dict[str, str] = {}
    if not declared_secrets:
        return brokered
    for sec_name in declared_secrets:
        val = os.environ.get(sec_name)
        if val:
            brokered[sec_name] = val
    return brokered


def save_default_policy(repo_root: Path) -> Path:
    out_file = repo_root / "skills" / "policy.json"
    data = {
        "version": 1,
        "description": "Formal capability policy configuration for agent execution.",
        "capabilities": {
            k: {
                "verdict": v["verdict"].value,
                "risk": v["risk"].value,
                "description": v["description"]
            }
            for k, v in DEFAULT_CAPABILITY_POLICIES.items()
        }
    }
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        f.write("\n")
    return out_file
