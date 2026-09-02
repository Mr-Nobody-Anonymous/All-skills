# Upstream Source Audit

Audit date: 2026-09-01

Third-party repositories were cloned into the operating-system temporary directory and inspected before integration. No upstream installation or executable script was run.

## Selected repositories

| Repository | Pinned commit | License | Imported adaptations | Rationale |
|---|---|---|---:|---|
| `obra/superpowers` | `b36e0829c6d0140e93cfef2ca599b1b07d4a7797` | MIT | 6 | Mature, modular engineering workflows that add design, verification, review-feedback, worktree, and parallel-agent behavior without replacing local coding/TDD/debugging skills. |
| `anthropics/skills` | `53048666b05b4799081517d00e09e0a2dd688678` | Apache-2.0 for selected skill | 1 | `mcp-builder` adds a missing MCP-server workflow and carries its own Apache-2.0 license. |

## Imported skills

- `development.brainstorming`
- `development.verification-before-completion`
- `development.receiving-code-review`
- `development.requesting-code-review`
- `development.git-worktrees`
- `utilities.parallel-agents`
- `development.mcp-server-development`

Each imported skill preserves the upstream `SKILL.md` under `references/upstream-SKILL.md`, includes the applicable license, records repository/path/commit/author metadata, and is marked modified because local frontmatter and safety guidance were added. Upstream executable scripts were excluded.

## Reviewed but not imported

- `agentskills/agentskills`: used as the format/specification reference, not a general skill source.
- `K-Dense-AI/scientific-agent-skills`: reputable and broad, but its highly specialized catalog and dependency footprint were beyond this library's general-purpose scope; existing research skills were retained to avoid bulk duplication.
- Anthropic document skills (`pdf`, `docx`, `pptx`, `xlsx`): excluded because they overlap local skills and the upstream repository describes these particular skills as source-available rather than open source.
- Overlapping Superpowers skills (`systematic-debugging`, `test-driven-development`, `writing-plans`): excluded because equivalent local skills already exist.
- `mattpocock/skills`: reviewed as a maintained MIT collection, but its principal coding, research, TDD, and code-review workflows overlap the selected sources and local skills.

## Security findings

- Static suspicious-pattern scans found no blocking issue in the selected content.
- One initial warning on `process.env.EXAMPLE_API_KEY` was reviewed as a false positive for environment-variable access, not a credential-file read. The validator was narrowed to detect actual credential-file paths while retaining `.env`, SSH, AWS, npm, and netrc checks.
- No skill was quarantined. Future unaudited or suspicious imports must be placed under `skills/_quarantine/` and cannot be loaded or routed.
