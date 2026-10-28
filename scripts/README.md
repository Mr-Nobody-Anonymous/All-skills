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
| `python scripts/build_awesome_lock.py --verify` | `awesome_skills.lock` digests match every catalog `SKILL.md` |
| `python scripts/refresh_registry.py --check` | `skills/registry.json` & `dependencies.json` are current |
| `python scripts/run_evals.py` | Behavioral, routing and adversarial evals (`evals/`) |
| `python scripts/scan_skills_security.py` | Security & prompt-injection scanner |
| `python scripts/allskills.py doctor --full` | 11-layer platform diagnostic |

## Regenerating generated files

```bash
python scripts/refresh_registry.py                                    # registry.json + dependencies.json
python scripts/skills/skills.py lock                                  # skills.lock (canonical + active)
python scripts/build_awesome_lock.py                                  # awesome_skills.lock (catalog)
python scripts/mcp_catalog.py generate                               # docs/MCP-CATALOG.md + mcps/generated/*
python scripts/mcp_catalog.py install --harness claude --profile core  # wire MCP into a harness
python scripts/compute_stats.py && python scripts/generate_readme_stats.py   # stats.json + README numbers
python scripts/generate_baselines.py                                  # baselines/v0-current
```

## Everyday tools

| Command | Purpose |
| :--- | :--- |
| `python scripts/skills/skills.py <command>` | Canonical engine CLI (`route`, `search`, `explain`, `validate`, `doctor`, `chain`, `lock`, `execute --safe`, …) — also available as `all-skills` |
| `python scripts/allskills.py <command>` | Universal platform CLI (`doctor`, `search`, `explain`, `setup`, profiles, `sources`, `run --safe`) |
| `python scripts/manage_awesome_skills.py` | Search, inspect and install skills from the `awesome_skills/` catalog |
| `python scripts/setup_tools.py [--status]` | Link skills into Claude Code, Cursor, Codex and other harnesses |
| `python scripts/run_hook.py pre\|post\|failure <skill_id>` | Run lifecycle hooks (see [`hooks/`](../hooks/README.md)) |
| `python scripts/build_catalog.py` | Rebuild `awesome_skills/skills_index.json` and `CATALOG.md` |
| `python scripts/build_indexes.py` | Rebuild the central `registry/` layer (skills, categories, sources, indexes) |
| `python scripts/build_awesome_lock.py [--verify]` | Regenerate (or verify) the catalog digest lock `awesome_skills.lock` |
| `python scripts/mcp_catalog.py <action>` | MCP catalog: `list`, `doctor`, `verify`, `generate`, `install`, `sync-optin` |
| `python scripts/generate_integration_skills.py [--check]` | Generate (or verify) the 12 canonical `integration` skills |
| `python scripts/build_marketplace.py` | Rebuild the static web marketplace in `marketplace/` |
| `python scripts/dev/add_catalog_servers.py` | Maintainer helper: append registry-verified connectors to `mcps/catalog.json` (additive, idempotent) |
| `python scripts/dev/add_missing_skills.py [--force]` | Maintainer helper: emit the curated `skills/<category>/<name>/SKILL.md` playbooks that close coverage gaps |
| `node scripts/dev/generate-skill-triggers.js --refresh-digests` | Re-pin `manifests/context-packs/skill-triggers@1.json` offline after the skill tree changes |

### Importing upstream skills

`python scripts/sync_sources.py` (also `allskills sync`) imports skills from the sources in
`sources/registry.yaml`. It copies whole skill packages, preserves upstream frontmatter,
records full commit SHAs, detected licenses (never assumed) and content hashes in
`sources/imports.lock.json`, and never overwrites existing imports silently:

```bash
python scripts/sync_sources.py --source superpowers      # import new skills
python scripts/sync_sources.py --update                  # review upstream changes (no writes)
python scripts/sync_sources.py --update --apply          # apply them, with a backup
python scripts/sync_sources.py --rollback <backup-id>    # restore the backup
```

Other import and maintenance scripts (`import_*`, `normalize_*`, `synthesize_*`, `clone_*`)
change catalog content in bulk — review their docstrings and run them on a branch. Each
script supports `--help`.
