# Agent Skills Library

A dependency-light Python registry, natural-language router, validator, quality
scorer, lifecycle manager, named-chain resolver, and CLI for **64** modular
skills following the open Agent Skills standard.

## Quick Start

```bash
# List skills
python scripts/skills/skills.py list

# Search
python scripts/skills/skills.py search productivity

# Get info (loaded on demand — only this skill's body is read)
python scripts/skills/skills.py info productivity.unlazy
python scripts/skills/skills.py load documents.pdf

# Route a natural-language request or a composed chain
python scripts/skills/skills.py route "I'm procrastinating"
python scripts/skills/skills.py route --chain --dry-run "I have a huge project and I'm procrastinating"

# Explain why a skill was selected (per-signal breakdown)
python scripts/skills/skills.py explain "I'm procrastinating"

# Named deterministic workflows
python scripts/skills/skills.py chain deep-research --dry-run

# Lifecycle, quality, conflicts, static security scan
python scripts/skills/skills.py lifecycle productivity.unlazy
python scripts/skills/skills.py quality
python scripts/skills/skills.py conflicts
python scripts/skills/skills.py scan

# Check upstream pins without applying changes
python scripts/skills/skills.py update

# Run diagnostics
python scripts/skills/skills.py doctor
python scripts/skills/skills.py validate

# Run tests
python scripts/skills/skills.py test
```

## Structure

- `skills/` — All skill implementations organized by category (canonical source)
- `src/skills/` — Router, registry, loader, validator, quality, lifecycle, chains, conflicts, security scanner
- `scripts/` — CLI (`skills.py`), registry refresh, doc generators, import tools
- `docs/skills/` — Per-category docs, architecture, and security policy
- `tests/skill_tests/` — Validation, loading, dependency, provenance, quality, lifecycle, chain, and routing tests
- `.github/workflows/` — validate, test, security, registry, and skill-integrity CI

## Key Files

- `SKILLS.md` — Library overview and quick start
- `skills/registry.json` — Machine-readable skill index (includes lifecycle + quality)
- `skills/registry.md` — Human-readable skill index
- `skills/SOURCES.json` — Source attribution / provenance for imported skills
- `skills/DEPENDENCIES.md` + `skills/dependencies.json` — Human + machine-readable dependency tracking
- `skills/chains.json` — Named deterministic workflows (`deep-research`, `anti-procrastination`, …)
- `skills/conflicts.json` — Declared pairwise skill conflicts

## License

Each skill retains its original license. See `skills/SOURCES.json` for attribution.