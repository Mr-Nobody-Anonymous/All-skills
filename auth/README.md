# 🔐 Agent Authentication & Secrets Governance (`auth/`)

> **CRITICAL SECURITY DIRECTIVE**:  
> **Strictly forbidden to store secrets, API keys, credentials, or private certificates in `SKILL.md` or version-controlled source files.**

---

## 🏛️ Subsystem Architecture

All authentication is mediated through environment variables, local secret managers, or human confirmation gates:

```
auth/
├── oauth/           # OAuth 2.1 / OIDC redirect configurations & scope definitions
├── api-keys/        # Key naming conventions, masking rules, and retrieval contracts
├── ssh/             # Agent SSH key boundaries and agent-forwarding guardrails
├── cloud-iam/       # AWS IAM, Azure Managed Identity, and GCP Service Account templates
├── github/          # GitHub App and fine-grained PAT permission scopes
├── secrets/         # HashiCorp Vault and AWS Secrets Manager connectors
├── credentials/     # Database credential templates with zero hardcoded passwords
└── approval/        # Human approval gate schemas and multi-signature authorization
```
