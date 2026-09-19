---
name: agent-transcript
description: "Create a redacted, consent-gated agent transcript for a pull request or issue."
category: utilities
aliases: []
triggers:
  - "use agent-transcript"
  - "run agent-transcript"
keywords: [agent-transcript, utilities, create, redacted, consent, gated, agent]
dependencies: [optional:node, optional:gh]
risk: low
version: 1.0.0
source: custom
enabled: true
capabilities: [agent-transcript, utilities]
inputs: [task, context]
outputs: [result, report]
lifecycle: enabled
---

# Agent Transcript

## Purpose
Create a redacted, consent-gated agent transcript for a pull request or issue.

## When to Use
Use when you need to create a redacted, consent-gated agent transcript for a pull request or issue. or trigger commands matching use agent-transcript, run agent-transcript.

## When NOT to Use
Do not use outside permitted scope or when authorization is missing.

## Capabilities
- Create a redacted, consent-gated agent transcript for a pull request or issue.
- Deterministic step-by-step execution
- Structured artifact validation

## Inputs
Natural-language request, execution context, and configuration parameters.

## Workflow
1. Parse inputs and verify environment prerequisites.
2. Execute bounded operations with continuous validation.
3. Return verified results and logs.

## Tools
optional:node, optional:gh

## Examples
Example usage:
```bash
# Invoke via skills CLI
python scripts/skills/skills.py route "use agent-transcript"
```

## Safety
Never perform destructive unconfirmed modifications. Adhere to zero-trust boundaries.

## Source
Imported from openclawskills.net.

## Notes
Maintained as part of canonical utilities category.
