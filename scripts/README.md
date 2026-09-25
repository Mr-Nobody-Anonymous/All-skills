# `scripts/` — platform tooling

Command-line tools for validating, generating and managing the skill library. Run
everything from the **repository root** after `python -m pip install -e .`.

## CI & quality gates

These run in [`.github/workflows/ci.yml`](../.github/workflows/ci.yml) and
[`security.yml`](../.github/workflows/security.yml):

| Command | Purpose |
| :--- | :--- |
| `python scripts/skills/skills.py test` | Platform test suite (unittest discovery of `tests/`) |
| `python scripts/validate_schema.py` | Validate `SKILL.md` frontmatter against `schemas/skill-frontmatter.schema.json` |
| `python scripts/validate_skillhub_spec.py` | SkillHub & multi-agent specification lint |
| `python scripts/verify_registry_integrity.py` | Cross-file version, statistics and lockfile integrity |
| `python scripts/compute_stats.py --verify` | `stats.json` matches the repository |
| `python scripts/generate_readme_stats.py --verify` | README metrics match `stats.json` |
| `python scripts/generate_baselines.py --verify` | Architecture baselines in `baselines/` are intact |
| `python scripts/refresh_registry.py --check` | `skills/registry.json` & `dependencies.json` are current |
| `python scripts/run_evals.py` | Behavioral, routing and adversarial evals (`evals/`) |
| `python scripts/scan_skills_security.py` | Security & prompt-injection scanner |
| `python scripts/allskills.py doctor --full` | 11-layer platform diagnostic |

## Regenerating generated files

```bash
python scripts/refresh_registry.py                                    # registry.json + dependencies.json
python scripts/skills/skills.py lock                                  # skills.lock
python scripts/compute_stats.py && python scripts/generate_readme_stats.py   # stats.json + README numbers
python scripts/generate_baselines.py                                  # baselines/v0-current
```

## Everyday tools

| Command | Purpose |
| :--- | :--- |
| `python scripts/skills/skills.py <command>` | Canonical engine CLI (`route`, `search`, `validate`, `doctor`, `chain`, `lock`, …) — also available as `all-skills` |
| `python scripts/allskills.py <command>` | Universal package manager CLI (`doctor`, `search`, profiles, sources) |
| `python scripts/manage_awesome_skills.py` | Search, inspect and install skills from the `awesome_skills/` catalog |
| `python scripts/setup_tools.py [--status]` | Link skills into Claude Code, Cursor, Codex and other harnesses |
| `python scripts/run_hook.py pre\|post\|failure <skill_id>` | Run lifecycle hooks (see [`hooks/`](../hooks/README.md)) |
| `python scripts/build_catalog.py` | Rebuild `awesome_skills/skills_index.json` and `CATALOG.md` |
| `python scripts/build_marketplace.py` | Rebuild the static web marketplace in `marketplace/` |

Import and maintenance scripts (`import_*`, `sync_*`, `normalize_*`, `synthesize_*`,
`clone_*`) change catalog content in bulk — review their docstrings and run them on a
branch. Each script supports `--help`.
