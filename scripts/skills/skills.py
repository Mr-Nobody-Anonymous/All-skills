#!/usr/bin/env python3
"""Agent Skills CLI — list, search, route, validate, and test skills.

Usage:
    python scripts/skills/skills.py list
    python scripts/skills/skills.py search <query>
    python scripts/skills/skills.py info <skill-id>
    python scripts/skills/skills.py route "<natural language>"
    python scripts/skills/skills.py validate
    python scripts/skills/skills.py test
    python scripts/skills/skills.py doctor
    python scripts/skills/skills.py categories
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Make src/ importable
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from skills.registry import load_registry  # noqa: E402
from skills.router import Router  # noqa: E402
from skills.validator import Validator  # noqa: E402
from skills.loader import load_skill  # noqa: E402
from skills.dependencies import check_dependencies  # noqa: E402
from skills.updater import check_updates  # noqa: E402


def _workspace_root() -> Path:
    return ROOT


def _print_table(rows, headers):
    """Simple fixed-width table."""
    widths = [len(h) for h in headers]
    for r in rows:
        for i, cell in enumerate(r):
            widths[i] = max(widths[i], len(str(cell)))
    sep = "  "
    def fmt(row):
        return sep.join(str(c).ljust(widths[i]) for i, c in enumerate(row))
    print(fmt(headers))
    print(sep.join("-" * w for w in widths))
    for r in rows:
        print(fmt(r))


def cmd_list(args, _parser):
    reg = load_registry(_workspace_root())
    cats = reg.categories()
    print(f"Total skills: {len(reg.entries)}")
    print()
    if args.category:
        rows = [(e.id, e.name, e.description[:60]) for e in reg.by_category(args.category)]
        _print_table(rows, ["ID", "Name", "Description"])
    else:
        for cat in sorted(cats.keys()):
            print(f"\n[{cat}] ({cats[cat]})")
            for e in sorted(reg.by_category(cat), key=lambda x: x.id):
                print(f"  {e.id:40}  {e.name}  -  {e.description[:80]}")


def cmd_categories(args, _parser):
    reg = load_registry(_workspace_root())
    cats = sorted(reg.categories().items())
    _print_table([(c, n) for c, n in cats], ["Category", "Count"])


def cmd_search(args, _parser):
    reg = load_registry(_workspace_root())
    matches = reg.search(args.query)
    if not matches:
        print(f"No skills match: {args.query}")
        return 1
    print(f"Found {len(matches)} skill(s) matching '{args.query}':\n")
    _print_table(
        [(e.id, e.category, e.risk, e.description[:60]) for e in matches],
        ["ID", "Category", "Risk", "Description"],
    )
    return 0


def cmd_info(args, _parser):
    reg = load_registry(_workspace_root())
    entry = reg.get(args.skill_id)
    if not entry:
        print(f"Skill not found: {args.skill_id}")
        return 1
    print(f"Name:        {entry.name}")
    print(f"ID:          {entry.id}")
    print(f"Category:    {entry.category}")
    print(f"Path:        {entry.path}")
    print(f"Risk:        {entry.risk}")
    print(f"Enabled:     {entry.enabled}")
    print(f"Version:     {entry.version}")
    print(f"Description: {entry.description}")
    if entry.aliases:
        print(f"Aliases:     {', '.join(entry.aliases)}")
    if entry.triggers:
        print(f"Triggers:    {', '.join(entry.triggers)}")
    if entry.keywords:
        print(f"Keywords:    {', '.join(entry.keywords)}")
    if entry.dependencies:
        print(f"Dependencies:{', '.join(entry.dependencies)}")
    if entry.source:
        print(f"Source:      {entry.source}")
    loaded = load_skill(_workspace_root() / "skills", entry.id)
    if loaded:
        print(f"\nFiles:")
        for f in loaded.files:
            print(f"  {f}")
        # Print body excerpt
        body = loaded.body.strip()
        if body:
            excerpt = body[:400] + ("..." if len(body) > 400 else "")
            print(f"\n--- SKILL.md body (excerpt) ---\n{excerpt}")
    return 0


def cmd_route(args, _parser):
    reg = load_registry(_workspace_root())
    router = Router(reg)
    matches = (
        router.route_chain(args.query, top_k=args.top_k)
        if args.chain else router.route(args.query, top_k=args.top_k)
    )
    if not matches:
        print(f"No skill matches: {args.query}")
        return 1
    for i, m in enumerate(matches, 1):
        print(f"{i}. {m.skill.id}  (score={m.score:.1f}, matched_on={m.matched_on})")
        print(f"   {m.skill.description}")
    return 0


def cmd_set_enabled(args, _parser):
    registry_path = _workspace_root() / "skills" / "registry.json"
    data = json.loads(registry_path.read_text(encoding="utf-8"))
    entry = next((item for item in data.get("skills", []) if item.get("id") == args.skill_id), None)
    if not entry:
        print(f"Skill not found: {args.skill_id}")
        return 1
    enabled = args.cmd == "enable"
    entry["enabled"] = enabled
    temporary = registry_path.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    temporary.replace(registry_path)
    print(f"{'Enabled' if enabled else 'Disabled'} {args.skill_id}")
    return 0


def cmd_update(args, _parser):
    print("Checking pinned upstream repositories (no files will be changed)...")
    statuses = check_updates(_workspace_root())
    if not statuses:
        print("No imported upstream repositories are registered.")
        return 0
    errors = 0
    for status in statuses:
        if status.error:
            errors += 1
            print(f"ERROR  {status.repository}: {status.error}")
        elif status.changed:
            print(f"UPDATE {status.repository}: {status.pinned_commit[:12]} -> {status.upstream_commit[:12]}")
        else:
            print(f"OK     {status.repository}: {status.pinned_commit[:12]}")
    print("Updates are never applied automatically; re-import, audit, and test changed sources.")
    return 1 if errors else 0


def cmd_validate(args, _parser):
    reg = load_registry(_workspace_root())
    val = Validator(reg, _workspace_root() / "skills")
    if args.skill_id:
        result = val.validate_one(args.skill_id)
    else:
        result = val.validate_all()
    print(f"Errors:   {len(result.errors)}")
    print(f"Warnings: {len(result.warnings)}")
    print(f"Info:     {len(result.info)}")
    if result.errors:
        print("\nERRORS:")
        for e in result.errors:
            print(f"  - {e}")
    if result.warnings:
        print("\nWARNINGS:")
        for w in result.warnings:
            print(f"  - {w}")
    if args.verbose and result.info:
        print("\nINFO:")
        for i in result.info:
            print(f"  - {i}")
    return 0 if not result.errors else 1


def cmd_test(args, _parser):
    import unittest

    sys.path.insert(0, str(ROOT / "tests"))
    loader = unittest.TestLoader()
    suite = loader.discover(str(ROOT / "tests"), pattern="test_*.py")
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return 0 if result.wasSuccessful() else 1


def cmd_doctor(args, _parser):
    reg = load_registry(_workspace_root())
    print("== Skill Library Diagnostics ==\n")
    print(f"Total skills: {len(reg.entries)}")
    print(f"Enabled:      {len(reg.enabled())}")
    print(f"Disabled:     {len(reg.entries) - len(reg.enabled())}")
    print(f"Categories:   {len(reg.categories())}")
    for cat, n in sorted(reg.categories().items()):
        print(f"  - {cat}: {n}")
    # Validate
    val = Validator(reg, _workspace_root() / "skills")
    result = val.validate_all()
    print(f"\nValidation:")
    print(f"  Errors:   {len(result.errors)}")
    print(f"  Warnings: {len(result.warnings)}")
    if result.errors:
        for e in result.errors[:5]:
            print(f"  - {e}")
    if result.warnings:
        print("\nTop warnings:")
        for w in result.warnings[:5]:
            print(f"  - {w}")
    # Quarantine check
    qdir = _workspace_root() / "skills" / "_quarantine"
    quarantined = 0
    if qdir.exists():
        quarantined = sum(1 for _ in qdir.rglob("SKILL.md"))
    print(f"\nQuarantined: {quarantined}")
    dependencies = check_dependencies(reg.enabled())
    missing_required = [d for d in dependencies if not d.available and not d.optional]
    missing_optional = [d for d in dependencies if not d.available and d.optional]
    print(f"Dependencies checked: {len(dependencies)}")
    print(f"Missing required:      {len(missing_required)}")
    print(f"Missing optional:      {len(missing_optional)}")
    for dep in missing_required:
        print(f"  - {dep.skill_id}: {dep.dependency}")
    return 0 if not result.errors and not missing_required else 1


def cmd_export(args, _parser):
    reg = load_registry(_workspace_root())
    out = args.output or (_workspace_root() / "skills" / "registry.json")
    out.write_text(reg.to_json(), encoding="utf-8")
    print(f"Wrote registry to {out}")
    return 0


def main():
    p = argparse.ArgumentParser(prog="skills", description="Agent Skills CLI")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("list", help="List all skills")
    s.add_argument("--category", help="Filter by category")
    s.set_defaults(func=cmd_list)

    s = sub.add_parser("categories", help="List categories")
    s.set_defaults(func=cmd_categories)

    s = sub.add_parser("search", help="Search skills")
    s.add_argument("query", help="Search string")
    s.set_defaults(func=cmd_search)

    s = sub.add_parser("info", help="Skill details")
    s.add_argument("skill_id", help="Skill ID (e.g. productivity.unlazy)")
    s.set_defaults(func=cmd_info)

    s = sub.add_parser("route", help="Route natural language to a skill")
    s.add_argument("query", help="Natural language request")
    s.add_argument("--top-k", type=int, default=3, help="Number of matches")
    s.add_argument("--chain", action="store_true", help="Include compatible follow-on skills")
    s.set_defaults(func=cmd_route)

    for command in ("enable", "disable"):
        s = sub.add_parser(command, help=f"{command.title()} a skill")
        s.add_argument("skill_id", help="Skill ID")
        s.set_defaults(func=cmd_set_enabled)

    s = sub.add_parser("update", help="Check imported skills for upstream changes")
    s.set_defaults(func=cmd_update)

    s = sub.add_parser("validate", help="Validate skills")
    s.add_argument("skill_id", nargs="?", help="Validate a single skill")
    s.add_argument("-v", "--verbose", action="store_true")
    s.set_defaults(func=cmd_validate)

    s = sub.add_parser("test", help="Run skill tests")
    s.set_defaults(func=cmd_test)

    s = sub.add_parser("doctor", help="Diagnose library health")
    s.set_defaults(func=cmd_doctor)

    s = sub.add_parser("export", help="Export the registry to JSON")
    s.add_argument("-o", "--output", help="Output path")
    s.set_defaults(func=cmd_export)

    args = p.parse_args()
    rc = args.func(args, p) or 0
    sys.exit(rc)


if __name__ == "__main__":
    main()