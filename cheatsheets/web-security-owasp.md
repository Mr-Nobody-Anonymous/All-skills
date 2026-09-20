# 🛡️ OWASP Top 10 Security Cheatsheet

| Vulnerability | Mechanism | Core Defense |
| :--- | :--- | :--- |
| **A01: Broken Access Control** | Unauthorized privilege escalation / IDOR | Enforce RBAC on server side; deny by default |
| **A02: Cryptographic Failures** | Plaintext sensitive data / weak ciphers | Use TLS 1.3, AES-GCM-256, bcrypt/Argon2 for passwords |
| **A03: Injection (SQL, Command)** | Unsanitized input concatenated into queries | Parameterized queries (Prepared Statements), ORM |
| **A04: Insecure Design** | Architectural flaws, missing rate limits | Threat modeling, defense in depth, failure isolation |
| **A05: Security Misconfiguration** | Default credentials, verbose error traces | Hardened baselines, disable debugging in production |
| **A06: Vulnerable Components** | Outdated third-party packages | Automated SCA scanning (Dependabot, Snyk, SBOM) |
| **A07: Identification & Auth** | Credential stuffing, weak session tokens | Multi-factor auth, secure cookies, brute-force limits |
| **A08: Software & Data Integrity** | Untrusted deserialization, CI/CD tampering | Signed commits, cryptographic verification (Sigstore) |
| **A09: Logging & Monitoring** | Undetected intrusions, unlogged audits | Centralized append-only SIEM logs, alerting thresholds |
| **A10: SSRF** | Server tricked into fetching internal URLs | Validate URL protocols, deny loopback & internal IPs |
