# `skills/` — canonical skill engine

The curated, routed and quality-scored skill library, plus the Python handler
packages of the voice/multimodal OS.

## Layout

| Path | Contents |
| :--- | :--- |
| `<category>/<skill>/SKILL.md` | Canonical skills (frontmatter + instructions) with `README.md`, `examples/`, `references/`, `tests/` |
| `<category>/<skill>/handler.py` | Python handlers used by the voice/multimodal OS (subclass `base_skill.BaseSkill`) |
| `registry.json` | **Generated** index: metadata, trust tier, quality scores, lifecycle state |
| `dependencies.json` | **Generated** dependency index |
| `chains.json` / `conflicts.json` / `policy.json` | Named workflows, declared conflicts, capability policy |
| `SOURCES.json` / `registry.md` / `DEPENDENCIES.md` | Provenance and human-readable registry docs |
| `_quarantine/` | Isolated skills — never routed, validated or executed |

## How to run

```bash
all-skills list                                  # or: python scripts/skills/skills.py list
all-skills route "review my pull request"
python scripts/skills/skills.py validate         # structure & conflict checks
python scripts/skills/skills.py doctor           # lifecycle, quality, conflicts, dependencies
python scripts/skills/skills.py chain code-review-flow --dry-run
```

## Adding or changing a skill

1. Follow the layout and frontmatter rules in [`CONTRIBUTING.md`](../CONTRIBUTING.md).
2. Regenerate the generated files and commit them:

   ```bash
   python scripts/refresh_registry.py
   python scripts/skills/skills.py lock
   python scripts/compute_stats.py && python scripts/generate_readme_stats.py
   ```

3. Run `python scripts/validate_schema.py` and `python scripts/skills/skills.py test`.
