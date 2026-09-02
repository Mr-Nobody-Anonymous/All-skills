---
name: cmd-safety-check
description: Classify terminal commands by impact and require safeguards before risky execution.
category: media_and_utilities
aliases: [command, safety, terminal, security, risk, execute]
triggers:
  - Is this command safe
  - Check this command
  - Should I run this
  - Command safety
  - Risk assessment
keywords: [command, terminal, safety, risk, execute, shell, bash]
required_tools: []
risk: medium
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

# Terminal Command Safety Check

## Purpose

Classify terminal commands by their potential impact and risk level, requiring
appropriate safeguards before execution. The skill prevents accidental destructive
actions and ensures users understand the consequences of risky commands.

## When to Use

- Before running unfamiliar or complex commands
- When executing potentially destructive operations
- For commands involving system changes or deletions
- Before running commands with sudo/elevated privileges

## When NOT to Use

- For simple, well-understood commands (echo, ls, cd)
- When speed is critical for trivial operations
- For read-only diagnostic commands

## Capabilities

- Command parsing and analysis
- Risk classification (safe, caution, dangerous, critical)
- Impact prediction (what will be affected)
- Safeguard recommendations
- Rollback strategy suggestions
- Dry-run support where available

## Risk Levels

1. **Safe** â€” Read-only, reversible operations (ls, cat, grep)
2. **Caution** â€” Minor changes, easily reversible (mkdir, touch, chmod)
3. **Dangerous** â€” Significant changes, harder to reverse (rm, mv, sed)
4. **Critical** â€” Destructive or system-wide (dd, rm -rf, format, chmod 777)

## Workflow

1. **Parse** â€” Analyze command syntax and arguments
2. **Classify** â€” Assign risk level based on command and context
3. **Explain** â€” Describe what the command will do
4. **Recommend** â€” Suggest safeguards or safer alternatives
5. **Confirm** â€” Require explicit approval for dangerous+ commands
6. **Execute** â€” Run only after confirmation

## Examples

**User:** "Is it safe to run: rm -rf node_modules/"
**Response:**
```
âš ï¸ Risk Level: DANGEROUS

Analysis:
- Command: rm -rf node_modules/
- Impact: Permanently deletes node_modules folder
- Scope: All nested files and folders
- Reversibility: Cannot be undone

Safeguards recommended:
â–¡ Verify you're in the correct directory first
â–¡ Use --dry-run flag if available
â–¡ Consider: rm -i node_modules/ for interactive mode

Say "confirm" to proceed, or I'll suggest a safer alternative.
```

## Safety

- ALWAYS explain risk before any destructive command
- Require explicit confirmation for dangerous+ operations
- Suggest safer alternatives when available
- Never auto-execute risky commands
- Provide rollback strategies where possible

## Source

Auto-generated from openclawskills.net description.

## Pairs Well With

- `system-monitor` (post-command verification)
- `security-scanner` (security-sensitive operations)
- `docker-manager` (container command validation)
