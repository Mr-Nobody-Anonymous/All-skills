# Security & Sandboxing Directive

## Operational Guardrails
- **Forbidden Files**: Never read, write, or transmit `.env*`, `*.pem`, `*.key`, `id_rsa`, AWS/GCP/Azure credentials, or OS system paths (`C:\Windows`, `/etc`). Inspect `.env.example` templates instead.
- **Forbidden Commands**: Never execute destructive commands (`rm -rf /`, `del /s /q C:\*`, `format`, `dd`), untrusted pipe-to-shell invocations (`curl | sh`), destructive force pushes (`git push -f`), or hard resets destroying uncommitted work.
- **Workspace Anchoring**: Anchor all tool operations within the workspace root.
- **Param Sanitization**: Quote paths and parameters. Do not concatenate untrusted strings into shell commands.
