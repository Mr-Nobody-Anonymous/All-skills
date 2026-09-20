#!/usr/bin/env python3
"""AAS State & Stack Manager CLI (aas-stack.json).

Usage:
    python scripts/manage_state.py init <stack_name>
    python scripts/manage_state.py status
    python scripts/manage_state.py step <index_or_name> [--status pending|in_progress|completed|failed]
    python scripts/manage_state.py set <key> <value>
    python scripts/manage_state.py get <key>
    python scripts/manage_state.py decide "<decision>" "<rationale>"
    python scripts/manage_state.py sync-context
"""
from __future__ import annotations

import argparse
import datetime
import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent
STACK_FILE = REPO_ROOT / "aas-stack.json"
TEMPLATE_FILE = REPO_ROOT / "templates" / "aas-stack.template.json"
CONTEXT_FILE = REPO_ROOT / "CONTEXT.md"


def get_timestamp() -> str:
    return datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")


def load_stack() -> dict:
    if not STACK_FILE.exists():
        if TEMPLATE_FILE.exists():
            with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return {
            "stack_name": "default",
            "status": "initialized",
            "current_phase": "planning",
            "step_index": 0,
            "updated_at": get_timestamp(),
            "state_variables": {},
            "plan_progress": [],
            "decisions_log": []
        }
    with open(STACK_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_stack(data: dict) -> None:
    data["updated_at"] = get_timestamp()
    with open(STACK_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def cmd_init(stack_name: str) -> None:
    if TEMPLATE_FILE.exists():
        with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {
            "stack_name": stack_name,
            "status": "initialized",
            "current_phase": "planning",
            "step_index": 0,
            "state_variables": {},
            "plan_progress": [],
            "decisions_log": []
        }
    data["stack_name"] = stack_name
    data["updated_at"] = get_timestamp()
    save_stack(data)
    print(f"Initialized AAS Stack state at {STACK_FILE} (Workflow: '{stack_name}')")


def cmd_status() -> None:
    stack = load_stack()
    print("=" * 60)
    print(f"📊 AAS STACK STATUS: {stack.get('stack_name', 'unknown').upper()}")
    print(f"Status: {stack.get('status')} | Phase: {stack.get('current_phase')} | Step: {stack.get('step_index')}")
    print(f"Last Updated: {stack.get('updated_at')}")
    print("=" * 60)

    print("\n📋 Plan Progress:")
    for i, item in enumerate(stack.get("plan_progress", [])):
        st = item.get("status", "pending")
        icon = {"completed": "✅", "in_progress": "🔄", "failed": "❌"}.get(st, "⚪")
        print(f"  {icon} [{st.upper()}] Step {i+1}: {item.get('step')} ({item.get('skill_used', 'none')})")

    vars_dict = stack.get("state_variables", {})
    if vars_dict:
        print("\n🔑 State Variables:")
        for k, v in vars_dict.items():
            print(f"  • {k}: {v}")

    adrs = stack.get("decisions_log", [])
    if adrs:
        print("\n💡 Decisions Log (ADR):")
        for adr in adrs:
            print(f"  • {adr.get('decision')} (Rationale: {adr.get('rationale')})")
    print("=" * 60)


def cmd_step(step_target: str, status: str) -> None:
    stack = load_stack()
    progress = stack.get("plan_progress", [])
    updated = False

    # Try numeric index first
    try:
        idx = int(step_target) - 1
        if 0 <= idx < len(progress):
            progress[idx]["status"] = status
            stack["step_index"] = idx
            stack["current_phase"] = progress[idx].get("step")
            updated = True
    except ValueError:
        for item in progress:
            if step_target.lower() in item.get("step", "").lower():
                item["status"] = status
                stack["current_phase"] = item.get("step")
                updated = True
                break

    if updated:
        save_stack(stack)
        print(f"Updated step '{step_target}' to status: {status}")
    else:
        print(f"Error: Step matching '{step_target}' not found.", file=sys.stderr)


def cmd_set(key: str, val: str) -> None:
    stack = load_stack()
    try:
        parsed_val = json.loads(val)
    except Exception:
        parsed_val = val
    stack.setdefault("state_variables", {})[key] = parsed_val
    save_stack(stack)
    print(f"Set state variable: {key} = {parsed_val}")


def cmd_get(key: str) -> None:
    stack = load_stack()
    val = stack.get("state_variables", {}).get(key)
    if val is not None:
        print(json.dumps(val, indent=2) if isinstance(val, (dict, list)) else val)
    else:
        print(f"Key '{key}' not found in state variables.", file=sys.stderr)


def cmd_decide(decision: str, rationale: str) -> None:
    stack = load_stack()
    stack.setdefault("decisions_log", []).append({
        "timestamp": get_timestamp(),
        "decision": decision,
        "rationale": rationale
    })
    save_stack(stack)
    print(f"Logged architectural decision: '{decision}'")


def cmd_sync_context() -> None:
    stack = load_stack()
    lines = [
        "# Active Execution Context (`CONTEXT.md`)\n",
        f"> Automatically synchronized with `aas-stack.json` at {get_timestamp()}.\n",
        "---\n",
        "## 🎯 Current Mission",
        f"- **Workflow / Stack**: `{stack.get('stack_name')}`",
        f"- **Active Phase**: `{stack.get('current_phase')}`",
        f"- **Status**: `{stack.get('status')}`",
        f"- **Step Index**: `{stack.get('step_index')}`\n",
        "---\n",
        "## 📋 Progress Tracker"
    ]
    for item in stack.get("plan_progress", []):
        st = item.get("status")
        box = "[x]" if st == "completed" else "[-]" if st == "in_progress" else "[ ]"
        lines.append(f"- {box} **{item.get('step')}** (`{item.get('skill_used', 'general')}`)")

    lines.append("\n---\n## 🔑 Session State Variables")
    lines.append("| Variable | Value |")
    lines.append("| :--- | :--- |")
    for k, v in stack.get("state_variables", {}).items():
        val_str = json.dumps(v) if isinstance(v, (dict, list)) else str(v)
        lines.append(f"| `{k}` | `{val_str}` |")

    lines.append("\n---\n## 💡 Architectural Decisions Log (ADR)")
    for adr in stack.get("decisions_log", []):
        lines.append(f"- **{adr.get('decision')}**")
        lines.append(f"  *Rationale*: {adr.get('rationale')}")

    CONTEXT_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Synchronized {CONTEXT_FILE}")


def main() -> int:
    parser = argparse.ArgumentParser(description="AAS Stack State Manager CLI")
    sub = parser.add_subparsers(dest="command")

    init_p = sub.add_parser("init")
    init_p.add_argument("stack_name", help="Name of workflow/stack to initialize")

    sub.add_parser("status")

    step_p = sub.add_parser("step")
    step_p.add_argument("target", help="Index (1-based) or substring name of step")
    step_p.add_argument("--status", choices=["pending", "in_progress", "completed", "failed"], default="completed")

    set_p = sub.add_parser("set")
    set_p.add_argument("key")
    set_p.add_argument("value")

    get_p = sub.add_parser("get")
    get_p.add_argument("key")

    decide_p = sub.add_parser("decide")
    decide_p.add_argument("decision")
    decide_p.add_argument("rationale")

    sub.add_parser("sync-context")

    args = parser.parse_args()

    if args.command == "init":
        cmd_init(args.stack_name)
    elif args.command == "status":
        cmd_status()
    elif args.command == "step":
        cmd_step(args.target, args.status)
    elif args.command == "set":
        cmd_set(args.key, args.value)
    elif args.command == "get":
        cmd_get(args.key)
    elif args.command == "decide":
        cmd_decide(args.decision, args.rationale)
    elif args.command == "sync-context":
        cmd_sync_context()
    else:
        cmd_status()
    return 0


if __name__ == "__main__":
    sys.exit(main())
