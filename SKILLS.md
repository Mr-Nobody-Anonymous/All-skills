# ⚡ Agent Skills Specification & Platform Overview

A unified, high-performance universal operating system of **12,755+ unique specialized Agent Skills** (**14,855 cataloged instances** across **251 domain categories** and **15 universal super-domains**) designed for modern AI coding assistants (Claude Code, Cursor, Codex CLI, GitHub Copilot, VS Code Agent, Antigravity, Gemini CLI, Windsurf, OpenCode, Cline, Roo Code, and Block Goose).

---

## 🏛️ Platform Architecture

The repository is organized into a modular architecture:

```
All-skills/
├── registry/              # Single Source of Truth (skills.json, categories.json, ontologies.json, etc.)
├── sources/               # Upstream Source Registry (16 verified vendor & community sources) & Policies
├── ontology/              # Universal Multi-Dimensional Ontology (Domains, Capabilities, Tasks, Stacks)
├── policies/              # Security & High-Risk Human Approval Gates (READ, MODIFY, DELETE, PRODUCTION)
├── mcp/                   # Scalable MCP Connector Architecture (12 Servers, 9 Role Profiles, Policies)
├── adapters/              # Platform Adapter Contracts (Claude, Cursor, Codex, Copilot, Gemini, etc.)
├── platforms/             # Dynamic Platform Discovery Registry (platforms.yaml)
├── profiles/              # Role-Based Skill Collections (Software Engineer, Cybersecurity, AI, DevOps, etc.)
├── evals/                 # Evaluation Benchmarks (Routing, Security, Behavioral, Compatibility)
├── skills/                # Canonical Engine (122 core routed skills, 8 core categories)
├── awesome_skills/        # Awesome Skills Library (14,855 skills across 251 domain categories)
│   └── execution/         # Dedicated 15-Skill Autonomous Execution Layer
└── .agents/skills/        # Universal Active Agent Harness (70 pre-loaded staff engineer skills)
```

### 1. ⚡ Canonical Engine (`skills/`) — 122 Core Routed Skills
- **8 Core Categories**: `productivity`, `development`, `research`, `web`, `documents`, `design`, `security`, `utilities`.
- **9-Signal Scored Router**: Sub-millisecond natural language routing without reading file bodies upfront.
- **Deterministic Chaining**: Multi-skill workflows defined in `skills/chains.json`.
- **Quality & Security**: 6-axis quality scoring, static scanning, and quarantine isolation.

### 2. 🚀 Awesome Skills Library (`awesome_skills/`) — 14,855 Categorized Skills
- **251 Domain Categories**: Grouped into dedicated folders under 15 universal super-domains (`01-computer-science-and-software`, `04-ai-and-machine-learning`, `05-cybersecurity`, `06-cloud-and-infrastructure`, `07-systems-and-networking`, `10-engineering-and-architecture`, `11-healthcare-and-life-sciences`, etc.).
- **Complete Catalog Reference**: [CATALOG.md](awesome_skills/CATALOG.md) lists all 14,855 skills with descriptions, risk ratings, and direct links.
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

### 5. 🏛️ Agent Operating System & v2 Master Plan (`docs/spec/`)
- **Formal Specifications**: Complete architectural blueprints formalized in [V2_RUNTIME_MASTER_PLAN.md](docs/spec/V2_RUNTIME_MASTER_PLAN.md) and [AGENT_RUNTIME_SPECIFICATION.md](docs/spec/AGENT_RUNTIME_SPECIFICATION.md).
- **6 Core Primitives**: Registry, Router, Runtime, Composer, Workflow Engine, and Evaluation.
- **5 Autonomy Levels (L0–L4)**: Informational (`L0`), Read-Only (`L1`), Local Modification (`L2`), External Side Effects (`L3`), and Production-Impacting (`L4`).
- **Top 10 Reference Ecosystem Repositories**: Synthesizes architecture from `NVIDIA/SkillEvaluator`, `zhengyanzhao1997/SkillRouter`, `oneal2000/SR-Agents`, `SkillLens-AI/skilllens`, `Aakash2512git/skillregistry`, `nikships/skills-registry`, `anthropics/skills`, `darkrishabh/agent-skills-eval`, `simota/agent-skills`, and `open-agent-craft/awesome-agent-skills`.

### 6. 🌐 25 Major Categories & Structural Directories
- **25 Major Categories Directory**: [**`categories/`**](categories/README.md) organizing exhaustive skill domains with structured READMEs.
- **Learning Resources**: [**`resources/`**](resources/README.md) with books, video courses, certifications, channels, podcasts, blogs, communities, and tools.
- **Career & Skill Roadmaps**: [**`roadmaps/`**](roadmaps/README.md) with visual Mermaid roadmaps for AI, Fullstack, DevOps, Security, Data, and Architecture.
- **Hands-On Projects**: [**`projects/`**](projects/README.md) tiered into Beginner, Intermediate, and Advanced challenges.
- **High-Yield Cheatsheets**: [**`cheatsheets/`**](cheatsheets/README.md) covering Git, Docker, Linux, System Design, and OWASP.
- **Canonical Skill Template**: [**`templates/SKILL_ENTRY.template.md`**](templates/SKILL_ENTRY.template.md) standardizing 8-part skill specifications.

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
# Search across all 14,855 skills
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

---

## 🏛️ Autonomous Agent Runtime Blueprint: The 14 Core Tenets & Trust Engine

All-skills is engineered not merely as a large collection of prompt files, but as a **measurable, resilient Agent Operating System and Skill Runtime**. Below is the formal specification of the 14 core runtime pillars and the trust engine.

### 1. The Router as the System Heart & Telemetry Protocol
The router transforms natural language user intents into executable, verified workflows through a formal 10-stage pipeline:
```
USER INTENT
    ↓
TASK CLASSIFICATION
    ↓
REQUIRED CAPABILITIES
    ↓
CANDIDATE SKILLS
    ↓
DEPENDENCY RESOLUTION
    ↓
RISK / PERMISSION CHECK
    ↓
SKILL SELECTION
    ↓
EXECUTION PLAN
    ↓
VERIFICATION
    ↓
RESULT & EVALUATION
```

For every routed task, the runtime generates structured machine-readable telemetry:
```json
{
  "intent": "fix authentication bug",
  "selected_skills": [
    "systematic-debugging",
    "security-review",
    "testing"
  ],
  "confidence": 0.91,
  "risk": "high",
  "required_tools": ["git", "filesystem"],
  "dependencies": [],
  "verification": [
    "unit-tests",
    "integration-tests",
    "security-check"
  ]
}
```

### 2. Multi-Dimensional Behavior Evaluations
Beyond unit tests, the runtime enforces behavioral evaluations across four distinct dimensions:
- **Routing Evals**: Verifies precision and recall across ambiguous prompts (e.g., verifying `Next.js OAuth 401` selects `debugging`, `authentication`, `security`, and `testing` while avoiding irrelevant skills).
- **Execution Evals**: Evaluates whether the agent plans before modifying files, adheres to least-privilege boundaries, runs regression tests, and logs verification evidence.
- **Adversarial Evals**: Tests prompt-injection resilience and quarantine boundaries against adversarial attacks (e.g., attempts to exfiltrate `~/.ssh/id_rsa` or execute destructive commands).
- **Regression Evals**: Automated differential testing across 500+ standard prompt corpora when routing heuristics or ontology graphs are updated.

### 3. Tiered Trust Levels (T0 to T4)
To separate unverified community submissions from mission-critical autonomous playbooks, skills are classified into explicit trust tiers:
- **T0 — Untrusted**: Raw discovered or imported skills awaiting automated scanning.
- **T1 — Reviewed**: Human-reviewed instruction content with verified syntax and documentation.
- **T2 — Tested**: Validated through automated structural parsing, linting, and regression tests.
- **T3 — Certified**: Passes comprehensive security, behavioral evaluation, and multi-agent compatibility checks.
- **T4 — Core**: Canonical foundational skills permitted to participate in autonomous agent workflows and execution chains.

```yaml
trust_level: T3
version: 1.4.2
tested_models:
  - claude-3-5-sonnet
  - gpt-4o
  - gemini-1.5-pro
tested_agents:
  - claude-code
  - cursor
  - antigravity
security_review: "2026-09-20"
```

### 4. First-Class Provenance & Skill Software Bill of Materials (SBOM)
Every skill package retains cryptographically locked upstream provenance:
- Source repository, original commit hash, author attribution, and license classification.
- Cryptographic SHA-256 content hashes pinned in `awesome_skills.lock`.
- Audit trail detailing upstream synchronization dates and local modifications.

### 5. Granular Capability Security & Least Privilege
Permissions are enforced at the resource and pattern level rather than granting broad tool access:
```yaml
capabilities:
  filesystem:
    read:
      - "src/**"
      - "tests/**"
    write:
      - "src/**"
      - "tests/**"
  shell:
    allow:
      - "npm test"
      - "npm run build"
      - "pytest"
    deny:
      - "rm -rf *"
      - "curl *"
      - "git push --force"
  network:
    allow:
      - "api.github.com"
```

### 6. Central Execution Policy & Human Approval Gates
Execution follows a centralized operational policy defined in `policies/high-risk.yaml`:
| Action Category | Policy Verdict | Side Effects / Triggers |
| :--- | :---: | :--- |
| **Read Source / Logs** | `AUTO` | Read-only inspection; non-mutating |
| **Edit Workspace Files** | `AUTO` | File write bounded within workspace |
| **Run Unit / Regression Tests** | `AUTO` | Bounded process execution |
| **Install Dependencies** | `ASK` | Package manager modifications |
| **Push Git Branch** | `ASK` | Remote state modification |
| **Deploy Production** | `ASK` | Cloud/container release deployment |
| **Credential Rotation / Export** | `ASK` | Sensitive secret operations |
| **Delete Database / Drop Table** | `BLOCK` | Destructive database operations |
| **Destructive File Purge (`rm -rf`)** | `BLOCK` | Sandbox boundary protection |

### 7. Resumable State Machine & Crash Recovery
Agent execution is formalized as an inspectable, persistent state machine:
```
DISCOVERED → PLANNED → AUTHORIZED → EXECUTING → VERIFYING → COMPLETED
                                        │
                                        ▼ (on error)
                                     FAILED
                                        │
                         ┌──────────────┴──────────────┐
                         ▼                             ▼
                    RECOVERING                    NEEDS_HUMAN
                         │
                         ▼
                    REPLANNING → EXECUTING
```
Execution states, intermediate checkpoints, and ADRs are persisted to `aas-stack.json` and `CONTEXT.md`, enabling resumption via `allskills resume <task-id>` without losing progress.

### 8. Formal 9-Stage Skill Lifecycle
Skills advance through an audited lifecycle managed via CLI:
`DISCOVER → IMPORT → SCAN → VALIDATE → EVALUATE → CERTIFY → PUBLISH → MONITOR → DEPRECATE`
- `allskills audit`: Audit security and licensing conformance.
- `allskills verify`: Cryptographically verify lockfiles and schemas.
- `allskills doctor`: Run end-to-end system health and platform diagnostics.

### 9. Multi-Platform Compatibility Matrices
Compatibility is actively tested and audited with explicit technical rationale across 11 major AI agent environments:
| Skill Discipline | Claude Code | Cursor | Codex CLI | GitHub Copilot | Antigravity | Windsurf | Cline | Roo | Goose |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Standard Coding & Refactoring** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **AST Transformation** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Browser Automation & Puppeteer** | ✅ | ⚠️ | ⚠️ | ⚠️ | ✅ | ⚠️ | ✅ | ✅ | ⚠️ |
| **MCP Tool Servers** | ✅ | ✅ | ⚠️ | ⚠️ | ✅ | ⚠️ | ✅ | ✅ | ✅ |

### 10. Declarative Skill Composition Contracts
Skills declare typed inputs, outputs, and side-effects to enable automatic workflow composition:
```yaml
inputs:
  - repository-codebase
  - user-requirements
outputs:
  - architecture-spec
  - architectural-decision-records
requires:
  - filesystem.read
produces:
  - system-architecture
```

### 11. Enforced Negative Invariants
Universal security and architectural invariants enforced globally across all skills:
- `never-commit-secrets`: Block staging or writing private keys and `.env` credentials.
- `never-modify-production-directly`: Require staging/CI validation before release actions.
- `never-disable-tests`: Prohibit commenting out or removing failing assertions.
- `never-delete-user-data`: Block unbacked-up drop table or truncate commands.
- `never-bypass-auth`: Enforce RBAC validation on all API endpoint generation.

### 12. Trust-Oriented Marketplace Discovery
Marketplace search incorporates trust certifications, evaluation scores, and platform compatibility into discovery cards:
```
Skill: database-migration
─────────────────────────────────────────────
Trust Level : T3 Certified (Passed Security)
Eval Score  : 99.1% Behavioral Accuracy
Platforms   : Claude (✅), Cursor (✅), Codex (✅), Copilot (✅)
Capabilities: database-design, migration-rollback
Dependencies: database-design, typescript
Conflicts   : none
```

### 13. Minimal Installation & Project Profiling
Eliminates prompt bloat through automated workspace detection:
- `allskills init` analyzes local repo technologies (e.g. Next.js, PostgreSQL, Docker, GitHub Actions).
- Selects and installs the minimal necessary skill bundle into active harnesses (`.agents/skills/`), keeping active context windows lean.

### 14. Authoritative Ecosystem Metrics & Terminology
Unambiguous single-source-of-truth counts:
- **Canonical Skills**: `122` tested foundational skills in `skills/`.
- **Active Harness Skills**: `70` staff-engineer playbooks pre-loaded in `.agents/skills/`.
- **Manifest Skills**: `192` tool-mapped skills in `manifest.json`.
- **Unique Skills**: `12,755` distinct skill capabilities across the platform.
- **Catalog Skills**: `14,855` categorized implementations across 251 domains in `awesome_skills/`.

---

## 📚 Authoritative Ecosystem Reference Repositories

The All-skills architecture synthesizes foundational patterns from the top 10 reference repositories in the AI agent ecosystem:

1. **`agentskills/agentskills`**: The open Agent Skills standard (`SKILL.md` format, progressive disclosure model, discovery-activation-execution lifecycle).
2. **`anthropics/skills`**: Anthropic's official skills architecture (self-contained skill directories, progressive references, document workflows).
3. **`addyosmani/agent-skills`**: Rigorous engineering workflows (testing, systematic debugging, code review, anti-patterns, red flags, verification before completion).
4. **`microsoft/skills`**: Large-scale categorized catalog organization (.NET, Python, Azure SDK, AI Foundry).
5. **`github/awesome-copilot`**: Community ecosystem, agent prompts, and marketplace discovery patterns.
6. **`getsentry/skills`**: Quality and security scanning (detecting prompt injections, excessive permissions, AST security scanning).
7. **`obra/superpowers`**: Autonomous agent orchestration, structured execution, and subagent collaboration workflows.
8. **`mattpocock/skills`**: Modern TypeScript, testing standards, Git worktrees, and engineering workflows.
9. **`gptnius/skills-library`**: Curated library governance, upstream provenance tracking, and executable sandboxing.
10. **`agentoperations/agent-registry`**: Agent registry governance, Software Bill of Materials (SBOM), trust promotion lifecycles, and evaluation harnesses.