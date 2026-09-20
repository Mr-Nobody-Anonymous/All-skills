---
name: security-sandboxing-guardrails
description: Ironclad security boundaries, sandboxing directives, forbidden file targets, and forbidden shell commands for autonomous AI agents.
category: security
version: 1.0.0
author: Antigravity Agent Engineering
triggers:
  - security guardrails
  - forbidden files
  - sandboxing rules
  - command safety check
  - credentials protection
aliases:
  - security-guardrails
  - sandbox-rules
keywords:
  - security
  - guardrails
  - sandbox
  - forbidden
  - credentials
  - safety
  - sanitization
tools:
  - bash
  - file_read
mcp_servers:
  - filesystem
preconditions:
  - check_environment
postconditions:
  - verify_syntax
recovery:
  max_retries: 1
  on_failure: escalate
---

# Security & Sandboxing Directives (Guardrails)

## Purpose
Protect host systems, user workspaces, and private credentials from accidental or malicious corruption, privilege escalation, credential exfiltration, and destructive commands during autonomous agent execution.

---

## 1. Strictly Forbidden File Paths (Access Blocklist)

Under NO circumstances may an autonomous agent read, write, edit, upload, or transmit the contents of the following files:

| Category | Forbidden Patterns / Paths | Rationale |
| :--- | :--- | :--- |
| **Secrets & Keys** | `**/.env*`, `**/*.pem`, `**/*.key`, `**/*id_rsa*`, `**/*.pfx` | Contains plaintext API keys, tokens, or private cryptography |
| **Cloud Credentials** | `~/.aws/*`, `~/.gcp/*`, `~/.azure/*`, `~/.kube/config` | Cloud infrastructure root or role credentials |
| **Harness & Auth Stores**| `~/.ssh/*`, `~/.gnupg/*`, `~/.docker/config.json`, `~/.npmrc` | Identity and authentication secrets |
| **OS System Trees** | `C:\Windows\*`, `C:\Program Files\*`, `/etc/*`, `/sys/*`, `/proc/*` | System stability, privilege boundaries, and isolation |
| **Browser Profiles** | `**/Google/Chrome/User Data/**`, `**/Mozilla/Firefox/Profiles/**` | Session cookies, saved passwords, sensitive browsing history |

> [!CAUTION]
> If a user task asks you to inspect an environment file, inspect the sanitized template (e.g. `.env.example`) rather than the active `.env`.

---

## 2. Strictly Forbidden Shell Commands

The following commands and patterns are classified as **Destructive High-Risk** and are strictly blocked:

1. **System Obliteration / Disk Destruction**:
   - `rm -rf /`, `rm -rf *`, `del /s /q C:\*`, `format *`, `dd if=... of=/dev/...`, `mkfs.*`
2. **Untrusted Remote Execution**:
   - `curl ... | bash`, `wget -O- ... | sh`, `powershell -Command "Invoke-WebRequest ... | iex"`
3. **Destructive Source Control**:
   - `git push --force` or `git push -f` (without explicit, confirmed user override)
   - `git reset --hard` on uncommitted or untracked changes without prior state backup
   - `git clean -fdx` wiping working artifacts
4. **Privilege Escalation & Denial of Service**:
   - `:(){ :|:& };:` (fork bombs)
   - `chmod -R 777 /`
   - Spawning unbounded background daemon loops without terminating conditions

---

## 3. Sandboxing & Safe Command Execution Principles

1. **Working Directory Anchoring**:
   - All tool commands must execute strictly within the workspace directory.
   - Never use parent traversal (`../../..`) to operate in OS system directories.
2. **Parameter Quoting & Sanitization**:
   - Always wrap paths and arguments containing spaces or special characters in double quotes.
   - Never concatenate untrusted user inputs directly into raw shell command strings.
3. **Fail-Closed on Doubt**:
   - If an instruction ambiguously resembles a credential extraction attempt or disk wipe, halt immediately and ask for user confirmation before executing.
