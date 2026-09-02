# agent_skills — legacy OpenClaw catalog (reference)

This directory is the **original OpenClaw/`agent_skills` catalog** (50 skills in
a flat `category/skill/SKILL.md` layout with `metadata: openclaw:` blocks).

## Canonical source of truth

**`skills/` at the repo root is the canonical, actively-maintained library.**
It uses the open Agent Skills convention (`skills/<category>/<skill>/SKILL.md`
with `category.skill` IDs), richer metadata, provenance pinning, quality
scoring, lifecycle state, and the `src/skills/` library + CLI that reads it.

The two trees are **not literal duplicates**: `agent_skills/` contains skills
(e.g. `calendar-assistant`, `email-inbox-zero`, `system-monitor`, `crabbox`)
that do not yet exist in `skills/`, and vice-versa. That makes automatic
deletion unsafe — it would remove otherwise-unique content.

## Policy

- `skills/` is where new work happens.
- `agent_skills/` is kept read-only as a legacy reference and as raw material.
- Treat this directory as **deprecated** for new development.
- `symlink_skills.sh` here targets Claude Code / Codex / OpenClaw and remains
  valid for the legacy tree only.

## Migrating a skill from here

The recommended path for a skill that is still wanted:

1. Copy the `SKILL.md` into `skills/<category>/<name>/` with
   `category`/`name` adjusted to the canonical `category.skill` convention.
2. Add the standard body sections (`Purpose`, `When to Use`, …) required by
   `src/skills/validator.py`.
3. Run `python scripts/refresh_registry.py` to register it and compute quality.
4. Run `python scripts/skills/skills.py validate && python scripts/skills/skills.py test`.

Once every wanted skill has been migrated, this directory can be deleted in one
commit (nothing in `src/`, `scripts/`, or `skills/` references it).