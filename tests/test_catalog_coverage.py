"""Coverage guards for the two "install anything" surfaces.

These tests exist so the catalog and the curated library cannot silently shrink
again: every curated skill must be installable, every MCP server must be
structurally complete, and the install profiles must resolve.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from skills.mcp import Catalog, expand_profile, verify_catalog  # noqa: E402

CURATED = ROOT / "skills"
MODULES = json.loads((ROOT / "manifests" / "install-modules.json").read_text(encoding="utf-8"))
PROFILES = json.loads((ROOT / "manifests" / "install-profiles.json").read_text(encoding="utf-8"))


def curated_skill_dirs() -> list[Path]:
    """Every ``skills/<category>/<name>/SKILL.md`` directory."""
    return sorted({path.parent for path in CURATED.glob("*/*/SKILL.md")})


def owned_paths() -> set[str]:
    return {path for module in MODULES["modules"] for path in module["paths"]}


def test_curated_library_is_large_and_categorised() -> None:
    dirs = curated_skill_dirs()
    assert len(dirs) >= 448, f"curated library shrank to {len(dirs)} skills"
    categories = {path.parent.name for path in dirs}
    assert len(categories) >= 30, f"only {len(categories)} categories remain"


def test_every_curated_skill_is_installable() -> None:
    """A skill nobody can install is documentation, not a capability."""
    owned = owned_paths()
    unowned = [
        path.relative_to(ROOT).as_posix()
        for path in curated_skill_dirs()
        if path.relative_to(ROOT).as_posix() not in owned
    ]
    assert unowned == [], f"{len(unowned)} curated skills are not in any install module: {unowned[:5]}"


def test_every_curated_skill_has_readme_and_frontmatter() -> None:
    problems = []
    for path in curated_skill_dirs():
        if not (path / "README.md").is_file():
            problems.append(f"{path.relative_to(ROOT)}: missing README.md")
        text = (path / "SKILL.md").read_text(encoding="utf-8")
        front = re.match(r"^---\n([\s\S]*?)\n---", text)
        if not front:
            problems.append(f"{path.relative_to(ROOT)}: missing frontmatter")
            continue
        for key in ("name", "description", "category", "version"):
            if not re.search(rf"^{key}:", front.group(1), re.MULTILINE):
                problems.append(f"{path.relative_to(ROOT)}: missing {key}")
    assert problems == [], problems[:5]


def test_install_modules_reference_existing_paths_only() -> None:
    """Machine-local, gitignored harness dirs must never be source paths."""
    missing = sorted(
        path for path in owned_paths()
        if not (ROOT / path).exists()
    )
    assert missing == [], f"install modules reference missing paths: {missing[:5]}"
    for forbidden in (".codex", ".cursor", ".opencode"):
        assert forbidden not in owned_paths(), f"{forbidden} is per-machine and gitignored"


def test_profiles_resolve_and_library_profile_installs_the_library() -> None:
    module_ids = {module["id"] for module in MODULES["modules"]}
    for name, profile in PROFILES["profiles"].items():
        unknown = [module for module in profile["modules"] if module not in module_ids]
        assert unknown == [], f"profile {name} references unknown modules: {unknown}"
    library = PROFILES["profiles"]["library"]["modules"]
    assert "canonical-library" in library
    assert "hooks-runtime" not in library, "the library profile must stay hook-free"


def test_canonical_library_module_is_opt_in_and_heavy() -> None:
    module = next(m for m in MODULES["modules"] if m["id"] == "canonical-library")
    assert module["defaultInstall"] is False, "448 skills must never be a default install"
    assert module["cost"] == "heavy"
    assert len(module["paths"]) >= 400


def test_mcp_catalog_keeps_its_new_coverage() -> None:
    catalog = Catalog.load(ROOT)
    assert verify_catalog(catalog) == []
    servers = {server.id: server for server in catalog.servers}
    assert len(servers) >= 96, f"catalog shrank to {len(servers)} servers"
    assert len({server.category for server in catalog.servers}) >= 31
    expected = {
        "mysql", "neo4j", "qdrant", "chroma", "pinecone", "snowflake", "bigquery", "duckdb",
        "neon", "azure", "digitalocean", "heroku", "netlify", "google-cloud-run", "firebase",
        "pulumi", "clickup", "trello", "airtable", "todoist", "google-calendar",
        "google-sheets", "n8n", "apify", "e2b", "circleci", "sonarqube", "postman",
        "paypal", "resend", "twilio", "elevenlabs",
    }
    assert expected <= set(servers), f"missing connectors: {sorted(expected - set(servers))}"


def test_mcp_server_definitions_are_runnable() -> None:
    """Every entry must name a real runner and declare the env it references."""
    catalog = Catalog.load(ROOT)
    problems = []
    for server in catalog.servers:
        if server.transport == "stdio":
            if server.command not in {"npx", "uvx", "node", "python", "docker", "deno"}:
                problems.append(f"{server.id}: unusual command {server.command!r}")
            if not server.args:
                problems.append(f"{server.id}: no args")
        placeholders = set(re.findall(r"\$\{([A-Z0-9_]+)\}", " ".join(server.args)))
        undeclared = placeholders - set(server.required_env) - {"WORKSPACE"}
        if undeclared:
            problems.append(f"{server.id}: undeclared placeholders {sorted(undeclared)}")
        if not server.docs.startswith("https://"):
            problems.append(f"{server.id}: docs must be an https URL")
    assert problems == [], problems[:5]


def test_mcp_profiles_are_nested_and_documented() -> None:
    catalog = Catalog.load(ROOT)
    core = {server.id for server in expand_profile(catalog, "core")}
    standard = {server.id for server in expand_profile(catalog, "standard")}
    full = {server.id for server in expand_profile(catalog, "full")}
    assert core <= standard <= full
    assert len(core) == 5 and all(not catalog.get(s).required_env for s in core)
    assert len(standard) >= 20
    assert full == {server.id for server in catalog.servers}


def test_optin_connector_file_covers_the_catalog() -> None:
    """`mcp-configs/mcp-servers.json` is the plugin opt-in surface; keep it a superset."""
    optin = json.loads((ROOT / "mcp-configs" / "mcp-servers.json").read_text(encoding="utf-8"))
    servers = set(optin.get("mcpServers", {}))
    catalog = {server.id for server in Catalog.load(ROOT).servers}
    assert catalog <= servers, f"opt-in file is missing: {sorted(catalog - servers)[:5]}"


# ─── One inventory, not two ──────────────────────────────────────────────────
# The repo used to ship a hand-maintained `mcp/` tree next to `mcps/catalog.json`
# and they disagreed (12 servers vs 113). These tests make a second inventory
# impossible: `mcp/` is generated, and regeneration is compared byte for byte.


def test_generated_mcp_tree_matches_the_catalog() -> None:
    """`mcp/` must be a projection of `mcps/catalog.json`, never a sibling copy."""
    sys.path.insert(0, str(ROOT / "scripts" / "dev"))
    import generate_mcp_registry  # noqa: PLC0415

    files = generate_mcp_registry.render()
    stale = [
        path.relative_to(ROOT).as_posix()
        for path, text in files.items()
        if not path.exists() or path.read_text(encoding="utf-8") != text
    ]
    assert stale == [], (
        "mcp/ is out of date with mcps/catalog.json; run "
        f"python scripts/dev/generate_mcp_registry.py ({stale[:5]})"
    )


def test_generated_mcp_tree_has_no_orphan_servers() -> None:
    catalog = {server.id for server in Catalog.load(ROOT).servers}
    on_disk = {path.stem for path in (ROOT / "mcp" / "servers").glob("*.json")}
    assert on_disk == catalog, f"orphan stubs: {sorted(on_disk - catalog)[:5]}"


def test_mcp_registry_declares_the_real_counts() -> None:
    registry = json.loads((ROOT / "mcp" / "registry.json").read_text(encoding="utf-8"))
    servers = Catalog.load(ROOT).servers
    assert registry["servers_count"] == len(servers)
    assert registry["categories_count"] == len({server.category for server in servers})
    assert registry["generated_from"] == "mcps/catalog.json"


def test_every_skill_mcp_declaration_resolves() -> None:
    """A skill must not require a server that is not installable."""
    servers = {server.id for server in Catalog.load(ROOT).servers}
    problems = []
    for path in sorted(CURATED.glob("*/*/SKILL.md")):
        text = path.read_text(encoding="utf-8")
        front = re.match(r"^---\n([\s\S]*?)\n---", text)
        if not front:
            continue
        block = re.search(r"^mcp_servers:\n((?:\s+-\s+\S+\n?)+)", front.group(1), re.MULTILINE)
        if not block:
            continue
        declared = re.findall(r"-\s+(\S+)", block.group(1))
        unknown = [name for name in declared if name not in servers]
        if unknown:
            problems.append(f"{path.relative_to(ROOT)}: unknown servers {unknown}")
    assert problems == [], problems[:5]


def test_skill_mcp_map_is_current() -> None:
    """`registry/skill-mcp-map.json` documents the dependency graph; keep it true."""
    mapping = json.loads((ROOT / "registry" / "skill-mcp-map.json").read_text(encoding="utf-8"))
    catalog = {server.id for server in Catalog.load(ROOT).servers}
    assert set(mapping["servers"]) == catalog
    declared_servers = {
        name for record in mapping["skills"].values() for name in record["declared"]
    }
    assert declared_servers <= catalog
    assert mapping["counts"]["skills_with_declared_servers"] >= 50, (
        "skills stopped declaring their connectors; the map is only useful if it is used"
    )
