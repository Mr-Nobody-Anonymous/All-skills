# Security Policy

## 🛡️ Supported Versions

| Version | Supported | Status |
| :--- | :---: | :--- |
| `3.0.x` (Current `main`) | :white_check_mark: | Active Security Maintenance |
| `2.0.x` | :warning: | Critical Security Fixes Only |
| `< 2.0` | :x: | End of Life / Unsupported |

---

## 🔒 Reporting a Vulnerability

The security of autonomous agent instructions, tools, and execution environments is paramount. Malicious skills containing prompt injections, command injections, or exfiltration hooks will be immediately quarantined and revoked.

If you discover a security vulnerability, prompt injection bypass, or malicious skill payload:

1. **Do NOT open a public GitHub issue.**
2. Report via **GitHub Private Security Advisory**: [Submit Advisory](https://github.com/Mr-Nobody-Anonymous/All-skills/security/advisories/new)
3. Or email our security maintainers directly: **`security@allskills.dev`**
4. Please provide:
   - Skill name, category, and exact file path.
   - Attack vector classification (e.g. prompt injection, command injection, path traversal, credential theft).
   - Minimal, reproducible proof-of-concept (PoC).
   - Affected client runtimes (e.g. Claude Code, Cursor, Codex, OpenClaw, Antigravity).

### Response SLA & Disclosure Policy
- **Initial Response & Acknowledgment**: Within 24 hours.
- **Triage & Severity Classification**: Within 48 hours.
- **Patch & Revocation Deployment**: Within 7 business days for high/critical findings.
- **Public Disclosure**: Coordinated disclosure after release of fix or revocation entry in `registry/revocations.json`.

---

## 🛑 Automated Security Gates & Pipeline

Every commit and pull request is strictly verified across multi-layer security gates:
- **Static & AST Analysis**: Inspected via `src/skills/security.py` and `scripts/scan_skills_security.py`
- **Prompt Injection Defense**: Validated against `evals/adversarial/` benchmark suite
- **Fail-Closed Lifecycle Hooks**: Required hooks enforce non-zero failure exits
- **Kill-Switch Enforcement**: Instant revocation lookup via `registry/revocations.json`
- **Network Egress Constraints**: Outbound filtering per `docs/security/network-security.md`
