# All-Skills Public Compatibility Contract

**Effective Version:** 3.0.0  
**Effective Date:** 2026-09-21  
**Status:** Canonical & Enforced  

---

## 1. Purpose & Scope

This contract establishes the architectural stability guarantees for the **All-Skills** universal platform. As the repository scales across thousands of skills and integrates with numerous autonomous agent harnesses, this document guarantees that **no existing, working interface will be silently removed or broken**.

---

## 2. Invariant Compatibility Guarantees

### 2.1. Skill Paths & File Hierarchy
- **Canonical Skills**: All 124 canonical skills under `skills/<category>/<skill_name>/` maintain permanent paths and stable identifiers.
- **Active Agent Harness**: The 72 active skills under `.agents/skills/` (and their synchronized mirrors in `.claude/skills/`, `.cursor/skills/`, `.codex/skills/`) are guaranteed to remain discovered and executable.
- **Awesome Skills Catalog**: The 14,855 catalog entries indexed in `awesome_skills/` retain their permanent category and domain placement.

### 2.2. Public CLI Interfaces
The following CLI commands and their invocation signatures are guaranteed stable:
- `allskills` / `python scripts/allskills.py`
  - `doctor [--full]`
  - `profile <install|list>`
  - `verify`
  - `test`
- `python scripts/skills/skills.py`
  - `test`
  - `doctor`
  - `chain <name> [--dry-run]`
- Standard Python entry points:
  - `from skills.registry import Registry`
  - `from skills.router import Router`
  - `from skills.runtime import ExecutionRuntime`
  - `from skills.policy import PolicyEngine`
  - `from skills.security import SecurityScanner`

### 2.3. Agent Harness Interfaces
Compatibility is guaranteed across 11 supported agent platforms:
1. **Claude Code** (`.claude/skills/`)
2. **Cursor** (`.cursor/skills/`)
3. **Codex CLI** (`.codex/skills/`)
4. **Antigravity / Gemini CLI** (`.agents/skills/`)
5. **OpenClaw / Kiro** (`.agents/skills/`)
6. **Windsurf** (`.agents/skills/`)
7. **VS Code** (`.vscode/`)
8. **GitHub Copilot** (`.github/`)
9. **Goose** (`.goose/`)
10. **Cline** (`.cline/`)
11. **Roo Code** (`.roo/`)

Any changes to how an agent discovers or executes skills must maintain backward compatibility with existing configuration layouts.

---

## 3. Deprecation & Evolution Policy

1. **No Silent Removals**: Functionality, skills, or APIs are never deleted without formal advance notice.
2. **Deprecation Window**: Any capability or API marked for deprecation must remain functional for at least **two minor versions** (e.g., deprecated in `3.1.0` remains functional until at least `3.3.0`).
3. **Machine-Readable Warnings**: Deprecated interfaces must emit structured diagnostic warnings pointing users and agents to the modern replacement.
4. **Quarantine Rather Than Delete**: Vulnerable or superseded skills are moved to a forensic quarantine or archival state, preserving auditability and git provenance.
