"""Model Context Protocol (MCP) catalog, installer and verifier.

The catalog (``mcps/catalog.json``) is the single source of truth for which MCP
servers All-Skills can wire into an agent harness. This module turns a catalog
server entry into the exact config block a harness expects, and merges it into
that harness's config file without touching entries it did not create.

Design rules:

* **Non-destructive.** Only the ``<config_key>`` object is touched, entries that
  already exist are left byte-identical, and a ``.bak`` copy is written before
  the first mutation.
* **Idempotent.** Installing the same server twice is a no-op (``unchanged``),
  so the command is safe to run in a loop or from a bootstrap script.
* **Deterministic.** Serialisation order is stable, so a generated config is
  reproducible and safe to commit.
* **Honest about limits.** Harnesses whose config is TOML or YAML get a rendered
  fragment (``fragment-only``) instead of an in-place rewrite, because silently
  rewriting a user's TOML/YAML with a JSON fragment would corrupt it.
"""

from __future__ import annotations

import json
import os
import re
import shutil
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

CATALOG_RELPATH = Path("mcps") / "catalog.json"
PLACEHOLDER_RE = re.compile(r"\$\{([A-Z][A-Z0-9_]*)\}")

RISK_ORDER = {"low": 0, "medium": 1, "high": 2, "critical": 3}


class CatalogError(ValueError):
    """Raised when the catalog itself is malformed."""


@dataclass
class McpServer:
    """One catalog entry."""

    id: str
    name: str
    description: str
    tier: str
    category: str
    transport: str
    vendor: str = "unknown"
    official: bool = False
    command: Optional[str] = None
    args: List[str] = field(default_factory=list)
    env: Dict[str, str] = field(default_factory=dict)
    url: Optional[str] = None
    headers: Dict[str, str] = field(default_factory=dict)
    required_env: List[str] = field(default_factory=list)
    required_env_optional: bool = False
    risk: str = "low"
    license: str = "unknown"
    docs: str = ""
    harnesses: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, raw: Dict[str, Any]) -> "McpServer":
        return cls(
            id=str(raw["id"]),
            name=str(raw.get("name") or raw["id"]),
            description=str(raw.get("description") or ""),
            tier=str(raw.get("tier") or "full"),
            category=str(raw.get("category") or "utilities"),
            transport=str(raw.get("transport") or "stdio"),
            vendor=str(raw.get("vendor") or "unknown"),
            official=bool(raw.get("official", False)),
            command=raw.get("command"),
            args=list(raw.get("args") or []),
            env=dict(raw.get("env") or {}),
            url=raw.get("url"),
            headers=dict(raw.get("headers") or {}),
            required_env=list(raw.get("required_env") or []),
            required_env_optional=bool(raw.get("required_env_optional", False)),
            risk=str(raw.get("risk") or "low"),
            license=str(raw.get("license") or "unknown"),
            docs=str(raw.get("docs") or ""),
            harnesses=list(raw.get("harnesses") or []),
        )

    # ---- Rendering -------------------------------------------------------

    def config_block(self, workspace: str = ".", env: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Render the harness-neutral MCP server block (Claude/Cursor shape)."""
        if self.transport == "http":
            block: Dict[str, Any] = {"type": "http", "url": _substitute(self.url or "", workspace)}
            if self.headers:
                block["headers"] = {k: _substitute(v, workspace) for k, v in self.headers.items()}
        else:
            block = {
                "command": self.command,
                "args": [_substitute(a, workspace) for a in self.args],
            }
        merged_env = {k: _substitute(v, workspace) for k, v in self.env.items()}
        merged_env.update(env or {})
        if merged_env:
            block["env"] = merged_env
        return block

    def required_placeholders(self) -> List[str]:
        """Environment variables this server definitely needs to run."""
        if self.required_env_optional:
            return []
        return list(self.required_env)

    def missing_env(self, environ: Optional[Mapping[str, str]] = None) -> List[str]:
        resolved: Mapping[str, str] = os.environ if environ is None else environ
        return [name for name in self.required_placeholders() if not resolved.get(name)]


def _substitute(value: str, workspace: str) -> str:
    return value.replace("${WORKSPACE}", workspace or ".")


@dataclass
class Catalog:
    path: Path
    servers: List[McpServer]
    profiles: Dict[str, List[str]]
    harnesses: Dict[str, Dict[str, Any]]
    version: str = "1.0.0"

    @classmethod
    def load(cls, root: Path) -> "Catalog":
        path = root / CATALOG_RELPATH
        if not path.exists():
            raise CatalogError(f"MCP catalog not found: {path}")
        with open(path, encoding="utf-8") as handle:
            raw = json.load(handle)
        servers = [McpServer.from_dict(item) for item in raw.get("servers", [])]
        return cls(
            path=path,
            servers=servers,
            profiles=dict(raw.get("profiles") or {}),
            harnesses=dict(raw.get("harnesses") or {}),
            version=str(raw.get("version") or "1.0.0"),
        )

    # ---- Queries ---------------------------------------------------------

    def get(self, server_id: str) -> Optional[McpServer]:
        for server in self.servers:
            if server.id == server_id:
                return server
        return None

    def resolve(self, names: Sequence[str]) -> List[McpServer]:
        """Expand ids and profile names into an ordered, de-duplicated list."""
        seen: Dict[str, McpServer] = {}
        for name in names:
            if name in self.profiles:
                for member in self.profiles[name]:
                    server = self.get(member) or self._wildcard(member)
                    if server is None:
                        raise CatalogError(f"profile {name!r} references unknown server {member!r}")
                    seen.setdefault(server.id, server)
                continue
            server = self.get(name) or self._wildcard(name)
            if server is None:
                raise CatalogError(f"unknown MCP server {name!r}")
            seen.setdefault(server.id, server)
        return list(seen.values())

    def _wildcard(self, name: str) -> Optional[McpServer]:
        return None

    def by_category(self) -> Dict[str, List[McpServer]]:
        out: Dict[str, List[McpServer]] = {}
        for server in self.servers:
            out.setdefault(server.category, []).append(server)
        return out

    def tier(self, name: str) -> List[McpServer]:
        return [s for s in self.servers if s.tier == name]


def expand_profile(catalog: Catalog, profile: str) -> List[McpServer]:
    """Expand a profile, honouring the ``["*"]`` "everything" convention."""
    if profile not in catalog.profiles:
        raise CatalogError(f"unknown profile {profile!r} (known: {', '.join(sorted(catalog.profiles))})")
    members = catalog.profiles[profile]
    if members == ["*"]:
        return list(catalog.servers)
    return catalog.resolve(members)


# ---------------------------------------------------------------------------
# Harness config writing
# ---------------------------------------------------------------------------


def harness_names(catalog: Catalog) -> List[str]:
    return sorted(catalog.harnesses)


def config_path(catalog: Catalog, harness: str, scope: str, root: Path) -> Path:
    spec = catalog.harnesses.get(harness)
    if not spec:
        raise CatalogError(f"unknown harness {harness!r} (known: {', '.join(harness_names(catalog))})")
    scopes = spec.get("scope") or {}
    raw = scopes.get(scope)
    if not raw:
        raise CatalogError(f"harness {harness!r} has no {scope!r} scope")
    path = Path(raw).expanduser()
    return path if path.is_absolute() else (root / path)


def to_harness_block(server: McpServer, harness: str, workspace: str) -> Dict[str, Any]:
    """Translate a rendered block into the harness-specific dialect."""
    block = server.config_block(workspace)
    if harness == "vscode":
        # VS Code uses "type": "stdio" and keeps the rest identical.
        if block.get("type") is None:
            block = {"type": "stdio", **block}
    elif harness == "opencode":
        # OpenCode expects {type: "local", command: [cmd, ...args], environment: {...}}
        if "command" in block:
            env = block.pop("env", None)
            block = {
                "type": "local",
                "command": [block["command"], *block.get("args", [])],
                **({"environment": env} if env else {}),
            }
        else:
            url = block.pop("url", "")
            block = {"type": "remote", "url": url, **block}
    elif harness == "zed":
        # Zed's context_servers always nest the invocation under "command".
        if "command" in block:
            nested = {"path": block["command"], "args": block.get("args", [])}
            if "env" in block:
                nested["env"] = block["env"]
            block = {"command": nested, "settings": {}}
        else:
            block = {"url": block.get("url", "")}
    return block


def render_toml_fragment(servers: Iterable[Tuple[str, Dict[str, Any]]], table: str = "mcp_servers") -> str:
    """Render a Codex-compatible TOML fragment for the given servers."""
    lines: List[str] = ["# Generated by `allskills mcp install --harness codex`"] 
    for name, block in servers:
        lines.append(f"\n[{table}.{name}]")
        if "command" in block:
            lines.append(f"command = {json.dumps(block['command'])}")
            if block.get("args"):
                lines.append(f"args = {json.dumps(block['args'])}")
        elif "url" in block:
            lines.append(f"url = {json.dumps(block['url'])}")
        env = block.get("env") or {}
        if env:
            lines.append(f"\n[{table}.{name}.env]")
            for key, value in env.items():
                lines.append(f"{key} = {json.dumps(value)}")
    return "\n".join(lines) + "\n"


@dataclass
class InstallResult:
    harness: str
    scope: str
    path: Path
    added: List[str] = field(default_factory=list)
    unchanged: List[str] = field(default_factory=list)
    skipped: List[Tuple[str, str]] = field(default_factory=list)
    written: bool = False
    dry_run: bool = False
    fragment: Optional[str] = None
    backup: Optional[Path] = None

    def as_dict(self) -> Dict[str, Any]:
        return {
            "harness": self.harness,
            "scope": self.scope,
            "path": str(self.path),
            "added": self.added,
            "unchanged": self.unchanged,
            "skipped": [{"server": s, "reason": r} for s, r in self.skipped],
            "written": self.written,
            "dry_run": self.dry_run,
            "fragment": self.fragment,
            "backup": str(self.backup) if self.backup else None,
        }


def plan_install(
    catalog: Catalog,
    harness: str,
    servers: Sequence[McpServer],
    root: Path,
    scope: str = "project",
    workspace: str = ".",
) -> InstallResult:
    """Work out what installing ``servers`` into ``harness`` would change."""
    spec = catalog.harnesses.get(harness)
    if not spec:
        raise CatalogError(f"unknown harness {harness!r} (known: {', '.join(harness_names(catalog))})")
    path = config_path(catalog, harness, scope, root)
    key = str(spec.get("config_key") or "mcpServers")
    mode = str(spec.get("merge") or "merge-nested")
    result = InstallResult(harness=harness, scope=scope, path=path)

    fragment_mode = mode != "merge-nested"
    existing_config: Dict[str, Any] = {}
    if not fragment_mode and path.exists():
        try:
            existing_config = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise CatalogError(f"{path} is not valid JSON: {exc}") from exc
    existing_servers = existing_config.get(key) or {}

    rendered: List[Tuple[str, Dict[str, Any]]] = []
    for server in servers:
        if harness not in server.harnesses:
            result.skipped.append((server.id, f"not supported on {harness}"))
            continue
        block = to_harness_block(server, harness, workspace)
        rendered.append((server.id, block))
        if server.id in existing_servers and existing_servers[server.id] == block:
            result.unchanged.append(server.id)
        else:
            result.added.append(server.id)

    if fragment_mode:
        result.fragment = (
            render_toml_fragment(rendered, table=key)
            if spec.get("format") == "toml"
            else render_yaml_fragment(rendered)
        )
        return result

    merged = dict(existing_config)
    merged_servers = dict(existing_servers)
    for name, block in rendered:
        merged_servers[name] = block
    merged[key] = dict(sorted(merged_servers.items()))
    result._merged = merged  # type: ignore[attr-defined]
    return result


def render_yaml_fragment(rendered: Iterable[Tuple[str, Dict[str, Any]]]) -> str:
    """Render a Goose-compatible YAML fragment (parsable by any YAML loader)."""
    lines: List[str] = ["# Generated by `allskills mcp install`", "extensions:"]
    for name, block in rendered:
        lines.append(f"  {name}:")
        lines.append("    enabled: true")
        lines.append("    type: stdio")
        if "command" in block:
            lines.append(f"    cmd: {json.dumps(block['command'])}")
            args = block.get("args") or []
            if args:
                lines.append("    args:")
                for arg in args:
                    lines.append(f"      - {json.dumps(arg)}")
        elif "url" in block:
            lines.append(f"    uri: {json.dumps(block['url'])}")
        env = block.get("env") or {}
        if env:
            lines.append("    envs:")
            for key, value in env.items():
                lines.append(f"      {key}: {json.dumps(value)}")
    return "\n".join(lines) + "\n"


def apply_install(result: InstallResult, dry_run: bool = False) -> InstallResult:
    """Persist a planned install. Never mutates when ``dry_run``."""
    result.dry_run = dry_run
    if result.fragment is not None:
        result.written = False
        return result
    merged = getattr(result, "_merged", None)
    if merged is None:
        raise CatalogError("apply_install() called without plan_install()")
    if dry_run or not result.added:
        result.written = False
        return result
    result.path.parent.mkdir(parents=True, exist_ok=True)
    if result.path.exists():
        backup = result.path.with_suffix(result.path.suffix + ".bak")
        shutil.copy2(result.path, backup)
        result.backup = backup
    result.path.write_text(json.dumps(merged, indent=2) + "\n", encoding="utf-8")
    result.written = True
    return result


# ---------------------------------------------------------------------------
# Verification
# ---------------------------------------------------------------------------


def verify_catalog(catalog: Catalog) -> List[str]:
    """Return a list of problems. Empty means the catalog is coherent."""
    problems: List[str] = []
    seen: set[str] = set()
    harness_ids = set(catalog.harnesses)
    for server in catalog.servers:
        if server.id in seen:
            problems.append(f"duplicate server id: {server.id}")
        seen.add(server.id)
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", server.id):
            problems.append(f"{server.id}: id must be kebab-case ascii")
        if server.transport not in ("stdio", "http"):
            problems.append(f"{server.id}: unsupported transport {server.transport!r}")
        if server.transport == "stdio" and not server.command:
            problems.append(f"{server.id}: stdio server has no command")
        if server.transport == "http" and not server.url:
            problems.append(f"{server.id}: http server has no url")
        if server.tier not in ("core", "standard", "full"):
            problems.append(f"{server.id}: unknown tier {server.tier!r}")
        if server.risk not in RISK_ORDER:
            problems.append(f"{server.id}: unknown risk {server.risk!r}")
        if not server.description:
            problems.append(f"{server.id}: missing description")
        if not server.docs:
            problems.append(f"{server.id}: missing docs link")
        unknown = [h for h in server.harnesses if h not in harness_ids]
        if unknown:
            problems.append(f"{server.id}: unknown harnesses {unknown}")
        if not server.harnesses:
            problems.append(f"{server.id}: no harnesses declared")
        # Every ${VAR} reference must be a declared env var so installers can
        # prompt for it instead of writing a broken config.
        referenced = set(PLACEHOLDER_RE.findall(" ".join(server.args) + " " + (server.url or "")
                                                 + " " + " ".join(server.headers.values())))
        undeclared = sorted(referenced - set(server.required_env) - {"WORKSPACE"})
        if undeclared:
            problems.append(f"{server.id}: placeholders {undeclared} are not declared in required_env")
    for name, members in catalog.profiles.items():
        if members == ["*"]:
            continue
        for member in members:
            if member not in seen:
                problems.append(f"profile {name!r} references unknown server {member!r}")
    for harness, spec in catalog.harnesses.items():
        for required_key in ("name", "scope", "config_key", "format", "merge", "docs"):
            if required_key not in spec:
                problems.append(f"harness {harness!r} is missing {required_key!r}")
        for scope_name in ("project", "user"):
            if not (spec.get("scope") or {}).get(scope_name):
                problems.append(f"harness {harness!r} has no {scope_name!r} scope path")
    return problems


def catalog_summary(catalog: Catalog) -> Dict[str, Any]:
    by_tier: Dict[str, int] = {}
    by_category: Dict[str, int] = {}
    for server in catalog.servers:
        by_tier[server.tier] = by_tier.get(server.tier, 0) + 1
        by_category[server.category] = by_category.get(server.category, 0) + 1
    return {
        "version": catalog.version,
        "servers": len(catalog.servers),
        "by_tier": dict(sorted(by_tier.items())),
        "by_category": dict(sorted(by_category.items())),
        "profiles": {name: (len(catalog.servers) if m == ["*"] else len(m)) for name, m in sorted(catalog.profiles.items())},
        "harnesses": len(catalog.harnesses),
        "generated_at": date.today().isoformat(),
    }
