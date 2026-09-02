---
name: security-scanner
description: Gate releases with defensive static, dependency, secret, and configuration security checks.
category: media_and_utilities
aliases: [security, scan, vulnerability, secret, scan, audit]
triggers:
  - Security scan
  - Check for vulnerabilities
  - Scan for secrets
  - Security audit
  - Vulnerability check
keywords: [security, scan, vulnerability, secret, audit, cve, sast]
required_tools: [security-scanners]
risk: medium
version: 1.0.0
source: openclawskills.net
enabled: true
metadata:
  openclaw:
    requires:
      env: []
      bins: []
    primaryEnv: null
---

# Security Scanner Gate

## Purpose

Gate releases with comprehensive security checks including static analysis, dependency
vulnerability scanning, secret detection, and configuration hardening. The skill
ensures security issues are caught before deployment.

## When to Use

- Before releasing code to production
- Running CI/CD security gates
- Auditing codebase for security issues
- Pre-commit security checks

## When NOT to Use

- As the only security measure (use comprehensive program)
- For real-time threat detection (use dedicated tools)
- Without proper security tooling installed

## Capabilities

- Static Application Security Testing (SAST)
- Dependency vulnerability scanning (CVE detection)
- Secret and credential detection
- Configuration hardening checks
- License compliance scanning
- Container image scanning
- Infrastructure as Code security
- Report generation in multiple formats

## Inputs

- `scope` (optional) â€” full, diff, modified-files
- `checks` (optional) â€” sast, dependencies, secrets, config, all
- `severity` (optional) â€” critical, high, medium, low (default: high+)
- `fail_on` (optional) â€” severity level to fail the gate

## Workflow

1. **Scan** â€” Run configured security tools
2. **Collect** â€” Aggregate findings from all scanners
3. **Filter** â€” Remove duplicates, apply severity filters
4. **Assess** â€” Evaluate findings for false positives
5. **Report** â€” Present findings with remediation
6. **Gate** â€” Pass or fail based on configured thresholds

## Tools

- SAST: Semgrep, Bandit, ESLint security, etc.
- Dependencies: npm audit, pip-audit, Snyk, Dependabot
- Secrets: TruffleHog, Gitleaks, detect-secrets
- Config: kube-bench, Prowler, Checkov

## Examples

**User:** "Run a security scan before release"
**Response:**
```
Security Scan Results
=====================

[FAIL] Secret Detection: 1 finding
  - app/config.py:123 â€” Potential AWS key detected

[FAIL] Dependency Scan: 2 findings
  - lodash@4.17.20 â€” Prototype Pollution (CVE-2021-23337)
  - requests@2.28.0 â€” Information Disclosure (CVE-2023-32681)

[PASS] SAST: No issues
[PASS] Configuration: No issues

RELEASE GATE: FAILED
Critical/High issues must be resolved before release.

Recommendations:
1. Remove/rotate exposed credential
2. Update lodash to >=4.17.21
3. Update requests to >=2.31.0
```

## Safety

- Never skip security gates for speed
- Require human review for critical findings
- Don't expose sensitive findings in logs
- Maintain audit trail of scan results

## Source

Auto-generated from openclawskills.net description.

## Pairs Well With

- `npm-auditor` (dependency-specific scanning)
- `secret-detection` (deeper secret analysis)
- `git-workflow` (pre-commit security checks)
