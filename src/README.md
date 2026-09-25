# `src/` — the `skills` Python package

The installable core of All-Skills (distribution name **`all-skills`**, import name
**`skills`**). It provides the registry, router, policy engine, execution runtime,
validator and security scanner used by the CLI and every CI gate.

## How to run

```bash
python -m pip install -e ".[dev]"    # from the repository root
all-skills --help                    # console entry point → skills.cli:main

# Library use. From the repository root the top-level `skills/` data folder
# shadows the package, so put src/ first on the path (tests and scripts do too):
PYTHONPATH=src python -c "from pathlib import Path; from skills import load_registry; print(len(load_registry(Path('.')).entries))"
```

`all-skills` detects a source checkout and runs the full CLI in
`scripts/skills/skills.py`; when installed from a wheel it falls back to a built-in
subset (`list`, `search`, `route`, `execute`, `doctor`, `scan`).

## Modules

| Module | Responsibility |
| :--- | :--- |
| `registry.py` | Loads and queries `skills/registry.json`; trust tiers (T0–T6) |
| `router.py` | Maps natural language to skill IDs with 9-signal layered scoring |
| `policy.py` | Capability-based execution policy and least-privilege secret brokering |
| `runtime.py` | Universal execution runtime with audit logging and revocation checks |
| `security.py` | Read-only static inspection of skill folders, quarantine workflow |
| `validator.py` | Validates `SKILL.md` files, paths, conflicts and basic safety |
| `loader.py` / `frontmatter.py` | Loads skill folders and parses YAML frontmatter (no external deps) |
| `lock.py` | Platform-independent SHA-256 tree hashing, `skills.lock` generation & verification |
| `graph.py` / `dependencies.py` / `conflicts.py` | Dependency graph, tool checks and declared conflicts |
| `chains.py` | Named, deterministic multi-skill chains (`skills/chains.json`) |
| `quality.py` / `lifecycle.py` | Quality scoring and the 8-state skill lifecycle |
| `updater.py` | Non-destructive upstream change detection |
| `cli.py` / `library.py` | Console entry point and convenience helpers |
| `_version.py` | Package version (kept in sync with `VERSION`, `pyproject.toml`, `package.json`) |

## Quality gates

```bash
ruff check src          # correctness lint (rules in pyproject.toml)
mypy                    # type-checks src/skills (configured in pyproject.toml)
pytest tests --cov      # coverage is measured for src/skills
```
