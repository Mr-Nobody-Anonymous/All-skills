---
name: daily-journal
description: Generate a daily journal / reflection template with prompts, then convert the user's freeform notes into a structured entry with gratitude, wins, lessons, intentions.
category: adhd_and_productivity
aliases: [journal, daily, reflection, gratitude, intention, mood]
triggers:
  - Daily journal
  - Reflect on today
  - What did I do today
  - Morning prompt
  - Evening wrap
keywords: [journal, daily, reflection, gratitude, mood, intention, win, lesson, log]
required_tools: []
risk: low
version: 1.0.0
source: openclawskills.net
enabled: true
metadata:
  openclaw:
    requires:
      env: []
      bins: []
    primaryEnv: null
---

# Daily Journal & Reflection

## Purpose

Run a short, structured **daily check-in** that helps the user notice what mattered,
what worked, and what to carry into tomorrow. The skill is intentionally lightweight:
three prompts in, three blocks out, no scoring, no streak pressure.

## When to Use

- The user wants a morning intention prompt
- The user wants an evening wrap-up
- The user wants to start journaling but has no template

## When NOT to Use

- The user is in acute distress (route to support)
- The user wants long-form memoir writing (different skill)

## Capabilities

- Three-mode operation: `morning`, `midday`, `evening`
- Prompts that are open enough to feel easy, specific enough to be useful
- A template that survives a 90-second answer
- Optional append to a vault (see `obsidian-sync`)
- Track wins (â‰¤ 3), friction (â‰¤ 3), one lesson, one intention

## Inputs

- `mode` (morning | midday | evening)
- Optional `append_to` (path to a daily-note file or vault)
- Optional `template` (custom prompts; default is shipped)

## Workflow (morning)

1. **One intention for today** â€” verb phrase, â‰¤ 8 words.
2. **One thing that would make today a win** â€” concrete and small.
3. **One thing to protect** â€” a block of time, a boundary, a habit.

## Workflow (evening)

1. **Three wins** (one line each).
2. **One friction point** (one line).
3. **One lesson** (one line).
4. **One intention for tomorrow** (carries forward).

## Output

A markdown block with today's date, the prompts, and the user's answers. Optional
frontmatter:

```yaml
---
date: 2026-02-09
mode: evening
mood: 6
energy: 7
tags: [daily, journal]
---
```

## Tools

- None required
- Optional: filesystem append, `obsidian-sync`

## Examples

**User:** "Start my morning journal."
**Response:** "1. Intention? 2. Win for today? 3. What will you protect?"

**User:** "Wrap up today."
**Response:** "Wins? Friction? Lesson? Intention for tomorrow?" â€” and writes a
markdown file `daily/2026-02-09.md`.

## Safety

- Never log mood/energy to a third party
- Honor a "private" flag (no write, output only to chat)
- Do not pressure the user to write long answers
- If distress appears, suggest a break and a support contact

## Source

Auto-generated from openclawskills.net description.

## Pairs Well With

- `obsidian-sync` (vault destination)
- `unlazy` (morning kickoff)
- `time-blocking` (carry tomorrow's intention into a calendar block)
