# 🔄 Multi-Step Execution Playbooks (Workflows)

Individual agent skills excel at **isolated tasks**, but building non-trivial features, resolving complex bugs, or launching products requires disciplined **multi-step handoffs** between specialized skill profiles.

The playbooks in this directory provide deterministic, end-to-end execution flows with explicit verification gates, state tracking, and fallback routes.

---

## 📚 Workflow Catalog

| Workflow Playbook | Target Objective | Key Skills Chained | State Tracking |
| :--- | :--- | :--- | :---: |
| [`feature-development.md`](feature-development.md) | End-to-end feature lifecycle from idea to release | `brainstorming` ➔ `concise-planning` ➔ `api-and-interface-design` ➔ `tdd` ➔ `code-reviewer` ➔ `changelog-automation` | `aas-stack.json` |
| [`bug-investigation-and-fix.md`](bug-investigation-and-fix.md) | Disciplined root-cause isolation and regression-proof fix | `code-showcase-systematic-debugging` ➔ `ast-code-transformation` ➔ `verification-before-completion` | `aas-stack.json` |
| [`fullstack-saas-launch.md`](fullstack-saas-launch.md) | Fast full-stack SaaS MVP delivery | `saas-mvp-launcher` ➔ `design-system` ➔ `database-design` ➔ `api-designer` ➔ `wcag-audit-patterns` ➔ `cloud-devops` | `aas-stack.json` |
| [`security-hardening-audit.md`](security-hardening-audit.md) | Comprehensive vulnerability and secrets audit | `security-sandboxing-guardrails` ➔ `sast-configuration` ➔ `top-web-vulnerabilities` ➔ `secrets-management` | `aas-stack.json` |
| [`ai-rag-agent-pipeline.md`](ai-rag-agent-pipeline.md) | Production AI agents, MCP tools, and RAG systems | `context-budget-and-pruning` ➔ `mcp-builder` ➔ `agent-memory` ➔ `multi-agent-architect` ➔ `agent-evaluation` | `aas-stack.json` |

---

## ⚡ How Autonomous Agents Run Workflows

1. **Initialize State**:
   ```bash
   python scripts/manage_state.py init <workflow-name>
   ```
2. **Execute Phase by Phase**:
   - The agent reads the phase instructions and loads the relevant `SKILL.md`.
   - The agent runs the task and records outputs.
   - The agent marks phase completion:
     ```bash
     python scripts/manage_state.py step <phase-number> --status completed
     python scripts/manage_state.py sync-context
     ```
3. **Automated Quality Gate Checkpoints**:
   - Run pre- and post-hooks before and after every major phase:
     ```bash
     python scripts/run_hook.py post <skill-id>
     ```
