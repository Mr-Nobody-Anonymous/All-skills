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
from typing import List, Optional, Tuple

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def _extract_workspace(argv: List[str]) -> Tuple[Optional[str], List[str]]:
    """Pull ``--workspace PATH`` / ``--workspace=PATH`` out of ``argv`` (any position)."""
    rest: List[str] = []
    workspace: Optional[str] = None
    it = iter(argv)
    for arg in it:
        if arg == "--workspace":
            workspace = next(it, None)
        elif arg.startswith("--workspace="):
            workspace = arg.split("=", 1)[1]
        else:
            rest.append(arg)
    return workspace, rest


def _run_native_cli(workspace: Optional[Path] = None, argv: Optional[List[str]] = None,
                    workspace_error: Optional[str] = None) -> None:
    """Built-in command subset, used when the workspace has no scripts/skills/skills.py."""
    from ._version import __version__
    from .registry import load_registry
    from .router import Router
    from .runtime import ExecutionRuntime, approval_from_args, exit_code_for
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
        s_exec.add_argument("--approval-id", help="request_id from an approval_required result")
        s_exec.add_argument("--approved-by", help="Name of the human approving an ASK capability")
        s_exec.add_argument("--json", action="store_true", help="Output as JSON")

    # 5. doctor
    sub.add_parser("doctor", help="Check skill library health")

    # 6. scan
    s_scan = sub.add_parser("scan", help="Run static security scan")
    s_scan.add_argument("--json", action="store_true", help="Output findings as JSON")

    args = parser.parse_args(argv)
    if args.cmd is None:
        parser.print_help()
        sys.exit(0)
    if workspace is None:
        print(f"Error: {workspace_error or 'no All-Skills workspace found'}", file=sys.stderr)
        sys.exit(2)
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
        approval = approval_from_args(args.approval_id, args.approved_by)
        res = runtime.execute(args.skill_id, input=inp, tools=tools, dry_run=args.dry_run, approval=approval)
        if getattr(args, "json", False):
            print(json.dumps(res.to_dict(), indent=2))
        else:
            print(f"Skill: {res.skill}")
            print(f"Status: {res.status.upper()}")
            print(f"Duration: {res.duration_ms:.2f}ms")
            print(f"Audit ID: {res.audit_id}")
            if res.error:
                print(f"Error: {res.error}")
            if res.approval_request:
                print(f"Approval required: re-run with --approval-id {res.approval_request['request_id']} --approved-by <name>")
        sys.exit(exit_code_for(res.status))

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
    """Resolve the workspace; delegate to its full CLI if present, else use the built-in subset."""
    from .workspace import ENV_VAR, WorkspaceNotFound, resolve_workspace

    explicit, argv = _extract_workspace(sys.argv[1:])
    try:
        workspace: Optional[Path] = resolve_workspace(explicit)
        error = None
    except WorkspaceNotFound as exc:
        workspace, error = None, str(exc)
    script = workspace / "scripts" / "skills" / "skills.py" if workspace else None
    if script is not None and script.exists():
        os.environ[ENV_VAR] = str(workspace)
        sys.argv = [str(script), *argv]
        runpy.run_path(str(script), run_name="__main__")
        return
    _run_native_cli(workspace, argv, error)


if __name__ == "__main__":
    main()
