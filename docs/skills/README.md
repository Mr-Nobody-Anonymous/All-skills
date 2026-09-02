# Skills Documentation

Per-category reference for the agent skills library.

## Index

- [productivity.md](productivity.md) — ADHD, focus, anti-procrastination, planning, prioritization
- [development.md](development.md) — coding, debugging, refactoring, code review, testing, Git/GitHub
- [research.md](research.md) — web research, deep research, fact checking, source verification
- [web.md](web.md) — browser automation, scraping, web extraction, SEO, accessibility
- [documents.md](documents.md) — PDF, DOCX, XLSX, PPTX, Markdown, CSV
- [design.md](design.md) — UI/UX, frontend design, presentations, branding
- [security-category.md](security-category.md) — secure coding, dependency audit, secret detection, prompt-injection defense
- [utilities.md](utilities.md) — file management, text processing, automation, documentation, writing
- [SECURITY.md](SECURITY.md) — security policy for the skills library
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
3. Register the skill in `skills/registry.json` with id, category, description,
   path, aliases, triggers, keywords, source, risk, and version.
4. Run `python scripts/skills/skills.py validate` to catch missing fields.
5. Run `python scripts/skills/skills.py test` to run the test suite.
6. Run `python scripts/generate_registry_docs.py` to refresh
   `skills/registry.md`, `skills/SOURCES.json`, and `skills/DEPENDENCIES.md`.

## How to invoke a skill

The router (`src/skills/router.py`) maps natural language to skill IDs:

```bash
python scripts/skills/skills.py route "I'm procrastinating on my homework"
# 1. productivity.unlazy (score=..., matched_on=trigger)
# 2. productivity.task-decomposition
# 3. productivity.planning
```

The router scores on (in order): exact ID, alias, trigger phrase, keyword, and
token overlap with stopword filtering.
