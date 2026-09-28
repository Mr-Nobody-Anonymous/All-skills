# Contributing to All Skills

Thank you for contributing to **All Skills** — the universal Agent Skills ecosystem for Claude Code, Cursor, Codex, OpenClaw, SkillHub, Antigravity, and all modern AI coding agents!

---

## 🛠️ Development Setup

Requires **Python 3.10+** and Git. The steps are identical on Windows, macOS and Linux
(on Windows use `.venv\Scripts\activate` instead of `source .venv/bin/activate`).

```bash
git clone https://github.com/Mr-Nobody-Anonymous/All-skills.git
cd All-skills
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"   # package + pytest, pytest-cov, ruff, mypy, pre-commit
pre-commit install                  # optional: run lint & secret checks on every commit
```

Everyday commands:

| Task | Command |
| :--- | :--- |
| Lint (correctness rules, see `pyproject.toml`) | `ruff check .` |
| Type-check the core package | `mypy` |
| Platform test suite | `python scripts/skills/skills.py test` |
| Tests with coverage report | `pytest tests scratch_priority_import/tests --cov` |
| Full platform diagnostics | `python scripts/allskills.py doctor --full` |
| Run the CLI | `all-skills --help` |

Line endings are normalised to LF by `.gitattributes`, and `.editorconfig` configures
indentation for most editors automatically.

---

## 🏛️ Repository Architecture

When proposing or updating skills, note the hybrid architecture:
1. **Active Harness Playbooks (`.agents/skills/`)**: Curated staff-engineer playbooks loaded into active contexts for Claude Code, Cursor, Codex CLI, Antigravity, and linked harnesses.
2. **Canonical Engine (`skills/`)**: Routed, quality-scored skills with Python handlers and 100% unit test coverage.
3. **Awesome Skills Catalog (`awesome_skills/`)**: Extended library of 14,855 catalog entries (12,757 unique skills) across 251 functional domains.
4. **Agent Harnesses (`.claude/`, `.cursor/`, etc.)**: Generated runtime views created safely via `python scripts/setup_tools.py`.

---

## 📋 Skill Submission Standards & Schema Compliance

Agent skill registries (such as SkillHub, Claude Code plugin ecosystems, and Anthropic's Agent standards) expect a strict, reproducible layout.

### 1. Standardized Directory Structure
Every skill submitted to `skills/` or `.agents/skills/` must follow this layout:

```text
skill-name/
├── SKILL.md              # Instructions with YAML frontmatter (Required)
├── README.md             # Human-readable documentation & quick start (Required)
├── templates/            # Markdown scaffolding & boilerplate templates (Recommended)
├── references/           # Technical specifications, formulas, cheatsheets (Recommended)
├── examples/             # Real-world prompt traces & good vs bad outputs (Required)
└── tests/                # Automated verification or eval inputs (Recommended)
```

### 2. YAML Frontmatter Schema
Every `SKILL.md` must start with valid YAML frontmatter conforming to [`schemas/skill-frontmatter.schema.json`](schemas/skill-frontmatter.schema.json):

```yaml
---
name: architecture-decision-records
version: 1.0.0
description: "Comprehensive patterns for creating, maintaining, and managing ADRs. Use when capturing architectural trade-offs."
author: Mr-Nobody-Anonymous
category: architecture
tags:
  - architecture
  - documentation
  - decision-records
compatibility:
  claude-code: ">=1.0"
  skillhub: "*"
  cursor: ">=0.40"
  codex: "*"
risk: low
network_access: false
filesystem_access: read
credential_access: false
destructive_operations: false
disable-model-invocation: false
tools:
  - file_read
  - file_write
triggers:
  - write an adr
  - document architecture decision
  - draft architecture trade-off
---
```

### 3. Natural Language Trigger Guidance
To ensure agents activate skills reliably without false positives:
- Include an explicit `## Use this skill when` section with 3-6 concrete triggers.
- Include an explicit `## Do not use this skill when` section delineating negative boundaries.

### 4. Security, Sandboxing & Boundaries
All skills must include prompt-injection hardening and safe execution boundaries:
- Define permissions explicitly (`network_access`, `filesystem_access`, `credential_access`).
- Include a `## Security & Sandboxing Boundaries` section.
- Wrap user-supplied data in boundary markers (e.g. `<user_input>...</user_input>`).
- Instruct the agent to strictly refuse execution of destructive commands (`rm -rf /`, `curl | sh`, secret reads).

---

## 🔄 Lifecycle Hooks

All Skills supports pre-, post-, and failure hooks to orchestrate execution:

```bash
# Run pre-execution lifecycle check
python scripts/run_hook.py pre <skill_id>

# Run post-execution verification
python scripts/run_hook.py post <skill_id>

# Report failure and trigger automated rollback
python scripts/run_hook.py failure <skill_id> --error "details"
```

---

## 🧪 Local Quality Gates & Verification

Before submitting a Pull Request, run the complete quality pipeline locally:

```bash
# 1. Validate YAML frontmatter against JSON Schema
python scripts/validate_schema.py

# 2. Validate SkillHub and Claude Code specification compliance
python scripts/validate_skillhub_spec.py

# 3. Run canonical unit test suite
python scripts/skills/skills.py test

# 4. Run full system diagnostics
python scripts/allskills.py doctor --full

# 5. Run security and prompt-injection scan
python scripts/scan_skills_security.py

# 6. Run behavioral and routing evals
python scripts/run_evals.py

# 7. Lint, type-check and measure coverage
ruff check .
mypy
pytest tests scratch_priority_import/tests --cov

# 8. Verify zero unintentional file deletions
git status
git diff --diff-filter=D
```

### Regenerating generated files

Several files are generated and verified in CI. Never edit them by hand — regenerate them:

```bash
python scripts/refresh_registry.py                                 # skills/registry.json + dependencies.json
python scripts/skills/skills.py lock                               # skills.lock (platform-independent hashes)
python scripts/compute_stats.py && python scripts/generate_readme_stats.py   # stats.json + README metrics
python scripts/generate_baselines.py                               # baselines/v0-current (when test counts change)
```

---

## 🚀 Pull Request Process

1. Fork the repository and create a feature branch (`git checkout -b skill/your-skill-name`).
2. Implement your skill following the standard directory structure and frontmatter schema.
3. Verify all local quality gates pass with 0 errors.
4. Open a Pull Request using the [Pull Request Template](.github/pull_request_template.md).
5. Ensure the CI checks pass: [`CI`](.github/workflows/ci.yml) (lint, type-check, tests on Python 3.10–3.12, library validation, package and Docker builds), [`Security`](.github/workflows/security.yml) (skill scans, Gitleaks, dependency review) and [`CodeQL`](.github/workflows/codeql.yml).
