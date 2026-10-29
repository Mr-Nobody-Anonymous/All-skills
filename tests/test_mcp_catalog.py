"""Tests for the MCP catalog, installer and verifier (``skills.mcp``)."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

try:
    import pytest
except ModuleNotFoundError:  # minimal install: only the dev/test extra provides it
    # unittest discovery (`scripts/skills/skills.py test`) imports every test
    # module; without pytest this one used to surface as a collection failure.
    raise unittest.SkipTest("test_mcp_catalog needs pytest (install the 'test' extra)")

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from skills.mcp import (  # noqa: E402
    Catalog,
    CatalogError,
    apply_install,
    catalog_summary,
    expand_profile,
    plan_install,
    render_toml_fragment,
    render_yaml_fragment,
    to_harness_block,
    verify_catalog,
)


@pytest.fixture(scope="module")
def catalog() -> Catalog:
    return Catalog.load(ROOT)


def test_catalog_is_coherent(catalog: Catalog) -> None:
    assert verify_catalog(catalog) == []


def test_catalog_has_meaningful_coverage(catalog: Catalog) -> None:
    summary = catalog_summary(catalog)
    assert summary["servers"] >= 50, "the catalog must cover the common connector surface"
    assert summary["harnesses"] >= 15, "every mainstream harness must be installable"
    assert set(summary["profiles"]) == {"core", "standard", "full"}
    assert summary["by_tier"]["core"] >= 3
    ids = {s.id for s in catalog.servers}
    for required in ("filesystem", "git", "fetch", "github", "playwright", "postgres"):
        assert required in ids


def test_profiles_are_nested_subsets(catalog: Catalog) -> None:
    core = {s.id for s in expand_profile(catalog, "core")}
    standard = {s.id for s in expand_profile(catalog, "standard")}
    full = {s.id for s in expand_profile(catalog, "full")}
    assert core <= standard <= full
    assert len(full) == len(catalog.servers)


def test_unknown_server_and_profile_are_errors(catalog: Catalog) -> None:
    with pytest.raises(CatalogError):
        catalog.resolve(["does-not-exist"])
    with pytest.raises(CatalogError):
        expand_profile(catalog, "nope")


def test_stdio_and_http_blocks(catalog: Catalog) -> None:
    fs = catalog.get("filesystem")
    assert fs is not None
    block = fs.config_block(workspace="/work")
    assert block["command"] == "npx"
    assert block["args"][-1] == "/work", "${WORKSPACE} must be substituted"

    github = catalog.get("github")
    assert github is not None
    block = github.config_block()
    assert block["type"] == "http"
    assert block["url"].startswith("https://")
    assert "Authorization" in block["headers"]


def test_placeholders_are_declared(catalog: Catalog) -> None:
    for server in catalog.servers:
        for name in server.required_placeholders():
            assert name.isupper(), f"{server.id}: {name} must be an env var"


def test_harness_dialects(catalog: Catalog) -> None:
    fs = catalog.get("filesystem")
    assert fs is not None
    opencode = to_harness_block(fs, "opencode", ".")
    assert opencode["type"] == "local"
    assert isinstance(opencode["command"], list)
    zed = to_harness_block(fs, "zed", ".")
    assert zed["command"]["path"] == "npx"
    vscode = to_harness_block(fs, "vscode", ".")
    assert vscode["type"] == "stdio"


def test_install_merges_without_clobbering(tmp_path: Path, catalog: Catalog) -> None:
    target = tmp_path / ".cursor" / "mcp.json"
    target.parent.mkdir(parents=True)
    target.write_text(
        json.dumps({"mcpServers": {"mine": {"command": "custom"}}, "theme": "dark"}),
        encoding="utf-8",
    )

    result = plan_install(catalog, "cursor", [catalog.get("filesystem")], tmp_path, workspace="/w")  # type: ignore[list-item]
    apply_install(result)

    data = json.loads(target.read_text(encoding="utf-8"))
    assert data["theme"] == "dark"
    assert data["mcpServers"]["mine"] == {"command": "custom"}
    assert data["mcpServers"]["filesystem"]["args"][-1] == "/w"
    assert result.written is True
    assert result.backup is not None and result.backup.exists()


def test_install_is_idempotent(tmp_path: Path, catalog: Catalog) -> None:
    servers = expand_profile(catalog, "core")
    first = plan_install(catalog, "cursor", servers, tmp_path)
    apply_install(first)
    before = (tmp_path / ".cursor" / "mcp.json").read_text(encoding="utf-8")
    second = plan_install(catalog, "cursor", servers, tmp_path)
    apply_install(second)
    after = (tmp_path / ".cursor" / "mcp.json").read_text(encoding="utf-8")
    assert before == after
    assert second.added == []
    assert second.written is False
    assert len(second.unchanged) == len(servers)


def test_dry_run_writes_nothing(tmp_path: Path, catalog: Catalog) -> None:
    result = plan_install(catalog, "claude", [catalog.get("memory")], tmp_path)  # type: ignore[list-item]
    apply_install(result, dry_run=True)
    assert result.dry_run is True
    assert result.written is False
    assert not (tmp_path / ".mcp.json").exists()


def test_non_json_harnesses_emit_fragments(tmp_path: Path, catalog: Catalog) -> None:
    for harness in ("codex", "goose"):
        result = plan_install(catalog, harness, [catalog.get("filesystem")], tmp_path)  # type: ignore[list-item]
        apply_install(result)
        assert result.fragment, f"{harness} must render a fragment, not rewrite its config"
        assert result.written is False
        target = result.path
        assert not target.exists() or harness == "codex"


def test_fragments_are_parsable(catalog: Catalog) -> None:
    servers = expand_profile(catalog, "core")
    toml_text = render_toml_fragment([(s.id, s.config_block()) for s in servers])
    assert "[mcp_servers.filesystem]" in toml_text
    try:  # Python 3.11+ only; the repo supports 3.10 where tomllib is absent
        import tomllib
    except ModuleNotFoundError:  # pragma: no cover - 3.10 fallback
        pytest.skip("tomllib unavailable")
    parsed = tomllib.loads(toml_text)
    assert set(parsed["mcp_servers"]) == {s.id for s in servers}

    yaml = pytest.importorskip("yaml")
    parsed_yaml = yaml.safe_load(render_yaml_fragment([(s.id, s.config_block()) for s in servers]))
    assert set(parsed_yaml["extensions"]) == {s.id for s in servers}


def test_http_servers_do_not_require_a_command(catalog: Catalog) -> None:
    for server in catalog.servers:
        if server.transport == "http":
            assert server.url
            assert server.command is None


def test_verify_detects_a_broken_catalog(tmp_path: Path) -> None:
    raw = json.loads((ROOT / "mcps" / "catalog.json").read_text(encoding="utf-8"))
    raw["servers"][0]["harnesses"] = ["not-a-harness"]
    raw["servers"][1]["required_env"] = []
    raw["servers"][1]["args"] = raw["servers"][1].get("args", []) + ["${UNDECLARED_VAR}"]
    raw["profiles"]["core"] = ["ghost-server"]

    broken = tmp_path / "mcps"
    broken.mkdir()
    (broken / "catalog.json").write_text(json.dumps(raw), encoding="utf-8")

    problems = verify_catalog(Catalog.load(tmp_path))
    joined = "\n".join(problems)
    assert "unknown harnesses" in joined
    assert "UNDECLARED_VAR" in joined
    assert "ghost-server" in joined


def test_generated_artifacts_match_the_catalog(catalog: Catalog) -> None:
    summary_path = ROOT / "mcps" / "summary.json"
    assert summary_path.exists(), "run `python scripts/mcp_catalog.py generate`"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    assert summary["servers"] == len(catalog.servers)
    for harness in catalog.harnesses:
        candidates = [ROOT / "mcps" / "generated" / f"{harness}{ext}" for ext in (".json", ".toml", ".yaml")]
        assert any(p.exists() for p in candidates), f"missing generated bundle for {harness}"
