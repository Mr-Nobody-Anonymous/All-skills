#!/usr/bin/env python3
"""Agent Skills CLI — list, search, route, explain, chain, validate, and scan skills.

Usage:
    python scripts/skills/skills.py list
    python scripts/skills/skills.py search <query>
    python scripts/skills/skills.py info <skill-id>
    python scripts/skills/skills.py route "<natural language>" [--chain] [--dry-run]
    python scripts/skills/skills.py explain "<natural language>"
    python scripts/skills/skills.py chain <name> [--dry-run]
    python scripts/skills/skills.py lifecycle <skill-id> [<state>]
    python scripts/skills/skills.py conflicts
    python scripts/skills/skills.py quality [<skill-id>]
    python scripts/skills/skills.py load <skill-id>
    python scripts/skills/skills.py scan [--strict]
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
from skills.quality import score_all  # noqa: E402
from skills.lifecycle import LIFECYCLE_STATES, can_transition, transition  # noqa: E402
from skills.chains import ChainResolver, load_chains  # noqa: E402
from skills.conflicts import load_conflicts  # noqa: E402
from skills.security import scan_all  # noqa: E402


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
    if args.dry_run:
        print("DRY RUN — plan shown below; nothing was executed.\n")
    for i, m in enumerate(matches, 1):
        print(f"{i}. {m.skill.id}  (score={m.score:.1f}, matched_on={m.matched_on})")
        print(f"   {m.skill.description}")
    return 0


def _registry_path() -> Path:
    return _workspace_root() / "skills" / "registry.json"


def _update_registry_entry(skill_id: str, **fields):
    """Overwrite fields on one registry.json entry (atomic-ish write)."""
    registry_path = _registry_path()
    if not registry_path.exists():
        return None
    data = json.loads(registry_path.read_text(encoding="utf-8"))
    entry = next(
        (item for item in data.get("skills", []) if item.get("id") == skill_id),
        None,
    )
    if entry is None:
        return None
    entry.update(fields)
    temporary = registry_path.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    temporary.replace(registry_path)
    return entry


def cmd_set_enabled(args, _parser):
    enabled = args.cmd == "enable"
    lifecycle = "enabled" if enabled else "disabled"
    entry = _update_registry_entry(args.skill_id, enabled=enabled, lifecycle=lifecycle)
    if entry is None:
        print(f"Skill not found: {args.skill_id}")
        return 1
    print(f"{'Enabled' if enabled else 'Disabled'} {args.skill_id} (lifecycle={lifecycle})")
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
    # Lifecycle distribution
    lifecycle_counts = {}
    for e in reg.entries:
        state = (e.lifecycle or "enabled").strip().lower()
        lifecycle_counts[state] = lifecycle_counts.get(state, 0) + 1
    print("\nLifecycle:")
    for state in LIFECYCLE_STATES:
        if state in lifecycle_counts:
            print(f"  - {state}: {lifecycle_counts[state]}")
    # Quality snapshot
    reports = score_all(reg, _workspace_root() / "skills")
    if reports:
        ranked = sorted(reports.items(), key=lambda kv: kv[1].overall_score, reverse=True)
        average = sum(rep.overall_score for _, rep in ranked) / len(ranked)
        print(f"\nQuality: average {average:.1f}")
        print("  Top:    " + ", ".join(f"{sid} ({rep.overall_score:.1f})" for sid, rep in ranked[:3]))
        print("  Bottom: " + ", ".join(f"{sid} ({rep.overall_score:.1f})" for sid, rep in ranked[-3:]))
    # Declared conflicts
    conflicts = load_conflicts(_workspace_root())
    active_conflicts = conflicts.active(reg)
    print(f"\nConflicts declared: {len(conflicts.all())}, active: {len(active_conflicts)}")
    for conflict in active_conflicts:
        print(f"  - {' + '.join(conflict.skills)} ({conflict.severity})")
    return 0 if not result.errors and not missing_required else 1


def cmd_export(args, _parser):
    reg = load_registry(_workspace_root())
    out = args.output or (_workspace_root() / "skills" / "registry.json")
    out.write_text(reg.to_json(), encoding="utf-8")
    print(f"Wrote registry to {out}")
    return 0


def cmd_explain(args, _parser):
    reg = load_registry(_workspace_root())
    router = Router(reg)
    breakdowns = router.explain(args.query, top_k=args.top_k)
    if not breakdowns:
        print(f"No skills match: {args.query}")
        return 1
    for i, bd in enumerate(breakdowns, 1):
        print(f"{i}. {bd.skill.id}  (score={bd.score:.1f}, primary={bd.primary_signal})")
        print(f"   {bd.skill.description}")
        for sig, val in sorted(bd.signals.items()):
            print(f"     {sig}: {val:+.1f}")
    chain_matches = router.route_chain(args.query, top_k=min(args.top_k + 3, 10))
    if len(chain_matches) > 1:
        print("\nPlanned chain (scored + composition):")
        for i, m in enumerate(chain_matches, 1):
            print(f"  {i}. {m.skill.id}")
    return 0


def cmd_chain(args, _parser):
    reg = load_registry(_workspace_root())
    chains = load_chains(_workspace_root())
    plan = chains.get(args.name)
    if plan is None:
        print(f"No chain named {args.name!r}. Available chains:")
        for name in chains.names():
            chain = chains.get(name)
            print(f"  - {name}: {chain.description}")
        return 1
    resolver = ChainResolver(reg)
    missing = resolver.unresolved_steps(plan)
    if missing:
        print(f"Chain {args.name!r} has unresolved steps: {', '.join(missing)}")
        return 1
    if args.dry_run:
        print("DRY RUN — plan shown below; nothing was executed.\n")
    print(f"Chain: {args.name}")
    print(f"  {plan.description}")
    if plan.inputs:
        print(f"  Inputs:  {', '.join(plan.inputs)}")
    if plan.outputs:
        print(f"  Outputs: {', '.join(plan.outputs)}")
    print("\nSteps:")
    for i, step in enumerate(plan.steps, 1):
        entry = reg.get(step)
        print(f"  {i}. {step}  -  {entry.description if entry else '???'}")
    print("\nPermission summary:")
    for item in resolver.permission_summary(plan):
        perms = item["permissions"] or {}
        perm_str = ", ".join(f"{k}={v}" for k, v in perms.items()) or "not declared"
        print(f"  {item['id']}: [{perm_str}] (risk={item['risk']}, lifecycle={item['lifecycle']})")
    return 0


def cmd_lifecycle(args, _parser):
    reg = load_registry(_workspace_root())
    entry = reg.get(args.skill_id)
    if entry is None:
        print(f"Skill not found: {args.skill_id}")
        return 1
    current = (entry.lifecycle or "enabled").strip().lower()
    if not args.state:
        print(f"{args.skill_id} lifecycle: {current}")
        allowed = [s for s in LIFECYCLE_STATES if can_transition(current, s)]
        print(f"Possible transitions: {', '.join(sorted(allowed)) or 'none (terminal state)'}")
        return 0
    target = args.state.strip().lower()
    if target not in LIFECYCLE_STATES:
        print(f"Unknown lifecycle state: {args.state}")
        print(f"Valid states: {', '.join(LIFECYCLE_STATES)}")
        return 1
    try:
        new_state = transition(current, target)
    except ValueError as exc:
        print(f"Cannot transition: {exc}")
        return 1
    _update_registry_entry(args.skill_id, lifecycle=new_state)
    if new_state == "enabled":
        _update_registry_entry(args.skill_id, enabled=True)
    elif new_state in {"disabled", "quarantined", "deprecated"}:
        _update_registry_entry(args.skill_id, enabled=False)
    print(f"{args.skill_id}: {current} -> {new_state}")
    return 0


def cmd_conflicts(args, _parser):
    reg = load_registry(_workspace_root())
    conflicts = load_conflicts(_workspace_root())
    records = conflicts.all()
    if not records:
        print("No declared conflicts.")
        return 0
    active_keys = {tuple(c.skills) for c in conflicts.active(reg)}
    for conflict in records:
        marker = "ACTIVE" if tuple(conflict.skills) in active_keys else "declared"
        print(f"[{marker}] severity={conflict.severity} priority={conflict.priority or '-'}")
        print(f"  {' + '.join(conflict.skills)}")
        print(f"  {conflict.reason}")
    return 0


def cmd_quality(args, _parser):
    reg = load_registry(_workspace_root())
    reports = score_all(reg, _workspace_root() / "skills")
    if args.skill_id:
        entry = reg.get(args.skill_id)
        if entry is None:
            print(f"Skill not found: {args.skill_id}")
            return 1
        rep = reports.get(args.skill_id)
        if rep is None:
            print(f"No quality report for {args.skill_id}")
            return 1
        print(f"{args.skill_id}: overall={rep.overall_score:.1f}")
        for axis in ("documentation", "maintenance", "reliability", "security", "compatibility", "usefulness"):
            print(f"  {axis}: {getattr(rep, axis):.1f}")
        return 0
    ranked = sorted(reports.items(), key=lambda kv: kv[1].overall_score, reverse=True)
    if not ranked:
        print("No skills to score.")
        return 1
    average = sum(rep.overall_score for _, rep in ranked) / len(ranked)
    print(f"Quality scores for {len(ranked)} skills (average {average:.1f}):\n")
    _print_table(
        [(sid, f"{rep.overall_score:.1f}") for sid, rep in ranked],
        ["Skill", "Score"],
    )
    return 0


def cmd_scan(args, _parser):
    reg = load_registry(_workspace_root())
    findings = scan_all(reg, _workspace_root() / "skills")
    high = [f for f in findings if f.severity == "high"]
    warnings = [f for f in findings if f.severity != "high"]
    if getattr(args, "json", False):
        payload = {
            "scanned": len(reg.entries),
            "findings": [
                {"skill_id": f.skill_id, "path": f.path, "label": f.label, "severity": f.severity}
                for f in findings
            ],
            "high": [f.skill_id + " " + f.path for f in high],
        }
        print(json.dumps(payload, indent=2))
    else:
        print(f"Scanned {len(reg.entries)} skills (static inspection only, nothing executed).")
        print(f"High severity: {len(high)}   Warnings: {len(warnings)}\n")
        for f in findings:
            print(f"  [{f.severity.upper()}] {f.skill_id} :: {f.path} :: {f.label}")
        if high:
            print("\nHigh-severity findings must be reviewed before import/use.")
    if high:
        return 1
    if args.strict and warnings:
        return 1
    return 0


def cmd_load(args, _parser):
    loaded = load_skill(_workspace_root() / "skills", args.skill_id)
    if loaded is None:
        print(f"Cannot load skill: {args.skill_id}")
        return 1
    print(f"Loaded: {loaded.entry.id}")
    print(f"Path:   {loaded.skill_md_path}")
    print(f"Files:  {len(loaded.files)}")
    for name in loaded.files:
        print(f"  - {name}")
    print(f"\nBody ({len(loaded.body)} chars):\n")
    print(loaded.body[: args.max_chars] + ("..." if len(loaded.body) > args.max_chars else ""))
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
    s.add_argument("--dry-run", action="store_true", help="Print the plan without side effects")
    s.set_defaults(func=cmd_route)

    s = sub.add_parser("explain", help="Explain why skills matched a request")
    s.add_argument("query", help="Natural language request")
    s.add_argument("--top-k", type=int, default=3, help="Number of matches")
    s.set_defaults(func=cmd_explain)

    s = sub.add_parser("chain", help="Show/resolve a named chain from skills/chains.json")
    s.add_argument("name", help="Chain name (e.g. deep-research)")
    s.add_argument("--dry-run", action="store_true", help="Print the plan without side effects")
    s.set_defaults(func=cmd_chain)

    s = sub.add_parser("lifecycle", help="Show or change a skill's lifecycle state")
    s.add_argument("skill_id", help="Skill ID")
    s.add_argument("state", nargs="?", help="Target lifecycle state to transition to")
    s.set_defaults(func=cmd_lifecycle)

    s = sub.add_parser("conflicts", help="List declared skill conflicts")
    s.set_defaults(func=cmd_conflicts)

    s = sub.add_parser("quality", help="Show quality scores")
    s.add_argument("skill_id", nargs="?", help="Score a single skill")
    s.set_defaults(func=cmd_quality)

    s = sub.add_parser("scan", help="Static security scan of all skills (never executes)")
    s.add_argument("--strict", action="store_true", help="Treat warnings as failures too")
    s.add_argument("--json", action="store_true", help="Emit findings as JSON")
    s.set_defaults(func=cmd_scan)

    s = sub.add_parser("load", help="Load one skill's body and file list")
    s.add_argument("skill_id", help="Skill ID")
    s.add_argument("--max-chars", type=int, default=2000, help="Body excerpt length")
    s.set_defaults(func=cmd_load)

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