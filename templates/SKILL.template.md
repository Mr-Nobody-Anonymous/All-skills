---
name: example-skill-name
description: One-sentence summary explaining exactly what the skill does. Use when [trigger criteria].
disable-model-invocation: false
category: development
version: 1.0.0
author: Your Name
triggers:
  - trigger phrase 1
  - trigger phrase 2
aliases:
  - example-alias
keywords:
  - keyword1
  - keyword2
tools:
  - file_read
  - file_edit
  - bash
mcp_servers:
  - filesystem
preconditions:
  - check_environment
postconditions:
  - verify_syntax
recovery:
  fallback_skill: active.code-reviewer
  max_retries: 3
  on_failure: rollback
---

# Example Skill Name

## Purpose
Explain the primary goal of this skill and what specialized role the agent adopts when executing it.

---

## When to Use
- Scenario 1: Specific problem or user prompt
- Scenario 2: Intermediate step in a larger pipeline

## When NOT to Use
- Scenario 1: Unrelated task that should use a different skill
- Scenario 2: Anti-pattern to avoid

---

## Inputs
| Parameter | Type | Required | Description |
| :--- | :--- | :---: | :--- |
| `target_path` | string | Yes | Path to file or directory |

## Outputs
| Output | Type | Description |
| :--- | :--- | :--- |
| `status` | string | Result outcome |

---

## Workflow Steps
1. **Step 1: Preparation & Inspection**
   - Details of what to check first before modifying anything.
2. **Step 2: Execution**
   - Details of transformation or analysis.
3. **Step 3: Verification & Invariant Checks**
   - Verification command (e.g. AST parse check or unit test).

---

## Examples

### Example 1: Standard Request
**User Prompt**:
> "Do task X on file Y"

**Agent Behavior**:
1. Inspects file Y.
2. Applies minimal, clean changes.
3. Runs verification and reports outcome.

---

## Safety & Boundaries
- Strictly adhere to forbidden file blocklists (`.env*`, private keys).
- Never execute destructive shell commands (`rm -rf /`, `git push --force`).
