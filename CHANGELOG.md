# Changelog

All notable changes to the **All-Skills** Universal Agent Skill Operating System and Multi-Agent Harness will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [3.0.0] - 2026-09-21

### Added
- **Single Source of Truth (`VERSION`)**: Established canonical root `VERSION` file (`3.0.0`) synchronizing `pyproject.toml`, `package.json`, `config.yaml`, `manifest.json`, and `stats.json`.
- **Registry & Stats Integrity Engine (`scripts/verify_registry_integrity.py`)**: Automated verification command (`allskills verify-registry`) recalculating all repository numbers and asserting zero metadata drift.
- **Fail-Closed Security Hooks (`scripts/run_hook.py`)**: Guaranteed non-zero exit codes when required or security-critical hook scripts are missing or fail.
- **AST Code Verification (`src/skills/security.py`)**: Added semantic AST parsers for Python scripts and YAML documents.
- **Skill Revocation Registry (`registry/revocations.json`)**: Cryptographic revocation list with advisory IDs and immediate router kill-switch blocking.
- **Skill Verification Matrix (`registry/verification_matrix.json`)**: Comprehensive verification tracking across schema, security, provenance, and license compliance for all skills.
- **STRIDE Threat Model (`docs/security/threat-model.md`)**: Formal threat model documenting attack vectors, mitigations, and residual risks for autonomous agent skills.
- **Network Security Policy (`docs/security/network-security.md`)**: Strict localhost binding in development (`127.0.0.1`), reverse proxy with TLS 1.3, rate limiting, and egress whitelisting in production.
- **SPDX License Compliance Policy (`docs/security/license-policy.yaml`)**: Permitted permissive inbound licenses, banned copyleft/proprietary licenses, and provenance validation rules.
- **Repository Architecture Inventory (`docs/architecture/repository-map.md`)**: Taxonomy table delineating source, generated, runtime, and experimental boundaries.
- **Code Ownership Governance (`CODEOWNERS`)**: Strict review assignments for security scanners, hooks, schemas, and adapters.
- **Out-of-Distribution Routing Benchmarks (`evals/routing/ood_cases.json`)**: Versioned dataset of 25 ambiguous, out-of-domain, and deceptive prompt test cases.

### Changed
- **Removed Security Scanner Line Bypass**: Eliminated dangerous substring check (`if any(k in line for k in ["input:", "payload:", "test_"]): continue`) in `src/skills/security.py`, preventing malicious payloads from disguising themselves as test cases.
- **Updated Production Host Binding**: Changed default `web.host` in `config.yaml` from `0.0.0.0` to `127.0.0.1` for safe default deployment.
- **Synchronized Workflows Counting**: `stats.json` explicitly distinguishes between 5 autonomous agent workflows (`workflows/`) and 8 CI/CD GitHub Actions workflows (`.github/workflows/`).
- **Standardized Documentation**: Reconciled all prose counts in `README.md` and `CONTRIBUTING.md` with authoritative platform metrics (14,855 catalog skills, 143 tests, 12 adapters, 20 profiles).

### Fixed
- Fixed trailing literal backslash in 23 `skills/*/__init__.py` files that caused `SyntaxError` on import.
- Fixed fail-open security bypass in lifecycle hook runner.
- Added console UTF-8 reconfigure across CLI entry points to prevent Windows `cp1252` encoding exceptions on emojis.

---

## [2.0.0] - 2026-09-20

### Added
- Hub-and-Spoke universal multi-agent harness linking `.agents/skills/` to `.claude/skills/`, `.cursor/skills/`, and `.codex/skills/`.
- 11-layer comprehensive diagnostic system (`allskills doctor --full`).
- 20 standardized role profiles in `profiles/` and `registry/profiles.json`.
- 12 platform adapters (`claude.yaml`, `cursor.yaml`, `codex.yaml`, `gemini.yaml`, `copilot.yaml`, `windsurf.yaml`, `cline.yaml`, etc.).
- Non-destructive setup scripts (`scripts/setup_tools.py`, `scripts/setup_skills.py`).
- Evaluation and behavioral benchmarks in `evals/`.
- SkillHub specification validation engine (`scripts/validate_skillhub_spec.py`).

---

## [1.0.0] - 2026-09-15

### Added
- Initial release with 122 canonical skills and 8 core categories.
- Basic intent routing engine with keyword and trigger phrase scoring.
- JSON Schema frontmatter validation (`schemas/skill-frontmatter.schema.json`).
- Static regex security scanner in `src/skills/security.py`.
- Dependency conflict resolver and import queue.
