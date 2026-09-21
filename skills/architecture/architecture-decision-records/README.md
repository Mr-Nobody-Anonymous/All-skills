# Architecture Decision Records (ADRs)

An agent skill for creating, documenting, reviewing, and maintaining architectural decision records across software systems.

## Features
- **4 Scaffold Templates**: MADR, Nygard, Lightweight, and Deprecation/Migration.
- **Decision Matrix Framework**: Multi-criteria comparison of candidate technologies.
- **Lifecycle Management**: Tracking statuses (`Proposed`, `Accepted`, `Deprecated`, `Superseded`).
- **Prompt-Hardened Boundaries**: XML delimiter protections against untrusted input.

## Quick Start
Tell your AI assistant:
> "Draft an ADR evaluating PostgreSQL vs DynamoDB for our user activity logging service."

## Directory Structure
- `SKILL.md`: Main instruction playbook for AI agents.
- `templates/`: Markdown templates ready for immediate scaffolding.
- `examples/`: Reference examples showing good vs bad ADR practices.
- `tests/`: Structural and format validation tests.
