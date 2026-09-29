# Claude Code Project Guidelines

Welcome to the **All Skills** agent engineering workspace.

## Agent Instructions & Workflows

### Skills, Routing & Workflows
- Active skills are available in `.claude/skills/` (linked to `.agents/skills/`).
- Use the `which-skill` playbook to identify the optimal skill or workflow for any user task.
- Multi-step execution playbooks are located in `workflows/` (`feature-development.md`, `bug-investigation-and-fix.md`, etc.).
- Maintain multi-step workflow state using `python scripts/manage_state.py` (`aas-stack.json` and `CONTEXT.md`).
- Consult `awesome_skills/CATALOG.md` when looking for domain-specific skills from the categorized skills library (current counts in `stats.json`).
- Setup or re-link harness with `./setup.sh` or `python scripts/setup_skills.py`.
- Install additional skills into your active harness with:
  ```bash
  python scripts/manage_awesome_skills.py install <skill-name> --claude
  ```

### Everything Claude Code (ECC) Ecosystem
- **Specialized Subagents**: 68 subagents available in `agents/` (`planner`, `architect`, `code-reviewer`, `security-reviewer`, `tdd-guide`, `loop-operator`, etc.). Inspect with `python scripts/allskills.py agents`.
- **Slash Commands**: 94 slash-commands in `commands/` (`/plan`, `/code-review`, `/checkpoint`, `/evolve`, `/instinct-status`, etc.).
- **Instincts & Continuous Learning v2**: Observe sessions, capture atomic instincts, and evolve into skills: `python scripts/allskills.py instincts [status|evolve|health]`.
- **ECC Engine & CLI**: `node bin/ecc.js <command>` or `python scripts/allskills.py ecc <command>`.
- **Dashboards**: Tkinter GUI (`python ecc_dashboard.py` or `python scripts/allskills.py dashboard`) and Web UI (`python scripts/allskills.py dashboard --web`).
- **Rust Engine**: High-performance engine available in `ecc2/`.

### Development & Verification
- Run tests: `python scripts/skills/skills.py test`
- Run diagnostics: `python scripts/skills/skills.py doctor` or `python scripts/allskills.py doctor --full`
- Validate skill schemas: `python scripts/validate_schema.py`
- Run pre/post hooks: `python scripts/run_hook.py <pre|post> <skill_id>`

### Guardrails
- Never inspect or print `.env*` or private key files (`.pem`, `.key`, `id_rsa`).
- Never run destructive commands (`rm -rf /`, `git push --force`, `git reset --hard` without state backup).
- Always verify AST syntax after code edits before presenting work as complete.
