---
name: deep-research
description: Conduct long-horizon, multi-source deep research with synthesis, contradiction handling, and a final report.
category: research
aliases: [deep-dive, long-research, exhaustive-research]
triggers:
  - deep research
  - do a deep dive
  - exhaustive research
  - comprehensive analysis
  - research everything about
keywords: [deep, dive, exhaustive, comprehensive, research, multi-source, report]
dependencies: []
risk: low
version: 1.0.0
source: custom
enabled: true
---

# Deep Research

## Purpose

Conduct long-horizon, multi-source research on a topic and produce a synthesized report with
citations, contradictions surfaced, and uncertainty called out.

## When to Use

- User explicitly asks for deep / comprehensive research
- The question is open-ended and benefits from many sources
- A report / briefing is the deliverable

## When NOT to Use

- The question is answerable from one source (route to `web-research`)
- The user wants a quick answer (route to `web-research` or `fact-checking`)

## Capabilities

- Multi-source synthesis
- Contradiction handling
- Structured report output
- Citation tracking
- Confidence calibration

## Inputs

- Research question
- Scope / boundaries
- Audience and purpose

## Workflow

1. **Scope.** Define what's in and out. Define "done."
2. **Sub-questions.** 5–10 sub-questions covering the topic.
3. **Source plan.** For each sub-question: 2–4 sources minimum, diverse types.
4. **Iterate.** Run searches, extract claims, follow citations.
5. **Synthesize per sub-question.** With sources.
6. **Cross-synthesize.** Identify patterns across sub-questions.
7. **Final report.** Executive summary, sections per sub-question, contradictions, gaps, sources.

## Tools

- Web search
- Browser
- Notes / outline tool

## Safety

- Explicitly mark uncertainty
- Don't manufacture consensus
- Surface conflicts

## Source

Custom skill, written for this library.

## Notes

Longer-horizon version of `web-research`. Pairs with:
- `academic-research` (when scholarly sources matter most)
- `report-generation`
- `fact-checking`

## Examples

Requests that should activate this skill include: "deep research"; "do a deep dive"; "exhaustive research".
