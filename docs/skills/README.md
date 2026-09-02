# Skills Documentation

Per-category reference for the agent skills library.

## Index

- [ARCHITECTURE.md](ARCHITECTURE.md) — layered router, lifecycle, quality, chains, load-on-demand
- [productivity.md](productivity.md) — ADHD, focus, anti-procrastination, planning, prioritization
- [development.md](development.md) — coding, debugging, refactoring, code review, testing, Git/GitHub
- [research.md](research.md) — web research, deep research, fact checking, source verification
- [web.md](web.md) — browser automation, scraping, web extraction, SEO, accessibility
- [documents.md](documents.md) — PDF, DOCX, XLSX, PPTX, Markdown, CSV
- [design.md](design.md) — UI/UX, frontend design, presentations, branding
- [security-category.md](security-category.md) — secure coding, dependency audit, secret detection, prompt-injection defense
- [utilities.md](utilities.md) — file management, text processing, automation, documentation, writing
- [SECURITY.md](SECURITY.md) — security policy and import pipeline for the skills library
- [SOURCE_AUDIT.md](SOURCE_AUDIT.md) — upstream selection, exclusions, pins, and audit findings

## How skills are structured

Each skill lives at `skills/<category>/<skill-name>/` and contains at minimum:

- `SKILL.md` — the frontmatter + body that the agent reads
- `README.md` — human-facing overview
- `scripts/`, `references/`, `examples/`, `assets/` (as needed)

`SKILL.md` frontmatter is parsed by `src/skills/frontmatter.py` and validated by
`src/skills/validator.py`. Required keys: `name`, `description`, `category`, and `version`; the standard body sections and `README.md` are also enforced.

## How to add a new skill

1. Create `skills/<category>/<skill-name>/SKILL.md` with the required frontmatter.
2. Optionally add a `README.md`, scripts, or examples.
3. Add optional machine-readable metadata to the frontmatter:
   - `capabilities`, `inputs`, `outputs` — what the skill can actually do
   - `permissions:` — `filesystem` / `network` / `shell` / `secrets` (least privilege)
   - `compatibility:` — `generic`, `cline`, `claude_code`, `codex`, `cursor`,
     `opencode`, `gemini_cli`
   - `lifecycle:` — `discovered | imported | validated | security_scanned |
     ready | enabled | disabled | quarantined | deprecated`
4. Register the skill in `skills/registry.json` with id, category, description,
   path, aliases, triggers, keywords, source, risk, and version. To backfill
   registry fields + quality scores automatically, run
   `python scripts/refresh_registry.py`.
5. Run `python scripts/skills/skills.py validate` to catch missing fields.
6. Run `python scripts/skills/skills.py test` to run the test suite.
7. Run `python scripts/generate_registry_docs.py` to refresh
   `skills/registry.md`, `skills/SOURCES.json`, and `skills/DEPENDENCIES.md`.

## How to invoke a skill

The router (`src/skills/router.py`) maps natural language to skill IDs using
**layered scoring** (see [ARCHITECTURE.md](ARCHITECTURE.md)):

```bash
python scripts/skills/skills.py route "I'm procrastinating"
python scripts/skills/skills.py explain "I'm procrastinating"   # per-signal breakdown
python scripts/skills/skills.py chain deep-research --dry-run   # named workflow
```

Scoring signals: exact ID → alias → category → trigger phrase → keyword overlap
→ capability/input/output vocabulary → token overlap → dependency availability
penalty → quality-score boost.
