# ⚡ Agent Skills Library

<p align="center">
  <img src="https://img.shields.io/badge/skills-112%20Active-7c3aed?style=for-the-badge&logo=codewars&logoColor=white" alt="112 Skills" />
  <img src="https://img.shields.io/badge/tests-86%2F86%20Passing-10b981?style=for-the-badge&logo=pytest&logoColor=white" alt="86 Tests Passing" />
  <img src="https://img.shields.io/badge/dependencies-Zero%20External-0ea5e9?style=for-the-badge&logo=python&logoColor=white" alt="Zero External Dependencies" />
  <img src="https://img.shields.io/badge/python-3.10+-3776ab?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.10+" />
  <img src="https://img.shields.io/badge/standard-Agent%20Skills-f59e0b?style=for-the-badge" alt="Agent Skills Standard" />
  <img src="https://img.shields.io/badge/security-Static%20Scanned-ef4444?style=for-the-badge&logo=shield" alt="Security Scanned" />
</p>

<p align="center">
  <strong>A high-performance, dependency-light Agent Skills engine, natural-language router, quality scorer, lifecycle manager, and deterministic workflow platform for 112 modular skills.</strong>
</p>

---

## 🌟 Why Agent Skills Library?

When AI coding assistants and autonomous agents are loaded with dozens of full skill prompts upfront, context windows bloat, instruction adherence collapses, and token costs explode.

**Agent Skills Library** solves this with a **load-on-demand architecture**:
- 🧠 **Context-Efficient ($O(1)$)**: The LLM is never given all 112 skills at once. Discovery, routing, and scoring select the optimal skill before reading a single line of skill body.
- 🎯 **9-Signal Layered Router**: Sub-millisecond natural-language routing with deterministic scoring (Exact ID → Alias → Category → Trigger Phrase → Keyword Overlap → Capabilities/IO Vocabulary → Token Overlap → Dependency Availability → Quality Boost).
- ⛓️ **Deterministic Chaining**: Compose complex multi-step workflows like `deep-research`, `anti-procrastination`, and `code-review-flow` with dry-run telemetry.
- 🛡️ **Defensive Security & Quarantine**: AST-free static inspection against prompt injections, credential leaks, and pipe-to-shell payloads with a hardened quarantine boundary (`skills/_quarantine/`).
- 📊 **Deterministic 6-Axis Quality Scoring**: Automated quality ratings across documentation, maintenance, reliability, security, compatibility, and usefulness.
- 🚦 **Formal 8-State Lifecycle**: Enforces strict transitions from `discovered` through `enabled`, `quarantined`, or `deprecated`.

---

## 🏛️ Architecture

```
                               ┌────────────────────────┐
                               │   User Prompt / Goal   │
                               └───────────┬────────────┘
                                           │
                                           ▼
┌──────────────────────────────────────────────────────────────────────────────────────┐
│                            ⚡ 9-SIGNAL SCORING ROUTER                                │
│  Exact ID (100) → Alias (90) → Category (80) → Triggers (+100) → Keywords (+40)      │
│  → Capability/IO (+15) → Tokens (+25) → Dep Penalty (-) → Quality Boost (+4)         │
└──────────────────────────┬───────────────────────────────────────┬───────────────────┘
                           │                                       │
                           ▼                                       ▼
               ┌───────────────────────┐               ┌───────────────────────┐
               │    Candidate Match    │               │    Candidate Chain    │
               │  (Single Best Skill)  │               │   (Multi-Step Plan)   │
               └───────────┬───────────┘               └───────────┬───────────┘
                           │                                       │
                           └───────────────────┬───────────────────┘
                                               │
                                               ▼
                               ┌───────────────────────────────┐
                               │    Load-on-Demand Runtime     │
                               │   Reads 1 SKILL.md on Demand  │
                               └───────────────┬───────────────┘
                                               │
                                               ▼
                               ┌───────────────────────────────┐
                               │       Active AI Agent         │
                               └───────────────────────────────┘
```

---

## 🚀 Quick Start

The entire library runs on pure Python 3.10+ standard library with **zero required third-party dependencies**.

```bash
# Clone the repository
git clone https://github.com/Mr-Nobody-Anonymous/All-skills.git
cd "All skills"

# Check library health & run complete verification
python scripts/skills/skills.py doctor
python scripts/skills/skills.py test
```

### 🎮 Common CLI Workflows

#### 1. Discovery & Search
```bash
# List all 112 skills grouped by category
python scripts/skills/skills.py list

# Search skills by query or keyword
python scripts/skills/skills.py search productivity

# Show skill metadata (loaded on demand — zero file body read)
python scripts/skills/skills.py info productivity.unlazy

# Load a specific skill's body into agent context
python scripts/skills/skills.py load documents.pdf
```

#### 2. Natural Language Routing
```bash
# Route a natural language request to the best-matching skill
python scripts/skills/skills.py route "I'm procrastinating on a paper"

# Route with chained follow-on suggestions and dry-run preview
python scripts/skills/skills.py route --chain --dry-run "Break my project into tasks"

# Explain routing scores with a per-signal breakdown
python scripts/skills/skills.py explain "Review this Python code for security problems"
```

#### 3. Deterministic Workflow Chains
```bash
# Execute or dry-run named canonical workflows
python scripts/skills/skills.py chain deep-research --dry-run
python scripts/skills/skills.py chain anti-procrastination --dry-run
python scripts/skills/skills.py chain code-review-flow --dry-run
```

#### 4. Quality, Lifecycle, Conflicts & Security
```bash
# Inspect quality scores across all skills or for a specific skill
python scripts/skills/skills.py quality productivity.focus

# View declared pairwise conflicts & priority arbitration
python scripts/skills/skills.py conflicts

# Inspect or transition skill lifecycle state
python scripts/skills/skills.py lifecycle productivity.unlazy
python scripts/skills/skills.py lifecycle productivity.unlazy disabled

# Run static security inspection on all skill directories
python scripts/skills/skills.py scan --strict
```

#### 5. Diagnostics & Integrity
```bash
# Run comprehensive library health diagnostics
python scripts/skills/skills.py doctor

# Validate SKILL.md frontmatter, required sections, and links
python scripts/skills/skills.py validate

# Run the complete test suite (unit, routing, lifecycle, provenance)
python scripts/skills/skills.py test
```

---

## 💻 Interactive Showcase

<details open>
<summary><strong>🔍 Route Natural Language Query</strong></summary>

```console
$ python scripts/skills/skills.py route "I'm procrastinating on my programming assignment."

Matched: productivity.unlazy (score 97.0 via trigger)
Description: Anti-procrastination engine — breaks inertia with immediate micro-actions and friction removal.
```
</details>

<details>
<summary><strong>📊 Explain Route Decision (Signal Breakdown)</strong></summary>

```console
$ python scripts/skills/skills.py explain "I'm procrastinating"

Top matches for: "I'm procrastinating"
1. productivity.unlazy (score: 97.0, primary: trigger)
   Signals: trigger=87.0, token=6.2, quality=3.12
2. productivity.focus (score: 13.08, primary: token)
   Signals: token=10.0, quality=3.08
3. productivity.adhd (score: 13.08, primary: token)
   Signals: token=10.0, quality=3.08
```
</details>

<details>
<summary><strong>⛓️ Named Deterministic Chain Preview</strong></summary>

```console
$ python scripts/skills/skills.py chain deep-research --dry-run

Chain: deep-research
Description: Research a topic on the web, verify sources, fact-check, summarize, and produce a Markdown report.
Steps (5):
  1. research.web-research
  2. research.source-verification
  3. research.fact-checking
  4. utilities.summarization
  5. documents.markdown
Declared permissions across chain:
  filesystem: read
  network: required
```
</details>

<details>
<summary><strong>🩺 Library Diagnostics (doctor)</strong></summary>

```console
$ python scripts/skills/skills.py doctor

== Skill Library Diagnostics ==

Total skills: 112
Enabled:      112
Disabled:     0
Categories:   8
  - design: 8
  - development: 34
  - documents: 7
  - productivity: 18
  - research: 8
  - security: 7
  - utilities: 20
  - web: 10

Validation:
  Errors:   0
  Warnings: 1
Quarantined: 0
Dependencies checked: 48
Missing required:      0
Lifecycle:
  - enabled: 112
Quality: average 6.5
```
</details>

---

## 📚 Skill Catalog by Category

The library organizes **112 production-ready skills** across 8 core domains:

| Category | Skills | Highlights & Core Capabilities | Reference |
|---|:---:|---|---|
| **💻 Development** | **34** | Architecture, coding, debugging, refactoring, code review, git worktrees, Docker, MCP server builder, Dokploy, GitHub CLI, API mock generator, behavior validation. | [development.md](docs/skills/development.md) |
| **🛠️ Utilities** | **20** | Parallel agent dispatching, audio transcription, system monitor, Sonos CLI, Telegram/WhatsApp routers, Slack synthesizer, text processing, automation. | [utilities.md](docs/skills/utilities.md) |
| **🚀 Productivity** | **18** | Anti-procrastination (`unlazy`), ADHD task breakdown, focus guard, calendar assistant, inbox zero, Obsidian sync, time blocking, meeting action extractor. | [productivity.md](docs/skills/productivity.md) |
| **🌐 Web** | **10** | Agent browser automation, web scraper, form filler, media downloader, SEO audit, accessibility, web extraction. | [web.md](docs/skills/web.md) |
| **🔬 Research** | **8** | Web research, search synthesizer, fact-checking, deep research, competitive analysis, data analysis, source verification. | [research.md](docs/skills/research.md) |
| **🎨 Design** | **8** | UI/UX design, frontend design, slide presentations, Remotion video, avatar creator, image generation, Google Veo video generation. | [design.md](docs/skills/design.md) |
| **📄 Documents** | **7** | PDF analysis, Markdown editing, DOCX, XLSX, PPTX, CSV processing, automated expense & receipt parser. | [documents.md](docs/skills/documents.md) |
| **🛡️ Security** | **7** | Secure coding guidance (OWASP Top 10), release security scanner, npm auditor, secret detection, command safety guard, prompt-injection defense. | [security-category.md](docs/skills/security-category.md) |

---

## 📋 Anatomy of an Agent Skill

Every skill in this repository complies with the open **Agent Skills specification** and is laid out as:

```
skills/<category>/<skill-name>/
├── SKILL.md        # Canonical prompt instructions with YAML frontmatter
├── README.md       # Human-readable documentation & provenance
├── LICENSE         # Preserved third-party license (for imported skills)
└── references/     # Auxiliary guides, schemas, or upstream snapshots
```

### Required Frontmatter Specification

```yaml
---
name: web-research
description: Conduct structured web research — query formulation, source diversification, synthesis, and source tracking.
category: research
aliases: [research, internet-research, search]
triggers:
  - research this
  - research this topic
  - look this up
keywords: [research, search, web, lookup, find, information, query]
dependencies: []
risk: low
version: 1.0.0
source: custom
enabled: true
lifecycle: enabled
capabilities: [web-research, query-decomposition, source-tracking]
inputs: [topic, constraints]
outputs: [research_report, citations]
permissions:
  filesystem: read
  network: required
---
```

Each `SKILL.md` body strictly implements the **11 mandatory structural sections**:
1. `## Purpose`
2. `## When to Use`
3. `## When NOT to Use`
4. `## Capabilities`
5. `## Inputs`
6. `## Workflow`
7. `## Tools`
8. `## Examples`
9. `## Safety`
10. `## Source`
11. `## Notes`

---

## 📁 Repository Structure

```
.
├── skills/                     # 112 Canonical Skill Implementations
│   ├── design/                 # Avatar creator, Remotion, Veo, UI/UX (8 skills)
│   ├── development/            # Coding, debugging, MCP builder, Docker (34 skills)
│   ├── documents/              # PDF, DOCX, XLSX, PPTX, Expense Parser (7 skills)
│   ├── productivity/           # Unlazy, Focus, ADHD, Inbox Zero (18 skills)
│   ├── research/               # Web research, search synthesizer (8 skills)
│   ├── security/               # Secure coding, scanner, npm audit (7 skills)
│   ├── utilities/              # Parallel agents, system monitor, beam (20 skills)
│   ├── web/                    # Browser automation, scraper, form filler (10 skills)
│   ├── _quarantine/            # Isolated directory for untrusted/flagged skills
│   ├── registry.json           # Machine-readable skill catalog & quality scores
│   ├── registry.md             # Human-readable registry overview
│   ├── dependencies.json       # Machine-readable dependency matrix
│   ├── DEPENDENCIES.md         # Human-readable dependency audit
│   ├── chains.json             # Named deterministic multi-skill workflows
│   ├── conflicts.json          # Declared pairwise skill conflicts & arbitration
│   └── SOURCES.json            # Pinned upstream provenance, commits & licenses
├── src/skills/                 # Core Python Engine (Zero Dependencies)
│   ├── router.py               # 9-signal layered natural-language router
│   ├── registry.py             # Metadata loader and skill indexer
│   ├── loader.py               # On-demand lazy body loader
│   ├── validator.py            # Static validation and integrity checker
│   ├── quality.py              # Deterministic 6-axis quality scoring engine
│   ├── lifecycle.py            # State-machine lifecycle manager
│   ├── chains.py               # Deterministic workflow resolver
│   ├── conflicts.py            # Pairwise conflict detector
│   └── security.py             # AST-free pattern-based static security scanner
├── scripts/                    # CLI and Automation Tools
│   ├── skills/skills.py        # Primary CLI executable
│   ├── refresh_registry.py     # Registry metadata synchronization tool
│   ├── generate_registry_docs.py # Automated doc generator
│   └── generate_category_docs.py # Category doc generator
├── docs/skills/                # Architecture, Security & Category Docs
│   ├── ARCHITECTURE.md         # Load-on-demand platform architecture
│   ├── SECURITY.md             # Threat model and security policy
│   ├── SOURCE_AUDIT.md         # Upstream audit log and exclusion rationale
│   └── *.md                    # Individual category reference guides
└── tests/skill_tests/          # Comprehensive Pytest / Unittest Suite (86 tests)
```

---

## 🛡️ Security & Provenance

- **Static Inspection Only**: The security scanner (`src/skills/security.py`) never executes upstream code. Every script and instruction is treated strictly as text.
- **Strict Quarantine**: Any flagged or unverified skill is isolated in `skills/_quarantine/`, completely unrouteable and excluded from runtime indexing.
- **Pinned Provenance**: All third-party skills (adapted from `obra/superpowers` and `anthropics/skills`) are pinned to explicit Git commit SHAs with original author attribution in [skills/SOURCES.json](skills/SOURCES.json) and upstream references in `references/upstream-SKILL.md`.

---

## 🤝 Contributing & Adding Skills

1. Create a new skill folder: `skills/<category>/<skill-name>/`
2. Add `SKILL.md` following the required frontmatter schema and 11 standard sections.
3. Add a companion `README.md`.
4. Refresh metadata and run diagnostics:
   ```bash
   python scripts/refresh_registry.py
   python scripts/generate_registry_docs.py
   python scripts/generate_category_docs.py
   python scripts/skills/skills.py validate
   python scripts/skills/skills.py test
   ```

---

## 📄 License

Individual skills retain their respective open-source licenses (MIT, Apache-2.0, or Custom). Detailed provenance and copyright details are documented in [skills/SOURCES.json](skills/SOURCES.json).