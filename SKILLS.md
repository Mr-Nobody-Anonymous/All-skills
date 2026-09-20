# ⚡ Agent Skills Specification & Platform Overview

A unified, high-performance universal operating system of **12,740+ unique specialized Agent Skills** (**14,840 cataloged instances** across **250 domain categories** and **15 universal super-domains**) designed for modern AI coding assistants (Claude Code, Cursor, Codex CLI, GitHub Copilot, VS Code Agent, Antigravity, Gemini CLI, Windsurf, OpenCode, Cline, Roo Code, and Block Goose).

---

## 🏛️ Platform Architecture

The repository is organized into a modular four-layer architecture:

```
All-skills/
├── sources/               # Upstream Source Registry (16 verified vendor & community sources) & Policies
├── ontology/              # Universal Multi-Dimensional Ontology (Domains, Capabilities, Tasks, Stacks)
├── adapters/              # Platform Adapter Contracts (Claude, Cursor, Codex, Copilot, Gemini, etc.)
├── platforms/             # Dynamic Platform Discovery Registry (platforms.yaml)
├── skills/                # Canonical Engine (122 core routed skills, 8 core categories)
├── awesome_skills/        # Awesome Skills Library (14,840 skills across 250 domain categories)
└── .agents/skills/        # Universal Active Agent Harness (70 pre-loaded staff engineer skills)
```

### 1. ⚡ Canonical Engine (`skills/`) — 122 Core Routed Skills
- **8 Core Categories**: `productivity`, `development`, `research`, `web`, `documents`, `design`, `security`, `utilities`.
- **9-Signal Scored Router**: Sub-millisecond natural language routing without reading file bodies upfront.
- **Deterministic Chaining**: Multi-skill workflows defined in `skills/chains.json`.
- **Quality & Security**: 6-axis quality scoring, static scanning, and quarantine isolation.

### 2. 🚀 Awesome Skills Library (`awesome_skills/`) — 14,840 Categorized Skills
- **250 Domain Categories**: Grouped into dedicated folders under 15 universal super-domains (`01-computer-science-and-software`, `04-ai-and-machine-learning`, `05-cybersecurity`, `06-cloud-and-infrastructure`, `07-systems-and-networking`, `10-engineering-and-architecture`, `11-healthcare-and-life-sciences`, etc.).
- **Complete Catalog Reference**: [CATALOG.md](awesome_skills/CATALOG.md) lists all 14,840 skills with descriptions, risk ratings, and direct links.
- **Metadata Database**: [skills_index.json](awesome_skills/skills_index.json) provides structured records for programmatic tools and harnesses.
- **Cryptographic Lockfile**: [awesome_skills.lock](awesome_skills.lock) tracks SHA-256 integrity hashes for all cataloged skills.

### 3. 🤖 Universal Active Agent Harness (`.agents/skills/`, `.claude/skills/`, `.cursor/skills/`, `.codex/skills/`, `.github/skills/`, etc.)
- **70 Pre-Loaded Staff Engineer Skills**: Pre-installed in the workspace root for immediate discovery by all AI harnesses without prompt token bloat.
- **Multi-Platform Adapters**: Full specification contracts in `adapters/` and dynamic configuration in `platforms/platforms.yaml`.
- **Cross-Agent Synchronization**: Dynamically linked across 11 AI coding assistants.

### 4. 🌐 Universal Ontology & Provenance Layer (`ontology/`, `sources/`)
- **Multi-Dimensional Taxonomy**: Decouples domain, subdomain, discipline, role, capability, task, and tool contracts.
- **Upstream Source Registry**: Tracks vendor, specialized, and community repositories in `sources/registry.yaml`.
- **Strict Governance**: Automated license auditing, credential detection, and destructive operation guardrails in `sources/policies.yaml`.

---

## 🧭 Multi-Tool Compatibility & Harness Setup

Every skill uses the open standard:
- Folder format: `<skill-id>/SKILL.md`
- YAML frontmatter: `name`, `description`, `category`, `risk`, `source`, `license`
- Standard sections: `Purpose`, `When to Use`, `Workflow`, `Examples`, `Safety`

### Universal Harness Setup

```bash
# Set up all local workspace harnesses (.agents, .claude, .cursor, .codex, .github, etc.)
python scripts/setup_tools.py

# Check status across all discovered agent harnesses
python scripts/setup_tools.py --status

# Verify integrity and readable manifests across all targets
python scripts/setup_tools.py --verify

# Repair, update, or force-refresh harnesses
python scripts/setup_tools.py --repair

# Cleanly unlink workspace harnesses without touching source skills
python scripts/setup_tools.py --unlink

# Also link to user home profile directories
python scripts/setup_tools.py --global
```

---

## 🎮 CLI Quick Reference

### Awesome Skills Manager (`scripts/manage_awesome_skills.py`)
```bash
# Search across all 14,840 skills
python scripts/manage_awesome_skills.py search "rag"
python scripts/manage_awesome_skills.py search "prompt"
python scripts/manage_awesome_skills.py search "accessibility"

# Inspect detailed skill specifications
python scripts/manage_awesome_skills.py info multi-agent-architect

# List categories or skills in a category
python scripts/manage_awesome_skills.py list
python scripts/manage_awesome_skills.py list --category ai-ml

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

# Run full health diagnostics and test suite (94 tests)
python scripts/skills/skills.py doctor
python scripts/skills/skills.py test
```

---

## 🛡️ Security & Lifecycle Policy

1. **Static Inspection**: No execution of external code during indexing or scanning (`src/skills/security.py`).
2. **Quarantine Isolation**: Suspicious or unverified instructions are isolated in `skills/_quarantine/`.
3. **8-State Lifecycle**: `discovered` → `imported` → `validated` → `security_scanned` → `ready` → `enabled` | `disabled` | `quarantined` | `deprecated`.
4. **Explicit Provenance**: Upstream source commits, paths, and licenses pinned in YAML frontmatter and `sources/registry.yaml`.