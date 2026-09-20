# Security Policy

## 🛡️ Supported Versions

| Version | Supported |
| :--- | :---: |
| 1.x (Current `main`) | :white_check_mark: |
| < 1.0 | :x: |

---

## 🔒 Reporting a Vulnerability

The security of autonomous agent instructions is critical. Malicious skills containing prompt injections, command injections, or data exfiltration will be immediately quarantined and purged.

If you discover a security vulnerability, prompt injection vector, or unsafe tool pattern:

1. **Do NOT open a public GitHub issue.**
2. Send an email report to the security maintainers or file a private security advisory on GitHub.
3. Include:
   - Skill name and file path.
   - Attack vector description (e.g. prompt injection, pipe-to-shell, secret leakage).
   - Minimal proof of concept.

---

## 🛑 Automated Security Scanning

Every commit is statically scanned via `scripts/scan_skills_security.py` against:
- Prompt injection and system prompt override payloads
- Destructive commands (`rm -rf /`, `mkfs`, `dd`)
- Pipe-to-shell patterns (`curl | bash`, `wget | sh`)
- Exposed secrets, private keys, and cloud API tokens
- Unauthorized webhook egress
