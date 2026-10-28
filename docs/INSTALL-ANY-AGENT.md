# Install All-Skills Into Any Agent

**One command links the skill library, installs MCP connectors and verifies both.**

```bash
# From a checkout
python scripts/allskills.py bootstrap --harness cursor --profile standard

# From an installed CLI
allskills bootstrap --harness claude --profile core

# Every harness at once, then verify
allskills bootstrap --all --profile standard
```

Prefer a shell script (CI images, containers)? The same flow:

```bash
./scripts/bootstrap_agent.sh --harness claude --profile standard --global
./scripts/bootstrap_agent.sh --all --profile core --dry-run   # preview only
```

What it does, in order:

1. **Links skills** — `scripts/setup_tools.py` connects the canonical
   `.agents/skills/` source to every harness directory it can detect, recording each
   link in `state/managed_harnesses.json`.
2. **Installs MCP connectors** — `scripts/mcp_catalog.py install` merges the chosen
   profile into the target harness config (additive, idempotent, backed up).
3. **Verifies** — harness links, MCP catalog and skill-library validation must all pass.

---

## 1. What "installed" means

| Layer | Where it lives | Installed by |
| :--- | :--- | :--- |
| **Skills** (504 canonical, 89 preloaded) | `skills/` → linked into `.claude/skills`, `.cursor/skills`, `.agents/skills`, … | `scripts/setup_tools.py` |
| **Catalog** (15k searchable skills) | `awesome_skills/` | nothing to install — searched via `allskills search` |
| **MCP connectors** (113 servers) | `mcps/catalog.json` → merged into each harness config | `scripts/mcp_catalog.py` |
| **Agents & commands** (68 / 94) | `agents/`, `commands/` | read natively by Claude Code and mirrored for others |

## 2. Harness matrix

Skills are linked by `setup_tools.py`; MCP is written in each harness's own dialect by
`mcp_catalog.py`.

| Harness | Skills directory | Project MCP config | User MCP config | Dialect |
| :--- | :--- | :--- | :--- | :--- |
| Claude Code | `.claude/skills/` | `.mcp.json` | `~/.claude.json` | JSON |
| Cursor | `.cursor/skills/` | `.cursor/mcp.json` | `~/.cursor/mcp.json` | JSON |
| Codex CLI | `.codex/skills/` | `.codex/config.toml` | `~/.codex/config.toml` | TOML fragment |
| Gemini CLI / Antigravity | `.agents/skills/` | `.gemini/settings.json` | `~/.gemini/settings.json` | JSON |
| GitHub Copilot | `.github/skills/` | — | — | uses skills only |
| VS Code agent | `.vscode/skills/` | `.vscode/mcp.json` | `~/.vscode/mcp.json` | JSON (`type: stdio`) |
| Windsurf | `.windsurf/skills/` | `.windsurf/mcp.json` | `~/.codeium/windsurf/mcp_config.json` | JSON |
| OpenCode | `.opencode/skills/` | `opencode.json` | `~/.config/opencode/opencode.json` | JSON (`type: local`) |
| Cline | `.cline/skills/` | `.cline/mcp.json` | `~/.cline/mcp_settings.json` | JSON |
| Roo Code | `.roo/skills/` | `.roo/mcp.json` | `~/.roo/mcp_settings.json` | JSON |
| Block Goose | `.goose/skills/` | `.goose/config.yaml` | `~/.config/goose/config.yaml` | YAML fragment |
| Zed | `.zed/settings.json` | `.zed/settings.json` | `~/.config/zed/settings.json` | JSON (`context_servers`) |
| Kimi CLI | `.kimi/` | `.kimi/mcp.json` | `~/.kimi/mcp.json` | JSON |
| Qwen Code | `.qwen/` | `.qwen/settings.json` | `~/.qwen/settings.json` | JSON |
| Trae | `.trae/` | `.trae/mcp.json` | `~/.trae/mcp.json` | JSON |
| CodeBuddy | `.codebuddy/` | `.codebuddy/mcp.json` | `~/.codebuddy/mcp.json` | JSON |
| Hermes | `.hermes/` | `.hermes/mcp.json` | `~/.hermes/mcp.json` | JSON |
| OpenClaw | `.openclaw/` | `.openclaw/mcp.json` | `~/.openclaw/mcp.json` | JSON |
| Continue.dev | — | `.continue/mcpServers/mcp.json` | `~/.continue/mcpServers/mcp.json` | JSON |

Harnesses with a **fragment** dialect never have their config rewritten in place: the
installer prints the exact TOML/YAML block to paste, because a JSON-shaped guess would
corrupt the file.

## 3. Profiles

| Profile | Servers | Use it when |
| :--- | ---: | :--- |
| `core` | 5 | You want the safest, keyless baseline (filesystem, git, fetch, memory, time). |
| `standard` | 20 | Everyday engineering: adds GitHub, Playwright, Chrome DevTools, Postgres, Sentry, Context7, sequential thinking, DuckDB, Pinecone, Qdrant, Airtable, Todoist, Apify, E2B, ElevenLabs. |
| `full` | 113 | "Give the agent everything": every connector, including credential-gated SaaS, cloud, payments and infra servers. |

```bash
allskills mcp list --profile standard      # what is included
allskills mcp doctor                       # what still needs a key
allskills mcp install --harness cursor --servers github postgres playwright   # hand-picked
```

Install profiles select *skills and assets* (a different axis from the MCP profiles above):

| Install profile | What you get |
| :--- | :--- |
| `minimal` / `core` | rules, agents, commands and the quality workflow baseline |
| `developer` | adds the framework/language, database and orchestration modules |
| `library` | core baseline **plus all 504 curated `skills/` skills** (`canonical-library`) |
| `full` | every module: all skills, all agent packs, MCP conventions and domain packs |

```bash
node scripts/install-apply.js --profile library --target cursor --dry-run
node scripts/install-apply.js --profile full --target cursor
```

## 4. Credentials

Nothing is required for `core`. For credential-gated servers, export the variable named
in `allskills mcp doctor` (each catalog entry declares `required_env`):

```bash
export GITHUB_PERSONAL_ACCESS_TOKEN=...   # github
export POSTGRES_URL=postgres://...        # postgres
export SENTRY_ACCESS_TOKEN=...            # sentry
allskills mcp doctor
```

Secrets are never written into the repository: the installer writes `${VAR}` placeholders
or `YOUR_VAR_HERE` values, and `allskills mcp verify` fails if a `${VAR}` is undeclared.

## 5. Uninstall / rollback

```bash
python scripts/setup_tools.py --unlink        # removes only ledger-recorded links
allskills mcp install --harness cursor --servers filesystem   # configs keep a .bak
```

Every MCP config write leaves `<config>.bak` next to the original, and only keys under the
harness's server object are touched — your other settings are byte-identical.

## 6. Troubleshooting

| Symptom | Fix |
| :--- | :--- |
| "harness has no project scope" | Use `--scope user` or pick a harness that has that scope. |
| Agent sees no skills | `python scripts/setup_tools.py --status`, then `--replace-managed-links`. |
| MCP server listed but tools missing | Restart the harness — MCP configs are read at startup. |
| `allskills mcp verify` fails | A catalog entry has an undeclared `${ENV}` placeholder or duplicate id. |
| Too much context used | Drop to `--profile core`; each enabled server costs schema tokens every session. |

See [`MCP-CONNECTOR-POLICY.md`](MCP-CONNECTOR-POLICY.md) for why the default set is small, and
[`MCP-CATALOG.md`](MCP-CATALOG.md) for every server, its tier and its credentials.
