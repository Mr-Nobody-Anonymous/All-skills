# Skill Dependencies

_Generated: 2026-09-19T17:23:17+00:00_

**Total skills:** 116
**Skills with declared dependencies:** 44
**Skills with no dependencies:** 72

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
| `git` | 4 |
| `optional:node` | 3 |
| `optional:codex-or-claude-cli` | 2 |
| `optional:gh` | 2 |
| `optional:image-generator` | 2 |
| `gh-cli-optional` | 1 |
| `optional:BEAM_ACCESS_TOKEN` | 1 |
| `optional:DOKPLOY_API_KEY` | 1 |
| `optional:GOOGLE_API_KEY` | 1 |
| `optional:TELEGRAM_BOT_TOKEN` | 1 |
| `optional:agent-browser` | 1 |
| `optional:browser-automation` | 1 |
| `optional:calendar-access` | 1 |
| `optional:clipboard-tool` | 1 |
| `optional:crabbox` | 1 |
| `optional:cursor-agent` | 1 |
| `optional:database-client` | 1 |
| `optional:docker` | 1 |
| `optional:email-access` | 1 |
| `optional:exchange-rate-source` | 1 |
| `optional:http-client` | 1 |
| `optional:media-downloader` | 1 |
| `optional:npm` | 1 |
| `optional:obsidian` | 1 |
| `optional:ocr` | 1 |
| `optional:playwright-or-cypress` | 1 |
| `optional:playwright-or-similar` | 1 |
| `optional:remotion` | 1 |
| `optional:security-scanners` | 1 |
| `optional:slack-access` | 1 |
| `optional:sonos-cli` | 1 |
| `optional:system-tools` | 1 |
| `optional:test-framework` | 1 |
| `optional:transcript` | 1 |
| `optional:transcription-engine` | 1 |
| `optional:weather-api` | 1 |
| `optional:web-search` | 1 |
| `optional:whatsapp-api` | 1 |
| `optional:wrangler` | 1 |
| `python-or-node` | 1 |

## Per-Skill Status

| Skill | Dependency | Required/Optional | Installation command | Platform | Status |
|---|---|---|---|---|---|
| `design.avatar-creator` | `optional:image-generator` | optional | Install `image-generator` per vendor documentation | all | missing |
| `design.branding` | — | built-in | — | all | available |
| `design.frontend-design` | — | built-in | — | all | available |
| `design.image-gen` | `optional:image-generator` | optional | Install `image-generator` per vendor documentation | all | missing |
| `design.presentations` | — | built-in | — | all | available |
| `design.remotion-best-practices` | `optional:node` | optional | Install `node` per vendor documentation | all | available |
| `design.remotion-best-practices` | `optional:remotion` | optional | Install `remotion` per vendor documentation | all | missing |
| `design.ui-ux` | — | built-in | — | all | available |
| `design.veo-video-generator` | `optional:GOOGLE_API_KEY` | optional | Install `GOOGLE_API_KEY` per vendor documentation | all | missing |
| `development.api-mock-generator` | `optional:test-framework` | optional | Install `test-framework` per vendor documentation | all | missing |
| `development.architecture` | — | built-in | — | all | available |
| `development.autoreview` | `optional:codex-or-claude-cli` | optional | Install `codex` per vendor documentation or Install `claude-cli` per vendor documentation | all | missing |
| `development.backend` | — | built-in | — | all | available |
| `development.behavior-validator` | — | built-in | — | all | available |
| `development.brainstorming` | — | built-in | — | all | available |
| `development.cf-worker-deploy` | `optional:wrangler` | optional | Install `wrangler` per vendor documentation | all | missing |
| `development.code-review` | — | built-in | — | all | available |
| `development.coding` | — | built-in | — | all | available |
| `development.coding-agent` | `optional:codex-or-claude-cli` | optional | Install `codex` per vendor documentation or Install `claude-cli` per vendor documentation | all | missing |
| `development.crabbox` | `optional:crabbox` | optional | Install `crabbox` per vendor documentation | all | missing |
| `development.cursor-agent` | `optional:cursor-agent` | optional | Install `cursor-agent` per vendor documentation | all | missing |
| `development.databases` | — | built-in | — | all | available |
| `development.db-inspector` | `optional:database-client` | optional | Install `database-client` per vendor documentation | all | missing |
| `development.debugging` | — | built-in | — | all | available |
| `development.devops` | — | built-in | — | all | available |
| `development.docker-manager` | `optional:docker` | optional | Install `docker` per vendor documentation | all | available |
| `development.dokploy` | `optional:DOKPLOY_API_KEY` | optional | Install `DOKPLOY_API_KEY` per vendor documentation | all | missing |
| `development.frontend` | — | built-in | — | all | available |
| `development.git` | `git` | required | Install Git from https://git-scm.com/downloads | all | available |
| `development.git-workflow` | `git` | required | Install Git from https://git-scm.com/downloads | all | available |
| `development.git-worktrees` | `git` | required | Install Git from https://git-scm.com/downloads | all | available |
| `development.github` | `git` | required | Install Git from https://git-scm.com/downloads | all | available |
| `development.github` | `gh-cli-optional` | optional | Install GitHub CLI from https://cli.github.com/ | all | available |
| `development.github-cli` | `optional:gh` | optional | Install `gh` per vendor documentation | all | available |
| `development.mcp-builder` | `python-or-node` | required | Install `python` per vendor documentation or Install `node` per vendor documentation | all | available |
| `development.mcp-server-development` | — | built-in | — | all | available |
| `development.performance-optimization` | — | built-in | — | all | available |
| `development.receiving-code-review` | — | built-in | — | all | available |
| `development.refactoring` | — | built-in | — | all | available |
| `development.requesting-code-review` | — | built-in | — | all | available |
| `development.summarize-repo` | — | built-in | — | all | available |
| `development.tdd` | — | built-in | — | all | available |
| `development.testing` | — | built-in | — | all | available |
| `development.verification-before-completion` | — | built-in | — | all | available |
| `documents.csv` | — | built-in | — | all | available |
| `documents.docx` | — | built-in | — | all | available |
| `documents.expense-parser` | `optional:ocr` | optional | Install `ocr` per vendor documentation | all | missing |
| `documents.markdown` | — | built-in | — | all | available |
| `documents.pdf` | — | built-in | — | all | available |
| `documents.pptx` | — | built-in | — | all | available |
| `documents.xlsx` | — | built-in | — | all | available |
| `productivity.adhd` | — | built-in | — | all | available |
| `productivity.adhd-divergent-brainstorm` | — | built-in | — | all | available |
| `productivity.adhd-output-style` | — | built-in | — | all | available |
| `productivity.adhd-task-breakdown` | — | built-in | — | all | available |
| `productivity.brainstorming` | — | built-in | — | all | available |
| `productivity.calendar-assistant` | `optional:calendar-access` | optional | Install `calendar-access` per vendor documentation | all | missing |
| `productivity.context-summarize` | — | built-in | — | all | available |
| `productivity.daily-journal` | — | built-in | — | all | available |
| `productivity.email-inbox-zero` | `optional:email-access` | optional | Install `email-access` per vendor documentation | all | missing |
| `productivity.executive-summary` | — | built-in | — | all | available |
| `productivity.first-principles-reasoning` | — | built-in | — | all | available |
| `productivity.focus` | — | built-in | — | all | available |
| `productivity.focus-guard` | — | built-in | — | all | available |
| `productivity.meeting-action-extractor` | — | built-in | — | all | available |
| `productivity.obsidian-sync` | `optional:obsidian` | optional | Install `obsidian` per vendor documentation | all | missing |
| `productivity.planning` | — | built-in | — | all | available |
| `productivity.prioritization` | — | built-in | — | all | available |
| `productivity.task-decomposition` | — | built-in | — | all | available |
| `productivity.time-blocking` | — | built-in | — | all | available |
| `productivity.time-management` | — | built-in | — | all | available |
| `productivity.unlazy` | — | built-in | — | all | available |
| `productivity.voice-to-action` | `optional:transcript` | optional | Install `transcript` per vendor documentation | all | missing |
| `research.academic-research` | — | built-in | — | all | available |
| `research.competitive-analysis` | — | built-in | — | all | available |
| `research.data-analysis` | — | built-in | — | all | available |
| `research.deep-research` | — | built-in | — | all | available |
| `research.fact-checking` | — | built-in | — | all | available |
| `research.search-synthesizer` | `optional:web-search` | optional | Install `web-search` per vendor documentation | all | missing |
| `research.source-verification` | — | built-in | — | all | available |
| `research.web-research` | — | built-in | — | all | available |
| `security.cmd-safety-check` | — | built-in | — | all | available |
| `security.dependency-audit` | — | built-in | — | all | available |
| `security.npm-auditor` | `optional:npm` | optional | Install `npm` per vendor documentation | all | available |
| `security.prompt-injection-defense` | — | built-in | — | all | available |
| `security.secret-detection` | — | built-in | — | all | available |
| `security.secure-coding` | — | built-in | — | all | available |
| `security.security-scanner` | `optional:security-scanners` | optional | Install `security-scanners` per vendor documentation | all | missing |
| `utilities.agent-transcript` | `optional:node` | optional | Install `node` per vendor documentation | all | available |
| `utilities.agent-transcript` | `optional:gh` | optional | Install `gh` per vendor documentation | all | available |
| `utilities.audio-transcribe` | `optional:transcription-engine` | optional | Install `transcription-engine` per vendor documentation | all | missing |
| `utilities.automation` | — | built-in | — | all | available |
| `utilities.beam` | `optional:node` | optional | Install `node` per vendor documentation | all | available |
| `utilities.beam` | `optional:BEAM_ACCESS_TOKEN` | optional | Install `BEAM_ACCESS_TOKEN` per vendor documentation | all | missing |
| `utilities.documentation` | — | built-in | — | all | available |
| `utilities.file-management` | — | built-in | — | all | available |
| `utilities.handoff` | `optional:clipboard-tool` | optional | Install `clipboard-tool` per vendor documentation | all | missing |
| `utilities.image` | — | built-in | — | all | available |
| `utilities.parallel-agents` | — | built-in | — | all | available |
| `utilities.readme-standard` | — | built-in | — | all | available |
| `utilities.slack-synthesizer` | `optional:slack-access` | optional | Install `slack-access` per vendor documentation | all | missing |
| `utilities.sonos-cli` | `optional:sonos-cli` | optional | Install `sonos-cli` per vendor documentation | all | missing |
| `utilities.summarization` | — | built-in | — | all | available |
| `utilities.system-monitor` | `optional:system-tools` | optional | Install `system-tools` per vendor documentation | all | missing |
| `utilities.telegram-actions` | `optional:TELEGRAM_BOT_TOKEN` | optional | Install `TELEGRAM_BOT_TOKEN` per vendor documentation | all | missing |
| `utilities.text-processing` | — | built-in | — | all | available |
| `utilities.unit-converter` | `optional:exchange-rate-source` | optional | Install `exchange-rate-source` per vendor documentation | all | missing |
| `utilities.weather-now` | `optional:weather-api` | optional | Install `weather-api` per vendor documentation | all | missing |
| `utilities.whatsapp-router` | `optional:whatsapp-api` | optional | Install `whatsapp-api` per vendor documentation | all | missing |
| `utilities.writing` | — | built-in | — | all | available |
| `web.accessibility` | — | built-in | — | all | available |
| `web.agent-browser` | `optional:agent-browser` | optional | Install `agent-browser` per vendor documentation | all | missing |
| `web.browser-automation` | `optional:playwright-or-similar` | optional | npm install --save-dev playwright or Install a supported browser automation tool | all | missing |
| `web.form-filler` | `optional:browser-automation` | optional | Install `browser-automation` per vendor documentation | all | missing |
| `web.media-downloader` | `optional:media-downloader` | optional | Install `media-downloader` per vendor documentation | all | missing |
| `web.seo` | — | built-in | — | all | available |
| `web.web-extraction` | — | built-in | — | all | available |
| `web.web-scraper` | `optional:http-client` | optional | Install `http-client` per vendor documentation | all | missing |
| `web.web-scraping` | — | built-in | — | all | available |
| `web.website-testing` | `optional:playwright-or-cypress` | optional | npm install --save-dev playwright or npm install --save-dev cypress | all | missing |
