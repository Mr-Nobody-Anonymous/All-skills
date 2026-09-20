# Contributing to All Skills

Thank you for contributing to **All Skills** — the universal Agent Skills ecosystem!

---

## 🏛️ Repository Architecture

When proposing or updating skills, note the two main layers:
1. **Active Harness Playbooks (`.agents/skills/`)**: Curated staff-engineer playbooks loaded into active contexts for Claude Code, Cursor, Codex CLI, and Antigravity.
2. **Awesome Skills Catalog (`awesome_skills/`)**: Extended library of 2,041+ categorized skills across 100 functional domains.
3. **Canonical Engine (`skills/`)**: 122 routed, quality-scored skills with 100% unit test coverage.

---

## 📋 Skill Submission Checklist

Before submitting a new skill via Pull Request:

1. **Standardized Directory Structure**:
   ```
   skill-name/
   ├── SKILL.md          # Instructions with YAML frontmatter (Required)
   ├── README.md         # Human-readable documentation (Required)
   ├── examples/         # Usage examples and prompt traces (Recommended)
   └── references/       # API references, cheatsheets (Optional)
   ```

2. **YAML Frontmatter Schema**:
   Every `SKILL.md` must conform to [`schemas/skill-frontmatter.schema.json`](schemas/skill-frontmatter.schema.json):
   ```yaml
   ---
   name: your-skill-name
   description: One-sentence summary. Use when [trigger criteria].
   disable-model-invocation: false
   category: development # or security, workflow, ai-ml, etc.
   version: 1.0.0
   author: Your Name or GitHub Handle
   triggers:
     - user trigger phrase 1
     - user trigger phrase 2
   keywords:
     - keyword1
     - keyword2
   tools:
     - bash
     - file_read
     - file_edit
   mcp_servers:
     - filesystem
   preconditions:
     - check_environment
   postconditions:
     - verify_syntax
   ---
   ```

3. **Required Markdown Headings**:
   - `## Purpose`
   - `## When to Use`
   - `## When NOT to Use`
   - `## Workflow`
   - `## Examples`
   - `## Safety & Boundaries`

---

## 🧪 Local Quality Gates

Run these commands locally before opening your PR:

```bash
# 1. Validate YAML frontmatter schemas
python scripts/validate_schema.py

# 2. Run unit test suite
python scripts/skills/skills.py test

# 3. Run security and prompt injection scan
python scripts/scan_skills_security.py

# 4. Regenerate manifest
python scripts/generate_manifest.py
```
