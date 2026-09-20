# Claude Code Project Guidelines

Welcome to the **All Skills** agent engineering workspace.

## Agent Instructions & Workflows

### Skills & Tool Ingestion
- Active skills are available in `.claude/skills/` (linked to `.agents/skills/`).
- Consult `awesome_skills/CATALOG.md` when looking for domain-specific skills from the 2,041+ categorized skills library.
- Install additional skills into your active harness with:
  ```bash
  python scripts/manage_awesome_skills.py install <skill-name> --claude
  ```

### Development & Verification
- Run tests: `python scripts/skills/skills.py test`
- Run diagnostics: `python scripts/skills/skills.py doctor`
- Validate skill schemas: `python scripts/validate_schema.py`
- Run pre/post hooks: `python scripts/run_hook.py <pre|post> <skill_id>`

### Guardrails
- Never inspect or print `.env*` or private key files (`.pem`, `.key`, `id_rsa`).
- Never run destructive commands (`rm -rf /`, `git push --force`, `git reset --hard` without state backup).
- Always verify AST syntax after code edits before presenting work as complete.
