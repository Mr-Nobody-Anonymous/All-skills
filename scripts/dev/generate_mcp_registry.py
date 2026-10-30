#!/usr/bin/env python3
"""Generate the ``mcp/`` connector view from ``mcps/catalog.json``.

Why this exists
---------------
The repository used to carry two MCP inventories: ``mcps/catalog.json`` (what the
installer actually writes into a harness config) and a hand-maintained ``mcp/``
tree whose ``registry.json`` claimed 12 servers while the catalog had 113. Two
hand-edited inventories always drift, and a stale profile can reference servers
that no longer exist.

``mcps/catalog.json`` is the single source of truth. This script derives
``mcp/`` from it, so the view can never disagree again:

* ``mcp/servers/<id>.json``  — one file per catalog server, with its policy
* ``mcp/registry.json``      — counts, categories, and the source it came from
* ``mcp/profiles/<role>.json`` — role bundles, filtered to servers that exist

    python scripts/dev/generate_mcp_registry.py            # write
    python scripts/dev/generate_mcp_registry.py --check    # fail on drift (CI)

Role profiles are declared here, not on disk: a profile naming a server that is
not in the catalog is a bug, and generation refuses to write one.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "mcps" / "catalog.json"
OUT = ROOT / "mcp"

POLICY = {
    "policy": "least-privilege",
    "read_only_default": True,
    "require_approval_for_destructive": True,
}

# Role bundles. Every id here must exist in the catalog — the generator asserts
# it, so a renamed server breaks the build instead of rotting in a profile.
ROLE_PROFILES: dict[str, list[str]] = {
    "administrator": ["filesystem", "git", "fetch", "memory", "time", "notion", "airtable", "todoist"],
    "business": ["notion", "airtable", "linear", "slack", "stripe", "hubspot", "google-sheets"],
    "data-scientist": ["postgres", "duckdb", "bigquery", "snowflake", "filesystem"],
    "designer": ["figma", "inkscape", "blender", "sketchfab", "meshy", "filesystem"],
    "developer": ["filesystem", "git", "github", "fetch", "memory", "context7", "playwright", "serena"],
    "finance": ["stripe", "paypal", "google-sheets", "postgres"],
    "geospatial": ["qgis", "gdal", "geoserver", "mapbox", "filesystem"],
    "healthcare": ["filesystem", "fetch", "memory", "notion"],
    "researcher": ["fetch", "exa", "tavily", "brave-search", "firecrawl", "deepwiki", "filesystem"],
    "security": ["semgrep", "snyk", "git", "github", "fetch", "filesystem"],
}


def load_catalog() -> dict:
    return json.loads(CATALOG.read_text(encoding="utf-8"))


def server_document(server: dict) -> dict:
    """The per-server file: identity, how to launch it, and its policy."""
    doc = {
        "id": server["id"],
        "name": server.get("name", server["id"]),
        "description": server.get("description", ""),
        "category": server.get("category", "utilities"),
        "tier": server.get("tier", "full"),
        "transport": server.get("transport", "stdio"),
        "vendor": server.get("vendor", "unknown"),
        "official": bool(server.get("official", False)),
    }
    if doc["transport"] == "stdio":
        doc["command"] = server.get("command")
        doc["args"] = list(server.get("args") or [])
    else:
        doc["url"] = server.get("url")
    doc["required_env"] = list(server.get("required_env") or [])
    doc["risk"] = server.get("risk", "low")
    doc["license"] = server.get("license", "unknown")
    doc["docs"] = server.get("docs", "")
    doc["harnesses"] = list(server.get("harnesses") or [])
    doc["policy"] = dict(POLICY)
    return doc


def registry_document(catalog: dict) -> dict:
    servers = catalog["servers"]
    categories: dict[str, list[str]] = {}
    for server in sorted(servers, key=lambda s: s["id"]):
        categories.setdefault(server.get("category", "utilities"), []).append(server["id"])
    return {
        "version": "2.0.0",
        "generated_from": "mcps/catalog.json",
        "generated_by": "scripts/dev/generate_mcp_registry.py",
        "do_not_edit": "This file is generated. Change mcps/catalog.json and regenerate.",
        "servers_count": len(servers),
        "categories_count": len(categories),
        "harnesses_count": len(catalog.get("harnesses", {})),
        "profiles_count": len(catalog.get("profiles", {})),
        "role_profiles_count": len(ROLE_PROFILES),
        "categories": dict(sorted(categories.items())),
    }


def render() -> dict[Path, str]:
    """Every file this generator owns, as {path: text}."""
    catalog = load_catalog()
    by_id = {server["id"]: server for server in catalog["servers"]}
    missing = sorted({sid for ids in ROLE_PROFILES.values() for sid in ids} - set(by_id))
    if missing:
        raise SystemExit(
            "role profiles reference servers that are not in mcps/catalog.json: "
            + ", ".join(missing)
        )

    files: dict[Path, str] = {}
    for server in catalog["servers"]:
        files[OUT / "servers" / f"{server['id']}.json"] = (
            json.dumps(server_document(server), indent=2, ensure_ascii=False) + "\n"
        )
    files[OUT / "registry.json"] = json.dumps(registry_document(catalog), indent=2, ensure_ascii=False) + "\n"
    for role, ids in ROLE_PROFILES.items():
        doc = {
            "profile": role,
            "servers": sorted(ids),
            "default_policy": POLICY["policy"],
            "read_only_default": POLICY["read_only_default"],
            "note": "Generated from mcps/catalog.json by scripts/dev/generate_mcp_registry.py.",
        }
        files[OUT / "profiles" / f"{role}.json"] = json.dumps(doc, indent=2, ensure_ascii=False) + "\n"
    return files


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if mcp/ is out of date")
    args = parser.parse_args()

    files = render()
    changed: list[str] = []
    for path, text in files.items():
        current = path.read_text(encoding="utf-8") if path.exists() else None
        if current != text:
            changed.append(path.relative_to(ROOT).as_posix())
            if not args.check:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(text, encoding="utf-8", newline="")

    # Orphan files: a server removed from the catalog must leave no stub behind.
    stale = [
        p for p in (OUT / "servers").glob("*.json")
        if p not in files and p.relative_to(ROOT).as_posix() not in changed
    ]

    if args.check:
        if changed:
            print("[FAIL] mcp/ is out of date; regenerate with scripts/dev/generate_mcp_registry.py:")
            for path in changed[:10]:
                print(f"  - {path}")
            return 1
        print(f"[PASS] mcp/ matches mcps/catalog.json ({len(files)} files)")
        return 0

    for path in stale:
        path.unlink()
    print(f"wrote {len(files)} file(s) under mcp/ ({len(changed)} changed)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
