"""Compatibility evidence: configured and discoverable are verified; nothing is claimed without evidence.

Levels (see compatibility/matrix.json):
- configured          adapter configuration exists and validates
- discoverable        the agent's skills directory is linked to the source harness and
                      every active SKILL.md meets the Agent Skills format
- invocable           manual check in a named agent version (recorded evidence only)
- workflow_completed  manual end-to-end task in a named agent version (recorded evidence only)
"""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

import yaml

_ROOT = Path(__file__).resolve().parents[1]
MATRIX = json.loads((_ROOT / "compatibility" / "matrix.json").read_text(encoding="utf-8"))
AGENTS = json.loads((_ROOT / "registry" / "agents.json").read_text(encoding="utf-8"))["agents"]
PLATFORMS = yaml.safe_load((_ROOT / "platforms" / "platforms.yaml").read_text(encoding="utf-8"))
NAME_RE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")


def skills_paths(agent: dict) -> list[str]:
    adapter = yaml.safe_load((_ROOT / agent["adapter"]).read_text(encoding="utf-8"))
    return [p for p in (adapter.get("discovery_paths") or {}).get("workspace", []) if p.endswith("/skills")]


class TestDiscoverability(unittest.TestCase):
    def test_every_agent_skills_directory_is_linked_to_the_source_harness(self):
        source = PLATFORMS["source_harness"]["path"]
        linked = {t["path"] for t in PLATFORMS["local_targets"]}
        self.assertTrue((_ROOT / source).is_dir())
        for key, agent in AGENTS.items():
            paths = skills_paths(agent)
            self.assertTrue(paths, f"{key}: adapter declares no workspace skills directory")
            for path in paths:
                self.assertIn(path, linked, f"{key}: {path} is not linked by platforms.yaml")

    def test_active_skills_meet_the_agent_skills_format(self):
        problems = []
        for skill_md in sorted((_ROOT / ".agents" / "skills").glob("*/SKILL.md")):
            block = re.match(r"^---\s*\n(.*?)\n---", skill_md.read_text(encoding="utf-8"), re.S)
            meta = yaml.safe_load(block.group(1)) if block else None
            if not isinstance(meta, dict):
                problems.append(f"{skill_md.parent.name}: frontmatter does not parse")
                continue
            name, desc = str(meta.get("name", "")), str(meta.get("description", ""))
            if not NAME_RE.fullmatch(name) or len(name) > 64 or name != skill_md.parent.name:
                problems.append(f"{skill_md.parent.name}: invalid name {name!r}")
            if not 0 < len(desc) <= 1024:
                problems.append(f"{skill_md.parent.name}: description length {len(desc)}")
        self.assertEqual(problems, [])


class TestCompatibilityClaims(unittest.TestCase):
    def test_matrix_matches_verifiable_evidence(self):
        self.assertEqual(set(MATRIX["platforms"]), set(AGENTS))
        linked = {t["path"] for t in PLATFORMS["local_targets"]}
        for key, claim in MATRIX["platforms"].items():
            self.assertTrue((_ROOT / claim["adapter"]).is_file(), key)
            self.assertEqual(claim["configured"], True, key)
            paths = skills_paths(AGENTS[key])
            self.assertEqual(claim["discoverable"], bool(paths) and all(p in linked for p in paths), key)

    def test_manual_levels_require_recorded_evidence(self):
        evidence = MATRIX["manual_evidence"]
        for entry in evidence:
            for field in ("platform", "level", "agent_version", "date", "verified_by", "skill"):
                self.assertTrue(entry.get(field), f"evidence entry missing {field}: {entry}")
            self.assertRegex(entry["date"], r"^\d{4}-\d{2}-\d{2}$")
        for key, claim in MATRIX["platforms"].items():
            for level in ("invocable", "workflow_completed"):
                if claim[level]:
                    self.assertTrue(any(e["platform"] == key and e["level"] == level for e in evidence),
                                    f"{key} claims {level} without recorded evidence")


if __name__ == "__main__":
    unittest.main()
