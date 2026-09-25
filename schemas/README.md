# `schemas/` — JSON Schemas

| Schema | Describes |
| :--- | :--- |
| `skill-frontmatter.schema.json` | YAML frontmatter of every `SKILL.md` — enforced by `scripts/validate_schema.py` in CI |
| `skill-metadata.schema.json` | Extended skill metadata |
| `skill_identity.schema.json` | Formal skill identity (ID, trust tier, provenance) |
| `skills-lock.schema.json` | `skills.lock` lockfile format |
| `capability.schema.json` / `policy.schema.json` / `tool.schema.json` | Capability, policy and tool contracts |
| `aas-stack.schema.json` | Agent stack definitions (`scripts/manage_state.py`) |

## How to run

```bash
python scripts/validate_schema.py     # validates all SKILL.md frontmatter
```

Most editors (VS Code, JetBrains) validate JSON files automatically when a
`"$schema"` key points at one of these files.
