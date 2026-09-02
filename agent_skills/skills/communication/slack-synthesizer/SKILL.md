---
name: slack-synthesizer
description: Summarize Slack threads into decisions, evidence, disagreements, and action items.
category: communication
aliases: [slack, summary, thread, summarize]
triggers:
  - Summarize this Slack thread
  - What was decided in this channel
  - Extract action items from Slack
  - Slack summary
keywords: [slack, summary, thread, decision, action-items, channel]
required_tools: [slack-access]
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

# Slack Synthesizer

## Purpose

Summarize Slack threads and channels into structured information: decisions made,
key evidence and arguments, disagreements noted, and action items with owners.
The skill helps users catch up on conversations without reading everything.

## When to Use

- The user wants to catch up on a Slack channel
- A thread needs to be summarized for someone who missed it
- Extracting action items from a discussion
- Identifying decisions made in a channel

## When NOT to Use

- Real-time conversation monitoring (use Slack's built-in features)
- Accessing private channels without authorization
- Archiving or storing Slack data beyond the session

## Capabilities

- Fetch thread messages with context
- Identify key speakers and their positions
- Extract decisions (explicit or implicit)
- Surface disagreements or open questions
- Extract action items with owners
- Generate summaries in multiple formats (brief, detailed, bullet)

## Inputs

- `source` (required) â€” channel ID, thread URL, or message IDs
- `format` (optional) â€” one of: brief, detailed, bullet-points
- `focus` (optional) â€” decisions, actions, disagreements, or all

## Workflow

1. **Fetch** â€” Retrieve messages from specified source
2. **Analyze** â€” Identify speakers, sentiment, and structure
3. **Extract** â€” Find decisions, actions, and key points
4. **Synthesize** â€” Generate coherent summary
5. **Format** â€” Output in requested format

## Tools

- Slack API (with appropriate read scopes)
- Thread/message access permissions

## Examples

**User:** "Summarize the decisions from #project-alpha this week"
**Response:**
```
# #project-alpha Weekly Summary

## Decisions Made
- âœ“ API v2 deadline: March 15 (owner: @alice)
- âœ“ Technology: Use PostgreSQL over MongoDB
- âœ“ Deprecation timeline: 6 months for v1

## Open Questions
- Authentication provider (discussion ongoing)

## Action Items
- [ ] @bob: Update technical spec (by Friday)
- [ ] @carol: Schedule migration planning meeting
```

## Safety

- Respect channel privacy settings
- Never store Slack data beyond the session
- Only access channels the user has permission for
- Flag sensitive content without disclosing details

## Source

Auto-generated from openclawskills.net description.

## Pairs Well With

- `meeting-action-extractor` (structured meeting notes)
- `context-summarize` (context compression)
- `calendar-assistant` (follow up on action items)
