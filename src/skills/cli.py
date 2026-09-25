"""Installed entry point for the Agent Skills / All-skills CLI.

Operates both in development workspace and when installed as a standalone wheel.
"""
from __future__ import annotations

import argparse
import json
import os
import runpy
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def _find_repo_script() -> Path | None:
    """Return the repository script path if running in a source tree."""
    try:
        candidate = Path(__file__).resolve().parents[2] / "scripts" / "skills" / "skills.py"
        if candidate.exists():
            return candidate
    except Exception:
        pass
    return None


def _run_native_cli() -> None:
    """Package-native CLI execution when installed without repository scripts."""
    from ._version import __version__
    from .registry import load_registry
    from .router import Router
    from .runtime import ExecutionRuntime
    from .validator import Validator
    from .security import scan_all

    parser = argparse.ArgumentParser(
        prog="all-skills",
        description="Universal AI Agent Skill Operating System & Execution Runtime",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="cmd", help="Command to execute")

    # 1. list
    s_list = sub.add_parser("list", help="List registered skills")
    s_list.add_argument("--json", action="store_true", help="Output as JSON")

    # 2. search
    s_search = sub.add_parser("search", help="Search skills by query")
    s_search.add_argument("query", help="Keywords or description")

    # 3. route
    s_route = sub.add_parser("route", help="Route natural language query to best skill")
    s_route.add_argument("query", help="User intent or natural language prompt")
    s_route.add_argument("--top-k", type=int, default=3, help="Number of results")
    s_route.add_argument("--json", action="store_true", help="Output as JSON")

    # 4. execute / run
    for exec_cmd in ("execute", "run"):
        s_exec = sub.add_parser(exec_cmd, help="Execute a skill through the universal runtime")
        s_exec.add_argument("skill_id", help="Canonical skill ID")
        s_exec.add_argument("--input", help="JSON execution inputs")
        s_exec.add_argument("--tools", help="Comma-separated tools")
        s_exec.add_argument("--dry-run", action="store_true", help="Simulate execution")
        s_exec.add_argument("--json", action="store_true", help="Output as JSON")

    # 5. doctor
    sub.add_parser("doctor", help="Check skill library health")

    # 6. scan
    s_scan = sub.add_parser("scan", help="Run static security scan")
    s_scan.add_argument("--json", action="store_true", help="Output findings as JSON")

    args = parser.parse_args()
    workspace = Path.cwd()
    reg = load_registry(workspace)

    if args.cmd == "list":
        if getattr(args, "json", False):
            print(reg.to_json())
        else:
            print(f"Loaded {len(reg.entries)} skills:")
            for e in reg.entries[:50]:
                print(f"  * {e.id:<32} [{e.category}] {e.name}")
            if len(reg.entries) > 50:
                print(f"  ... and {len(reg.entries) - 50} more")
        sys.exit(0)

    elif args.cmd == "search":
        results = reg.search(args.query)
        print(f"Found {len(results)} matches for '{args.query}':")
        for r in results[:15]:
            print(f"  * {r.id:<32} {r.name} — {r.description[:70]}...")
        sys.exit(0)

    elif args.cmd == "route":
        router = Router(reg)
        matches = router.route(args.query, top_k=args.top_k)
        if getattr(args, "json", False):
            out = [{"id": m.skill.id, "score": m.score, "matched_on": m.matched_on} for m in matches]
            print(json.dumps(out, indent=2))
        else:
            for i, m in enumerate(matches, 1):
                print(f"{i}. {m.skill.id} (score={m.score:.1f}, matched_on={m.matched_on})")
                print(f"   {m.skill.description}")
        sys.exit(0)

    elif args.cmd in {"execute", "run"}:
        runtime = ExecutionRuntime(workspace)
        inp = json.loads(args.input) if getattr(args, "input", None) else {}
        tools = [t.strip() for t in args.tools.split(",")] if getattr(args, "tools", None) else None
        res = runtime.execute(args.skill_id, input=inp, tools=tools, dry_run=args.dry_run)
        if getattr(args, "json", False):
            print(json.dumps(res.to_dict(), indent=2))
        else:
            print(f"Skill: {res.skill}")
            print(f"Status: {res.status.upper()}")
            print(f"Duration: {res.duration_ms:.2f}ms")
            print(f"Audit ID: {res.audit_id}")
            if res.error:
                print(f"Error: {res.error}")
        sys.exit(0 if res.status == "completed" else 1)

    elif args.cmd == "doctor":
        validation = Validator(reg, workspace / "skills").validate_all()
        print(f"Doctor Diagnostic: {len(reg.entries)} registered skills.")
        print(f"Validation Errors: {len(validation.errors)}")
        print(f"Validation Warnings: {len(validation.warnings)}")
        sys.exit(0 if not validation.errors else 1)

    elif args.cmd == "scan":
        findings = scan_all(reg, workspace / "skills")
        if getattr(args, "json", False):
            print(json.dumps([f.__dict__ for f in findings], indent=2))
        else:
            print(f"Security Scan completed: {len(findings)} findings.")
            for f in findings:
                print(f"  [{f.severity.upper()}] {f.skill_id}: {f.path} - {f.label}")
        sys.exit(0)

    else:
        parser.print_help()
        sys.exit(0)


def main() -> None:
    repo_script = _find_repo_script()
    if repo_script is not None:
        runpy.run_path(str(repo_script), run_name="__main__")
    else:
        _run_native_cli()


if __name__ == "__main__":
    main()
