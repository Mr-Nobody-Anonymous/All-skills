#!/usr/bin/env python3
"""All-skills universal CLI.

Every command exits non-zero on failure.

  init             Link the active skill harness into agent tools (scripts/setup_tools.py)
  search           Ranked search: canonical skills via the router, then the catalog
  doctor           Health check; --full validates 11 layers by content, not presence
  verify           Verify lockfile hashes, frontmatter schema and harness links
  verify-registry  Registry & statistics integrity
  stats            Show (or --verify) platform statistics
  test             Run the platform test suite
  lock             Regenerate skills.lock (--verify checks it instead)
  sources          List registered upstream sources
  sync             Import / update skills from upstream sources (scripts/sync_sources.py)
  profile          list | show <name> | install <name> [--dest DIR] [--dry-run]
  execute, run     Execute a skill through the governed runtime
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent  # replaced by the resolved workspace in main()

def run_cmd(args_list: list[str]) -> int:
    return subprocess.run([sys.executable] + args_list, cwd=REPO_ROOT).returncode

# ─────────────────────────────────────────────────────────────────────────────
# DOCTOR — 11-layer full diagnostic
# ─────────────────────────────────────────────────────────────────────────────

def _check(label: str, ok: bool, detail: str = "") -> bool:
    """Print one diagnostic row and return the ok flag."""
    status = "PASS" if ok else "FAIL"
    symbol = "✅" if ok else "❌"
    detail_str = f"  ({detail})" if detail else ""
    print(f"  {symbol} {label:<28} {status}{detail_str}")
    return ok


def _validate_dependencies() -> tuple[bool, str]:
    sys.path.insert(0, str(REPO_ROOT / "src"))
    from skills.dependencies import generate_dependencies_json
    from skills.registry import load_registry

    deps_path = REPO_ROOT / "skills" / "dependencies.json"
    graph_path = REPO_ROOT / "dependency_graph.json"
    try:
        committed = json.loads(deps_path.read_text(encoding="utf-8"))
        registry = load_registry(REPO_ROOT)
        if committed != generate_dependencies_json(registry.entries):
            return False, "skills/dependencies.json is stale (run scripts/refresh_registry.py)"
        graph = json.loads(graph_path.read_text(encoding="utf-8"))
        nodes, edges = graph.get("nodes", {}), graph.get("edges", [])
        if graph.get("nodes_count") != len(nodes) or any(not {"source", "target"} <= set(e) for e in edges):
            return False, "dependency_graph.json structure is inconsistent"
        outside = sum(1 for e in edges if e["target"] not in nodes)
        return True, f"{len(registry.entries)} skills current; graph {len(nodes):,} nodes, {outside} tool/external edges"
    except Exception as exc:
        return False, str(exc)


def _validate_policies() -> tuple[bool, str]:
    sys.path.insert(0, str(REPO_ROOT / "src"))
    from skills.policy import PolicyEngine

    try:
        engine = PolicyEngine(REPO_ROOT)  # strict: malformed policy.json raises
        files = sorted((REPO_ROOT / "policies").glob("*"))
        for f in files:
            if f.suffix in (".yaml", ".yml"):
                _load_yaml(f)
            elif f.suffix == ".json":
                json.loads(f.read_text(encoding="utf-8"))
        return bool(files), f"{len(engine.policies)} capability policies valid, {len(files)} policy files parse"
    except Exception as exc:
        return False, str(exc)


def _validate_provenance() -> tuple[bool, str]:
    sys.path.insert(0, str(REPO_ROOT / "src"))
    from skills.registry import load_registry

    try:
        records = json.loads((REPO_ROOT / "skills" / "SOURCES.json").read_text(encoding="utf-8")).get("skills", [])
        recorded = {r.get("skill") for r in records}
        missing = [e.id for e in load_registry(REPO_ROOT).entries if e.id not in recorded]
        return not missing, (f"{len(records)} provenance records cover every canonical skill" if not missing
                             else f"{len(missing)} skills without provenance record, e.g. {missing[:3]}")
    except Exception as exc:
        return False, str(exc)


def _validate_lockfile() -> tuple[bool, str]:
    sys.path.insert(0, str(REPO_ROOT / "src"))
    from skills.lock import SkillLockManager

    res = SkillLockManager(REPO_ROOT).verify_all()
    if "error" in res:
        return False, str(res["error"])
    return res["failed"] == 0, f"{res['passed']}/{res['total']} skill hashes match skills.lock"


def cmd_doctor(full: bool = False) -> int:
    """Run system diagnostics. With --full, validates all 11 layers."""
    print()
    print("╔══════════════════════════════════════════════════════╗")
    print("║   All-skills Platform Doctor                        ║")
    print("╚══════════════════════════════════════════════════════╝")
    print(f"  Workspace: {REPO_ROOT}")
    print()

    failures = []

    # ── Layer 1: Registry ─────────────────────────────────────────────────────
    reg = REPO_ROOT / "registry" / "skills.json"
    if reg.exists():
        try:
            records = _catalog_records()
            invalid = [r for r in records if not r.get("id") or not r.get("path")]
            if not (REPO_ROOT / "awesome_skills").is_dir():
                ok = _check("Registry", not invalid,
                            f"{len(records):,} records; catalog content not provisioned (metadata only)")
            else:
                absent = [r["id"] for r in records if r.get("path") and not (REPO_ROOT / r["path"]).parent.is_dir()]
                ok = _check("Registry", not invalid and not absent,
                            f"{len(records):,} records" if not invalid and not absent
                            else f"{len(invalid)} invalid records, {len(absent)} missing folders (e.g. {absent[:3]})")
        except Exception as e:
            ok = _check("Registry", False, str(e))
    else:
        ok = _check("Registry", False, "registry/skills.json missing")
    if not ok:
        failures.append("Registry")

    if not full:
        # Quick doctor: only registry + harnesses + tests
        r = subprocess.run(
            [sys.executable, "scripts/setup_tools.py", "--verify"],
            cwd=REPO_ROOT, capture_output=True, text=True,
        )
        ok = _check("Harnesses", r.returncode == 0)
        if not ok:
            failures.append("Harnesses")

        t = subprocess.run(
            [sys.executable, "scripts/skills/skills.py", "test"],
            cwd=REPO_ROOT, capture_output=True, text=True,
        )
        ok = _check("Test suite", t.returncode == 0)
        if not ok:
            failures.append("Tests")

        print()
        if not failures:
            print("  🎉 All checks passed. Run with --full for complete 11-layer audit.")
            return 0
        else:
            print(f"  ⚠️  {len(failures)} check(s) failed: {', '.join(failures)}")
            return 1

    # ─── Full 11-layer diagnostic ─────────────────────────────────────────────
    print("  Full 11-layer audit:\n")

    # Layer 2: Skill frontmatter
    r = subprocess.run(
        [sys.executable, "scripts/validate_schema.py"],
        cwd=REPO_ROOT, capture_output=True, text=True,
    )
    lines = r.stdout.strip().split("\n")
    detail = lines[-1] if lines else ""
    ok = _check("Skill frontmatter", r.returncode == 0, detail)
    if not ok:
        failures.append("Skill frontmatter")

    # Layer 3: Dependencies
    ok = _check("Dependencies", *_validate_dependencies())
    if not ok:
        failures.append("Dependencies")

    # Layer 4: Profiles
    try:
        all_profiles = load_profiles()
        resolution = {sid: resolve_skill(sid) for prof in all_profiles.values() for sid in prof["skills"]}
        unresolved = sorted({f"{n}:{sid}" for n, prof in all_profiles.items()
                             for sid in prof["skills"] if resolution[sid][1] == "missing"})
        unprovisioned = sorted({sid for sid, (_, where) in resolution.items() if where.startswith("catalog (")})
        no_file = [n for n, prof in all_profiles.items() if not prof["file"]]
        ok = _check("Profiles", bool(all_profiles) and not unresolved and not no_file,
                    (f"{len(all_profiles)} profiles, every skill resolves"
                     + (f" ({len(unprovisioned)} in the unprovisioned catalog)" if unprovisioned else ""))
                    if not unresolved and not no_file
                    else f"unresolved skills {unresolved[:4]}, profiles without YAML {no_file[:4]}")
    except Exception as e:
        ok = _check("Profiles", False, str(e))
    if not ok:
        failures.append("Profiles")

    # Layer 5: Workflows
    workflows_dir = REPO_ROOT / "workflows"
    wf_files = [w for w in workflows_dir.glob("*.md") if w.name.lower() != "readme.md"] if workflows_dir.exists() else []
    empty = [w.name for w in wf_files if not w.read_text(encoding="utf-8").lstrip().startswith("#")]
    ok = _check("Workflows", bool(wf_files) and not empty,
                f"{len(wf_files)} workflows with headings" if not empty else f"no heading/empty: {empty}")
    if not ok:
        failures.append("Workflows")

    # Layer 6: Adapters
    adapters_dir = REPO_ROOT / "adapters"
    adapter_files = list(adapters_dir.glob("*.yaml")) if adapters_dir.exists() else []
    expected_agents = [
        "gemini", "claude", "cursor", "codex", "copilot",
        "vscode", "windsurf", "opencode", "cline", "roo", "goose",
    ]
    missing_adapters = [a for a in expected_agents
                        if not (adapters_dir / f"{a}.yaml").exists()]
    bad_adapters = []
    for a in expected_agents:
        path = adapters_dir / f"{a}.yaml"
        if path.exists():
            try:
                cfg = _load_yaml(path)
                if any(k not in cfg for k in ("agent_id", "display_name", "discovery_paths")):
                    bad_adapters.append(a)
            except Exception:
                bad_adapters.append(a)
    ok = _check("Adapters",
                not missing_adapters and not bad_adapters,
                f"{len(adapter_files)} YAML files, required keys present" if not missing_adapters and not bad_adapters
                else f"missing: {missing_adapters}, invalid: {bad_adapters}")
    if not ok:
        failures.append("Adapters")

    # Layer 7: Harnesses
    r = subprocess.run(
        [sys.executable, "scripts/setup_tools.py", "--verify"],
        cwd=REPO_ROOT, capture_output=True, text=True,
    )
    ok = _check("Harnesses", r.returncode == 0)
    if not ok:
        failures.append("Harnesses")

    # Layer 8: Permissions / Policies
    ok = _check("Permissions/Policies", *_validate_policies())
    if not ok:
        failures.append("Permissions")

    # Layer 9: Provenance
    ok = _check("Provenance", *_validate_provenance())
    if not ok:
        failures.append("Provenance")

    # Layer 10: Lockfile
    ok = _check("Lockfile", *_validate_lockfile())
    if not ok:
        failures.append("Lockfile")

    # Layer 11: Agent compatibility (registry/agents.json)
    agents_reg = REPO_ROOT / "registry" / "agents.json"
    if agents_reg.exists():
        try:
            with open(agents_reg, "r", encoding="utf-8") as f:
                ag_data = json.load(f)
            agents = ag_data.get("agents", {})
            n_agents = len(agents)
            no_adapter = [k for k, v in agents.items() if not (REPO_ROOT / str(v.get("adapter", ""))).is_file()]
            ok = _check("Agent compatibility", n_agents >= 11 and not no_adapter and ag_data.get("total") == n_agents,
                        f"{n_agents} agents, each with an adapter" if not no_adapter
                        else f"agents without adapter file: {no_adapter}")
        except Exception as e:
            ok = _check("Agent compatibility", False, str(e))
    else:
        ok = _check("Agent compatibility", False, "registry/agents.json missing")
    if not ok:
        failures.append("Agent compatibility")

    # ── Summary ──────────────────────────────────────────────────────────────
    total = 11
    passed = total - len(failures)
    print()
    print(f"  {'─'*50}")
    print(f"  Result: {passed}/{total} layers passed")
    if not failures:
        print("  🎉 ALL LAYERS PASSED — platform is fully healthy!")
        return 0
    else:
        print(f"  ⚠️  FAILED layers: {', '.join(failures)}")
        return 1

MIN_CANONICAL_SCORE = 10.0  # router scores below this are quality-boost noise
MIN_CATALOG_SCORE = 8.0     # at least a name/category token or two description tokens
_STOPWORDS = {"a", "an", "and", "the", "for", "to", "of", "in", "on", "with", "my", "me", "i", "is", "how"}


def _tokens(text: str) -> list[str]:
    import re
    return [t for t in re.findall(r"[a-z0-9]+", text.lower()) if len(t) > 1 and t not in _STOPWORDS]


def _catalog_records() -> list[dict]:
    reg = REPO_ROOT / "registry" / "skills.json"
    if not reg.exists():
        return []
    data = json.loads(reg.read_text(encoding="utf-8"))
    return data if isinstance(data, list) else list(data.get("skills", []))


def _score_catalog(record: dict, query: str, q_tokens: list[str]) -> float:
    ident = str(record.get("id", "")).lower()
    name = str(record.get("name", "")).lower()
    desc = str(record.get("description", "")).lower()
    q = query.lower().strip()
    if not q_tokens and not q:
        return 0.0
    score = 0.0
    if q in (ident, name):
        score += 60
    id_tokens = set(_tokens(ident)) | set(_tokens(name))
    cat_tokens = set(_tokens(str(record.get("category", ""))))
    desc_tokens = set(_tokens(desc))
    for t in q_tokens:
        score += 20 if t in id_tokens else 0
        score += 8 if t in cat_tokens else 0
        score += 4 if t in desc_tokens else 0
    if len(q) > 3 and (q in name or q in desc):
        score += 12
    return score


def search_catalog(query: str, category: str | None = None) -> list[dict]:
    """Rank canonical skills with the router, then catalog records by field relevance."""
    sys.path.insert(0, str(REPO_ROOT / "src"))
    from skills.registry import load_registry
    from skills.router import Router

    results: list[dict] = []
    seen: set[str] = set()
    registry = load_registry(REPO_ROOT)
    for match in Router(registry, workspace_root=REPO_ROOT).route(query, top_k=10):
        e = match.skill
        if match.score < MIN_CANONICAL_SCORE or (category and e.category != category):
            continue
        seen.add(e.name)
        results.append({"source": "canonical", "id": e.id, "name": e.name, "category": e.category,
                        "score": round(match.score, 1), "matched_on": match.matched_on,
                        "description": e.description, "path": f"skills/{e.path}"})
    q_tokens = _tokens(query)
    scored = []
    for rec in _catalog_records():
        if category and rec.get("category") != category:
            continue
        sc = _score_catalog(rec, query, q_tokens)
        if sc >= MIN_CATALOG_SCORE and rec.get("name") not in seen:
            scored.append((sc, rec))
    scored.sort(key=lambda item: (-item[0], str(item[1].get("id"))))
    for sc, rec in scored:
        results.append({"source": "catalog", "id": rec.get("id"), "name": rec.get("name"),
                        "category": rec.get("category"), "score": sc, "matched_on": "fields",
                        "description": rec.get("description", ""), "path": rec.get("path")})
    return results


def cmd_search(query: str, limit: int = 15, offset: int = 0, category: str | None = None, as_json: bool = False) -> int:
    results = search_catalog(query, category)
    page = results[offset: offset + limit]
    if as_json:
        print(json.dumps({"query": query, "category": category, "total": len(results),
                          "offset": offset, "limit": limit, "results": page}, indent=2))
        return 0
    if not results:
        print(f"No skills match {query!r}" + (f" in category {category!r}" if category else "") + ".")
        return 1
    if not page:
        print(f"No results on this page: {len(results)} matches in total (offset {offset}).")
        return 0
    print(f"\nSearch results for {query!r}: {len(results)} matches (showing {offset + 1}-{offset + len(page)})")
    for r in page:
        print(f"  [{r['source']:9}] {r['id']}  (score {r['score']}, {r['category']})")
        print(f"              {str(r['description'])[:100]}")
    if offset + len(page) < len(results):
        print(f"\n  More results: --offset {offset + limit}")
    return 0


# ─────────────────────────────────────────────────────────────────────────────
# PROFILES
# ─────────────────────────────────────────────────────────────────────────────

def _load_yaml(path: Path) -> dict:
    import yaml
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"{path}: profile must be a mapping")
    return data


def load_profiles() -> dict[str, dict]:
    """Merge profiles/*.yaml with the registry/profiles.json index."""
    reg_path = REPO_ROOT / "registry" / "profiles.json"
    index = json.loads(reg_path.read_text(encoding="utf-8")).get("profiles", {}) if reg_path.exists() else {}
    names = set(index) | {p.stem for p in (REPO_ROOT / "profiles").glob("*.yaml")}
    profiles: dict[str, dict] = {}
    for name in sorted(names):
        entry = dict(index.get(name, {}))
        yaml_path = REPO_ROOT / entry.get("file", f"profiles/{name}.yaml")
        data = _load_yaml(yaml_path) if yaml_path.exists() else {}
        skills = list(dict.fromkeys(list(data.get("active_skills") or []) + list(entry.get("skills") or [])))
        profiles[name] = {
            "name": name,
            "title": data.get("name", name),
            "description": data.get("description") or entry.get("description", ""),
            "file": str(yaml_path.relative_to(REPO_ROOT)) if yaml_path.exists() else None,
            "skills": skills,
            "unavailable": list(entry.get("unavailable") or []),
            "recommended_packs": list(data.get("recommended_packs") or []),
            "mcp_profile": data.get("mcp_profile"),
        }
    return profiles


def resolve_skill(skill_id: str) -> tuple[Path | None, str]:
    """Locate a skill folder: active harness, canonical library, then catalog."""
    active = REPO_ROOT / ".agents" / "skills" / skill_id
    if (active / "SKILL.md").is_file():
        return active, "active"
    canonical = sorted(REPO_ROOT.glob(f"skills/*/{skill_id}/SKILL.md"))
    if canonical:
        return canonical[0].parent, "canonical"
    catalog_here = (REPO_ROOT / "awesome_skills").is_dir()
    for rec in sorted(_catalog_records(), key=lambda r: str(r.get("path"))):
        if rec.get("id") == skill_id:
            folder = (REPO_ROOT / str(rec.get("path", ""))).parent
            if folder.is_dir():
                return folder, "catalog"
            if not catalog_here:
                return None, "catalog (not provisioned)"
    return None, "missing"


def cmd_profile(action: str, name: str | None, dest: str | None = None, dry_run: bool = False) -> int:
    import shutil
    from datetime import datetime, timezone

    profiles = load_profiles()
    if action == "list":
        print(f"\n{len(profiles)} profiles:\n")
        for prof in profiles.values():
            print(f"  {prof['name']:<20} {len(prof['skills']):>3} skills  {prof['description'][:70]}")
        return 0
    if not name or name not in profiles:
        print(f"Error: unknown profile {name!r}. Available: {', '.join(profiles)}", file=sys.stderr)
        return 1
    prof = profiles[name]
    resolved = {sid: resolve_skill(sid) for sid in prof["skills"]}

    if action == "show":
        print(f"\nProfile: {prof['name']} — {prof['title']}\n  {prof['description']}")
        print(f"  File: {prof['file']}   MCP profile: {prof['mcp_profile']}   Packs: {', '.join(prof['recommended_packs']) or '-'}")
        print(f"\n  Skills ({len(resolved)}):")
        for sid, (path, where) in resolved.items():
            print(f"    {'✓' if path else '✗'} {sid:<42} {where}")
        if prof["unavailable"]:
            print(f"\n  Planned but not in the library: {', '.join(prof['unavailable'])}")
        return 0

    # install — resolve everything first; nothing is copied if a skill is missing
    missing = [sid for sid, (path, where) in resolved.items() if path is None and where == "missing"]
    unprovisioned = [sid for sid, (path, where) in resolved.items() if path is None and where != "missing"]
    if missing:
        print(f"Error: profile {name!r} references skills that are not in the library: {', '.join(missing)}",
              file=sys.stderr)
        return 1
    if unprovisioned:
        print(f"Error: {', '.join(unprovisioned)} live in the awesome_skills catalog, which is not provisioned in "
              f"{REPO_ROOT}. Run inside a full clone or pass --workspace <clone>.", file=sys.stderr)
        return 1
    default_dest = REPO_ROOT / ".agents" / "skills"
    dest_dir = Path(dest).resolve() if dest else default_dest
    copied, present = [], []
    for sid, (src, where) in resolved.items():
        target = dest_dir / sid
        if (target / "SKILL.md").is_file():
            present.append(sid)
            continue
        if dry_run:
            print(f"  would install {sid} from {where} ({src.relative_to(REPO_ROOT)})")
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(src, target)
        copied.append(sid)
    if dry_run:
        print(f"Dry run: {len(resolved) - len(present)} to install, {len(present)} already present.")
        return 0
    absent = [sid for sid in resolved if not (dest_dir / sid / "SKILL.md").is_file()]
    if absent:
        print(f"Error: installation incomplete, missing after copy: {', '.join(absent)}", file=sys.stderr)
        return 1
    state_file = (REPO_ROOT / ".agents" / "state" / "active_profile.json") if dest_dir == default_dest \
        else dest_dir / ".all-skills-profile.json"
    state_file.parent.mkdir(parents=True, exist_ok=True)
    state_file.write_text(json.dumps({
        "profile": name, "skills": list(resolved), "destination": str(dest_dir),
        "installed_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "mcp_profile": prof["mcp_profile"], "recommended_packs": prof["recommended_packs"],
    }, indent=2) + "\n", encoding="utf-8")
    print(f"Profile {name!r}: installed {len(copied)} skill(s), {len(present)} already present, into {dest_dir}.")
    if prof["unavailable"]:
        print(f"Note: planned skills not yet in the library: {', '.join(prof['unavailable'])}")
    print(f"State recorded in {state_file}")
    return 0


def cmd_verify() -> int:
    """Lockfile hashes + frontmatter schema + harness links; non-zero if any fails."""
    checks = [
        ("Lockfile hashes", ["scripts/skills/skills.py", "lock", "--verify"]),
        ("Frontmatter schema", ["scripts/validate_schema.py"]),
        ("Harness links", ["scripts/setup_tools.py", "--verify"]),
    ]
    failed = []
    for label, args in checks:
        # Decode as UTF-8 explicitly: the child scripts write UTF-8, while text=True alone
        # would use the locale code page on Windows (cp1252) and can fail to decode.
        proc = subprocess.run([sys.executable] + args, cwd=REPO_ROOT, capture_output=True,
                              text=True, encoding="utf-8", errors="replace")
        ok = _check(label, proc.returncode == 0, (proc.stdout.strip().splitlines() or [""])[-1][:70])
        if not ok:
            failed.append(label)
            print(proc.stdout[-2000:] + proc.stderr[-2000:])
    return 1 if failed else 0


def main() -> int:
    parser = argparse.ArgumentParser(prog="allskills", description="All-skills Universal Operating System CLI")
    parser.add_argument("--workspace", help="All-Skills workspace (default: ALL_SKILLS_WORKSPACE, the current "
                                            "directory tree, then this installation)")
    subparsers = parser.add_subparsers(dest="subcommand", help="Command to execute")

    s_init = subparsers.add_parser("init", help="Link the active harness into agent tools, then verify")
    s_init.add_argument("--global", dest="is_global", action="store_true", help="Also link global user directories")
    s_search = subparsers.add_parser("search", help="Ranked search across canonical skills and the catalog")
    s_search.add_argument("query", help="Keywords or functional phrase")
    s_search.add_argument("--limit", type=int, default=15, help="Results per page (default 15)")
    s_search.add_argument("--offset", type=int, default=0, help="Skip the first N results")
    s_search.add_argument("--category", help="Only return skills in this category")
    s_search.add_argument("--json", action="store_true", help="Machine-readable output")

    s_doctor = subparsers.add_parser("doctor", help="Run system diagnostics")
    s_doctor.add_argument("--full", action="store_true", help="Run the complete 11-layer audit")
    subparsers.add_parser("verify", help="Verify harness and lockfile integrity")
    subparsers.add_parser("verify-registry", help="Run independent registry and statistics integrity verification")
    s_stats = subparsers.add_parser("stats", help="View or verify platform statistics")
    s_stats.add_argument("--verify", action="store_true", help="Verify stats.json without modifying")
    subparsers.add_parser("test", help="Run full regression test suite")
    subparsers.add_parser("sources", help="List registered upstream sources")
    subparsers.add_parser("sync", help="Synchronize upstream sources")
    s_lock = subparsers.add_parser("lock", help="Regenerate skills.lock (or --verify it)")
    s_lock.add_argument("--verify", action="store_true", help="Verify hashes instead of regenerating")

    s_prof = subparsers.add_parser("profile", help="Manage role profiles")
    s_prof.add_argument("action", choices=["list", "install", "show"])
    s_prof.add_argument("name", nargs="?", help="Profile name (see 'profile list')")
    s_prof.add_argument("--dest", help="Install into this directory instead of .agents/skills")
    s_prof.add_argument("--dry-run", action="store_true", help="Show what install would do")

    for exec_alias in ("execute", "run"):
        s_exec = subparsers.add_parser(exec_alias, help="Execute a skill through universal runtime")
        s_exec.add_argument("skill_id", help="Canonical skill ID")
        s_exec.add_argument("--input", help="JSON string of execution inputs")
        s_exec.add_argument("--tools", help="Comma-separated declared tools")
        s_exec.add_argument("--dry-run", action="store_true", help="Simulate execution without modifying artifacts")
        s_exec.add_argument("--json", action="store_true", help="Print structured ExecutionResult as JSON")
        s_exec.add_argument("--approval-id", help="request_id from an approval_required result")
        s_exec.add_argument("--approved-by", help="Name of the human approving an ASK capability")

    args = parser.parse_args()
    global REPO_ROOT
    sys.path.insert(0, str(REPO_ROOT / "src"))
    from skills.workspace import ENV_VAR, WorkspaceNotFound, resolve_workspace
    try:
        REPO_ROOT = resolve_workspace(args.workspace, cwd=Path.cwd())
    except WorkspaceNotFound as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    os.environ[ENV_VAR] = str(REPO_ROOT)

    if args.subcommand == "doctor":
        return cmd_doctor(full=getattr(args, "full", False))
    elif args.subcommand == "search":
        return cmd_search(args.query, limit=args.limit, offset=args.offset, category=args.category, as_json=args.json)
    elif args.subcommand == "init":
        setup = ["scripts/setup_tools.py"] + (["--global"] if args.is_global else [])
        return run_cmd(setup) or run_cmd(["scripts/setup_tools.py", "--verify"])
    elif args.subcommand == "lock":
        return run_cmd(["scripts/skills/skills.py", "lock"] + (["--verify"] if args.verify else []))
    elif args.subcommand in {"execute", "run"}:
        cmd = ["scripts/skills/skills.py", "execute", args.skill_id]
        if getattr(args, "input", None):
            cmd.extend(["--input", args.input])
        if getattr(args, "tools", None):
            cmd.extend(["--tools", args.tools])
        if getattr(args, "dry_run", False):
            cmd.append("--dry-run")
        if getattr(args, "json", False):
            cmd.append("--json")
        if getattr(args, "approval_id", None):
            cmd.extend(["--approval-id", args.approval_id, "--approved-by", args.approved_by or ""])
        return run_cmd(cmd)
    elif args.subcommand == "verify":
        return cmd_verify()
    elif args.subcommand == "verify-registry":
        return run_cmd(["scripts/verify_registry_integrity.py"])
    elif args.subcommand == "stats":
        cmd = ["scripts/compute_stats.py"]
        if getattr(args, "verify", False):
            cmd.append("--verify")
        return run_cmd(cmd)
    elif args.subcommand == "test":
        return run_cmd(["scripts/skills/skills.py", "test"])
    elif args.subcommand == "sources":
        reg = REPO_ROOT / "sources" / "registry.yaml"
        print(reg.read_text(encoding="utf-8"))
        return 0
    elif args.subcommand == "sync":
        return run_cmd(["scripts/sync_sources.py"])
    elif args.subcommand == "profile":
        return cmd_profile(args.action, args.name, dest=args.dest, dry_run=args.dry_run)
    else:
        parser.print_help()
        return 0 if args.subcommand is None else 1

if __name__ == "__main__":
    sys.exit(main())
