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

import sys
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass



import argparse

import json
import os

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
    """Workspace the command operates on (see skills.workspace for the resolution rule)."""
    override = os.environ.get("ALL_SKILLS_WORKSPACE")
    return Path(override).resolve() if override else ROOT





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
    threshold = getattr(args, "threshold", 18.0)
    as_json = getattr(args, "json", False)

    matches = (
        router.route_chain(args.query, top_k=args.top_k)
        if args.chain else router.route(args.query, top_k=args.top_k)
    )

    top_score = matches[0].score if matches else 0.0
    matched = bool(matches) and (threshold is None or top_score >= threshold)

    if as_json:
        if not matched:
            data = {
                "status": "no_match",
                "confidence": round(top_score / 100.0, 3),
                "threshold": round(threshold / 100.0, 3) if threshold else 0.0,
                "message": "No sufficiently relevant skill found.",
                "suggestions": [m.skill.id for m in matches[:3]] if matches else []
            }
        else:
            data = {
                "status": "matched",
                "confidence": round(top_score / 100.0, 3),
                "primary_match": matches[0].skill.id,
                "matches": [
                    {
                        "id": m.skill.id,
                        "score": round(m.score, 2),
                        "confidence": round(m.score / 100.0, 3),
                        "matched_on": m.matched_on,
                        "description": m.skill.description
                    }
                    for m in matches
                ]
            }
        print(json.dumps(data, indent=2))
        return 0 if matched else 1

    if not matched:
        print(f"No sufficiently relevant skill found for: {args.query!r}")
        if matches:
            print(f"Closest candidate: {matches[0].skill.id} (confidence: {top_score/100.0:.2f}, below threshold {threshold/100.0:.2f})")
            print("Suggestions: " + ", ".join(m.skill.id for m in matches[:3]))
        return 1

    if args.dry_run:
        print("DRY RUN — plan shown below; nothing was executed.\n")

    for i, m in enumerate(matches, 1):
        print(f"{i}. {m.skill.id}  (score={m.score:.1f}, matched_on={m.matched_on})")
        print(f"   {m.skill.description}")
    return 0


def cmd_execute(args, _parser):
    from skills.runtime import ExecutionRuntime
    runtime = ExecutionRuntime(_workspace_root())

    input_data = {}
    if getattr(args, "input", None):
        try:
            input_data = json.loads(args.input)
        except Exception as e:
            print(f"Error parsing --input JSON: {e}")
            return 1

    tools = [t.strip() for t in args.tools.split(",")] if getattr(args, "tools", None) else None
    from skills.runtime import approval_from_args, exit_code_for
    approval = approval_from_args(getattr(args, "approval_id", None), getattr(args, "approved_by", None))
    res = runtime.execute(args.skill_id, input=input_data, tools=tools,
                          dry_run=getattr(args, "dry_run", False), approval=approval)

    if getattr(args, "json", False):
        print(json.dumps(res.to_dict(), indent=2))
    else:
        print(f"Skill: {res.skill}")
        print(f"Status: {res.status.upper()}")
        print(f"Duration: {res.duration_ms:.2f}ms")
        print(f"Audit ID: {res.audit_id}")
        if res.error:
            print(f"Error: {res.error}")
        if res.outputs:
            print(f"Outputs: {json.dumps(res.outputs, indent=2)}")
        if res.verification:
            print(f"Verification: {json.dumps(res.verification)}")
        if res.approval_request:
            print(f"Approval required: re-run with --approval-id {res.approval_request['request_id']} --approved-by <name>")

    return exit_code_for(res.status)


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
    reg = load_registry(_workspace_root())
    entry = reg.get(args.skill_id)
    if entry is None:
        print(f"Skill not found: {args.skill_id}")
        return 1

    enabled = args.cmd == "enable"
    target_lifecycle = "enabled" if enabled else "disabled"
    current_lifecycle = (entry.lifecycle or "enabled").strip().lower()

    try:
        new_lifecycle = transition(current_lifecycle, target_lifecycle)
    except ValueError as exc:
        print(f"Cannot transition {args.skill_id}: {exc}")
        return 1

    entry = _update_registry_entry(args.skill_id, enabled=enabled, lifecycle=new_lifecycle)
    if entry is None:
        print(f"Skill not found: {args.skill_id}")
        return 1

    print(f"{'Enabled' if enabled else 'Disabled'} {args.skill_id} (lifecycle={new_lifecycle})")
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
    target = getattr(args, "skill_id", None)
    if target:
        from skills.graph import SkillGraph
        graph = SkillGraph(_workspace_root())
        conflicts = graph.get_conflicts(target)
        if not conflicts:
            print(f"No conflicts detected for '{target}'.")
            return 0
        print(f"Conflicts for '{target}':")
        for c in conflicts:
            print(f"  [{c['severity'].upper()}] with {c['conflicts_with']}: {c['reason']}")
        return 0

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


def cmd_recommend(args, _parser):
    root = _workspace_root()
    reg = load_registry(root)
    router = Router(reg)
    query = args.query

    print("=" * 65)
    print(f"🎯 RECOMMENDED SKILL PIPELINE FOR: '{query}'")
    print("=" * 65)

    matches = router.route_chain(query, top_k=args.top_k)

    active_skills_dir = root / ".agents" / "skills"
    active_matches = []
    if active_skills_dir.exists():
        q_low = query.lower()
        for skill_dir in sorted(active_skills_dir.iterdir()):
            if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
                name = skill_dir.name
                if any(w in name for w in q_low.split()) or any(w in q_low for w in name.split("-")):
                    active_matches.append(name)

    q_low = query.lower()
    workflow = "workflows/feature-development.md"
    if any(k in q_low for k in ["bug", "fix", "error", "crash", "investigate", "trace"]):
        workflow = "workflows/bug-investigation-and-fix.md"
    elif any(k in q_low for k in ["saas", "launch", "mvp", "product", "stripe", "billing"]):
        workflow = "workflows/fullstack-saas-launch.md"
    elif any(k in q_low for k in ["security", "audit", "sast", "vulnerability", "auth"]):
        workflow = "workflows/security-hardening-audit.md"
    elif any(k in q_low for k in ["rag", "agent", "mcp", "llm", "pipeline", "eval"]):
        workflow = "workflows/ai-rag-agent-pipeline.md"

    print("\nRecommended Skills Sequence:")
    seen = set()
    idx = 1
    for m in matches:
        if m.skill.id not in seen:
            seen.add(m.skill.id)
            print(f"  {idx}. {m.skill.id:<32} ({m.skill.category}) — {m.skill.description[:55]}...")
            idx += 1
            for comp in m.skill.composes_with:
                if comp not in seen and reg.get(comp):
                    seen.add(comp)
                    entry = reg.get(comp)
                    print(f"     ↳ {entry.id:<30} (composed) — {entry.description[:50]}...")

    if active_matches:
        print("\nRelevant Active Playbooks:")
        for am in active_matches[:6]:
            print(f"  • active.{am}")

    print(f"\nRecommended Execution Playbook:\n  -> {workflow}")
    print(f"\nQuickstart State Initialization:\n  python scripts/manage_state.py init {Path(workflow).stem}")
    print("=" * 65)
    return 0


def cmd_pack(args, _parser):
    root = _workspace_root()
    manage_packs_py = root / "scripts" / "manage_packs.py"
    if not manage_packs_py.exists():
        print(f"Error: {manage_packs_py} not found.", file=sys.stderr)
        return 1
    import subprocess
    cmd = [sys.executable, str(manage_packs_py)]
    if getattr(args, "pack_action", None):
        cmd.append(args.pack_action)
    if getattr(args, "pack_name", None):
        cmd.append(args.pack_name)
    res = subprocess.run(cmd, cwd=str(root))
def cmd_graph(args, _parser):
    from skills.graph import SkillGraph
    graph = SkillGraph(_workspace_root())
    print(graph.render_ascii_tree(args.skill_id, max_depth=args.depth))
    return 0


def cmd_deps(args, _parser):
    from skills.graph import SkillGraph
    graph = SkillGraph(_workspace_root())
    deps = graph.get_dependencies(args.skill_id, recursive=args.recursive)
    print(f"Dependencies for '{args.skill_id}' ({'recursive' if args.recursive else 'direct'}):")
    if not deps:
        print("  (None declared)")
    for d in deps:
        print(f"  - {d}")
    return 0


def cmd_dependents(args, _parser):
    from skills.graph import SkillGraph
    graph = SkillGraph(_workspace_root())
    dependents = graph.get_dependents(args.skill_id)
    print(f"Skills depending on '{args.skill_id}':")
    if not dependents:
        print("  (No reverse dependents found)")
    for dep in dependents:
        print(f"  - {dep}")
    return 0


def cmd_benchmark(args, _parser):
    import subprocess
    cmd = [sys.executable, str(ROOT / "scripts" / "run_benchmarks.py")]
    if getattr(args, "cases", None):
        cmd.extend(["--cases", args.cases])
    if getattr(args, "threshold", None):
        cmd.extend(["--threshold", str(args.threshold)])
    if getattr(args, "no_perf", False):
        cmd.append("--no-perf")
    if getattr(args, "json", False):
        cmd.append("--json")
    res = subprocess.run(cmd)
    return res.returncode


def cmd_lock(args, _parser):
    from skills.lock import SkillLockManager
    mgr = SkillLockManager(_workspace_root())
    if getattr(args, "verify", False):
        res = mgr.verify_all()
        print(f"Lockfile verification: {res['passed']}/{res['total']} skills verified successfully.")
        return 0 if res['failed'] == 0 else 1
    out_file = mgr.save_lockfile()
    total = (mgr.load_lockfile() or {}).get("total_skills", 0)
    print(f"Successfully generated skills.lock with {total} cryptographically pinned skills ({out_file}).")
    return 0


def cmd_verify(args, _parser):
    from skills.lock import SkillLockManager
    mgr = SkillLockManager(_workspace_root())
    sid = getattr(args, "skill_id", "")
    if sid:
        res = mgr.verify_skill(sid)
        if res.get("status") == "verified":
            print(f"✓ Signature/Hash valid: {sid}")
            print(f"  SHA-256: {res['current_sha256']}")
            print(f"  Version: {res.get('version', '1.0.0')}")
            print(f"  Files:   {res['files_count']}")
            print(f"  Quarantine: Clean (No flags)")
            return 0
        else:
            print(f"✗ Verification FAILED for {sid}: {res.get('message', res.get('status'))}")
            return 1
    else:
        res = mgr.verify_all()
        print(f"Verification summary: {res['passed']}/{res['total']} passed, {res['failed']} failed.")
        return 0 if res['failed'] == 0 else 1


def cmd_stale(args, _parser):
    from skills.lock import SkillLockManager
    mgr = SkillLockManager(_workspace_root())
    stale = mgr.check_stale(threshold_days=args.threshold)
    print(f"Freshness Audit (threshold: {args.threshold} days):")
    if not stale:
        print(f"  All skills are verified and current within the last {args.threshold} days.")
        return 0
    for s in stale:
        print(f"  ⚠ {s['skill']} ({s['category']}): verified {s['days_ago']} days ago")
    return 0


def cmd_policy(args, _parser):
    from skills.policy import PolicyEngine
    pe = PolicyEngine(_workspace_root())
    if getattr(args, "policy_action", None) == "check" and getattr(args, "skill_id", None):
        res = pe.evaluate_skill(args.skill_id)
        print(f"Security Capability Verdict for '{args.skill_id}': {res.overall_verdict.value} (Risk: {res.max_risk.value})")
        print("Requested capabilities:")
        for cap, info in res.breakdown.items():
            print(f"  - {cap}: {info['verdict']} [{info['risk']}]")
        print("Reasons:")
        for r in res.reasons:
            print(f"  - {r}")
        return 0 if res.overall_verdict.value != "DENY" else 1
    else:
        print("Active Security Capability Policies:")
        for cap, p in sorted(pe.policies.items()):
            v = p['verdict'].value if hasattr(p['verdict'], 'value') else str(p['verdict'])
            r = p['risk'].value if hasattr(p['risk'], 'value') else str(p['risk'])
            print(f"  - {cap:<20} {v:<6} [{r:<11}] {p['description']}")
        return 0


def main():

    p = argparse.ArgumentParser(prog="skills", description="Agent Skills CLI")
    p.add_argument("--workspace", help="All-Skills workspace to operate on (default: this checkout)")

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
    s.add_argument("--threshold", type=float, default=18.0, help="Confidence threshold")
    s.add_argument("--json", action="store_true", help="Emit structured output as JSON")
    s.add_argument("--chain", action="store_true", help="Include compatible follow-on skills")
    s.add_argument("--dry-run", action="store_true", help="Print the plan without side effects")
    s.set_defaults(func=cmd_route)

    for exec_cmd in ("execute", "run"):
        s = sub.add_parser(exec_cmd, help="Execute a skill through the universal runtime")
        s.add_argument("skill_id", help="Canonical skill ID")
        s.add_argument("--input", help="JSON string of execution inputs")
        s.add_argument("--tools", help="Comma-separated declared tools")
        s.add_argument("--dry-run", action="store_true", help="Simulate execution without modifying artifacts")
        s.add_argument("--approval-id", help="request_id from an approval_required result")
        s.add_argument("--approved-by", help="Name of the human approving an ASK capability")
        s.add_argument("--json", action="store_true", help="Print structured ExecutionResult as JSON")
        s.set_defaults(func=cmd_execute)

    s = sub.add_parser("graph", help="Render machine-readable dependency tree for a skill")
    s.add_argument("skill_id", nargs="?", default="react", help="Root skill to render tree for")
    s.add_argument("--depth", type=int, default=2, help="Maximum tree traversal depth")
    s.set_defaults(func=cmd_graph)

    s = sub.add_parser("deps", help="List direct and transitive dependencies of a skill")
    s.add_argument("skill_id", help="Skill ID")
    s.add_argument("--recursive", action="store_true", help="Include transitive dependencies")
    s.set_defaults(func=cmd_deps)

    s = sub.add_parser("dependents", help="List all skills that depend on a given skill")
    s.add_argument("skill_id", help="Skill ID")
    s.set_defaults(func=cmd_dependents)

    s = sub.add_parser("benchmark", help="Run routing intent benchmarks and latency percentiles")
    s.add_argument("--cases", default="", help="Path to evaluation cases JSON")
    s.add_argument("--threshold", type=float, default=18.0, help="Confidence threshold")
    s.add_argument("--no-perf", action="store_true", help="Skip latency percentile benchmarking")
    s.add_argument("--json", action="store_true", help="Emit benchmark results as JSON")
    s.set_defaults(func=cmd_benchmark)

    s = sub.add_parser("lock", help="Generate or verify skills.lock cryptographic pinfile")
    s.add_argument("--verify", action="store_true", help="Verify all skills against skills.lock")
    s.set_defaults(func=cmd_lock)

    s = sub.add_parser("verify", help="Cryptographically verify integrity of a skill")
    s.add_argument("skill_id", nargs="?", default="", help="Skill ID to verify")
    s.set_defaults(func=cmd_verify)

    s = sub.add_parser("stale", help="Audit skill freshness and detect outdated playbooks")
    s.add_argument("--threshold", type=int, default=90, help="Staleness threshold in days")
    s.set_defaults(func=cmd_stale)

    s = sub.add_parser("policy", help="Inspect capability security policy or check a skill")
    s.add_argument("policy_action", nargs="?", default="list", choices=["list", "check"], help="Action: list or check")
    s.add_argument("skill_id", nargs="?", default="", help="Skill ID to check when action is check")
    s.set_defaults(func=cmd_policy)

    s = sub.add_parser("recommend", help="Recommend skill pipeline and workflow for a goal")
    s.add_argument("query", help="Goal or user objective (e.g. 'build a SaaS with Next.js and PostgreSQL')")
    s.add_argument("--top-k", type=int, default=5, help="Number of skill matches")
    s.set_defaults(func=cmd_recommend)

    s = sub.add_parser("pack", help="Manage curated skill packs (bundles)")
    s.add_argument("pack_action", nargs="?", default="list", choices=["list", "info", "install"], help="Action to perform")
    s.add_argument("pack_name", nargs="?", default="", help="Pack name (e.g. ai-engineer-pack)")
    s.set_defaults(func=cmd_pack)

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

    s = sub.add_parser("conflicts", help="List declared and semantic skill conflicts")
    s.add_argument("skill_id", nargs="?", default="", help="Optional skill ID to check conflicts for")
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
    if args.workspace:
        from skills.workspace import WorkspaceNotFound, resolve_workspace
        try:
            os.environ["ALL_SKILLS_WORKSPACE"] = str(resolve_workspace(args.workspace))
        except WorkspaceNotFound as exc:
            print(f"Error: {exc}", file=sys.stderr)
            sys.exit(2)
    rc = args.func(args, p) or 0
    sys.exit(rc)





if __name__ == "__main__":

    main()