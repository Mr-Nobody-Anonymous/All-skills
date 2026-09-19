---
name: beam
description: "Publish a locally redacted coding-session snapshot only when explicitly requested."
category: utilities
aliases: []
triggers:
  - "use beam"
  - "run beam"
keywords: [beam, utilities, publish, locally, redacted, coding, session]
dependencies: [optional:node, optional:BEAM_ACCESS_TOKEN]
risk: low
version: 1.0.0
source: custom
enabled: true
capabilities: [beam, utilities]
inputs: [task, context]
outputs: [result, report]
lifecycle: enabled
---

# Beam

## Purpose
Publish a locally redacted coding-session snapshot only when explicitly requested.

## When to Use
Use when you need to publish a locally redacted coding-session snapshot only when explicitly requested. or trigger commands matching use beam, run beam.

## When NOT to Use
Do not use outside permitted scope or when authorization is missing.

## Capabilities
- Publish a locally redacted coding-session snapshot only when explicitly requested.
- Deterministic step-by-step execution
- Structured artifact validation

## Inputs
Natural-language request, execution context, and configuration parameters.

## Workflow
1. Parse inputs and verify environment prerequisites.
2. Execute bounded operations with continuous validation.
3. Return verified results and logs.

## Tools
optional:node, optional:BEAM_ACCESS_TOKEN

## Examples
Example usage:
```bash
# Invoke via skills CLI
python scripts/skills/skills.py route "use beam"
```

## Safety
Never perform destructive unconfirmed modifications. Adhere to zero-trust boundaries.

## Source
Imported from openclawskills.net.

## Notes
Maintained as part of canonical utilities category.
