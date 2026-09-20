# Universal Agent Harness Compatibility Matrix

This document defines compatibility between **All Skills** and modern AI coding agent harnesses.

---

## 📊 Compatibility Overview

| AI Agent Harness | Workspace Skill Path | Global Skill Path | Frontmatter Ingestion | Symlink / Junction | Model Context Protocol (MCP) | Automated Hooks | State Sidecars (`aas-stack`) |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Claude Code** | `.claude/skills/` | `~/.claude/skills/` | ✅ Native | ✅ Native | ✅ Supported (`mcp_config.json`) | ✅ via `scripts/run_hook.py` | ✅ Native |
| **Cursor** | `.cursor/skills/` | `~/.cursor/skills/` | ✅ Native | ✅ Native | ✅ Supported (`.cursor/mcp.json`) | ✅ via `scripts/run_hook.py` | ✅ Native |
| **Codex CLI** | `.codex/skills/` | `~/.codex/skills/` | ✅ Native | ✅ Native | ✅ Supported | ✅ via `scripts/run_hook.py` | ✅ Native |
| **Antigravity / Gemini CLI**| `.agents/skills/` | `~/.gemini/antigravity-cli/skills/` | ✅ Native | ✅ Native | ✅ Supported | ✅ Pre/Post Execution | ✅ Native |
| **Kiro / OpenClaw** | `.agents/skills/` | `~/.kiro/skills/` | ✅ Native | ✅ Native | ✅ Supported | ✅ via `scripts/run_hook.py` | ✅ Native |
| **Windsurf** | `.agents/skills/` | `~/.codeium/windsurf/skills/` | ✅ Native | ✅ Native | ✅ Supported | ✅ via `scripts/run_hook.py` | ✅ Native |

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
