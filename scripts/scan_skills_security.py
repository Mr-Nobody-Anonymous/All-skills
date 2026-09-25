#!/usr/bin/env python3
"""Comprehensive Skill Security & Prompt Injection Scanner.

Statically analyzes every file (including dotfiles) of:
- skills/ (canonical skills)
- .agents/skills/ (active harness skills)

Detects prompt-injection vectors, destructive shell commands, pipe-to-shell
payloads, hardcoded secrets and private keys, webhook exfiltration and hidden
base64 payloads. Nothing is ever executed.

Gate semantics:
- High-severity findings fail the scan.
- Incomplete scans (oversized or unreadable files) fail the scan: an
  unscanned package is never reported as clean.
- ``--strict`` (used in CI) also fails on warnings that are not covered by the
  maintainer-reviewed allowlist in ``registry/security_allowlist.json``.
Files cannot exempt themselves; allowlisted findings are still reported as
"suppressed", and each exception is pinned to the reviewed file's SHA-256.

Usage:
    python scripts/scan_skills_security.py
    python scripts/scan_skills_security.py --strict
    python scripts/scan_skills_security.py --json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from skills.registry import load_registry  # noqa: E402
from skills.security import (  # noqa: E402
    INCOMPLETE,
    Finding,
    SkillEntry,
    apply_allowlist,
    load_allowlist,
    scan_skill,
)


def collect(root: Path) -> tuple[List[Finding], Dict[str, Path]]:
    """Scan canonical and active skills; return findings and skill folders by id."""
    findings: List[Finding] = []
    dirs: Dict[str, Path] = {}
    reg = load_registry(root)
    for entry in reg.entries:
        skill_dir = root / "skills" / Path(*entry.path.split("/"))
        dirs[entry.id] = skill_dir
        findings.extend(scan_skill(entry, skill_dir))
    active_root = root / ".agents" / "skills"
    if active_root.exists():
        for skill_dir in sorted(active_root.iterdir()):
            if not skill_dir.is_dir() or not (skill_dir / "SKILL.md").exists():
                continue
            entry = SkillEntry(id=f"active.{skill_dir.name}", name=skill_dir.name, category="active",
                               description="", path=f".agents/skills/{skill_dir.name}")
            dirs[entry.id] = skill_dir
            findings.extend(scan_skill(entry, skill_dir))
    return findings, dirs


def main() -> int:
    parser = argparse.ArgumentParser(description="Skill Security Scanner")
    parser.add_argument("--strict", action="store_true",
                        help="Also fail on warnings not covered by registry/security_allowlist.json")
    parser.add_argument("--json", action="store_true", help="Print a machine-readable report")
    parser.add_argument("--root", type=Path, default=REPO_ROOT, help=argparse.SUPPRESS)
    args = parser.parse_args()

    findings, dirs = collect(args.root)
    active, suppressed, stale = apply_allowlist(findings, load_allowlist(args.root), dirs)
    high = [f for f in active if f.severity == "high"]
    incomplete = [f for f in active if f.severity == INCOMPLETE]
    warnings = [f for f in active if f.severity not in ("high", INCOMPLETE)]

    failed_reasons = []
    if high:
        failed_reasons.append(f"{len(high)} high-severity finding(s)")
    if incomplete:
        failed_reasons.append(f"{len(incomplete)} file(s) could not be scanned")
    if args.strict and warnings:
        failed_reasons.append(f"{len(warnings)} unreviewed warning(s) in strict mode")

    if args.json:
        as_dict = lambda f: {"skill_id": f.skill_id, "path": f.path, "label": f.label, "severity": f.severity}  # noqa: E731
        print(json.dumps({
            "skills_scanned": len(dirs),
            "passed": not failed_reasons,
            "high": [as_dict(f) for f in high],
            "incomplete": [as_dict(f) for f in incomplete],
            "warnings": [as_dict(f) for f in warnings],
            "suppressed": [as_dict(f) for f in suppressed],
            "stale_allowlist_entries": stale,
        }, indent=2))
        return 1 if failed_reasons else 0

    print("=" * 65)
    print("🛡️  ALL SKILLS — STATIC SECURITY & PROMPT INJECTION SCANNER")
    print("=" * 65)
    print(f"Scanned {len(dirs)} skills (canonical + active), every file incl. dotfiles.")
    print(f"High severity (unreviewed):   {len(high)}")
    print(f"Incomplete scans:             {len(incomplete)}")
    print(f"Warnings (unreviewed):        {len(warnings)}")
    print(f"Suppressed by allowlist:      {len(suppressed)}")
    for title, items in (("❌ HIGH FINDINGS", high), ("❌ NOT SCANNED", incomplete), ("⚠️  UNREVIEWED WARNINGS", warnings)):
        if items:
            print(f"\n{title}:")
            for f in items:
                print(f"  [{f.skill_id}] {f.path}: {f.label}")
    if stale:
        print(f"\nℹ️  {len(stale)} allowlist entr{'y' if len(stale) == 1 else 'ies'} no longer match "
              "(file changed or finding fixed) — review registry/security_allowlist.json:")
        for entry in stale:
            print(f"  [{entry['skill']}] {entry['path']}: {entry['label']}")

    print("\n" + "=" * 65)
    if failed_reasons:
        print(f"❌ FAILED: {'; '.join(failed_reasons)}.")
        return 1
    print("✅ PASSED: no unreviewed high-severity findings and every file was scanned.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
