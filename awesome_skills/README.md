# 🌌 Awesome Skills Library

<p align="center">
  <img src="https://img.shields.io/badge/skills-2%2C041%2B%20Imported-7c3aed?style=for-the-badge&logo=codewars&logoColor=white" alt="2041 Skills" />
  <img src="https://img.shields.io/badge/categories-100%20Domains-0ea5e9?style=for-the-badge&logo=folder" alt="100 Categories" />
  <img src="https://img.shields.io/badge/format-Open%20Agent%20Skills-f59e0b?style=for-the-badge" alt="Open Agent Skills" />
  <img src="https://img.shields.io/badge/tools-Claude%20%7C%20Cursor%20%7C%20Codex%20%7C%20Antigravity-10b981?style=for-the-badge" alt="Multi-Tool Compatible" />
</p>

A structured, clean, and categorized local catalog of **over 2,041 specialized agent skills** imported from [`sickn33/agentic-awesome-skills`](https://github.com/sickn33/agentic-awesome-skills).

Each skill is an isolated playbook containing a standard `SKILL.md` instruction block that teaches your AI coding assistant to operate like a staff or principal engineer across domains.

---

## 🧭 Navigation & Catalog

- **📖 [Complete Interactive Catalog (CATALOG.md)](CATALOG.md)**: Full searchable directory grouped by 100 categories with descriptions, skill IDs, and risk levels.
- **📊 [Metadata Database (skills_index.json)](skills_index.json)**: Machine-readable catalog containing all 2,141 skill records with tags, risk labels, and plugin compatibility.

---

## 🗂️ Directory Architecture

Unlike upstream flat directories containing thousands of unorganized files, this library is strictly structured into **100 functional domain directories**:

```
awesome_skills/
├── CATALOG.md                 # Full human-readable markdown catalog
├── skills_index.json          # Complete JSON metadata database
├── development/               # 187 skills (Refactoring, git, clean code, etc.)
├── cloud/                     # 146 skills (AWS, GCP, Azure, Terraform, K8s)
├── ai-ml/                     # 129 skills (Prompt optimization, RAG, tuning)
├── security/                  # 82 skills  (SAST, secrets, audit, hardening)
├── business/                  # 67 skills  (SaaS launch, strategy, finance)
├── content/                   # 67 skills  (Copywriting, documentation, technical writing)
├── web-development/           # 65 skills  (Frontend, responsive, fullstack)
├── workflow/                  # 62 skills  (Planning, subagents, review loops)
├── marketing/                 # 57 skills  (SEO, GEO, analytics, conversion)
├── automation/                # 54 skills  (Playwright, scraping, webhooks)
├── backend/                   # 40 skills  (Databases, REST, GraphQL, caching)
├── devops/                    # 39 skills  (Docker, CI/CD, deployment)
├── frontend/                  # 33 skills  (React, Vue, Tailwind, CSS)
├── productivity/              # 33 skills  (Focus, time-blocking, decomposition)
├── testing/                   # 30 skills  (TDD, integration, e2e, mutation)
├── project-management/        # 29 skills  (Agile, PRDs, task estimation)
├── architecture/              # 28 skills  (System design, microservices)
├── agent-orchestration/       # 27 skills  (Multi-agent, supervisors, state)
└── ... (81 additional specialized categories)
```

---

## 🎮 How to Use in Any Tool

Skills can be loaded into any AI harness on demand using the included manager CLI:

```bash
# Search for skills across the library
python scripts/manage_awesome_skills.py search "rag"
python scripts/manage_awesome_skills.py search "prompt"

# View skill details & inspect instructions
python scripts/manage_awesome_skills.py info multi-agent-architect

# Install a specific skill into your active harness
python scripts/manage_awesome_skills.py install redis-cli

# Install an entire category into your active harness
python scripts/manage_awesome_skills.py install security
```

### Pre-Configured Bundles

Install curated toolkits tailored for specific engineering roles:

```bash
# Senior Human Engineer (Planning, TDD, Review, Debugging, Worktrees)
python scripts/manage_awesome_skills.py install-bundle senior-engineer

# Agentic AI Architect (LangGraph, Swarms, Memory, Tool Building, Evals)
python scripts/manage_awesome_skills.py install-bundle agentic-architect

# Full-Stack Web Builder (Design Systems, State, Playwright, APIs, Prisma)
python scripts/manage_awesome_skills.py install-bundle fullstack

# Cloud & DevOps Engineer (Terraform, CI/CD, Kubernetes, Serverless)
python scripts/manage_awesome_skills.py install-bundle devops-cloud

# Defensive Security Engineer (SAST, Secrets, RBAC, Red Teaming)
python scripts/manage_awesome_skills.py install-bundle security

# SaaS Founder & Growth (Micro-SaaS, Stripe, SEO-GEO, Analytics, Email)
python scripts/manage_awesome_skills.py install-bundle saas-growth
```

---

## 🤖 Universal Compatibility Matrix

| AI Agent Tool | Active Workspace Path | Global User Path |
| :--- | :--- | :--- |
| **Antigravity / Gemini CLI** | `.agents/skills/` | `~/.gemini/antigravity-cli/skills` |
| **Claude Code** | `.claude/skills/` | `~/.claude/skills` |
| **Cursor** | `.cursor/skills/` | `~/.cursor/skills` |
| **Codex CLI** | `.codex/skills/` | `~/.codex/skills` |
| **Kiro / OpenClaw** | `.agents/skills/` | `~/.kiro/skills` |

Run the universal setup script to sync all local harnesses in one step:
```bash
python scripts/setup_tools.py
```
