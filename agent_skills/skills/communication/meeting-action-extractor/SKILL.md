---
name: meeting-action-extractor
description: Extract decisions, action items, owners, dates, and unresolved questions from meetings.
category: communication
aliases: [meeting, action-items, decisions, extract, notes]
triggers:
  - Extract action items from this meeting
  - What were the decisions
  - Meeting summary
  - Parse meeting notes
  - Extract follow-ups
keywords: [meeting, action-items, decisions, summary, follow-up, owner]
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

# Meeting Action Extractor

## Purpose

Extract structured information from meeting content: decisions made, action items
with owners and due dates, and unresolved questions. The skill helps teams stay
accountable and ensures nothing falls through the cracks.

## When to Use

- Processing meeting notes or transcripts
- Extracting action items for follow-up
- Creating meeting summaries for stakeholders
- Tracking decisions across meetings

## When NOT to Use

- Real-time meeting transcription (use specialized tools)
- Accessing private meeting content without consent
- Replacing human judgment on ambiguous assignments

## Capabilities

- Parse meeting text, transcripts, or notes
- Identify explicit and implicit decisions
- Extract action items with owners
- Detect due dates and deadlines
- Surface unresolved questions and open issues
- Generate structured output (markdown, JSON, task list)
- Track items across multiple meetings

## Inputs

- `content` (required) â€” meeting text, transcript, or notes
- `format` (optional) â€” one of: markdown, json, task-list, full-summary
- `context` (optional) â€” previous meeting context for tracking

## Workflow

1. **Parse** â€” Extract structured data from meeting content
2. **Identify** â€” Find decisions, actions, and questions
3. **Assign** â€” Match owners where explicitly stated
4. **Structure** â€” Format output according to request
5. **Validate** â€” Present for user review and correction

## Tools

- Text parsing and NLP
- Structured output generation

## Examples

**User:** "Extract action items from these meeting notes: [paste notes]"
**Response:**
```
# Meeting Action Items

## Decisions Made
- âœ“ Architecture: Use microservices over monolith
- âœ“ Timeline: Ship MVP by Q2
- âœ“ Team: Form dedicated platform team

## Action Items
- [ ] @alice: Finalize API spec (by Feb 15)
- [ ] @bob: Set up CI/CD pipeline (by Feb 20)
- [ ] @carol: Schedule user research sessions (by Feb 25)

## Open Questions
- ? Database vendor selection (deferred to next week)
- ? Third-party integrations (needs investigation)

## Next Steps
- Follow-up meeting scheduled for Feb 25
```

## Safety

- Never assume ownership without explicit mention
- Flag uncertain extractions for human review
- Respect meeting privacy and confidentiality
- Don't store extracted data without consent

## Source

Auto-generated from openclawskills.net description.

## Pairs Well With

- `calendar-assistant` (schedule follow-up meetings)
- `slack-synthesizer` (sync with communication channels)
- `adhd-task-breakdown` (break down action items)
- `focus-guard` (protect time for follow-up work)
