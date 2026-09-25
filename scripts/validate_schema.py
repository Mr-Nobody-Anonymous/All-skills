#!/usr/bin/env python3
"""Validate SKILL.md frontmatter with JSON Schema (schemas/skill-frontmatter.schema.json).

Frontmatter is parsed with a real YAML parser (dates stay strings) and checked
by the ``jsonschema`` library against the schema file — no hand-written
approximation of it.

Tiers
- canonical (``skills/``) and active harness (``.agents/skills/``): must pass the
  full schema plus tier rules — ``name`` equals the directory name and
  ``tools`` holds agent tools, not agent names. Any error fails the run.
- catalog (``awesome_skills/``, with ``--catalog``): minimum requirements are a
  YAML mapping with ``name`` and ``description``; the report also shows how
  many catalog skills pass the full schema. ``--max-catalog-errors N`` fails
  the run if more than N catalog skills miss the minimum (a ratchet for CI).

Usage:
    python scripts/validate_schema.py
    python scripts/validate_schema.py --catalog [--max-catalog-errors N] [--json]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import yaml  # noqa: E402

try:
    import jsonschema  # noqa: E402
except ImportError:  # pragma: no cover - dependency declared in pyproject.toml
    print("jsonschema is required: python -m pip install -e .", file=sys.stderr)
    sys.exit(2)

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = REPO_ROOT / "schemas" / "skill-frontmatter.schema.json"
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*(?:\n|$)", re.DOTALL)
AGENT_NAMES = {"antigravity", "claude", "claude-code", "cline", "codex", "codex-cli", "copilot", "cursor",
               "gemini", "gemini-cli", "goose", "kiro", "openclaw", "opencode", "roo", "vscode", "windsurf"}


class _NoTimestampLoader(yaml.SafeLoader):
    """SafeLoader that keeps ISO dates as strings (JSON Schema has no date type)."""


_NoTimestampLoader.yaml_implicit_resolvers = {
    key: [r for r in resolvers if r[0] != "tag:yaml.org,2002:timestamp"]
    for key, resolvers in yaml.SafeLoader.yaml_implicit_resolvers.items()
}


def load_frontmatter(path: Path) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """Return (frontmatter mapping, error message)."""
    text = path.read_text(encoding="utf-8", errors="replace")
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None, "no YAML frontmatter block (--- ... ---)"
    try:
        data = yaml.load(match.group(1), Loader=_NoTimestampLoader)
    except yaml.YAMLError as exc:
        return None, f"invalid YAML: {str(exc).splitlines()[0]}"
    if not isinstance(data, dict):
        return None, "frontmatter is not a mapping"
    return data, None


def schema_validator() -> Any:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    cls = jsonschema.validators.validator_for(schema)
    cls.check_schema(schema)
    return cls(schema)


def _fmt(error: Any) -> str:
    where = "/".join(str(p) for p in error.absolute_path) or "<root>"
    return f"{where}: {error.message[:160]}"


def validate_library_skill(path: Path, validator: Any) -> List[str]:
    """Full schema + tier rules for canonical and active-harness skills."""
    meta, err = load_frontmatter(path)
    if err:
        return [err]
    assert meta is not None
    errors = [_fmt(e) for e in sorted(validator.iter_errors(meta), key=lambda e: list(e.absolute_path))]
    if meta.get("name") != path.parent.name:
        errors.append(f"name: {meta.get('name')!r} must equal the skill directory name {path.parent.name!r}")
    agents_as_tools = sorted(set(meta.get("tools") or []) & AGENT_NAMES) if isinstance(meta.get("tools"), list) else []
    if agents_as_tools:
        errors.append(f"tools: {agents_as_tools} are agent names, not tools (use 'platforms')")
    return errors


def library_skill_files(root: Path) -> Iterable[Tuple[str, Path]]:
    for path in sorted((root / "skills").rglob("SKILL.md")):
        if "_quarantine" not in path.parts:
            yield "canonical", path
    active = root / ".agents" / "skills"
    if active.exists():
        for skill_dir in sorted(active.iterdir()):
            if skill_dir.is_dir():
                yield "active", skill_dir / "SKILL.md"


def catalog_report(root: Path, validator: Any) -> Dict[str, Any]:
    files = sorted((root / "awesome_skills").glob("*/*/SKILL.md"))
    minimum_failures: List[str] = []
    reasons: Counter = Counter()
    full_schema_pass = 0
    for path in files:
        meta, err = load_frontmatter(path)
        problems = [err] if err else []
        if meta is not None:
            problems += [f"missing {k}" for k in ("name", "description") if not meta.get(k)]
        if problems:
            minimum_failures.append(f"{path.relative_to(root)}: {'; '.join(problems)}")
            reasons.update(p.split(":")[0] for p in problems)
            continue
        if not any(True for _ in validator.iter_errors(meta)):
            full_schema_pass += 1
    return {
        "files": len(files),
        "meets_minimum": len(files) - len(minimum_failures),
        "minimum_failures": minimum_failures,
        "failure_reasons": dict(reasons.most_common()),
        "passes_full_schema": full_schema_pass,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--catalog", action="store_true", help="Also report catalog (awesome_skills) coverage")
    parser.add_argument("--max-catalog-errors", type=int, default=None,
                        help="Fail if more catalog skills than this miss the minimum requirements")
    parser.add_argument("--json", action="store_true", help="Machine-readable report")
    parser.add_argument("--root", type=Path, default=REPO_ROOT, help=argparse.SUPPRESS)
    args = parser.parse_args()

    validator = schema_validator()
    results: Dict[str, Dict[str, List[str]]] = {"canonical": {}, "active": {}}
    for tier, path in library_skill_files(args.root):
        if not path.exists():
            results[tier][str(path.parent.relative_to(args.root))] = ["missing SKILL.md"]
            continue
        errors = validate_library_skill(path, validator)
        if errors:
            results[tier][str(path.relative_to(args.root))] = errors
    checked = {tier: sum(1 for t, _ in library_skill_files(args.root) if t == tier) for tier in results}
    failed = any(results[t] for t in results)

    catalog = catalog_report(args.root, validator) if args.catalog else None
    catalog_failed = bool(
        catalog is not None and args.max_catalog_errors is not None
        and len(catalog["minimum_failures"]) > args.max_catalog_errors
    )

    if args.json:
        print(json.dumps({"checked": checked, "errors": results, "catalog": catalog,
                          "passed": not failed and not catalog_failed}, indent=2))
        return 1 if failed or catalog_failed else 0

    for tier in ("canonical", "active"):
        n_bad = len(results[tier])
        print(f"{tier:9} {checked[tier]:>5} skills  {checked[tier] - n_bad:>5} pass the full schema  {n_bad} fail")
        for path, errors in list(results[tier].items())[:25]:
            for err in errors:
                print(f"    {path}: {err}")
    if catalog is not None:
        print(f"catalog   {catalog['files']:>5} skills  {catalog['meets_minimum']:>5} meet the minimum "
              f"(name + description)  {catalog['passes_full_schema']} pass the full schema")
        if catalog["failure_reasons"]:
            print(f"    catalog failures by reason: {catalog['failure_reasons']}")
        for line in catalog["minimum_failures"][:10]:
            print(f"    {line}")
        if catalog_failed:
            print(f"❌ {len(catalog['minimum_failures'])} catalog skills miss the minimum "
                  f"(allowed: {args.max_catalog_errors}).")

    if failed or catalog_failed:
        print("❌ Schema validation failed.")
        return 1
    print("[SUCCESS] Canonical and active skills conform to schemas/skill-frontmatter.schema.json.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
