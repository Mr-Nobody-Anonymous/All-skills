# ⚡ Agent Skills Specification & Platform Overview

A unified, high-performance platform of **2,160+ specialized Agent Skills** designed for modern AI coding assistants (Claude Code, Cursor, Codex CLI, Antigravity, and Gemini CLI).

---

## 🏛️ Platform Organization

The repository is organized into three complementary layers:

### 1. ⚡ Canonical Engine (`skills/`) — 122 Core Routed Skills
- **8 Core Categories**: `productivity`, `development`, `research`, `web`, `documents`, `design`, `security`, `utilities`.
- **9-Signal Scored Router**: Sub-millisecond natural language routing without reading file bodies upfront.
- **Deterministic Chaining**: Multi-skill workflows defined in `skills/chains.json`.
- **Quality & Security**: 6-axis quality scoring, static scanning, and quarantine isolation.

### 2. 🚀 Awesome Skills Library (`awesome_skills/`) — 2,041+ Categorized Skills
- **100 Functional Categories**: Grouped into dedicated folders (`development/`, `cloud/`, `ai-ml/`, `security/`, `workflow/`, etc.).
- **Complete Catalog Reference**: [CATALOG.md](awesome_skills/CATALOG.md) lists every single skill with descriptions, risk ratings, and quick links.
- **Metadata Database**: [skills_index.json](awesome_skills/skills_index.json) provides structured records for programmatic tools and harnesses.

### 3. 🤖 Universal Active Agent Harness (`.agents/skills/`, `.claude/skills/`, `.cursor/skills/`, `.codex/skills/`)
- **66 Pre-Loaded Staff Engineer Skills**: Pre-installed in the workspace root for immediate discovery by all AI harnesses without prompt token bloat.
- **Synced Across All Tools**: Linked seamlessly to Claude Code, Cursor, Codex CLI, and Antigravity.

---

## 🧭 Multi-Tool Compatibility & Harness Setup

Every skill uses the open standard:
- Folder format: `<skill-id>/SKILL.md`
- YAML frontmatter: `name`, `description`, `category`, `risk`, `tags`
- Standard sections: `Purpose`, `When to Use`, `Workflow`, `Examples`, `Safety`

### Universal Harness Sync
Connect your active skills to your preferred AI coding harness in one command:

```bash
# Sync all local workspace harnesses (.agents, .claude, .cursor, .codex)
python scripts/setup_tools.py

# Check status of local and global harnesses
python scripts/setup_tools.py --status

# Also sync to user home directories
python scripts/setup_tools.py --global
```

---

## 🎮 CLI Quick Reference

### Awesome Skills Manager (`scripts/manage_awesome_skills.py`)
```bash
# Search across 2,041+ skills
python scripts/manage_awesome_skills.py search "rag"
python scripts/manage_awesome_skills.py search "prompt"

# Inspect detailed skill specifications
python scripts/manage_awesome_skills.py info multi-agent-architect

# List categories or skills in a category
python scripts/manage_awesome_skills.py list
python scripts/manage_awesome_skills.py list --category ai-agents

# Check active skills status
python scripts/manage_awesome_skills.py status

# Install an individual skill or category into your active harness
python scripts/manage_awesome_skills.py install redis-cli
python scripts/manage_awesome_skills.py install security

# Install curated role bundles
python scripts/manage_awesome_skills.py install-bundle senior-engineer
python scripts/manage_awesome_skills.py install-bundle agentic-architect
python scripts/manage_awesome_skills.py install-bundle fullstack
python scripts/manage_awesome_skills.py install-bundle devops-cloud
python scripts/manage_awesome_skills.py install-bundle security
python scripts/manage_awesome_skills.py install-bundle saas-growth
```

### Canonical Skills Engine (`scripts/skills/skills.py`)
```bash
# Route a user goal to the best skill
python scripts/skills/skills.py route "I'm procrastinating on a paper"
python scripts/skills/skills.py route "Review this Python code for vulnerabilities"

# Route with chained follow-on suggestions and dry-run preview
python scripts/skills/skills.py route --chain --dry-run "Break this project into tasks"

# Explain score breakdowns
python scripts/skills/skills.py explain "Review this code"

# Execute or dry-run named deterministic chains
python scripts/skills/skills.py chain deep-research --dry-run
python scripts/skills/skills.py chain anti-procrastination --dry-run
python scripts/skills/skills.py chain code-review-flow --dry-run

# Run full health diagnostics and test suite
python scripts/skills/skills.py doctor
python scripts/skills/skills.py test
```

---

## 🛡️ Security & Lifecycle Policy

1. **Static Inspection**: No execution of external code during indexing or scanning (`src/skills/security.py`).
2. **Quarantine Isolation**: Suspicious or unverified instructions are isolated in `skills/_quarantine/`.
3. **8-State Lifecycle**: `discovered` → `imported` → `validated` → `security_scanned` → `ready` → `enabled` | `disabled` | `quarantined` | `deprecated`.
4. **Explicit Provenance**: Upstream adaptations are pinned to explicit Git commit SHAs in `skills/SOURCES.json`.