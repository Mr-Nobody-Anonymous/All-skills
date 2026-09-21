## Description
Briefly describe the new skill, update, or bug fix introduced by this pull request.

## Type of Change
- [ ] New Skill (`skills/<name>` or `.agents/skills/<name>`)
- [ ] Skill Specification Enhancement / Bug Fix
- [ ] Auxiliary Templates / References / Examples Addition
- [ ] Workflow or Platform Adapter Update
- [ ] Documentation or Governance Improvement

## Standards & Specification Checklist
- [ ] `SKILL.md` includes valid YAML frontmatter matching `schemas/skill-frontmatter.schema.json`.
- [ ] Frontmatter specifies: `name`, `version`, `description`, `author`, `tags`, `compatibility`.
- [ ] Contains clear trigger conditions: `## Use this skill when` and `## Do not use this skill when`.
- [ ] Contains `## Security & Sandboxing Boundaries` with prompt-injection defense directives.
- [ ] Auxiliary directory provided: `README.md`, `references/` or `templates/`, `examples/`.
- [ ] Ran `python scripts/validate_schema.py` (0 errors).
- [ ] Ran `python scripts/validate_skillhub_spec.py` (0 errors).
- [ ] Ran `python scripts/skills/skills.py test` (136/136 tests pass).
- [ ] Ran `python scripts/scan_skills_security.py` (0 high-severity security findings).
- [ ] Verified across agent harnesses (`Claude Code`, `Cursor`, `Codex CLI`, or `Antigravity`).
