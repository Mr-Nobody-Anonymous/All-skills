---
name: whatsapp-router
description: Classify and route WhatsApp messages with consent, privacy, and escalation boundaries.
category: communication
aliases: [whatsapp, message, route, classify]
triggers:
  - Route this WhatsApp message
  - Categorize WhatsApp message
  - Process WhatsApp input
keywords: [whatsapp, message, route, classify, triage]
required_tools: [whatsapp-api]
risk: high
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

# WhatsApp Router

## Purpose

Classify incoming WhatsApp messages and route them to appropriate handlers based
on content type, sender, and intent. The skill ensures proper consent verification
and privacy boundaries are maintained.

## When to Use

- Processing incoming WhatsApp messages for automation
- Routing messages to appropriate handlers or skills
- Classifying message intent (question, command, escalation)

## When NOT to Use

- Responding directly without user consent
- Storing message content without permission
- Processing messages from unknown senders

## Capabilities

- Message classification (command, question, notification, spam)
- Intent detection
- Sender verification
- Privacy-filtering (redact sensitive content)
- Routing to appropriate handlers
- Escalation detection for human review

## Inputs

- `message` (required) â€” message content
- `sender` (required) â€” sender identifier
- `timestamp` (required) â€” message timestamp
- `context` (optional) â€” conversation history

## Workflow

1. **Verify** â€” Check sender consent and authorization
2. **Classify** â€” Determine message type and intent
3. **Filter** â€” Apply privacy filters to content
4. **Route** â€” Direct to appropriate handler or skill
5. **Escalate** â€” Flag for human review if needed
6. **Respond** â€” Generate appropriate response (if authorized)

## Tools

- WhatsApp Business API
- Message classification model

## Safety

- NEVER process messages without verified consent
- Always filter sensitive content before routing
- Escalate ambiguous or concerning messages to human review
- Never store raw messages without consent
- Respect blocking and opt-out requests immediately

## Source

Auto-generated from openclawskills.net description.

## Pairs Well With

- `telegram-actions` (multi-platform messaging)
- `context-summarize` (summarize conversation context)
