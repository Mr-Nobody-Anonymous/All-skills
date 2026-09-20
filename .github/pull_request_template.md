## Description
Briefly describe the new skill, update, or bug fix introduced by this pull request.

## Type of Change
- [ ] New Skill
- [ ] Skill Enhancement / Bug Fix
- [ ] Workflow or Framework Update
- [ ] Documentation Improvement

## Quality Checklist
- [ ] `SKILL.md` includes valid YAML frontmatter matching `schemas/skill-frontmatter.schema.json`.
- [ ] Frontmatter specifies `disable-model-invocation: boolean`.
- [ ] Ran `python scripts/validate_schema.py` (0 errors).
- [ ] Ran `python scripts/skills/skills.py test` (All 86 tests pass).
- [ ] Ran `python scripts/scan_skills_security.py` (No high-severity findings).
- [ ] Tested in at least one agent harness (`Claude Code`, `Cursor`, `Codex CLI`, or `Antigravity`).
