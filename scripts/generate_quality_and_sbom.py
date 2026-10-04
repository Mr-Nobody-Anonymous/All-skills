"""Generate registry/quality.json and registry/sbom.json.

Pre-computes authoritative empirical quality cards and CycloneDX Software Bill of
Materials across all skills in the platform.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))
sys.path.insert(0, str(REPO_ROOT))

from skills.quality import score_entry
from skills.registry import load_registry
from skills.supply_chain import SupplyChainSecurityEngine


def generate():
    registry = load_registry(REPO_ROOT)
    skills_root = REPO_ROOT / "skills"
    reg_dir = REPO_ROOT / "registry"
    reg_dir.mkdir(parents=True, exist_ok=True)

    print(f"Generating empirical quality reports for {len(registry.entries)} skills...")
    quality_map = {}
    for entry in registry.entries:
        skill_dir = skills_root / Path(*entry.path.split("/"))
        if not skill_dir.exists():
            skill_dir = skills_root / entry.id

        rep = score_entry(entry, skill_dir)
        d = rep.to_dict()
        d["display_card"] = rep.to_display_card()
        quality_map[entry.id] = d

    quality_file = reg_dir / "quality.json"
    quality_file.write_text(json.dumps({
        "platform_version": "3.0.0",
        "total_skills_scored": len(quality_map),
        "quality_scores": quality_map,
    }, indent=2), encoding="utf-8")
    print(f"[SUCCESS] Wrote quality metrics to {quality_file}")

    print("Generating CycloneDX Software Bill of Materials (SBOM)...")
    sc = SupplyChainSecurityEngine(REPO_ROOT)
    sbom = sc.generate_repository_sbom()
    sbom_file = reg_dir / "sbom.json"
    sbom_file.write_text(json.dumps(sbom, indent=2), encoding="utf-8")
    print(f"[SUCCESS] Wrote SBOM to {sbom_file} ({len(sbom.get('components', []))} components)")


if __name__ == "__main__":
    generate()
