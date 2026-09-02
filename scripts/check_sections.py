#!/usr/bin/env python3
"""Check which required sections are missing from each SKILL.md."""
import re
import sys
from pathlib import Path

REQUIRED = [
    "Purpose", "When to Use", "When NOT to Use", "Capabilities",
    "Inputs", "Workflow", "Tools", "Examples", "Safety", "Source", "Notes"
]

ROOT = Path(__file__).resolve().parents[1]
skills_root = ROOT / "skills"

results = []
for p in sorted(skills_root.rglob("SKILL.md")):
    if "_quarantine" in p.parts:
        continue
    rel = str(p.parent.relative_to(skills_root)).replace("\\", "/")
    text = p.read_text(encoding="utf-8")
    headings = {m.group(1).strip().lower() for m in re.finditer(r"^##\s+(.+?)\s*$", text, re.MULTILINE)}
    missing = [s for s in REQUIRED if s.lower() not in headings]
    has_readme = (p.parent / "README.md").exists()
    results.append((rel, missing, has_readme))

print(f"{'Path':<50} {'Has README':<12} Missing sections")
print("-" * 120)
for rel, missing, has_readme in results:
    rm = "yes" if has_readme else "NO"
    miss = ", ".join(missing) if missing else "-"
    print(f"{rel:<50} {rm:<12} {miss}")

print(f"\nTotal: {len(results)} skills")
print(f"With missing sections: {len([1 for _, m, _ in results if m])}")
print(f"Missing README: {len([1 for _, _, r in results if not r])}")