# 🛠️ Universal Tool Registry (`tools/`)

The authoritative tool catalog defining machine-verifiable contracts, permissions, risks, authentication requirements, and health checks for all agent capabilities.

---

## 📑 Core Tool Categories

| Tool Domain | Tool ID | Primary Capability | Default Permission | Risk Level |
| :--- | :--- | :--- | :---: | :---: |
| **Filesystem** | `filesystem` | Bounded workspace read/write | Workspace scoped | `Low` |
| **Terminal** | `terminal` | Non-interactive command runner | Allowlist commands | `Medium` |
| **Shell** | `shell` | Wrapped sub-process invocation | Strictly bounded | `High` |
| **Browser** | `browser-playwright` | Headless navigation & inspection | HTTP/HTTPS allowlist | `Medium` |
| **Git** | `git` | Local repository version control | Workspace scoped | `Low` |
| **GitHub** | `github` | Issues, PRs, and repository API | Scoped PAT/App | `Medium` |
| **PostgreSQL** | `database-postgres` | SQL queries & schema inspection | Read-only default | `High` |
| **Docker** | `container-docker` | Container build & inspection | Local daemon | `High` |
| **Search** | `search-semantic` | Ripgrep & vector retrieval | Read-only | `Low` |
