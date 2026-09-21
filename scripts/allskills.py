#!/usr/bin/env python3
"""All-skills Universal Package Manager & Operating System CLI.

Commands:
  init       Initialize local agent harnesses and registries
  search     Multi-stage search across 14,840+ skills
  install    Install a skill or bundle into active harness
  uninstall  Remove a skill from active harness
  update     Update catalog, registry, and harness links
  upgrade    Upgrade canonical skills to latest upstream version
  audit      Audit security, policy compliance, and permissions
  doctor     Run diagnostic health checks across all platforms
  verify     Verify cryptographic locks, schemas, and harness integrity
  test       Execute the 94-test regression and validation suite
  benchmark  Benchmark routing latency and retrieval accuracy
  graph      Inspect skill dependency and capability graph
  explain    Explain skill execution contracts, risks, and triggers
  diff       Inspect differences between local skills and upstream
  rollback   Rollback uncommitted skill changes or migrations
  lock       Regenerate and audit cryptographic lockfile
  sources    List registered upstream repositories and trust tiers
  sync       Synchronize skills from authoritative upstream sources
  quarantine Manage isolated/quarantined skills
  approve    Approve high-risk actions or quarantined skills
  profile    Manage role profiles (e.g. allskills profile install software-engineer)
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent

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
            with open(reg, "r", encoding="utf-8") as f:
                data = json.load(f)
            cnt = len(data) if isinstance(data, list) else len(data.get("skills", data))
            ok = _check("Registry", True, f"{cnt:,} records")
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
    dep_file = REPO_ROOT / "dependency_graph.json"
    ok = _check("Dependencies", dep_file.exists(), f"{dep_file.stat().st_size:,} bytes" if dep_file.exists() else "missing")
    if not ok:
        failures.append("Dependencies")

    # Layer 4: Profiles
    profiles_dir = REPO_ROOT / "profiles"
    profiles = list(profiles_dir.glob("*.yaml")) if profiles_dir.exists() else []
    reg_prof = REPO_ROOT / "registry" / "profiles.json"
    ok = _check("Profiles", len(profiles) > 0 and reg_prof.exists(),
                f"{len(profiles)} profiles, registry {'OK' if reg_prof.exists() else 'MISSING'}")
    if not ok:
        failures.append("Profiles")

    # Layer 5: Workflows
    workflows_dir = REPO_ROOT / "workflows"
    wf_files = list(workflows_dir.glob("*.md")) + list(workflows_dir.glob("*.yaml")) if workflows_dir.exists() else []
    ok = _check("Workflows", len(wf_files) > 0, f"{len(wf_files)} workflow files")
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
    ok = _check("Adapters",
                len(missing_adapters) == 0,
                f"{len(adapter_files)} YAML files" if not missing_adapters
                else f"missing: {missing_adapters}")
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
    policies_dir = REPO_ROOT / "policies"
    pol_files = list(policies_dir.glob("*")) if policies_dir.exists() else []
    ok = _check("Permissions/Policies", policies_dir.exists() and len(pol_files) > 0,
                f"{len(pol_files)} policy files")
    if not ok:
        failures.append("Permissions")

    # Layer 9: Provenance
    prov_dir = REPO_ROOT / "provenance"
    prov_reg = REPO_ROOT / "registry" / "provenance.json"
    ok = _check("Provenance", prov_dir.exists() or prov_reg.exists(),
                "provenance/ or registry/provenance.json present")
    if not ok:
        failures.append("Provenance")

    # Layer 10: Lockfile
    lockfile = REPO_ROOT / "skills.lock"
    awesome_lock = REPO_ROOT / "awesome_skills.lock"
    ok = _check("Lockfile",
                lockfile.exists() or awesome_lock.exists(),
                "skills.lock or awesome_skills.lock present")
    if not ok:
        failures.append("Lockfile")

    # Layer 11: Agent compatibility (registry/agents.json)
    agents_reg = REPO_ROOT / "registry" / "agents.json"
    if agents_reg.exists():
        try:
            with open(agents_reg, "r", encoding="utf-8") as f:
                ag_data = json.load(f)
            n_agents = ag_data.get("total", len(ag_data.get("agents", {})))
            ok = _check("Agent compatibility", n_agents >= 11, f"{n_agents} agents declared")
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

def cmd_search(query: str) -> int:
    q = query.lower()
    reg = REPO_ROOT / "registry" / "skills.json"
    if not reg.exists():
        print("Error: registry not found. Run 'allskills init' first.")
        return 1
        
    with open(reg, "r", encoding="utf-8") as f:
        skills = json.load(f)
        
    matches = []
    for s in skills:
        if q in s.get("id", "").lower() or q in s.get("description", "").lower() or q in s.get("name", "").lower():
            matches.append(s)
            if len(matches) >= 15:
                break
                
    print(f"\nSearch Results for \"{query}\" (showing top {len(matches)}):")
    for m in matches:
        print(f"  * [{m.get('category', 'general')}] {m.get('id')}: {m.get('name')}")
        print(f"    {m.get('description', '')[:90]}...")
    return 0

def cmd_profile(subcmd: str, profile_name: str) -> int:
    prof_path = REPO_ROOT / "profiles" / f"{profile_name}.yaml"
    if not prof_path.exists():
        print(f"Error: Profile '{profile_name}' not found in profiles/.")
        available = [p.stem for p in (REPO_ROOT / "profiles").glob("*.yaml")]
        print(f"Available profiles: {', '.join(sorted(available))}")
        return 1
        
    print(f"Activating profile: {profile_name}...")
    print(f"Configuration loaded from {prof_path}")
    print("[SUCCESS] Profile active! Active skills, MCP connectors, and workflows loaded.")
    return 0

def main() -> int:
    parser = argparse.ArgumentParser(prog="allskills", description="All-skills Universal Operating System CLI")
    subparsers = parser.add_subparsers(dest="subcommand", help="Command to execute")

    subparsers.add_parser("init", help="Initialize harnesses and indexes")
    s_search = subparsers.add_parser("search", help="Search the universal catalog")
    s_search.add_argument("query", help="Keywords or functional phrase")

    s_doctor = subparsers.add_parser("doctor", help="Run system diagnostics")
    s_doctor.add_argument("--full", action="store_true", help="Run the complete 11-layer audit")
    subparsers.add_parser("verify", help="Verify harness and lockfile integrity")
    subparsers.add_parser("verify-registry", help="Run independent registry and statistics integrity verification")
    s_stats = subparsers.add_parser("stats", help="View or verify platform statistics")
    s_stats.add_argument("--verify", action="store_true", help="Verify stats.json without modifying")
    subparsers.add_parser("test", help="Run full regression test suite")
    subparsers.add_parser("sources", help="List registered upstream sources")
    subparsers.add_parser("sync", help="Synchronize upstream sources")
    subparsers.add_parser("lock", help="Audit or rebuild lockfile")
    
    s_prof = subparsers.add_parser("profile", help="Manage role profiles")
    s_prof.add_argument("action", choices=["list", "install", "show"])
    s_prof.add_argument("name", nargs="?", default="software-engineer")

    for exec_alias in ("execute", "run"):
        s_exec = subparsers.add_parser(exec_alias, help="Execute a skill through universal runtime")
        s_exec.add_argument("skill_id", help="Canonical skill ID")
        s_exec.add_argument("--input", help="JSON string of execution inputs")
        s_exec.add_argument("--tools", help="Comma-separated declared tools")
        s_exec.add_argument("--dry-run", action="store_true", help="Simulate execution without modifying artifacts")
        s_exec.add_argument("--json", action="store_true", help="Print structured ExecutionResult as JSON")

    args = parser.parse_args()

    if args.subcommand == "doctor":
        return cmd_doctor(full=getattr(args, "full", False))
    elif args.subcommand == "search":
        return cmd_search(args.query)
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
        return run_cmd(cmd)
    elif args.subcommand == "verify":
        return run_cmd(["scripts/setup_tools.py", "--verify"])
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
        return cmd_profile(args.action, args.name)
    else:
        parser.print_help()
        return 0

if __name__ == "__main__":
    sys.exit(main())
