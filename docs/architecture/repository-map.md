# Repository Architecture & Subsystem Inventory

**Document Version:** 1.0.0  
**Effective Date:** 2026-09-21  

To maintain platform clarity across autonomous agents, contributors, and package consumers, this document classifies every major directory in the repository by its architectural role, data mutability, and stability tier.

---

## 1. Directory Classification Matrix

| Directory | Architectural Role | Data Origin | Stability Tier | Notes |
| :--- | :--- | :--- | :--- | :--- |
| **`src/skills/`** | Core Registry & Router Engine | Source | **Stable** | Canonical routing, validation, quality scoring, and security scanner. |
| **`skills/`** | Canonical Skill Hierarchy | Source | **Stable** | 122 curated, tested skills organized into 8 canonical categories. |
| **`.agents/skills/`** | Active Agent Harness | Source / Linked | **Stable** | 72 pre-loaded skills consumed by Claude Code, Cursor, Codex, and Antigravity. |
| **`awesome_skills/`** | Universal Catalog Index | Source / Mirrored | **Stable** | 14,855 discovered skills across 251 domain categories with `CATALOG.md`. |
| **`schemas/`** | JSON Schema Contracts | Source | **Stable** | Strict frontmatter and manifest validation schemas. |
| **`adapters/`** | Agent Platform Translators | Source | **Stable** | 12 configuration adapters (Claude, Cursor, Codex, Windsurf, Copilot, etc.). |
| **`profiles/`** | Multi-Role Engineering Profiles | Source | **Stable** | 20 role configurations (`software-engineer`, `security-auditor`, `devops`, etc.). |
| **`policies/`** | Capability & Permission Rules | Source | **Stable** | Granular sandbox boundaries (`network`, `filesystem`, `credentials`). |
| **`hooks/`** | Autonomous Lifecycle Hooks | Source | **Stable** | Pre-execution, post-execution, and failure recovery scripts. |
| **`evals/`** | Evaluation & Benchmark Suites | Source | **Stable** | Ground-truth routing cases, prompt injection tests, and behavioral evals. |
| **`workflows/`** | Multi-Step Agent Playbooks | Source | **Stable** | Chained execution workflows (`feature-development`, `bug-investigation`, etc.). |
| **`registry/`** | Platform Manifests & Index | Generated / Managed | **Stable** | `profiles.json`, `agents.json`, `verification_matrix.json`, `revocations.json`. |
| **`tests/`** | Regression & Security Tests | Source | **Stable** | 143 unit and security integration tests. |
| **`scripts/`** | Platform CLI & Automation | Source | **Stable** | `allskills.py`, `verify_registry_integrity.py`, `compute_stats.py`, `run_evals.py`. |
| **`docs/`** | Specifications & Governance | Source | **Stable** | Threat models, network policies, architecture maps, and API guides. |
| **`packs/`** | Curated Skill Bundles | Source | **Stable** | 7 pre-packaged bundles for specialized domains. |
| **`sources/`** | Upstream Ecosystem Sources | Source | **Stable** | Registered upstream repositories and synchronization configurations. |
| **`scratch_priority_import/`**| Priority Import Engine | Source | **Maintenance** | Dependency resolver and topological import scheduler. |
| **`scratch/`** | Local Development & Artifacts | Scratch | **Experimental** | Transient logs, temporary test runs, and experimental scripts. |

---

## 2. Core Operational Rules

1. **Strict No-Deletion Policy**: Autonomous agents and automation scripts are forbidden from deleting existing directories or unmanaged files.
2. **Deterministic Regeneration**: Any file marked as **Generated** (`stats.json`, `skills.lock`, `registry/verification_matrix.json`) must be reproducibly regenerated via its corresponding CLI command.
3. **AST Safety**: Edits to Python, JavaScript, and YAML files must be verified for syntactic validity before committing.
