# Changelog

All notable changes to the **All-Skills** Universal Agent Skill Operating System and Multi-Agent Harness will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Fixed
- **CI was red on every workflow**: `pip install -e .` crashed in modern setuptools because `setup.py` duplicated metadata that the PEP 621 `[project]` table did not declare. `pyproject.toml` is now the single source of packaging metadata (readme, SPDX license, authors, URLs, classifiers) and `setup.py` is a thin shim.
- **Missing catalog skill**: an unanchored `build/` rule in `.gitignore` kept `awesome_skills/automation/build/` out of Git, so catalog statistics could never verify on a fresh clone. Build-output rules are now root-anchored and the skill is restored byte-for-byte (verified against its `awesome_skills.lock` digest).
- **Unimportable skill handlers**: 158 `skills/**/__init__.py` files contained literal `\n` escapes (`SyntaxError`) and all 142 `handler.py` modules subclassed `BaseSkill` before importing it (`NameError`). Every handler now imports and instantiates.
- **Platform-dependent lockfile**: `skills.lock` digests changed with the OS (CRLF checkouts, `Path` sort order, `__pycache__` files), so a lock generated on Windows reported every skill as "tampered" on Linux. Hashing now normalises line endings and ordering; `skills.lock` is regenerated.
- **Stale generated files**: `skills/registry.json` / `dependencies.json` were regenerated — two canonical skills (`architecture/architecture-decision-records`, `healthcare/health-economist`) were missing from the registry.
- **Packaged CLI `doctor`** crashed with `TypeError` (wrong `Validator` call); `skills/_quarantine/` was missing from Git; `skills.py lock` printed a hard-coded skill count.
- **Docker**: the image's default command crashed (`ModuleNotFoundError: core`), the compose service restart-looped, and the build context had no `.dockerignore` (copying `.git` and any local `.env`).
- 60 mypy errors and 3 undefined names in first-party code.

### Added
- Consolidated **CI** workflow: Ruff, mypy, actionlint; tests with coverage on Python 3.10–3.12; library/registry/lockfile integrity; package build + wheel smoke test; Docker build (hadolint) + smoke test.
- **Security** workflow (skill scans, Gitleaks secret scanning, dependency review), **CodeQL** code scanning and **Dependabot** (Actions, pip, Docker).
- `tests/test_regressions.py` — permanent regression tests for every fix above (No-Regression Policy §3).
- `.editorconfig`, `.gitattributes` (LF everywhere, CRLF for `.bat`), `.pre-commit-config.yaml`, `.gitleaks.toml`, `.dockerignore`.
- Full Contributor Covenant 2.1, issue-template chooser with a feature-request form, refreshed PR template.
- README table of contents, live status badges, Mermaid architecture diagrams, "Quick Start" and "Development, CI & Quality Gates" sections; how-to-run READMEs for `src/`, `scripts/`, `tests/`, `skills/`, `docker/`, `hooks/`, `evals/`, `adapters/`, `schemas/` and `docs/`.

### Changed
- All GitHub Actions upgraded to current Node 24 releases (pinned by commit SHA) on `ubuntu-24.04`; the release workflow now runs on tags or manual dispatch only and attaches built distributions.
- Docker image runs as a non-root user on Python 3.12, exposes the `all-skills` CLI and makes audio libraries opt-in.

### Security
- Removed the `security@allskills.dev` contact from `SECURITY.md` — the domain is not registered, so reports would have been lost (or received by whoever registers it).
- `.gitignore` now covers `.env.*` variants and `config/api_keys.yml`, which the setup docs instruct users to fill with real keys.

### Removed
- Redundant workflows `test.yml`, `validate.yml`, `validate-skills.yml`, `skill-integrity.yml` and `registry.yml` (every command they ran is now in `ci.yml`), and the duplicate `skill_request.yml` issue form (superseded by `skill_proposal.yml`).

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
