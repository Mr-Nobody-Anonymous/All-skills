#!/usr/bin/env python3
"""Generate the harness compatibility matrix from recorded evidence.

Why this exists
---------------
The multi-agent support table in `README.md` used to be hand-written, and it
drifted from the evidence in `compatibility/matrix.json` in both directions:

* it claimed **Tier 4 Verified** for Claude Code, Cursor, Codex and Gemini while
  `matrix.json` recorded `invocable: null` and `workflow_completed: null` for
  every platform and held **zero** `manual_evidence` entries — a verification
  claim with nothing behind it;
* it listed **OpenClaw**, which had no adapter, no registry entry and no
  `platforms.yaml` target, and it omitted **OpenCode**, which was fully
  configured and shipped.

Both are now impossible: the table is rendered from `compatibility/matrix.json`,
and the evidence level is computed, never typed.

Evidence levels (see `docs/COMPATIBILITY.md`)
----------------------------------------------
    Tier 4 Verified    invocable + workflow_completed, both backed by manual_evidence
    Tier 3 Validated   invocable, backed by manual_evidence
    Tier 2 Scanned     configured + discoverable, verified automatically by CI
    Tier 1 Configured  adapter exists and validates; discovery path not linked

Sources of truth
----------------
* `platforms/platforms.yaml` — harness ids, workspace paths, adapters
* `adapters/<id>.yaml`      — per-harness capability metadata
* `compatibility/matrix.json` — evidence per platform + `manual_evidence`

Generated outputs
-----------------
* `registry/agents.json` (the registry `allskills doctor` verifies)
* the compatibility table in `README.md`
* the compatibility table in `docs/COMPATIBILITY.md`

Usage
-----
    python scripts/generate_harness_matrix.py            # write outputs
    python scripts/generate_harness_matrix.py --check    # exit 1 if stale
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
PLATFORMS = ROOT / "platforms" / "platforms.yaml"
MATRIX = ROOT / "compatibility" / "matrix.json"
AGENTS_REGISTRY = ROOT / "registry" / "agents.json"
README = ROOT / "README.md"
COMPATIBILITY_DOC = ROOT / "docs" / "COMPATIBILITY.md"

README_BLOCK = "harness-compatibility"
DOC_BLOCK = "harness-compatibility"

TIER_4 = "Tier 4 Verified"
TIER_3 = "Tier 3 Validated"
TIER_2 = "Tier 2 Scanned"
TIER_1 = "Tier 1 Configured"
TIER_0 = "Not configured"


# ── evidence ────────────────────────────────────────────────────────────────


def evidence_level(claim: dict[str, Any]) -> str:
    """Derive the level from the record; never trust a hand-typed label."""
    if claim.get("invocable") and claim.get("workflow_completed"):
        return TIER_4
    if claim.get("invocable"):
        return TIER_3
    if claim.get("configured") and claim.get("discoverable"):
        return TIER_2
    if claim.get("configured"):
        return TIER_1
    return TIER_0


def _mark(value: Any, symbols: tuple[str, str, str]) -> str:
    yes, no, unknown = symbols
    if value is True:
        return yes
    if value is False:
        return no
    return unknown


# ── loading ─────────────────────────────────────────────────────────────────


def load_platforms() -> list[dict[str, Any]]:
    data = yaml.safe_load(PLATFORMS.read_text(encoding="utf-8")) or {}
    targets = data.get("local_targets") or []
    if not targets:
        raise SystemExit(f"{PLATFORMS.relative_to(ROOT)}: local_targets is empty")
    seen: set[str] = set()
    for target in targets:
        key = target.get("registry_id") or target.get("id")
        if not key:
            raise SystemExit(f"{PLATFORMS.relative_to(ROOT)}: a target has no id")
        if key in seen:
            raise SystemExit(f"{PLATFORMS.relative_to(ROOT)}: duplicate registry_id {key!r}")
        seen.add(key)
        if not target.get("adapter"):
            raise SystemExit(f"{PLATFORMS.relative_to(ROOT)}: {key} has no adapter")
    return targets


def load_adapter(relative: str) -> dict[str, Any]:
    path = ROOT / relative
    if not path.is_file():
        raise SystemExit(f"missing adapter file: {relative}")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict) or "agent_id" not in data or "discovery_paths" not in data:
        raise SystemExit(f"{relative}: adapter needs agent_id and discovery_paths")
    return data


def load_matrix() -> dict[str, Any]:
    return json.loads(MATRIX.read_text(encoding="utf-8"))


# ── generation ──────────────────────────────────────────────────────────────


def registry_ids(platforms: list[dict[str, Any]]) -> list[str]:
    return [str(t.get("registry_id") or t["id"]) for t in platforms]


def build_agents_registry(platforms: list[dict[str, Any]], matrix: dict[str, Any]) -> dict[str, Any]:
    agents: dict[str, Any] = {}
    for target in platforms:
        key = str(target.get("registry_id") or target["id"])
        adapter = load_adapter(str(target["adapter"]))
        workspace_paths = (adapter.get("discovery_paths") or {}).get("workspace") or []
        if str(target["path"]) not in workspace_paths:
            raise SystemExit(
                f"{target['adapter']}: discovery_paths.workspace {workspace_paths} does not "
                f"include platforms.yaml path {target['path']!r}"
            )
        agents[key] = {
            "id": key,
            "display_name": adapter.get("display_name") or target["name"],
            "workspace_path": target["path"],
            "global_path": target.get("global_path"),
            "adapter": target["adapter"],
            "manifest_format": adapter.get("manifest_format", "markdown_frontmatter"),
            "frontmatter_standard": adapter.get("frontmatter_standard", "agent_skills_v1"),
            "is_canonical_source": bool(target.get("is_canonical_source", False)),
            "context_loading": target.get("context_loading", "on-demand"),
            "description": target.get("description") or f"{target['name']} agent harness",
        }
    missing = sorted(set(matrix.get("platforms", {})) - set(agents))
    if missing:
        raise SystemExit(
            "compatibility/matrix.json records platforms with no platforms.yaml target: "
            + ", ".join(missing)
        )
    return {
        "_comment": (
            f"Registry of all {len(agents)} supported AI coding agents. Generated by "
            "scripts/generate_harness_matrix.py from platforms/platforms.yaml and "
            "adapters/*.yaml — do not edit by hand."
        ),
        "schema_version": "2.0",
        "agents": agents,
        "total": len(agents),
        "canonical_source": "gemini",
    }


def _row(target: dict[str, Any], claim: dict[str, Any], symbols: tuple[str, str, str]) -> str:
    yes, no, unknown = symbols
    return (
        f"| **{claim.get('display_name') or target['name']}** "
        f"| `{target['path']}/` "
        f"| {_mark(claim.get('configured'), symbols)} "
        f"| {_mark(claim.get('discoverable'), symbols)} "
        f"| {_mark(claim.get('invocable'), symbols)} "
        f"| {_mark(claim.get('workflow_completed'), symbols)} "
        f"| {evidence_level(claim)} |"
    )


HEADER = (
    "| AI Coding Agent | Skills directory | Configured | Discoverable | Invocable "
    "| Workflow completed | Evidence level |\n"
    "| :--- | :--- | :---: | :---: | :---: | :---: | :--- |"
)


def render_table(platforms: list[dict[str, Any]], matrix: dict[str, Any],
                 symbols: tuple[str, str, str]) -> str:
    claims = matrix.get("platforms", {})
    rows = [_row(t, claims[str(t.get("registry_id") or t["id"])], symbols) for t in platforms]
    return "\n".join([HEADER, *rows])


def render_readme_block(platforms: list[dict[str, Any]], matrix: dict[str, Any]) -> str:
    evidence = matrix.get("manual_evidence") or []
    table = render_table(platforms, matrix, ("✓", "✗", "—"))
    return (
        f"{table}\n\n"
        f"`✓` verified · `✗` not supported · `—` not recorded. "
        f"{len(platforms)} harnesses are configured and discoverable; "
        f"**{len(evidence)} manual evidence entr{'y' if len(evidence) == 1 else 'ies'}** "
        f"(named agent version, date, verifier, skill) are on record, so invocable and "
        f"workflow-completed claims stay empty until someone records one in "
        f"[`compatibility/matrix.json`](compatibility/matrix.json) — see "
        f"[`docs/COMPATIBILITY.md`](docs/COMPATIBILITY.md) for the levels and how to add evidence."
    )


def render_doc_block(platforms: list[dict[str, Any]], matrix: dict[str, Any]) -> str:
    table = render_table(platforms, matrix, ("✅", "❌", "not yet verified"))
    return table


# ── file surgery ────────────────────────────────────────────────────────────


def begin(name: str) -> str:
    return f"<!-- BEGIN GENERATED: {name} (scripts/generate_harness_matrix.py) -->"


def end(name: str) -> str:
    return f"<!-- END GENERATED: {name} -->"


def replace_block(text: str, name: str, body: str, path: Path) -> str:
    start, stop = begin(name), end(name)
    if start not in text or stop not in text:
        raise SystemExit(f"{path.relative_to(ROOT)}: missing generated block markers for {name}")
    head, rest = text.split(start, 1)
    _old, tail = rest.split(stop, 1)
    return f"{head}{start}\n{body}\n{stop}{tail}"


def write_or_check(path: Path, content: str, check: bool, problems: list[str]) -> None:
    current = path.read_text(encoding="utf-8") if path.exists() else ""
    if current == content:
        return
    if check:
        problems.append(str(path.relative_to(ROOT)))
        return
    path.write_text(content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="exit 1 if any generated file is stale")
    args = parser.parse_args()

    platforms = load_platforms()
    matrix = load_matrix()
    problems: list[str] = []

    registry = build_agents_registry(platforms, matrix)
    write_or_check(
        AGENTS_REGISTRY,
        json.dumps(registry, indent=2, ensure_ascii=False) + "\n",
        args.check,
        problems,
    )

    readme = README.read_text(encoding="utf-8")
    write_or_check(
        README,
        replace_block(readme, README_BLOCK, render_readme_block(platforms, matrix), README),
        args.check,
        problems,
    )

    doc = COMPATIBILITY_DOC.read_text(encoding="utf-8")
    write_or_check(
        COMPATIBILITY_DOC,
        replace_block(doc, DOC_BLOCK, render_doc_block(platforms, matrix), COMPATIBILITY_DOC),
        args.check,
        problems,
    )

    if problems:
        print("Stale generated harness documentation:")
        for problem in problems:
            print(f"  - {problem}")
        print("Run: python scripts/generate_harness_matrix.py")
        return 1

    levels: dict[str, int] = {}
    for key in registry_ids(platforms):
        level = evidence_level(matrix["platforms"][key])
        levels[level] = levels.get(level, 0) + 1
    summary = ", ".join(f"{count} × {level}" for level, count in sorted(levels.items()))
    verb = "up to date" if args.check else "written"
    print(f"Harness matrix {verb}: {len(platforms)} platforms ({summary})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
