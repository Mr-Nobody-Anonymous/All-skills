# Known Limitations & Operating Boundaries

This document provides a transparent, authoritative specification of the design invariants, operational boundaries, and known limitations of the **All-skills** platform.

---

## 1. Catalog vs. Execution Surface Distinction

A foundational distinction in All-skills is between **indexed discovery material** and the **verified execution surface**:

```
┌─────────────────────────────────────────────────────────────┐
│ 15,146 Catalog Records (Indexed across 252 categories)       │
├─────────────────────────────────────────────────────────────┤
│   ▼ 13,362 Unique Skill Identities                          │
├─────────────────────────────────────────────────────────────┤
│     ▼ 504 Manifest-Declared Specification Skills            │
├─────────────────────────────────────────────────────────────┤
│       ▼ 504 Curated Canonical Engine Skills (skills/)       │
├─────────────────────────────────────────────────────────────┤
│         ▼ 89 Active Harness Skills (.agents/skills/)        │
└─────────────────────────────────────────────────────────────┘
```

- **Catalog Records (15,146)**: Sourced from upstream repositories, domain taxonomies, and multi-agent indexes. These serve as discovery material, knowledge references, and search targets. They are not all independently unit-tested or guaranteed to have executable script backends.
- **Canonical Skills (504)**: Maintained directly in `skills/`, verified against `schemas/skill-frontmatter.schema.json`, tested via regression suites, and governed by deterministic routing.
- **Active Harness Skills (89)**: Symlinked or junctioned into agent platforms (`.agents/skills`, `.claude/skills`, `.cursor/skills`, `.codex/skills`) for immediate invocation.

---

## 2. Universal Skill Execution Runtime Boundaries

The `ExecutionRuntime` (`src/skills/runtime.py`) governs lifecycle transitions, permission policies, revocation kill-switches, and audit logging.

- **Agent Host Delegation**: In multi-agent IDE environments (Antigravity, Cursor, Claude Code, Codex), the AI model itself remains responsible for contextual generative reasoning, prompt execution, and AST block edits. The runtime provides the governance wrapper, tool broker, and audit verification.
- **Dry-Run Mode**: When invoked with `--dry-run`, the runtime computes the execution plan, verifies capability policies, and estimates token costs without dispatching side-effecting operations.
- **Gates, not a sandbox**: The runtime decides *whether* a skill may run (revocation, lifecycle, capability policy, enforced human approval for `ASK`, SSRF checks) and checks what the executor reports: missing declared outputs, or tool calls outside the tools and capabilities the run was authorised for, fail the run. A skill without a registered executor is returned as `prepared` instructions — it is never reported as done.
- **In-process executors are trusted code**: They run with the runtime's own privileges, so the tool-call check detects a violation after the fact; it cannot prevent it.
- **`SubprocessExecutor` bounds resources** (`src/skills/executors.py`): a separate process with a per-run scratch directory as `HOME`/`TMPDIR`, an environment reduced to an allow-list (parent credentials are not inherited), a timeout that kills the process group, an output cap, and on POSIX CPU/memory/file-size limits — a limit the platform would not enforce is refused rather than ignored (Windows has no `setrlimit`; macOS accepts `RLIMIT_AS` but does not enforce it, so memory limits are refused there). Wall time, exit status and child CPU time are measured by the runtime, not self-reported.
- **Not isolated**: the filesystem outside the scratch directory, and the network. On Windows only the direct child is killed on timeout; processes it started may survive. Run untrusted code in a container, microVM or OS job object.

---

## 3. Static Security Scanner Limitations

The built-in security scanner (`src/skills/security.py` / `scripts/scan_skills_security.py`) enforces strict AST parsing and regex heuristics:

- **What is detected**:
  - Python and YAML AST syntax malformations.
  - Dangerous system calls (`os.system`, `subprocess(shell=True)`, `eval`, `exec`).
  - Destructive disk operations (`rm -rf /`, `mkfs`, destructive `dd`).
  - Shell pipe-to-interpreter hazards (`curl | sh`, `wget | bash`).
  - Known prompt injection signatures and exfiltration markers.
  - Hardcoded cloud credentials and private key blocks (`BEGIN RSA PRIVATE KEY`, AWS/GitHub tokens).
- **What is NOT guaranteed**:
  - Complex dynamic obfuscation (e.g. multi-stage base64 + zlib + XOR payloads downloaded at runtime).
  - Advanced side-channel attacks or memory poisoning during extended host AI conversations.
  - Users operating in zero-trust environments must run untrusted third-party skills inside isolated microVMs, Docker containers, or OS Job Objects.

---

## 4. Platform Adapters & Harness Synchronization

- **Junction & Symlink Invariants**: The setup harness (`scripts/setup_tools.py` and `scripts/setup_skills.py`) strictly enforces that real directories and unmanaged symlinks are never modified or overwritten (`REFUSED: unmanaged directory or link`).
- **Copy Fallback Caveat**: On platforms without symlink or junction permissions (e.g. Windows without Developer Mode or unprivileged containers), the harness falls back to directory copies and tracks them in `managed_harnesses.json`. Upstream edits require running `allskills init` or `python scripts/setup_skills.py` to synchronize copies.
- **Platform Verification**: Declarative adapter definitions (`adapters/*.yaml`) provide configuration discovery and path mapping for 12 platforms. End-to-end integration is validated on Linux and Windows CI environments.

---

## 5. Tool Capabilities & MCP Connectivity

- **Default Tools**: The baseline MCP configuration (`mcp_config.json`) enables `filesystem`, `fetch`, `git`, and `memory`.
- **Network Access**: Skills demanding external network access require explicit capability declaration (`network.request`). In high-security profiles, network requests default to restricted policies.
- **Credentials Guardrail**: The policy engine strictly denies raw credential exposure (`credentials.read: DENY`). Secret tokens must be brokered through host environment variables or dedicated key vaults.

---

## 6. Deterministic Routing & Thresholds

- **Empirical Routing Threshold**: The router evaluates queries across exact ID, alias, category, trigger words, keyword overlap, and quality score boosts. Matches scoring below the empirical threshold (`18.0` / `0.18`) are rejected as out-of-distribution (`status: "no_match"`).
- **Ambiguous Multi-Intent Requests**: For complex multi-disciplinary prompts, direct routing may match only the primary intent. Users should utilize named skill chains (`python scripts/skills/skills.py chain <name>`) or the interactive `/grill-me` alignment flow.

---

## 7. Versioning & SemVer Policy

- All platform-wide components (package, CLI, manifest, schema, configuration) are unified under the canonical version specified in `VERSION` (currently `3.0.0`).
- Individual skills declare functional frontmatter versions (`version: 1.0.0`), but independent per-skill package registry distribution is part of the v4 roadmap.

---

## 8. Vendored ECC Tooling & Its Test Suite

The optional *Everything Claude Code* (ECC) tooling (`bin/ecc.js`, `scripts/profile.js`,
`scripts/install-apply.js`, `tests/run-all.js`) is vendored from a separate project whose
repository layout differs from this one:

- ECC discovers skills as flat `skills/<skill-name>/SKILL.md` directories, while this
  project's canonical library is categorised as `skills/<category>/<skill>/SKILL.md` and
  its ECC-authored playbooks live under `.kiro/skills/` and `awesome_skills/ecc/`.
- Because of that layout difference, `npm run test:ecc` (`node tests/run-all.js`) reports
  failures for ECC surfaces that this repository does not contain (install-module
  planning, OpenCode build output, Itô compute, Nasiko control plane, release workflows).
  It is **not** part of CI; the gated suites are `pytest`, `python scripts/skills/skills.py test`,
  `python scripts/run_evals.py` and `python scripts/allskills.py doctor --full`.
- Treat `tests/run-all.js` as a migration tracker: a failing file marks an ECC feature that
  has not been ported to the categorised layout yet, not a regression in the platform CLI.

---

## 9. Installer Source Mapping vs. the Categorised Library

`manifests/install-modules.json` declares skill sources by their real paths —
`awesome_skills/ecc/<name>` for the vendored ECC playbooks and
`skills/<category>/<name>` for the curated library. Two subsystems read that manifest:

- **`scripts/setup_tools.py` / `allskills bootstrap`** link the whole library into each
  harness (`.claude/skills`, `.cursor/skills`, `.agents/skills`, …). This is the supported
  install path and it handles every layout; `allskills bootstrap --dry-run` verifies it.
- **`scripts/install-apply.js` and the `scripts/lib/install-targets/*` adapters** implement
  the vendored ECC selective installer. Their destination mapping only rewrites sources that
  start with `skills/` (flattening them to `skills/<name>` in the harness root); sources under
  `awesome_skills/ecc/` are copied with their path preserved instead of being flattened.

Consequence: `node tests/scripts/install-apply.test.js` asserts the flat ECC layout
(`~/.claude/skills/tdd-workflow/SKILL.md`) and therefore fails for playbooks that now live
under `awesome_skills/ecc/`. These failures pre-date the current change, are not part of CI,
and do not affect `allskills bootstrap`, `allskills install`, `node scripts/install-apply.js
--profile library|full` (both install correctly), or any Python gate. Closing it means adding
an `awesome_skills/ecc/<name> → skills/<name>` rewrite to each adapter — tracked as installer
work, not a documentation gap.

