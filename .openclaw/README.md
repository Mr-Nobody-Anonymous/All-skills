# OpenClaw harness

OpenClaw is one of the 12 agent harnesses this repository installs into.

## Skills

`skills/` here is a **generated link** to the canonical harness source
(`.agents/skills/`), created per machine:

```bash
python scripts/setup_tools.py            # link every harness, including this one
python scripts/setup_tools.py --status   # show link state per harness
```

It is excluded from git (`.gitignore`) because it duplicates the whole skill
library; the tracked source of truth is `.agents/skills/`.

## MCP connectors

```bash
allskills mcp install --harness openclaw --profile standard
```

## Evidence level

`compatibility/matrix.json` records this harness as configured + discoverable
(verified automatically). Invocable and workflow-completed stay empty until
someone records a manual check — see `docs/COMPATIBILITY.md`.
