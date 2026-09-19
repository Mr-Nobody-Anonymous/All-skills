---
name: crabbox
description: "Coordinate isolated remote or clean-machine validation while preserving trust and credential boundaries."
category: development
aliases: []
triggers:
  - "use crabbox"
  - "run crabbox"
keywords: [crabbox, development, coordinate, isolated, remote, clean, machine]
dependencies: [optional:crabbox]
risk: low
version: 1.0.0
source: custom
enabled: true
capabilities: [crabbox, development]
inputs: [task, context]
outputs: [result, report]
lifecycle: enabled
---

# Crabbox

## Purpose
Coordinate isolated remote or clean-machine validation while preserving trust and credential boundaries.

## When to Use
Use when you need to coordinate isolated remote or clean-machine validation while preserving trust and credential boundaries. or trigger commands matching use crabbox, run crabbox.

## When NOT to Use
Do not use outside permitted scope or when authorization is missing.

## Capabilities
- Coordinate isolated remote or clean-machine validation while preserving trust and credential boundaries.
- Deterministic step-by-step execution
- Structured artifact validation

## Inputs
Natural-language request, execution context, and configuration parameters.

## Workflow
1. Parse inputs and verify environment prerequisites.
2. Execute bounded operations with continuous validation.
3. Return verified results and logs.

## Tools
optional:crabbox

## Examples
Example usage:
```bash
# Invoke via skills CLI
python scripts/skills/skills.py route "use crabbox"
```

## Safety
Never perform destructive unconfirmed modifications. Adhere to zero-trust boundaries.

## Source
Imported from openclawskills.net.

## Notes
Maintained as part of canonical development category.
