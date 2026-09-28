## Description

<!-- What does this pull request change, and why? Link related issues (e.g. "Closes #123"). -->

## Type of Change

- [ ] Bug fix (with a regression test under `tests/` — see `docs/NO_REGRESSION_POLICY.md` §3)
- [ ] New skill (`skills/<category>/<name>` or `.agents/skills/<name>`)
- [ ] Skill specification enhancement / fix
- [ ] Platform code (CLI, router, runtime, adapters)
- [ ] CI, tooling or documentation

## Quality Checklist

- [ ] `ruff check .` and `mypy` pass
- [ ] `python scripts/skills/skills.py test` passes
- [ ] `python scripts/validate_schema.py` and `python scripts/validate_skillhub_spec.py` report 0 errors
- [ ] `python scripts/scan_skills_security.py` reports 0 high-severity findings
- [ ] Generated files are refreshed if affected: `python scripts/refresh_registry.py`, `python scripts/compute_stats.py && python scripts/generate_readme_stats.py`
- [ ] No secrets, credentials or `.env` files are included

### For new or changed skills

- [ ] `SKILL.md` frontmatter validates against `schemas/skill-frontmatter.schema.json`
- [ ] Includes `## Use this skill when` / `## Do not use this skill when` trigger sections
- [ ] Includes `## Security & Sandboxing Boundaries` with prompt-injection defenses
- [ ] Verified in at least one agent harness (Claude Code, Cursor, Codex CLI, or Antigravity)
