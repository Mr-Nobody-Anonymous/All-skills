# Agent Skills Index

Master directory of all 50 Agent Skills with descriptions, categories, and trigger conditions.
Last updated: 2026-09-02

---

## Table of Contents

- [Verification & Gates](#verification--gates) (8 skills)
- [ADHD & Productivity](#adhd--productivity) (7 skills)
- [Coding & DevOps](#coding--devops) (10 skills)
- [Browser & Web](#browser--web) (5 skills)
- [Communication](#communication) (6 skills)
- [Media & Utilities](#media--utilities) (14 skills)

---

## Verification & Gates (8 skills)

| Skill | Description | Triggers |
|-------|-------------|----------|
| **autoreview** | Run an explicitly requested structured second-model code review. | Review this code, Run code review |
| **behavior-validator** | Validate user-visible behavior against a written contract. | Test behavior, Validate requirements |
| **agent-transcript** | Create a redacted, consent-gated agent transcript. | Create transcript, Export session |
| **crabbox** | Coordinate isolated remote validation with credential boundaries. | Remote validation, Clean machine test |
| **handoff** | Prepare a portable context-rich handoff prompt. | Handoff, Transfer context |
| **readme-standard** | Write concise READMEs with executable examples. | Write README, Create docs |
| **beam** | Publish a redacted coding-session snapshot. | Publish snapshot, Share session |
| **unlazy** | Transform overwhelming tasks into one frictionless step. | Start this task, Too big |

---

## ADHD & Productivity (7 skills)

| Skill | Description | Triggers |
|-------|-------------|----------|
| **adhd-task-breakdown** | Turn overwhelming work into actionable steps. | Break this down, Where to start |
| **obsidian-sync** | Sync Obsidian vault with working directory. | Sync Obsidian, Vault sync |
| **context-summarize** | Compress context into decisions and next actions. | Summarize context, Compress this |
| **time-blocking** | Build realistic deep-work time blocks. | Time block, Schedule focus |
| **daily-journal** | Create a concise daily journal. | Journal, Daily reflection |
| **focus-guard** | Protect a focus session from distractions. | Focus mode, Deep work |
| **voice-to-action** | Convert voice notes into tasks. | Voice note, Parse voice |

---

## Coding & DevOps (10 skills)

| Skill | Description | Triggers |
|-------|-------------|----------|
| **coding-agent** | Run headless coding agent as background process. | Run coding agent, Use Codex |
| **cursor-agent** | Drive Cursor CLI with tmux session control. | Use Cursor, Cursor task |
| **github-cli** | Interact with GitHub using gh CLI. | GitHub CLI, gh command |
| **dokploy** | Manage Dokploy deployments via API. | Dokploy, Deploy management |
| **frontend-design** | Build distinctive, production-grade frontend interfaces. | Frontend design, UI build |
| **remotion-best-practices** | Programmatic video generation in React with Remotion. | Remotion, React video |
| **git-workflow** | Commit and PR automation with conventional messages. | Commit this, Open PR |
| **summarize-repo** | Produce a navigable map of a whole repository. | Summarize repo, Map codebase |
| **npm-auditor** | Audit `node_modules` for vulnerabilities, outdated deps, license issues. | npm audit, Check deps |
| **docker-manager** | Manage Docker containers, images, networks, volumes. | Docker status, Restart container |


---

## Browser & Web (5 skills)

| Skill | Description | Triggers |
|-------|-------------|----------|
| **agent-browser** | Operate headless browser for navigation and extraction. | Navigate URL, Screenshot, Extract data |
| **web-scraper** | Extract public web data with rate limits. | Scrape webpage, Extract data |
| **form-filler** | Fill web forms with user approval. | Fill form, Submit application |
| **search-synthesizer** | Search web and synthesize cited answers. | Search, Research topic |
| **media-downloader** | Download authorized public media. | Download video, Save audio |

---

## Communication (6 skills)

| Skill | Description | Triggers |
|-------|-------------|----------|
| **telegram-actions** | Draft and send Telegram messages. | Send Telegram, Post to Telegram |
| **whatsapp-router** | Classify and route WhatsApp messages. | Route WhatsApp, Categorize message |
| **email-inbox-zero** | Triage email into action queues. | Triage emails, Process inbox |
| **slack-synthesizer** | Summarize Slack threads into decisions. | Summarize Slack, Extract actions |
| **calendar-assistant** | Plan events with conflict detection. | Schedule meeting, Find time |
| **meeting-action-extractor** | Extract decisions and action items from meetings. | Extract actions, Meeting summary |

---

## Media & Utilities (14 skills)

| Skill | Description | Triggers |
|-------|-------------|----------|
| **veo-video-generator** | Generate Google Veo videos from prompts. | Generate video, AI video |
| **image-gen** | Create AI image generation prompts. | Generate image, Create art |
| **audio-transcribe** | Transcribe audio to timestamped text. | Transcribe audio, Speech to text |
| **avatar-creator** | Design consistent avatars across formats. | Create avatar, Profile image |
| **system-monitor** | Inspect system telemetry and anomalies. | System status, Server metrics |
| **cmd-safety-check** | Classify commands by risk level. | Command safety, Risk check |
| **cf-worker-deploy** | Deploy Cloudflare Workers with safeguards. | Deploy to Cloudflare, Publish worker |
| **db-inspector** | Inspect database schemas read-only. | Check schema, Run query |
| **api-mock-generator** | Generate API mocks from schemas. | Generate mocks, Mock API |
| **weather-now** | Get current weather and forecasts. | Weather, Forecast |
| **sonos-cli** | Control Sonos playback. | Control Sonos, Play music |
| **expense-parser** | Extract data from receipts and invoices. | Parse receipt, Extract expense |
| **unit-converter** | Convert units and currencies. | Convert units, Currency conversion |
| **security-scanner** | Gate releases with security checks. | Security scan, Vulnerability check |

---

## Quick Reference

| Category | Count |
|----------|-------|
| Verification & Gates | 8 |
| ADHD & Productivity | 7 |
| Coding & DevOps | 10 |
| Browser & Web | 5 |
| Communication | 6 |
| Media & Utilities | 14 |
| **Total** | **50** |

---

## Usage

1. **Find a Skill**: Browse by category or search (`Ctrl+F`)
2. **Check Triggers**: Each skill lists common phrases that activate it
3. **Read SKILL.md**: Each skill directory contains detailed specifications
4. **Run Symlink**: Execute `symlink_skills.sh` to attach all skills to your agent

## Skill Metadata Format

```yaml
---
name: skill-name
description: Brief description
category: category-name
aliases: [alias1, alias2]
triggers:
  - trigger phrase
keywords: [keyword1, keyword2]
required_tools: [tool1, tool2]
risk: low|medium|high
version: 1.0.0
source: source-name
enabled: true
---
```

---

## Provenance

The task brief listed source URLs for each of the 50 skills. After verification
on 2026-09-02:

- **7 skills are unmodified upstream sources** from
  `https://github.com/openclaw/agent-skills/tree/main/skills/`: `agent-transcript`,
  `autoreview`, `beam`, `behavior-validator`, `crabbox`, `handoff`,
  `readme-standard`. Their source-of-truth lives upstream; updates should be
  synced from there via `robocopy` or `cp -r`.
- **1 skill (`unlazy`)** has no upstream source: the task's URL
  `https://github.com/steipete/unlazy` returns `Repository not found`
  (`git ls-remote` → `404 not found`). The `SKILL.md` is a scaffold written
  from the skill name's intent.
- **42 skills** were listed in the task brief under
  `https://github.com/openclaw/clawhub` (skill: `<name>`). The live clawhub
  repository **does not contain these skill names** — its real `.agents/skills/`
  directory holds `autoreview`, `axiom-sre`, `writing-evals`, `convex-*`, etc.
  The 42 `SKILL.md` files are scaffolds written from the skill name's intent,
  with a clear `source: openclawskills.net` field in their frontmatter
  (the original brief listed `https://openclawskills.net/` as their source;
  that site is reachable but renders a marketing landing page with no
  downloadable skill files).
- All scaffolded skills carry a `metadata.openclaw` block so they parse
  cleanly on OpenClaw, in addition to their existing `required_tools`,
  `triggers`, and `risk` fields which are supported by Claude Code, Cursor,
  and Codex.

When updating a **canonical** skill (the 7 from `openclaw/agent-skills`),
re-pull from upstream rather than editing in place. When updating a
**scaffolded** skill, edit its `SKILL.md` directly and replace the body
with real source content; keep the frontmatter name, description, and
`metadata.openclaw` block intact so routing keeps working.

---

Generated by Agent Skills Setup System
Last verified: 2026-09-02
