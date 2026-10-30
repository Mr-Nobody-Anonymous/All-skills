# Universal Agent Harness Compatibility Matrix

This document defines compatibility between **All Skills** and modern AI coding agent harnesses.

---

## 📊 Compatibility Evidence

Compatibility is recorded at four evidence levels, from weakest to strongest. The
authoritative, machine-readable record is [`compatibility/matrix.json`](../compatibility/matrix.json);
[`tests/test_agent_discovery.py`](../tests/test_agent_discovery.py) fails if it claims more than
the evidence supports, and the table below is **generated** from that file by
[`scripts/generate_harness_matrix.py`](../scripts/generate_harness_matrix.py) — the tier label is
computed, never typed.

| Level | Meaning | How it is verified | Tier badge |
| :--- | :--- | :--- | :--- |
| **Configured** | An adapter configuration exists and validates | Automated (`tests/test_adapters_conformance.py`) | Tier 1 Configured |
| **Discoverable** | The agent's skills directory is linked to `.agents/skills` and every active `SKILL.md` meets the Agent Skills format | Automated (`tests/test_agent_discovery.py`) | Tier 2 Scanned |
| **Invocable** | The skill is listed and loads inside a named agent version | Manual — recorded in `manual_evidence` | Tier 3 Validated |
| **Workflow completed** | An end-to-end task was completed with the skill in a named agent version | Manual — recorded in `manual_evidence` | Tier 4 Verified |

A row reads **Tier 2 Scanned** until someone records a named agent version, date, verifier and
skill in `manual_evidence`. That is the current state of every harness: configured and
discoverable are machine-checked on every push, invocable and workflow-completed are not claimed
because no one has run them yet. The previous hand-written table claimed Tier 4 Verified for four
harnesses with an empty `manual_evidence`, which is exactly the drift this generator removes.

<!-- BEGIN GENERATED: harness-compatibility (scripts/generate_harness_matrix.py) -->
| AI Coding Agent | Skills directory | Configured | Discoverable | Invocable | Workflow completed | Evidence level |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **Antigravity / Gemini CLI** | `.agents/skills/` | ✅ | ✅ | not yet verified | not yet verified | Tier 2 Scanned |
| **Claude Code** | `.claude/skills/` | ✅ | ✅ | not yet verified | not yet verified | Tier 2 Scanned |
| **Cursor** | `.cursor/skills/` | ✅ | ✅ | not yet verified | not yet verified | Tier 2 Scanned |
| **Codex CLI** | `.codex/skills/` | ✅ | ✅ | not yet verified | not yet verified | Tier 2 Scanned |
| **GitHub Copilot** | `.github/skills/` | ✅ | ✅ | not yet verified | not yet verified | Tier 2 Scanned |
| **VS Code Agent** | `.vscode/skills/` | ✅ | ✅ | not yet verified | not yet verified | Tier 2 Scanned |
| **Windsurf** | `.windsurf/skills/` | ✅ | ✅ | not yet verified | not yet verified | Tier 2 Scanned |
| **OpenCode** | `.opencode/skills/` | ✅ | ✅ | not yet verified | not yet verified | Tier 2 Scanned |
| **Cline** | `.cline/skills/` | ✅ | ✅ | not yet verified | not yet verified | Tier 2 Scanned |
| **Roo Code** | `.roo/skills/` | ✅ | ✅ | not yet verified | not yet verified | Tier 2 Scanned |
| **Block Goose** | `.goose/skills/` | ✅ | ✅ | not yet verified | not yet verified | Tier 2 Scanned |
| **OpenClaw** | `.openclaw/skills/` | ✅ | ✅ | not yet verified | not yet verified | Tier 2 Scanned |
<!-- END GENERATED: harness-compatibility -->

"Discoverable" means the files are where each agent documents that it looks for skills, in
the expected format — not that the agent was run. To record a manual check, add an entry to
`manual_evidence` in `compatibility/matrix.json` (agent version, date, who verified it and
which skill) and set the corresponding level to `true`.

---

## 🛠️ Harness Setup Commands

To link this repository to your preferred harness:

```bash
# Link all 12 local workspace harnesses (.claude, .cursor, .codex, .agents, .openclaw, …)
./setup.sh         # Linux / macOS
.\setup.bat        # Windows

# Link to global user home directories (~/.claude/skills, etc.)
python scripts/setup_skills.py --global

# Inspect detected harnesses
python scripts/setup_skills.py --status
```

---

## 🔌 Model Context Protocol (MCP) Support

All Skills includes a standardized [`mcp_config.json`](../mcp_config.json) with the keyless
`core` profile (`filesystem`, `git`, `fetch`, `memory`, `time`):
- **Claude Code**: Reads `mcp_config.json` directly.
- **Cursor**: Configure MCP under `Cursor Settings` ➔ `Features` ➔ `MCP` or link `mcp_config.json`.
- **Antigravity**: Native MCP discovery via `mcp_config.json`.

For anything beyond that baseline do not hand-edit the file — install from the catalog, which
knows every harness's dialect and every server's credentials:

```bash
allskills mcp list --profile standard                 # 20 keyless/single-token connectors
allskills mcp install --harness claude --profile full # all 117
allskills mcp doctor                                  # which keys are still missing
```

The catalog lives in [`mcps/catalog.json`](../mcps/catalog.json); the full matrix (tier,
category, risk, `required_env`) is regenerated into [`MCP-CATALOG.md`](MCP-CATALOG.md).
