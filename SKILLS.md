# Agent Skills Library

A clean, organized, scalable library of **62** independently discoverable skills across eight categories, following the open Agent Skills standard. The library contains 55 local skills and 7 vetted, pinned adaptations from two upstream repositories.

## Quick Start

```bash
# List all skills
python scripts/skills/skills.py list

# Search skills
python scripts/skills/skills.py search productivity

# Get info about a skill
python scripts/skills/skills.py info productivity.unlazy

# Route and include compatible follow-on skills
python scripts/skills/skills.py route --chain --top-k 6 "I am procrastinating on a large project"

# Enable or disable a skill
python scripts/skills/skills.py disable productivity.unlazy
python scripts/skills/skills.py enable productivity.unlazy

# Check pinned upstream commits without changing files
python scripts/skills/skills.py update

# Test and diagnose
python scripts/skills/skills.py test
python scripts/skills/skills.py doctor
```

## Natural Language Invocation

The skill router understands natural language. Examples:

| User says | Activates |
|---|---|
| "I'm procrastinating" | `productivity.unlazy` |
| "Help me focus for 30 minutes" | `productivity.focus` |
| "Break this project into steps" | `productivity.task-decomposition` |
| "I keep getting distracted" | `productivity.adhd` |
| "Review this code" | `development.code-review` |
| "Find bugs in my code" | `development.debugging` |
| "Research this topic" | `research.web-research` |
| "Analyze this PDF" | `documents.pdf` |
| "Check this for security issues" | `security.secure-coding` |

## Library Stats

- **Total skills:** 62
- **Categories:** 8
- **Custom skills:** 55
- **Imported skills:** 7 from 2 pinned repositories
- **Format:** Agent Skills standard (`SKILL.md` + frontmatter)
- **Discovery:** exact IDs, aliases, categories, triggers, keywords, and token matching
- **Composition:** `composes_with` / `suggests_after`, exposed by `route --chain`

## Categories

- **productivity** — ADHD, focus, anti-procrastination, planning, task decomposition
- **development** — Coding, debugging, refactoring, code review, testing, Git/GitHub
- **research** — Web research, deep research, fact checking, data analysis
- **web** — Browser automation, scraping, SEO, accessibility
- **documents** — PDF, DOCX, XLSX, PPTX, Markdown, CSV
- **design** — UI/UX, frontend design, presentations, branding
- **security** — Secure coding, dependency audit, secret detection
- **utilities** — File management, text processing, automation

## Architecture

```
                    ┌──────────────────┐
                    │      AGENT       │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  SKILL ROUTER    │
                    └────────┬─────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
        Productivity     Development     Research
              │              │              │
              ▼              ▼              ▼
           Skills         Skills         Skills
```

## Directory Structure

```
skills/
├── productivity/      # ADHD, focus, planning, unlazy
├── development/       # coding, debugging, testing, git
├── research/          # web research, fact checking
├── web/               # browser automation, scraping
├── documents/         # PDF, DOCX, XLSX, PPTX
├── design/            # UI/UX, presentations
├── security/          # secure coding, auditing
├── utilities/         # general utilities
├── _quarantine/       # suspicious skills held for review
├── registry.json      # skill index
├── registry.md        # human-readable registry
├── SOURCES.json       # source attribution
└── DEPENDENCIES.md    # dependency tracking
```

## Adding a New Skill

1. Create `skills/<category>/<skill-name>/` with `SKILL.md` and `README.md`.
2. Include `name`, `description`, `category`, and `version`, plus all standard body sections.
3. Add aliases, triggers, keywords, dependencies, composition targets, and risk metadata.
4. For imports, preserve `LICENSE`, `references/upstream-SKILL.md`, repository, source path, commit, author, and modification status.
5. Export and regenerate docs: `python scripts/skills/skills.py export`, then run both `scripts/generate_*.py` files.
6. Run `python scripts/skills/skills.py validate`, `test`, and `doctor`.

## Security Policy

- All downloaded skills are security audited before integration
- Suspicious skills go to `skills/_quarantine/`
- Skills are not auto-executed; they require explicit invocation
- Network access, file deletion, and credential access are flagged
- Each skill lists its risk profile in its SKILL.md

See [docs/skills/SECURITY.md](docs/skills/SECURITY.md) for the full policy.