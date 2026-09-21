# All-Skills No-Regression Policy & Quality Standard

**Effective Version:** 3.0.0  
**Effective Date:** 2026-09-21  
**Status:** Canonical & Enforced  

---

## 1. Core Principle

**No regression is tolerated in production or main.**  
Any capability, test assertion, security gate, or performance boundary currently verified in the All-Skills platform must remain passing on every future commit and release.

---

## 2. Invariant Quality Gates

Every code change proposed via Pull Request or direct commit must satisfy the following automated quality gates:

### Gate 1: Schema & Spec Validation
- **Requirement:** 100% of `SKILL.md` frontmatters must strictly validate against `schemas/skill.schema.json`.
- **Command:** `python scripts/validate_schema.py`

### Gate 2: Test Suite Inviolability
- **Requirement:** All 150 platform unit and integration tests must pass cleanly.
- **Rule:** Tests may not be deleted, skipped with `@unittest.skip` (unless for explicitly documented, non-passing upstream platform defects), or downgraded.
- **Command:** `python scripts/skills/skills.py test`

### Gate 3: Security & Prompt Injection Scans
- **Requirement:** Zero high-severity findings and zero uninspected bypasses.
- **Rule:** Files exceeding maximum size limits must fail as `UNSCANNABLE` rather than receiving implicit trust.
- **Command:** `python scripts/scan_skills_security.py`

### Gate 4: Zero Metric & Documentation Drift
- **Requirement:** Numbers in `README.md`, `stats.json`, and manifests must agree 100%.
- **Commands:**
  - `python scripts/compute_stats.py --verify`
  - `python scripts/generate_readme_stats.py --verify`

### Gate 5: 11-Layer Platform Diagnostic Doctor
- **Requirement:** All 11 diagnostic layers must report `PASS`.
- **Command:** `python scripts/allskills.py doctor --full`

---

## 3. Bug-to-Regression Test Rule

Whenever a bug, routing false-positive, security bypass, or adapter failure is identified:
1. A failing reproduction test must be committed first under `tests/`.
2. The implementation fix is applied.
3. The regression test remains a permanent member of the regression test suite and may never be removed.

---

## 4. Preservation Rule (Zero Deletions)

- No skill directory, category directory, adapter configuration, or profile may be deleted.
- Skills requiring revocation or quarantine are recorded in `revocations.json` or moved to an isolated quarantine state with full git forensic history intact.
