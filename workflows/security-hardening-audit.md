# Security Hardening & Audit Workflow Playbook

> **Target Objective**: Conduct an exhaustive security audit across source code, dependencies, cloud infrastructure, and secret management without exposing credentials or executing destructive payloads.

---

## Workflow Sequence

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              SECURITY AUDIT & HARDENING FLOW                           │
├─────────────────┬──────────────────┬─────────────────┬────────────────┬────────────────┤
│ 1. GUARDRAILS   │ 2. SAST SCANNING │ 3. OWASP & VULN │ 4. SECRETS     │ 5. ATTESTATION │
│    ENFORCEMENT  │    & STATIC RULES│    AUDITING     │    MANAGEMENT  │    & REPORT    │
├─────────────────┼──────────────────┼─────────────────┼────────────────┼────────────────┤
│ security-       │ sast-            │ top-web-        │ secrets-       │ executive      │
│ sandboxing      │ configuration    │ vulnerabilities │ management     │ summary report │
└─────────────────┴──────────────────┴─────────────────┴────────────────┴────────────────┘
```

---

## Phase 1: Operational Guardrail Check
- **Primary Skill**: [`.agents/skills/security-sandboxing-guardrails/SKILL.md`](../.agents/skills/security-sandboxing-guardrails/SKILL.md)
- **Actions**:
  1. Verify workspace isolation: execute all commands strictly within repository root.
  2. Confirm access blocklist: ensure `.env`, private keys (`*.pem`, `*.key`), and cloud credentials (`~/.aws/`) are untouched.
- **Exit Gate**: Sandboxing directives verified active.

---

## Phase 2: Static Application Security Testing (SAST)
- **Primary Skills**: [`.agents/skills/sast-configuration/SKILL.md`](../.agents/skills/sast-configuration/SKILL.md) & [`.agents/skills/security-scanning-security-sast/SKILL.md`](../.agents/skills/security-scanning-security-sast/SKILL.md)
- **Actions**:
  1. Configure language-specific static analysis (e.g. Bandit for Python, Semgrep, ESLint Security).
  2. Run scans to identify insecure regexes, SQL injection vectors, and command injection risks.
  3. Classify findings into High, Medium, and Low severity.
- **Exit Gate**: SAST report generated with 0 unaddressed High-severity issues.

---

## Phase 3: OWASP Top 10 & Supply Chain Vulnerabilities
- **Primary Skills**: [`.agents/skills/top-web-vulnerabilities/SKILL.md`](../.agents/skills/top-web-vulnerabilities/SKILL.md) & [`.agents/skills/vulnerability-scanner/SKILL.md`](../.agents/skills/vulnerability-scanner/SKILL.md)
- **Actions**:
  1. Inspect authentication flows, CORS configurations, and rate-limiting headers.
  2. Audit third-party packages for known CVEs (`pip check`, `npm audit`).
  3. Validate input sanitization on all exposed API routes.
- **Exit Gate**: Known critical CVEs patched or mitigated.

---

## Phase 4: Secrets Management & Masking
- **Primary Skill**: [`.agents/skills/secrets-management/SKILL.md`](../.agents/skills/secrets-management/SKILL.md)
- **Actions**:
  1. Verify `.gitignore` contains all sensitive extensions (`.env*`, `*.pem`, `*.key`).
  2. Audit git history for accidentally committed tokens (`git-filter-repo` check).
  3. Ensure application reads secrets from environment variables or Vault rather than hardcoded strings.
- **Exit Gate**: Zero hardcoded secrets found in codebase.

---

## Phase 5: Attestation & Remediation Report
- **Actions**:
  1. Compile an Executive Security Summary detailing audited surfaces, resolved vulnerabilities, and lingering risks.
  2. Record final state in `aas-stack.json`:
     ```bash
     python scripts/manage_state.py step 5 --status completed
     python scripts/manage_state.py sync-context
     ```
- **Exit Gate**: Attestation report signed off and archived.
