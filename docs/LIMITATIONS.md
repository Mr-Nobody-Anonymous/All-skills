# Known Limitations & Operating Boundaries

This document provides a transparent, authoritative specification of the design invariants, operational boundaries, and known limitations of the **All-skills** platform.

---

## 1. Catalog vs. Execution Surface Distinction

A foundational distinction in All-skills is between **indexed discovery material** and the **verified execution surface**:

```
┌─────────────────────────────────────────────────────────────┐
│ 14,855 Catalog Records (Indexed across 251 categories)       │
├─────────────────────────────────────────────────────────────┤
│   ▼ 12,757 Unique Skill Identities                          │
├─────────────────────────────────────────────────────────────┤
│     ▼ 192 Manifest-Declared Specification Skills            │
├─────────────────────────────────────────────────────────────┤
│       ▼ 122 Curated Canonical Engine Skills (skills/)       │
├─────────────────────────────────────────────────────────────┤
│         ▼ 72 Active Harness Skills (.agents/skills/)        │
└─────────────────────────────────────────────────────────────┘
```

- **Catalog Records (14,855)**: Sourced from upstream repositories, domain taxonomies, and multi-agent indexes. These serve as discovery material, knowledge references, and search targets. They are not all independently unit-tested or guaranteed to have executable script backends.
- **Canonical Skills (122)**: Maintained directly in `skills/`, verified against `schemas/skill-frontmatter.schema.json`, tested via regression suites, and governed by deterministic routing.
- **Active Harness Skills (72)**: Symlinked or junctioned into agent platforms (`.agents/skills`, `.claude/skills`, `.cursor/skills`, `.codex/skills`) for immediate invocation.

---

## 2. Universal Skill Execution Runtime Boundaries

The `ExecutionRuntime` (`src/skills/runtime.py`) governs lifecycle transitions, permission policies, revocation kill-switches, and audit logging.

- **Agent Host Delegation**: In multi-agent IDE environments (Antigravity, Cursor, Claude Code, Codex), the AI model itself remains responsible for contextual generative reasoning, prompt execution, and AST block edits. The runtime provides the governance wrapper, tool broker, and audit verification.
- **Dry-Run Mode**: When invoked with `--dry-run`, the runtime computes the execution plan, verifies capability policies, and estimates token costs without dispatching side-effecting operations.

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
