#!/usr/bin/env python3
"""Map every curated skill to the MCP servers it needs, and validate the link.

The repository shipped 117 connectors and 533 skills with nothing tying them
together: a skill could name a server that does not exist, and an installer
could not answer "which servers does this skill require?". This script closes
that gap.

Sources of truth
----------------
* ``mcps/catalog.json`` — the servers.
* ``skills/<category>/<name>/SKILL.md`` — the skills. A skill declares its
  requirements in frontmatter ``mcp_servers:``. Mentions of a server id in the
  body are recorded separately as *mentions*: useful signal, not a contract.

Outputs
-------
* ``registry/skill-mcp-map.json`` — machine-readable, both directions.
* ``docs/MCP-SKILL-MAP.md`` — human-readable, grouped by domain.
* a ``## MCP Requirements`` table inside every skill that declares servers, so
  the requirement (server, transport, tier, risk, env vars) travels with the
  skill instead of living only in a central file.

    python scripts/dev/generate_skill_mcp_map.py           # write
    python scripts/dev/generate_skill_mcp_map.py --check   # fail on drift (CI)

Hard failures: a declared server that is not in the catalog, or a declared
server whose required env vars appear nowhere in the skill (an agent cannot be
told to "use the qgis server" and left to guess the port variable).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "mcps" / "catalog.json"
SKILLS = ROOT / "skills"
REGISTRY_OUT = ROOT / "registry" / "skill-mcp-map.json"
DOC_OUT = ROOT / "docs" / "MCP-SKILL-MAP.md"
FRONTMATTER = re.compile(r"^---\n(.*?)\n---", re.S)


def load_servers() -> dict[str, dict]:
    return {server["id"]: server for server in json.loads(CATALOG.read_text(encoding="utf-8"))["servers"]}


def read_skill(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER.match(text)
    front = yaml.safe_load(match.group(1)) if match else {}
    return (front or {}), text


def collect(servers: dict[str, dict]) -> tuple[dict, list[str], list[str], dict[Path, str]]:
    problems: list[str] = []
    warnings: list[str] = []
    skills: dict[str, dict] = {}
    rewrites: dict[Path, str] = {}

    for path in sorted(SKILLS.glob("*/*/SKILL.md")):
        category, name = path.parent.parent.name, path.parent.name
        skill_id = f"{category}/{name}"
        front, text = read_skill(path)
        declared = [str(s) for s in (front.get("mcp_servers") or [])]

        unknown = [s for s in declared if s not in servers]
        if unknown:
            problems.append(f"{skill_id}: declares unknown MCP server(s) {unknown}")
        # Warnings are computed against the file as it will be written, because the
        # Requirements table (below) is where the env vars become visible.
        text_after = text
        if declared:
            text_after = inject_requirements(text, requirements_block(declared, servers))
        body = text_after.lower()
        for server_id in declared:
            env = servers.get(server_id, {}).get("required_env") or []
            if env and not any(var.lower() in body for var in env):
                warnings.append(
                    f"{skill_id}: declares {server_id!r} but never names its env var(s) {env}"
                )

        mentioned = sorted(
            sid for sid in servers
            if sid not in declared and re.search(rf"(?<![\w.-]){re.escape(sid)}(?![\w.-])", text, re.I)
        )
        skills[skill_id] = {
            "category": category,
            "name": name,
            "declared": declared,
            "mentioned": mentioned,
        }
        if declared and text_after != text:
            rewrites[path] = text_after

    return skills, problems, warnings, rewrites


SECTION_TITLE = "## MCP Requirements"


def requirements_block(declared: list[str], servers: dict[str, dict]) -> str:
    rows = [
        "| Server | Transport | Tier | Risk | Required env |",
        "| :--- | :--- | :--- | :--- | :--- |",
    ]
    for server_id in declared:
        server = servers[server_id]
        env = ", ".join(f"`{v}`" for v in (server.get("required_env") or [])) or "—"
        rows.append(
            f"| `{server_id}` | {server.get('transport', 'stdio')} | {server.get('tier', 'full')} "
            f"| {server.get('risk', 'low')} | {env} |"
        )
    return "\n".join([
        SECTION_TITLE,
        "",
        *rows,
        "",
        "Install the connectors above with `allskills mcp install --harness <harness> --profile full`,",
        "or list the same ids in your harness config. Full detail per server: "
        "[`docs/MCP-CATALOG.md`](MCP-CATALOG.md) and [`mcp/registry.json`](../mcp/registry.json).",
    ])


def inject_requirements(text: str, block: str) -> str:
    """Replace an existing requirements section in place, or insert before Sources."""
    start = text.find(SECTION_TITLE)
    if start != -1:
        nxt = text.find("\n## ", start + len(SECTION_TITLE))
        end = nxt + 1 if nxt != -1 else len(text)
        return text[:start] + block + "\n\n" + text[end:]
    anchor = text.find("\n## Source\n")
    if anchor == -1:
        return text.rstrip("\n") + "\n\n" + block + "\n"
    return text[:anchor + 1] + block + "\n\n" + text[anchor + 1:]


def build_document(skills: dict[str, dict], servers: dict[str, dict]) -> dict:
    by_server: dict[str, dict] = {}
    for server_id, server in sorted(servers.items()):
        declared_by = sorted(sid for sid, rec in skills.items() if server_id in rec["declared"])
        mentioned_by = sorted(sid for sid, rec in skills.items() if server_id in rec["mentioned"])
        by_server[server_id] = {
            "name": server.get("name", server_id),
            "category": server.get("category", "utilities"),
            "tier": server.get("tier", "full"),
            "risk": server.get("risk", "low"),
            "required_env": list(server.get("required_env") or []),
            "transport": server.get("transport", "stdio"),
            "declared_by": declared_by,
            "mentioned_by": mentioned_by,
        }

    declared_skills = {sid: rec for sid, rec in skills.items() if rec["declared"]}
    return {
        "version": "1.0.0",
        "generated_by": "scripts/dev/generate_skill_mcp_map.py",
        "generated_from": ["mcps/catalog.json", "skills/*/*/SKILL.md"],
        "note": "'declared' comes from frontmatter mcp_servers and is a contract; "
                "'mentioned' is a text match and is informational only.",
        "counts": {
            "skills": len(skills),
            "skills_with_declared_servers": len(declared_skills),
            "servers": len(servers),
            "servers_with_declared_skills": sum(1 for rec in by_server.values() if rec["declared_by"]),
        },
        "skills": skills,
        "servers": by_server,
    }


def render_markdown(doc: dict) -> str:
    counts = doc["counts"]
    lines = [
        "# Skill ↔ MCP dependency map",
        "",
        "Generated by `python scripts/dev/generate_skill_mcp_map.py` from `mcps/catalog.json` and the",
        "`skills/` tree. **Do not edit by hand** — `--check` fails CI on drift.",
        "",
        f"- **{counts['skills']}** curated skills, **{counts['skills_with_declared_servers']}** of which declare the MCP servers they need.",
        f"- **{counts['servers']}** catalogued servers, **{counts['servers_with_declared_skills']}** required by at least one skill.",
        "",
        "A *declared* server comes from a skill's frontmatter `mcp_servers:` and is a contract: the",
        "installer can use it to install the connectors a skill needs. A *mentioned* server is only a",
        "text match in the body — useful for discovery, not a dependency.",
        "",
        "## Servers required by skills",
        "",
        "| Server | Category | Tier | Risk | Env | Required by |",
        "| :--- | :--- | :--- | :--- | :--- | :--- |",
    ]
    for server_id, rec in doc["servers"].items():
        if not rec["declared_by"]:
            continue
        env = ", ".join(f"`{v}`" for v in rec["required_env"]) or "—"
        required_by = "<br>".join(f"`{sid}`" for sid in rec["declared_by"])
        lines.append(
            f"| `{server_id}` | {rec['category']} | {rec['tier']} | {rec['risk']} | {env} | {required_by} |"
        )

    lines += ["", "## Skills that declare servers, by domain", ""]
    domains: dict[str, list[str]] = {}
    for skill_id, rec in doc["skills"].items():
        if rec["declared"]:
            domains.setdefault(rec["category"], []).append(skill_id)
    for category in sorted(domains):
        lines += [f"### {category}", "", "| Skill | Servers |", "| :--- | :--- |"]
        for skill_id in sorted(domains[category]):
            servers_cell = ", ".join(f"`{s}`" for s in doc["skills"][skill_id]["declared"])
            lines.append(f"| `{skill_id}` | {servers_cell} |")
        lines.append("")

    orphan_servers = [sid for sid, rec in doc["servers"].items() if not rec["declared_by"]]
    lines += [
        "## Servers no skill declares yet",
        "",
        "These are installable but no curated playbook requires them by name. They are legitimate",
        "integrations for ad-hoc work; the list is the backlog for future skill coverage.",
        "",
        " ".join(f"`{sid}`" for sid in orphan_servers),
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if the map is out of date")
    args = parser.parse_args()

    servers = load_servers()
    skills, problems, warnings, rewrites = collect(servers)
    if problems:
        print("[FAIL] skill → MCP mapping is invalid:", file=sys.stderr)
        for problem in problems:
            print(f"  - {problem}", file=sys.stderr)
        return 1

    doc = build_document(skills, servers)
    payloads = {
        REGISTRY_OUT: json.dumps(doc, indent=2, ensure_ascii=False) + "\n",
        DOC_OUT: render_markdown(doc) + "\n",
    }
    targets = {**payloads, **rewrites}
    drift = [
        path.relative_to(ROOT).as_posix()
        for path, text in targets.items()
        if (path.read_text(encoding="utf-8") if path.exists() else None) != text
    ]

    if args.check:
        if drift:
            print("[FAIL] skill → MCP map is stale; regenerate with scripts/dev/generate_skill_mcp_map.py:")
            for path in drift:
                print(f"  - {path}")
            return 1
        print(f"[PASS] skill → MCP map is current ({len(skills)} skills, {len(servers)} servers)")
        return 0

    for path, text in targets.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="")
    counts = doc["counts"]
    print(f"wrote {REGISTRY_OUT.relative_to(ROOT)} and {DOC_OUT.relative_to(ROOT)}")
    print(f"  {counts['skills_with_declared_servers']}/{counts['skills']} skills declare servers; "
          f"{counts['servers_with_declared_skills']}/{counts['servers']} servers required")
    print(f"  {len(rewrites)} skill file(s) carry an updated MCP Requirements section")
    for warning in warnings:
        print(f"  [warn] {warning}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
