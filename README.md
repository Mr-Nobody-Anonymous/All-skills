# Agent Skills Library

A dependency-light Python registry, natural-language router, validator, updater, and CLI for 62 modular skills following the open Agent Skills standard.

## Quick Start

```bash
# List skills
python scripts/skills/skills.py list

# Search
python scripts/skills/skills.py search productivity

# Get info
python scripts/skills/skills.py info productivity.unlazy

# Route a natural-language request or a composed chain
python scripts/skills/skills.py route "I'm procrastinating"
python scripts/skills/skills.py route --chain "I have a huge project and I'm procrastinating"

# Check upstream pins without applying changes
python scripts/skills/skills.py update

# Run diagnostics
python scripts/skills/skills.py doctor

# Run tests
python scripts/skills/skills.py test
```

## Structure

- `skills/` — All skill implementations organized by category
- `docs/skills/` — Per-category documentation
- `tests/skill_tests/` — Validation, loading, dependency, provenance, and routing tests
- `scripts/skills/` — CLI tools
- `src/skills/` — Skill router, registry, and loader library

## Key Files

- `SKILLS.md` — Library overview and quick start
- `skills/registry.json` — Machine-readable skill index
- `skills/registry.md` — Human-readable skill index
- `skills/SOURCES.json` — Source attribution for imported skills
- `skills/DEPENDENCIES.md` — Dependency tracking

## License

Each skill retains its original license. See `skills/SOURCES.json` for attribution.