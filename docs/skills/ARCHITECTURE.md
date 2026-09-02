# Architecture — load-on-demand skill platform

This document describes how the library routes, selects, and loads skills so
that the **model never receives all ~64 skills at once**. Only the chosen skill
(and its declared references/scripts) is loaded.

```
                 AGENT
                   |
                   v
             SKILL DISCOVERY      list / search / categories
                   |
                   v
             SKILL ROUTER         layered scoring (route / explain)
                   |
        +----------+-----------+
        v                      v
  candidate skills       candidate chains   (chains.json)
        |                      |
        +----------+-----------+
                   v
             BEST MATCH          quality + permissions + dependencies + safety
                   |
                   v
             LOAD SKILL          Loader.load(skill_id) — one SKILL.md body
                   |
                   v
          references/scripts      pulled in only if needed
```

## Layered router (`src/skills/router.py`)

Each layer accumulates score instead of short-circuiting:

| Layer | Signal | Max |
|---|---|---|
| 1 | Exact skill ID | 100 |
| 2 | Alias exact match | 90 |
| 3 | Category match | 80 |
| 4 | Trigger phrase substring (longer = higher) | +100 |
| 5 | Keyword overlap (fraction hit) | +40 |
| 6 | Capability / input / output vocabulary | +15 |
| 7 | Token overlap (stopword-filtered) | +25 |
| 8 | Dependency availability | penalty |
| 9 | Quality-score boost | +4 |

`route()` returns `RouteMatch`; `explain()` returns `RouteBreakdown` with the
per-signal numbers so routing decisions are debuggable:

```bash
python scripts/skills/skills.py explain "I'm procrastinating on a big project"
```

## Load-on-demand

- The **registry** is metadata only (id, description, aliases, triggers,
  keywords, dependencies, risk, lifecycle, quality). Loading the registry does
  not read skill bodies.
- `Registry.load()` merges a JSON index with on-disk `SKILL.md` discovery; the
  full file contents are never loaded.
- `Loader.load(skill_id)` reads **one** `SKILL.md` body on demand and returns
  its file list — the agent pulls in `references/` and `scripts/` only if the
  chosen skill actually needs them.

```bash
python scripts/skills/skills.py load documents.pdf   # only that skill's body
```

## Quality scoring (`src/skills/quality.py`)

Deterministic heuristics (0-10) across six axes — documentation, maintenance,
reliability, security, compatibility, usefulness — stored under `quality` in
`registry.json`. The router adds a small boost for high-quality skills so a
maintained, documented, low-risk skill beats a sparse one with the same
keywords.

```bash
python scripts/skills/skills.py quality              # full ranking
python scripts/skills/skills.py quality documents.pdf
```

## Lifecycle (`src/skills/lifecycle.py`)

Every skill carries a lifecycle state:

```
DISCOVERED -> IMPORTED -> VALIDATED -> SECURITY_SCANNED -> READY -> ENABLED
                                                              -> DISABLED
                                                              -> QUARANTINED
                                                              -> DEPRECATED
```

Invalid transitions are rejected (state machine in `lifecycle.py`), and the
validator flags illegal states:

```bash
python scripts/skills/skills.py lifecycle productivity.unlazy
python scripts/skills/skills.py lifecycle productivity.unlazy disabled
```

## Dependencies (`src/skills/dependencies.py` + `skills/dependencies.json`)

Machine-readable per-skill dependency data: required/optional × system/python/api
plus what is currently missing on this host. The Markdown `DEPENDENCIES.md`
stays for humans; the JSON is for agents.

## Chains (`skills/chains.json`)

Named deterministic workflows (e.g. `deep-research`) resolved against the live
registry:

```bash
python scripts/skills/skills.py chain deep-research --dry-run
```

## Conflicts (`skills/conflicts.json`)

Declared pairwise conflicts (severity `info|warn|error`, a priority winner).
The validator reports active conflicts; `doctor` lists them.

## Permissions

Skills may declare least-privilege metadata in frontmatter:

```yaml
permissions:
  filesystem: read
  network: none
  shell: none
  secrets: none
```

Enforcement itself belongs to the agent runtime; the library validates and
surfaces the declaration (`chain --dry-run` prints a permission summary).

## Security

Static-only inspection (`src/skills/security.py`) with severity-graded patterns.
Nothing is ever executed. High-severity findings are validation errors; the CI
gate is `skills.py scan`. See [SECURITY.md](SECURITY.md) for the import pipeline.

## CLI surface

```bash
python scripts/skills/skills.py list|search|info|route|explain|chain
python scripts/skills/skills.py lifecycle|conflicts|quality|scan|load
python scripts/skills/skills.py validate|test|doctor|export|enable|disable
```