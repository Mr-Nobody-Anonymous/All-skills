#!/usr/bin/env python3
"""Comprehensive Skill Security & Prompt Injection Scanner.

Statically analyzes SKILL.md and associated files across:
- skills/ (Canonical skills)
- .agents/skills/ (Active harness skills)

Detects:
- Prompt injection vectors & jailbreak tags
- Destructive shell commands (rm -rf /, mkfs, dd)
- Pipe-to-shell payloads (curl | sh, wget | bash)
- Hardcoded secrets, private keys, and cloud API tokens
- Webhook exfiltration and hidden base64 payloads

Usage:
    python scripts/scan_skills_security.py
    python scripts/scan_skills_security.py --strict
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from skills.registry import load_registry
from skills.security import scan_all, scan_skill, SkillEntry


def scan_active_skills() -> list:
    active_root = REPO_ROOT / ".agents" / "skills"
    findings = []
    if not active_root.exists():
        return findings

    for skill_dir in active_root.iterdir():
        if not skill_dir.is_dir() or not (skill_dir / "SKILL.md").exists():
            continue
        mock_entry = SkillEntry(
            id=f"active.{skill_dir.name}",
            name=skill_dir.name,
            category="active",
            description="",
            path=f".agents/skills/{skill_dir.name}"
        )
        findings.extend(scan_skill(mock_entry, skill_dir))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Skill Security Scanner")
    parser.add_argument("--strict", action="store_true", help="Fail on warnings as well as high-severity findings")
    args = parser.parse_args()

    print("=" * 65)
    print("🛡️  ALL SKILLS — STATIC SECURITY & PROMPT INJECTION SCANNER")
    print("=" * 65)

    reg = load_registry(REPO_ROOT)
    canonical_findings = scan_all(reg, REPO_ROOT / "skills")
    active_findings = scan_active_skills()
    all_findings = canonical_findings + active_findings

    high_findings = [f for f in all_findings if f.severity == "high"]
    warn_findings = [f for f in all_findings if f.severity == "warn"]

    print(f"Scanned {len(reg.entries)} canonical skills and {len(list((REPO_ROOT / '.agents' / 'skills').iterdir()))} active skills.")
    print(f"High Severity Findings:   {len(high_findings)}")
    print(f"Warning Findings:         {len(warn_findings)}")

    if high_findings:
        print("\n❌ CRITICAL / HIGH FINDINGS:")
        for f in high_findings:
            print(f"  [{f.skill_id}] {f.path}: {f.label}")

    if warn_findings:
        print("\n⚠️  WARNING FINDINGS (Audited):")
        for f in warn_findings[:15]:
            print(f"  [{f.skill_id}] {f.path}: {f.label}")
        if len(warn_findings) > 15:
            print(f"  ... and {len(warn_findings) - 15} more warnings.")

    print("\n" + "=" * 65)
    if high_findings:
        print("❌ FAILED: High-severity security issues detected!")
        return 1

    if args.strict and warn_findings:
        print("❌ FAILED: Strict mode enabled and warnings were found.")
        return 1

    print("✅ PASSED: No malicious patterns or high-severity vulnerabilities found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
