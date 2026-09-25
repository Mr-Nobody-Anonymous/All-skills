# Universal Agent Harness Compatibility Matrix

This document defines compatibility between **All Skills** and modern AI coding agent harnesses.

---

## 📊 Compatibility Evidence

Compatibility is recorded at four evidence levels, from weakest to strongest. The
authoritative, machine-readable record is [`compatibility/matrix.json`](../compatibility/matrix.json);
[`tests/test_agent_discovery.py`](../tests/test_agent_discovery.py) fails if it claims more than
the evidence supports.

| Level | Meaning | How it is verified |
| :--- | :--- | :--- |
| **Configured** | An adapter configuration exists and validates | Automated (`tests/test_adapters_conformance.py`) |
| **Discoverable** | The agent's skills directory is linked to `.agents/skills` and every active `SKILL.md` meets the Agent Skills format | Automated (`tests/test_agent_discovery.py`) |
| **Invocable** | The skill is listed and loads inside a named agent version | Manual — recorded in `manual_evidence` |
| **Workflow completed** | An end-to-end task was completed with the skill in a named agent version | Manual — recorded in `manual_evidence` |

| Agent | Skills directory | Configured | Discoverable | Invocable | Workflow completed |
| :--- | :--- | :---: | :---: | :---: | :---: |
| Antigravity / Gemini CLI | `.agents/skills/` (source) | ✅ | ✅ | not yet verified | not yet verified |
| Claude Code | `.claude/skills/` | ✅ | ✅ | not yet verified | not yet verified |
| Cursor | `.cursor/skills/` | ✅ | ✅ | not yet verified | not yet verified |
| Codex CLI | `.codex/skills/` | ✅ | ✅ | not yet verified | not yet verified |
| GitHub Copilot | `.github/skills/` | ✅ | ✅ | not yet verified | not yet verified |
| VS Code Agent | `.vscode/skills/` | ✅ | ✅ | not yet verified | not yet verified |
| Windsurf | `.windsurf/skills/` | ✅ | ✅ | not yet verified | not yet verified |
| OpenCode | `.opencode/skills/` | ✅ | ✅ | not yet verified | not yet verified |
| Cline | `.cline/skills/` | ✅ | ✅ | not yet verified | not yet verified |
| Roo Code | `.roo/skills/` | ✅ | ✅ | not yet verified | not yet verified |
| Block Goose | `.goose/skills/` | ✅ | ✅ | not yet verified | not yet verified |

"Discoverable" means the files are where each agent documents that it looks for skills, in
the expected format — not that the agent was run. To record a manual check, add an entry to
`manual_evidence` in `compatibility/matrix.json` (agent version, date, who verified it and
which skill) and set the corresponding level to `true`.

---

## 🛠️ Harness Setup Commands

To link this repository to your preferred harness:

```bash
# Link all local workspace harnesses (.claude, .cursor, .codex, .agents)
./setup.sh         # Linux / macOS
.\setup.bat        # Windows

# Link to global user home directories (~/.claude/skills, etc.)
python scripts/setup_skills.py --global

# Inspect detected harnesses
python scripts/setup_skills.py --status
```

---

## 🔌 Model Context Protocol (MCP) Support

All Skills includes a standardized [`mcp_config.json`](../mcp_config.json):
- **Claude Code**: Reads `mcp_config.json` directly.
- **Cursor**: Configure MCP under `Cursor Settings` ➔ `Features` ➔ `MCP` or link `mcp_config.json`.
- **Antigravity**: Native MCP discovery via `mcp_config.json`.
