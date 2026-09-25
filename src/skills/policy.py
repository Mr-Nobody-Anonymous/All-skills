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


class AutonomyLevel(str, Enum):
    L0_INFORMATIONAL = "L0_INFORMATIONAL"
    L1_READ = "L1_READ"
    L2_LOCAL_WRITE = "L2_LOCAL_WRITE"
    L3_EXTERNAL = "L3_EXTERNAL"
    L4_PRODUCTION = "L4_PRODUCTION"


AUTONOMY_ALLOWED_CAPABILITIES: Dict[AutonomyLevel, Set[str]] = {
    AutonomyLevel.L0_INFORMATIONAL: set(),
    AutonomyLevel.L1_READ: {"filesystem.read", "git.read"},
    AutonomyLevel.L2_LOCAL_WRITE: {"filesystem.read", "filesystem.write", "git.read", "git.write", "shell.execute"},
    AutonomyLevel.L3_EXTERNAL: {"filesystem.read", "filesystem.write", "git.read", "git.write", "shell.execute", "network.request"},
    AutonomyLevel.L4_PRODUCTION: {
        "filesystem.read", "filesystem.write", "git.read", "git.write",
        "shell.execute", "network.request", "secret.access", "deployment.execute",
    },
}


def enforce_autonomy(requested_level: AutonomyLevel, capabilities: List[str]) -> tuple[bool, str]:
    """Validate whether requested capabilities are within bounds of autonomy level."""
    allowed = AUTONOMY_ALLOWED_CAPABILITIES.get(requested_level, set())
    for cap in capabilities:
        if cap not in allowed:
            return False, f"Capability '{cap}' exceeds permitted boundary for autonomy level '{requested_level.value}'."
    return True, "valid"


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
    },
    "tool.unclassified": {
        "verdict": PolicyVerdict.ASK,
        "risk": RiskLevel.HIGH_RISK,
        "description": "A tool with no capability mapping. Never allowed implicitly; requires explicit approval."
    },
}

UNCLASSIFIED_CAPABILITY = "tool.unclassified"

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
    "credentials": ["credentials.read"],
    # Common aliases used by agent harnesses
    "read_file": ["filesystem.read"],
    "write_file": ["filesystem.write"],
    "edit_file": ["filesystem.write"],
    "grep": ["filesystem.read"],
    "glob": ["filesystem.read"],
    "web_search": ["network.request"],
    "web_fetch": ["network.request"],
    "shell": ["shell.execute"],
}

# Harness / platform names are sometimes (wrongly) listed under ``tools``. They
# name the agent that runs the skill and grant no capability.
PLATFORM_NAMES = {
    "antigravity", "claude", "claude-code", "cline", "codex", "codex-cli", "copilot",
    "cursor", "gemini", "gemini-cli", "goose", "opencode", "roo", "vscode", "windsurf",
}


class PolicyConfigError(ValueError):
    """A policy input (policy.json, manifest.json, registry) is malformed."""


def capabilities_for_tool(tool: str) -> List[str]:
    """Capabilities a declared tool requires. Unknown tools are never implicitly allowed."""
    tl = str(tool).strip().lower()
    if tl in TOOL_TO_CAPABILITIES:
        return list(TOOL_TO_CAPABILITIES[tl])
    if tl in PLATFORM_NAMES:
        return []
    if "deploy" in tl or "production" in tl:
        return ["production.deploy"]
    if "credential" in tl or "secret" in tl:
        return ["credentials.read"]
    return [UNCLASSIFIED_CAPABILITY]


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
        """Merge ``skills/policy.json``. Malformed policy raises PolicyConfigError.

        Silently ignoring a broken policy file would drop any restrictions it
        adds, so the engine refuses to run instead (fail closed).
        """
        policy_file = self.workspace_root / "skills" / "policy.json"
        if not policy_file.exists():
            return
        try:
            data = json.loads(policy_file.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise PolicyConfigError(f"{policy_file}: unreadable policy file: {exc}") from exc
        capabilities = data.get("capabilities", {}) if isinstance(data, dict) else None
        if not isinstance(capabilities, dict):
            raise PolicyConfigError(f"{policy_file}: 'capabilities' must be an object")
        for cap, pdata in capabilities.items():
            if not isinstance(pdata, dict):
                raise PolicyConfigError(f"{policy_file}: policy for '{cap}' must be an object")
            verdict_str = str(pdata.get("verdict", "ASK")).upper()
            risk_str = str(pdata.get("risk", "MEDIUM_RISK")).upper()
            if verdict_str not in PolicyVerdict.__members__:
                raise PolicyConfigError(f"{policy_file}: invalid verdict '{verdict_str}' for '{cap}'")
            if risk_str not in RiskLevel.__members__:
                raise PolicyConfigError(f"{policy_file}: invalid risk '{risk_str}' for '{cap}'")
            self.policies[cap] = {
                "verdict": PolicyVerdict[verdict_str],
                "risk": RiskLevel[risk_str],
                "description": pdata.get("description", ""),
            }

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
                except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
                    raise PolicyConfigError(f"{manifest_file}: unreadable manifest: {exc}") from exc
                skill_info = m.get("skills", {}).get(skill_id, {}) if isinstance(m, dict) else {}
                tools.extend(skill_info.get("tools", []) or [])

        # Check frontmatter if still empty
        if not tools:
            skill_md = self.workspace_root / ".agents" / "skills" / skill_id / "SKILL.md"
            if not skill_md.exists():
                skill_md = self.workspace_root / "skills" / skill_id.replace(".", "/") / "SKILL.md"
            if skill_md.exists():
                from .frontmatter import parse_frontmatter

                try:
                    meta, _ = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
                except (OSError, UnicodeDecodeError) as exc:
                    raise PolicyConfigError(f"{skill_md}: unreadable skill manifest: {exc}") from exc
                declared = meta.get("tools", []) or []
                tools.extend([declared] if isinstance(declared, str) else list(declared))

        # If still empty, default to read/edit capabilities
        if not tools:
            tools = ["file_read", "file_edit"]

        # 2. Derive requested capabilities
        caps_requested: Set[str] = set()
        for t in tools:
            caps_requested.update(capabilities_for_tool(t))

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

        # Check negative capabilities (forbidden)
        from .registry import load_registry

        entry = load_registry(self.workspace_root).get(skill_id)  # corrupt registry raises
        forbidden_caps: List[str] = list(getattr(entry, "forbidden", []) or []) if entry else []

        for f_cap in forbidden_caps:
            if f_cap in caps_requested:
                overall = PolicyVerdict.DENY
                reasons.append(f"Negative capability violation: capability '{f_cap}' is explicitly forbidden for skill '{skill_id}'.")

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
