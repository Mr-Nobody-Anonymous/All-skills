# Skills Library — Security Policy

This document describes how the agent skills library is kept safe to use.

## Threat model

Skills are loaded as **prompt content** (their `SKILL.md` body) by the agent.
The realistic attack vectors are therefore:

1. **Prompt injection via skill content.** A malicious SKILL.md could try to
   override the agent's system instructions, exfiltrate data, or instruct the
   agent to run destructive commands.
2. **Destructive patterns in scripts.** A skill may ship a `scripts/` directory
   with shell or Python files. Those files are *not* auto-executed, but if the
   user later runs them, dangerous patterns would matter.
3. **Credential exposure.** A skill may instruct the agent to read
   `~/.ssh/id_rsa`, `~/.aws/credentials`, `.env`, or similar.
4. **Network exfiltration.** A skill may embed code that POSTs the user's
   context to an attacker-controlled host.

The validator at `src/skills/validator.py` exists to flag these patterns before
a skill is enabled.

## What the validator checks

Each `SKILL.md` and every readable file under a registered skill directory is scanned for:

| Pattern | Risk |
|---|---|
| `curl ... | sh` or `curl ... | bash` | Pipe-to-shell — classic RCE pattern. |
| `eval(...)` in shell/Python/JavaScript | Dynamic code execution. |
| `base64 -d` / `atob(...)` / `Buffer.from(..., 'base64')` | Obfuscated payload decode. |
| References to `~/.ssh/id_rsa`, `~/.aws/credentials`, `~/.npmrc`, `~/.netrc`, `~/.env` | Credential file access. |
| `rm -rf /` | Destructive root deletion. |
| `powershell -EncodedCommand ...` | Encoded PowerShell execution. |

Match results are returned as **warnings** in `ValidationResult.warnings` — they
do not block skill loading by themselves, but are surfaced by
`scripts/skills/skills.py doctor` and `validate`.

## Required frontmatter

Every skill MUST have `SKILL.md` frontmatter containing `name`, `description`, `category`, and `version`, all standard body sections, and a sibling `README.md`. Imported skills additionally require pinned repository/path/commit/author/license metadata, a preserved `LICENSE`, and `references/upstream-SKILL.md`.

## Quarantine

Suspicious or unaudited skills are moved to `skills/_quarantine/` with a
`QUARANTINE.md` describing why. Skills in quarantine:

- Are not loaded by `load_registry`.
- Cannot be invoked via the router.
- Are still visible in `skills/_quarantine/` so a reviewer can inspect them.

The current library has zero quarantined skills. It includes 55 locally maintained skills and 7 pinned adaptations from vetted upstream repositories. Imported executable scripts were intentionally excluded.

## Permissions model

- Skills are **not auto-executed**. The agent reads their content and decides
  what (if anything) to do.
- Skills never receive credentials, file system paths outside the current
  workspace, or network access without explicit user direction.
- `risk: medium` skills (e.g. `security.secret-detection`,
  `security.dependency-audit`) name concrete tools (gitleaks, pip-audit,
  npm audit). They are still not run automatically — they describe how the
  user would run those tools.

## Adding a new skill safely

1. Write the skill from scratch or adapt content only from sources you have
   read and trust.
2. Include only the `SKILL.md` frontmatter keys you actually use.
3. Do not include raw scripts that fetch network resources, read credential
   files, or run destructive commands.
4. Run `python scripts/skills/skills.py validate` and confirm there are no
   errors and no `suspicious pattern` warnings.
5. If the skill ships scripts, add a `RISK.md` (or a "Safety" section in
   `SKILL.md`) describing what they do and what they touch.
6. Set `source: custom` for local work. For adaptations, preserve repository, source path, commit, author, license, modification status, and upstream instructions.
7. If in doubt, put the skill in `skills/_quarantine/<skill-name>/` and add a
   `QUARANTINE.md` describing the concern.

## Incident reporting

If a user discovers that a skill prompted the agent to take a dangerous
action, that skill should be moved to `_quarantine/` immediately and the
validator patterns should be reviewed for whether the rule needs to be
extended.

## Per-category security skills

The per-category index for the four defensive security skills in this library
lives at [security-category.md](security-category.md) (auto-generated from the
registry) so it does not collide with this policy file.
