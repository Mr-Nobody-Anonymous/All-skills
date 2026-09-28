# `skills/_quarantine/` — Canonical Skill Quarantine Boundary

Skills moved into this directory are **excluded from routing, validation, locking
and execution**. The registry, loader, validator and schema checks all skip any
`SKILL.md` whose path contains `_quarantine`, and `python scripts/skills/skills.py doctor`
reports how many skills are currently quarantined.

- Move a suspicious skill here (keeping its `<category>/<skill>/` layout) instead of
  deleting it, so forensic evidence is preserved.
- Record the reason and evidence as described in the forensic vault policy:
  [`quarantine/README.md`](../../quarantine/README.md).
- Revocations that must also block harness skills belong in `registry/revocations.json`.

> This directory is intentionally tracked (Git does not store empty folders) because the
> test suite and runtime treat its existence as part of the security boundary.
