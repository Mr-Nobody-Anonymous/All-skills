# Skill Dependencies

_Generated: 2026-09-02T04:38:48+00:00_

**Total skills:** 64
**Skills with declared dependencies:** 6
**Skills with no dependencies:** 58

## Policy

Per master prompt §14, dependencies are tracked but **not auto-installed**.
Each skill that uses optional tooling lists its dependency here so the user
can install on demand.

Built-in capabilities (no install required):
- Python 3.10+ standard library
- The `src/skills/` loader/registry/router/validator library
- The `scripts/skills/skills.py` CLI

## Dependency Tally

| Dependency | Skill Count |
|---|---:|
| `git` | 3 |
| `gh-cli-optional` | 1 |
| `optional:playwright-or-cypress` | 1 |
| `optional:playwright-or-similar` | 1 |
| `python-or-node` | 1 |

## Per-Skill Status

| Skill | Dependency | Required/Optional | Installation command | Platform | Status |
|---|---|---|---|---|---|
| `design.branding` | — | built-in | — | all | available |
| `design.frontend-design` | — | built-in | — | all | available |
| `design.presentations` | — | built-in | — | all | available |
| `design.ui-ux` | — | built-in | — | all | available |
| `development.architecture` | — | built-in | — | all | available |
| `development.backend` | — | built-in | — | all | available |
| `development.brainstorming` | — | built-in | — | all | available |
| `development.code-review` | — | built-in | — | all | available |
| `development.coding` | — | built-in | — | all | available |
| `development.databases` | — | built-in | — | all | available |
| `development.debugging` | — | built-in | — | all | available |
| `development.devops` | — | built-in | — | all | available |
| `development.frontend` | — | built-in | — | all | available |
| `development.git` | `git` | required | Install Git from https://git-scm.com/downloads | all | available |
| `development.git-worktrees` | `git` | required | Install Git from https://git-scm.com/downloads | all | available |
| `development.github` | `git` | required | Install Git from https://git-scm.com/downloads | all | available |
| `development.github` | `gh-cli-optional` | optional | Install GitHub CLI from https://cli.github.com/ | all | available |
| `development.mcp-builder` | `python-or-node` | required | Install `python` per vendor documentation or Install `node` per vendor documentation | all | available |
| `development.mcp-server-development` | — | built-in | — | all | available |
| `development.performance-optimization` | — | built-in | — | all | available |
| `development.receiving-code-review` | — | built-in | — | all | available |
| `development.refactoring` | — | built-in | — | all | available |
| `development.requesting-code-review` | — | built-in | — | all | available |
| `development.tdd` | — | built-in | — | all | available |
| `development.testing` | — | built-in | — | all | available |
| `development.verification-before-completion` | — | built-in | — | all | available |
| `documents.csv` | — | built-in | — | all | available |
| `documents.docx` | — | built-in | — | all | available |
| `documents.markdown` | — | built-in | — | all | available |
| `documents.pdf` | — | built-in | — | all | available |
| `documents.pptx` | — | built-in | — | all | available |
| `documents.xlsx` | — | built-in | — | all | available |
| `productivity.adhd` | — | built-in | — | all | available |
| `productivity.brainstorming` | — | built-in | — | all | available |
| `productivity.focus` | — | built-in | — | all | available |
| `productivity.planning` | — | built-in | — | all | available |
| `productivity.prioritization` | — | built-in | — | all | available |
| `productivity.task-decomposition` | — | built-in | — | all | available |
| `productivity.time-management` | — | built-in | — | all | available |
| `productivity.unlazy` | — | built-in | — | all | available |
| `research.academic-research` | — | built-in | — | all | available |
| `research.competitive-analysis` | — | built-in | — | all | available |
| `research.data-analysis` | — | built-in | — | all | available |
| `research.deep-research` | — | built-in | — | all | available |
| `research.fact-checking` | — | built-in | — | all | available |
| `research.source-verification` | — | built-in | — | all | available |
| `research.web-research` | — | built-in | — | all | available |
| `security.dependency-audit` | — | built-in | — | all | available |
| `security.prompt-injection-defense` | — | built-in | — | all | available |
| `security.secret-detection` | — | built-in | — | all | available |
| `security.secure-coding` | — | built-in | — | all | available |
| `utilities.automation` | — | built-in | — | all | available |
| `utilities.documentation` | — | built-in | — | all | available |
| `utilities.file-management` | — | built-in | — | all | available |
| `utilities.image` | — | built-in | — | all | available |
| `utilities.parallel-agents` | — | built-in | — | all | available |
| `utilities.summarization` | — | built-in | — | all | available |
| `utilities.text-processing` | — | built-in | — | all | available |
| `utilities.writing` | — | built-in | — | all | available |
| `web.accessibility` | — | built-in | — | all | available |
| `web.browser-automation` | `optional:playwright-or-similar` | optional | npm install --save-dev playwright or Install a supported browser automation tool | all | missing |
| `web.seo` | — | built-in | — | all | available |
| `web.web-extraction` | — | built-in | — | all | available |
| `web.web-scraping` | — | built-in | — | all | available |
| `web.website-testing` | `optional:playwright-or-cypress` | optional | npm install --save-dev playwright or npm install --save-dev cypress | all | missing |
