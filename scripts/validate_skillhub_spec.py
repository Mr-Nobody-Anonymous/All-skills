#!/usr/bin/env python3
"""Validate active skills against the repository's Agent Skill metadata schema."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = REPO_ROOT / "schemas" / "skill-frontmatter.schema.json"


def load_frontmatter(skill_md: Path) -> Tuple[Dict[str, Any] | None, str | None]:
    """Read a skill's YAML frontmatter, returning a useful parse error if invalid."""
    text = skill_md.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---"):
        return None, "missing opening YAML frontmatter boundary (---)"
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None, "missing closing YAML frontmatter boundary (---)"
    try:
        metadata = yaml.safe_load(parts[1])
    except yaml.YAMLError as exc:
        return None, f"invalid YAML frontmatter: {exc}"
    if not isinstance(metadata, dict):
        return None, "frontmatter must be a YAML mapping"
    return metadata, None


def check_skill_spec(skill_dir: Path, validator: Any) -> List[str]:
    """Check required metadata and field types from the shared JSON Schema."""
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        return [f"{skill_dir.name}: missing SKILL.md"]

    metadata, error = load_frontmatter(skill_md)
    if error:
        return [f"{skill_dir.name}: {error}"]
    assert metadata is not None

    errors = [
        f"{skill_dir.name}: {issue.message}"
        for issue in sorted(validator.iter_errors(metadata), key=lambda item: list(item.absolute_path))
    ]
    if metadata.get("name") != skill_dir.name:
        errors.append(
            f"{skill_dir.name}: frontmatter name must match its directory"
        )
    return errors


def main() -> int:
    try:
        import jsonschema
    except ImportError:
        print("jsonschema is required: python -m pip install -e .", file=sys.stderr)
        return 2

    active_root = REPO_ROOT / ".agents" / "skills"
    if not active_root.is_dir():
        print(f"Error: {active_root} does not exist", file=sys.stderr)
        return 1

    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator_type = jsonschema.validators.validator_for(schema)
    validator_type.check_schema(schema)
    validator = validator_type(schema)

    skill_dirs = sorted(path for path in active_root.iterdir() if path.is_dir())
    errors = [
        error
        for skill_dir in skill_dirs
        for error in check_skill_spec(skill_dir, validator)
    ]
    print(f"Validated {len(skill_dirs)} active skills against the Agent Skill frontmatter schema.")
    if errors:
        print(f"\nFound {len(errors)} specification errors:")
        for error in errors[:25]:
            print(f"  - {error}")
        if len(errors) > 25:
            print(f"  ... and {len(errors) - 25} more.")
        return 1

    print("[SUCCESS] All active skills comply with the shared frontmatter schema.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
