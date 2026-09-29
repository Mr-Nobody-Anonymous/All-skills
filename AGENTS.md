# Agent Runtime Directives & Standards

This workspace is an advanced multi-agent engineering platform supporting **Antigravity**, **Claude Code**, **Cursor**, and **Codex CLI**.

---

## 1. Core Operating Principles

1. **Context Window Hygiene**:
   - Keep context lean. If a task requires heavy exploration, offload raw logs to `scratch/` files.
   - Do not dump multi-megabyte command outputs or file contents into conversational turns.
2. **Safe Code Modification (AST-First)**:
   - Prefer AST-aware tools or block replacements with $\ge 3$ lines of surrounding unique syntactic context.
   - Always verify the AST (`python -m py_compile`, `node --check`, `json.tool`) before completing a task.
3. **Security & Sandboxing Guardrails**:
   - Strictly forbidden from reading or exposing secrets (`.env`, `*.key`, `*.pem`, `id_rsa`, `~/.aws/credentials`).
   - Strictly forbidden from running destructive shell commands (`rm -rf /`, `format`, `curl ... | sh`, `git push --force`).
   - Execute all operations bounded within this workspace.

---

## 2. Platform Architecture & Skills

- **Active Agent Harness**: Located at `.agents/skills/` (mirrored to `.claude/skills`, `.cursor/skills`, `.codex/skills`).
- **Canonical Routing Engine**: 122 validated core skills managed via `python scripts/skills/skills.py`.
- **Awesome Skills Library**: the domain-categorized skills catalog (current counts in `stats.json`) located at `awesome_skills/` and indexed in `awesome_skills/CATALOG.md`.
- **Central Manifest**: `manifest.json` maps all skills to tool permissions, MCP servers, and lifecycle hooks.
- **Model Context Protocol (MCP)**: Defined in `mcp_config.json` (`filesystem`, `git`, `fetch`, `memory`).

---

## 3. Lifecycle Hooks & Quality Gates

Run lifecycle checks when executing autonomous workflows:
- **Pre-execution**: `python scripts/run_hook.py pre <skill_id>`
- **Post-execution**: `python scripts/run_hook.py post <skill_id>`
- **On-failure**: `python scripts/run_hook.py failure <skill_id> --error "details"`
- **Test Suite**: `python scripts/skills/skills.py test`
- **Frontmatter Validator**: `python scripts/validate_schema.py`

---

## 4. Workflows & State Tracking

- **Master Intent Router**: Use `which-skill` to locate appropriate skill files across the platform.
- **Multi-Step Workflows**: Chained execution playbooks live under `workflows/` (`feature-development.md`, `bug-investigation-and-fix.md`, `fullstack-saas-launch.md`, etc.).
- **State Tracking (`aas-stack.json`)**: Use `python scripts/manage_state.py` to initialize, step through, and synchronize session context to `CONTEXT.md`.

---

## 5. Harness Setup & Commands

- **One-Step Initializer**: Run `./setup.sh` (Linux/macOS) or `.\setup.bat` (Windows).
- **Setup Command**: Use `/setup-skills` or `python scripts/setup_skills.py`.

---

## 6. Everything Claude Code (ECC) Capabilities & Engine

- **Specialized Subagents**: 68 role-specific agents in `agents/` (`planner`, `architect`, `code-reviewer`, `security-reviewer`, `tdd-guide`, `loop-operator`, etc.). Route via `python scripts/allskills.py agents [name]`.
- **Slash Commands**: 94 slash-command definitions in `commands/` (`/plan`, `/code-review`, `/checkpoint`, `/evolve`, `/instinct-status`, etc.).
- **Instincts & Continuous Learning v2**: Automatic session observation, confidence scoring, and instinct evolution: `python scripts/allskills.py instincts [status|health|evolve]`.
- **Harness & LifeCycle Hooks**: Unified Claude Code lifecycle hooks in `hooks/hooks.json` and Python security execution gates in `hooks/execution_hooks.json`.
- **ECC Engine & Rust Core**: `node bin/ecc.js <cmd>`, `python scripts/allskills.py ecc <cmd>`, and native Rust core under `ecc2/`.
- **Dashboards**: Tkinter GUI via `python ecc_dashboard.py` (or `python scripts/allskills.py dashboard`) and Web UI via `python scripts/allskills.py dashboard --web`.

