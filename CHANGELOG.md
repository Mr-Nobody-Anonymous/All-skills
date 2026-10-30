# Changelog

All notable changes to the **All-Skills** Universal Agent Skill Operating System and Multi-Agent Harness will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Fixed
- **The multi-agent compatibility table was wrong in both directions — and is now generated.**
  - It claimed **Tier 4 Verified** for Claude Code, Cursor, Codex and Gemini, while
    `compatibility/matrix.json` recorded `invocable: null` / `workflow_completed: null` for every
    platform and held **zero** `manual_evidence` entries. Nothing backed the label.
  - It listed **OpenClaw** (`.openclaw/skills/`) as Tier 3 Validated, but OpenClaw had no adapter,
    no `registry/agents.json` entry and no `platforms/platforms.yaml` target — so `allskills doctor`
    and `tests/test_agent_discovery.py` could not see it at all. It omitted **OpenCode**, which was
    fully configured and shipping.
  - Every row is now rendered from `compatibility/matrix.json` by the new
    `scripts/generate_harness_matrix.py`, and the tier is *computed* from the recorded evidence:
    Tier 4 needs `invocable` **and** `workflow_completed` backed by a `manual_evidence` entry,
    Tier 3 needs `invocable`, Tier 2 is configured + discoverable. Current state: **12 harnesses,
    all Tier 2 Scanned, 0 manual evidence** — which is what the data actually supports.
  - `registry/agents.json` (11 → **12 agents**) is generated too, `adapters/openclaw.yaml` and the
    `.openclaw/skills` link target were added, and `scripts/setup_tools.py` now links all 12.
  - `scripts/verify_registry_integrity.py` cross-checks the three inventories: every agent in
    `registry/agents.json` needs an existing adapter and a real `platforms.yaml` target, and every
    adapter must be referenced by `platforms.yaml`. Its success line reported a hardcoded
    "12 adapters … 11 agents" and now prints measured counts.
  - `python scripts/generate_harness_matrix.py --check` runs in CI, and
    `tests/test_portability.py::TestHarnessClaimsAreGenerated` fails if a tier outside the block
    claims evidence that was never recorded.

- **CI red across every runner, for three unrelated reasons — all reproduced locally and fixed.**
  - `Tests` (Ubuntu, macOS, Windows × Python 3.10/3.11/3.12) failed in
    `test_cli_contracts::test_verify_and_lock_pass_on_a_consistent_checkout` because
    `.github/skills` was committed as a **symlink to `/home/user/All-skills/.agents/skills`**. Git
    stores a symlink as its target path, so the link resolved on exactly one machine and
    `allskills verify` reported `link points to /home/user/... expected /home/runner/...` on every
    runner. The link is machine-local output of `scripts/setup_tools.py` and was already in
    `.gitignore` — but a trailing-slash pattern (`.github/skills/`) does not match a symlink. Now
    untracked, deleted from the tree, and the pattern fixed. New `tests/test_portability.py` and the
    previously-unwired `scripts/ci/validate-no-personal-paths.js` (now in CI) reject any tracked
    symlink with an absolute target or one escaping the repository.
  - `Validate library & integrity` failed with `Tests count mismatch: stats.json has 280, discovered
    281`. The count came from unittest discovery, which **imports** every test module, so it changed
    with the installed extras: the validate job installs `-e .` without `[test]`, `pytest` was
    absent, `tests/test_mcp_catalog.py` failed to import and was counted as one extra `_FailedTest`.
    `compute_stats.count_test_cases()` now counts from the AST over exactly the CI selection
    (`tests/` + `scratch_priority_import/tests`, minus `tests/ecc`, which needs the optional `llm`
    package): **372 tests**, identical on every OS and Python version, and
    `verify_registry_integrity.py` shares that function instead of duplicating the logic.
    `tests/test_mcp_catalog.py` now raises `unittest.SkipTest` rather than an import error when
    pytest is absent.
  - `Security / Dependency vulnerability audit (pip-audit)` reported **27 advisories** in three
    pinned dev dependencies: `certifi 2026.7.22` (PYSEC-2026-4320), `filelock 4.0.3`
    (14 × CVE-2026-1128xx–1129xx) and `virtualenv 21.12.1` (11 × CVE-2026-1137xx). Bumped to
    `certifi 2026.10.23`, `filelock 4.2.4` and `virtualenv 21.15.1`;
    `pip-audit -r requirements.txt -r requirements-dev.txt` now reports **no known vulnerabilities**.

### Added
- **Round 4 — one inventory, not two; +29 skills, +4 connectors (504 → 533 skills, 44 → 45
  categories; 113 → 117 servers, 35 → 36 categories).** Triggered by an external audit that found
  the repository documenting two different inventories. Answer in full:
  [`docs/AUDIT-RESPONSE.md`](docs/AUDIT-RESPONSE.md).
  - **`mcp/` is now generated** from `mcps/catalog.json` by
    `scripts/dev/generate_mcp_registry.py` (117 server files, real category index, 10 role profiles
    validated against the catalog). It was a hand-maintained tree of 12 stubs whose `registry.json`
    claimed 12 servers — including servers that never existed (`bitbucket`, `asana`, `monday`,
    `canva`, `datadog`, `quickbooks`). Stale stubs are deleted on regeneration.
  - **MCP counts are now computed, not typed.** `mcp_servers`, `mcp_categories`, `mcp_harnesses`,
    `mcp_profiles`, `mcp_role_profiles` are part of `stats.json`, and `DOC_COUNT_RULES` syncs them
    into `README.md`, `SKILLS.md` and `docs/` — the same mechanism that already guarded the skill
    counts. `compute_stats --verify` fails on any disagreement.
  - **`SKILLS.md` corrected**: it claimed 122 canonical skills, 70 active harness skills, 12 MCP
    servers, 192 manifest skills and "94/94 tests passing", and described a `mcp/` layout that no
    longer existed. Every number is now derived; the "passing" claim is gone (CI badges report
    status, documents do not), and the fictional "15 universal super-domains" is replaced with the
    structure that exists.
  - **New: skill → connector dependency mapping.** Skills declare `mcp_servers:` in frontmatter; the
    generator writes `registry/skill-mcp-map.json` (both directions), `docs/MCP-SKILL-MAP.md`, and an
    `## MCP Requirements` table inside each declaring skill. 63 of 533 skills declare servers, 37 of
    117 servers are required by at least one skill, and the remaining 80 are listed as backlog.
  - **4 new connectors**: `serena` (symbol-aware code intelligence, `serena-agent`), `deepwiki`
    (repository comprehension), `prometheus` (PromQL) and `opentelemetry` (distributed traces) —
    each verified against PyPI/npm with the console-script name read from the wheel's
    `entry_points.txt`. `zapier` was rejected: npm `zapier-mcp@0.0.1` is UNLICENSED with no repository.
  - **29 new skills** for the gaps the audit correctly identified, after de-duplicating 26 proposals
    that already existed under other names (`graphql-api-design`, `grpc-service-design`,
    `websocket-realtime`, `data/dbt`, `ai/vllm`, `finops/ai-inference-cost`,
    `integration/mcp-security-review`, `observability/slo-sli`, `mobile/react-native`,
    `mobile/flutter`, `design/presentations`, …): `nextjs-app-router`, `react-performance`,
    `typescript-advanced`, `component-testing`, `visual-regression-testing`, `fastapi-expert`,
    `nestjs-expert`, `postgresql-performance`, `database-query-optimization`, `rag-evaluation`,
    `mlops`, `model-drift-monitoring`, `causal-inference`, `cloudflare-workers`,
    `platform-engineering`, `disaster-recovery`, `api-security-testing`, `mutation-testing`,
    `contract-testing`, `accessibility-automation`, `user-research`, `product-analytics`,
    `conversion-rate-optimization`, `pricing-strategy`, `customer-support-automation`, plus the new
    `agents` category: `mcp-integration-testing`, `agent-observability`, `agent-reliability`,
    `human-in-the-loop-design`.
  - **Five new regression tests** pin the invariants: the generated `mcp/` tree must match the
    catalog byte for byte, no orphan server stubs, registry counts must equal reality, every declared
    server must be installable, and the map must stay current.
- **56 new canonical skills and 17 MCP connectors for the non-software world (448 → 504 skills,
  30 → 44 categories; 96 → 113 servers, 31 → 35 categories).** The library covered engineering
  thoroughly and authoring not at all: an agent asked to make a map in QGIS, model a part in
  FreeCAD, rig a character in Blender or grade a cut in Resolve had no playbook and no connector.
  New categories and their skills:
  - `geospatial` (12): `qgis-map-production`, `spatial-reference-systems`, `postgis-spatial-sql`,
    `gdal-ogr-pipelines`, `remote-sensing-indices`, `vector-tile-web-maps`, `openstreetmap-data`,
    `lidar-point-clouds`, `geocoding-address-matching`, `cartographic-design`,
    `drone-photogrammetry`, `spatial-statistics`
  - `cad` (8): `freecad-parametric-modeling`, `openscad-programmatic-cad`, `dxf-dwg-interchange`,
    `autocad-drafting`, `fusion360-solid-modeling`, `rhino-grasshopper`, `bim-ifc-coordination`,
    `technical-drawing-gdt`
  - `3d` (13): `blender-modeling-topology`, `blender-sculpting-retopology`,
    `blender-rigging-animation`, `blender-geometry-nodes`, `blender-shading-materials`,
    `blender-rendering-lighting`, `blender-python-scripting`, `three-d-asset-pipeline`,
    `mesh-repair-printing`, `pbr-texture-authoring`, `character-animation-principles`,
    `houdini-procedural-vfx`, `vfx-compositing`
  - `audio` (4): `music-production-daw`, `audio-mixing-mastering`, `sound-design-foley`,
    `podcast-production` — `video` (4): `video-editing-workflow`, `color-grading`,
    `motion-graphics`, `video-encoding-delivery` — `photography` (1): `photography-raw-workflow`
    — `architecture` (2): `architectural-design-workflow`, `interior-space-planning`
  - New connectors, each verified against PyPI/npm with a launch command taken from the package's
    own README: `qgis`, `gdal`, `geoserver`, `mapbox`, `freecad`, `openscad`, `autocad`,
    `grasshopper`, `revit`, `ifc`, `kicad`, `blender`, `meshy`, `sketchfab`, `inkscape`,
    `ableton`, `davinci-resolve`. Token-gated servers (`mapbox`, `meshy`, `sketchfab`) are
    `full`-profile only; the `standard` profile is unchanged at 20 keyless/single-token servers.
  - Generated by `scripts/dev/add_domain_skills.py` (+ `domain_skills_geo.py`,
    `domain_skills_media.py`, `domain_skills_craft.py`) and `scripts/dev/add_domain_servers.py`,
    so the expansion is reproducible rather than hand-typed. `canonical-library` grew 407 → 463
    paths, so all 504 curated skills remain installable.
  - Craft batch (12, no new categories): `vector-illustration-svg`,
    `typography-and-type-systems`, `print-production-prepress`, `editorial-layout-design`,
    `iconography-systems` (`design`); `music-notation-engraving`, `live-sound-reinforcement`
    (`audio`); `live-streaming-broadcast` (`video`); `cnc-machining-fabrication`,
    `laser-cutting-engraving` (`cad`); `studio-lighting-color-management` (`photography`);
    `construction-documents-specifications` (`architecture`).
  - **[`docs/DOMAIN-COVERAGE.md`](docs/DOMAIN-COVERAGE.md)** now records the complete
    discipline inventory — what has playbooks and connectors, and an explicit list of the gaps
    still open (welding/sheet metal, textiles, structural and MEP engineering, clinical
    documentation, agriculture, aviation, and tools with no verified MCP server such as MuseScore,
    OBS, LightBurn and Photoshop) with what closing each one requires.
- **32 new MCP connectors (64 → 96 servers, 27 → 31 categories)**. Every new package was
  verified against the public registry before it was catalogued (`npm view` / PyPI JSON, plus
  the project's own `repository` metadata for the docs link). New capability areas:
  databases (`mysql`, `neo4j`, `qdrant`, `chroma`, `pinecone`, `snowflake`, `bigquery`,
  `duckdb`, `neon`), cloud and IaC (`azure`, `digitalocean`, `heroku`, `netlify`,
  `google-cloud-run`, `firebase`, `pulumi`), work tracking and knowledge (`clickup`, `trello`,
  `airtable`, `todoist`, `google-calendar`, `google-sheets`), automation and execution
  (`n8n`, `apify`, `e2b`), CI and quality (`circleci`, `sonarqube`, `postman`), and
  communication/media/payments (`paypal`, `resend`, `twilio`, `elevenlabs`). The `standard`
  profile grew 12 → 20 servers (keyless or single-token only); `mcp-configs/mcp-servers.json`
  now offers 116 opt-in connectors, and every generated harness bundle was regenerated.
- **38 new canonical skills (410 → 448, 30 categories)**. Each one is a real playbook — workflow,
  inputs, tools, safety, failure modes — generated by `scripts/dev/add_missing_skills.py`:
  languages (`php-modern`, `ruby-rails`, `elixir-otp`, `scala-fundamentals`,
  `r-statistical-programming`, `julia-scientific-computing`, `haskell-fundamentals`,
  `lua-scripting`), databases (`sql-server`, `oracle`), web frameworks (`vue-development`,
  `svelte-development`, `astro-sites`), API styles (`graphql-api-design`,
  `grpc-service-design`, `websocket-realtime`, `api-gateway-patterns`,
  `webhook-delivery-design`, `third-party-api-resilience`), infrastructure
  (`terraform-iac`, `pulumi-iac`, `circleci-pipelines`, `monorepo-management`),
  security and quality (`secrets-management`, `oauth2-oidc-integration`,
  `sonarqube-quality-gates`, `load-testing`, `postman-api-testing`), work apps
  (`google-sheets-automation`, `google-calendar-automation`, `airtable-workflows`,
  `clickup-workflows`, `transactional-email`, `sms-messaging`, `n8n-workflow-automation`),
  media and execution (`text-to-speech-production`, `sandboxed-code-execution`) and
  release safety (`feature-flag-management`).
- **The curated `skills/<category>/<name>` library is now installable** (`canonical-library`
  module, 407 paths) with a new `library` install profile. Previously only the vendored
  `awesome_skills/ecc` tree could be installed, so 448 curated skills existed but were
  unreachable from the installer.
- **`scripts/mcp_catalog.py sync-optin`** keeps `mcp-configs/mcp-servers.json` additive and
  current with the catalog (84 → 116 entries).
- **`scripts/dev/generate-skill-triggers.js --refresh-digests`** and **`package.json`
  `context-profiles:check`**: the trigger manifest can now be re-pinned offline (no provider
  call) and the context-profile schema gate runs in `npm test`.

### Fixed
- **Context-profile inventory was empty, which silently disabled the whole profile subsystem**:
  `manifests/context-packs/skill-registry@1.json` pointed at a flat `skills/` layout
  (`skills/<name>/SKILL.md`), but the tree is `skills/<category>/<name>/SKILL.md`, so
  `loadContextRegistry` discovered **0** skills and `ecc profile preview/show/explain` returned
  nothing. Discovery now walks for `SKILL.md` at any depth and rejects duplicate leaf names;
  the inventory root is the install-owned catalog library.
- **`validate-context-profiles.js` failed and was not wired into CI**: the trigger manifest's
  `registryDigest` was stale after every skill change. The validator now runs (3/3 tests pass)
  and `npm test` calls it.
- **`manifests/install-modules.json` referenced gitignored, machine-local harness directories**
  (`.codex/`, `.cursor/`, `.opencode/`), so `validate-install-manifests.js` failed on any clean
  checkout. Those paths are written per machine by the installers, not shipped as sources.
- **`scripts/dev/generate-skill-triggers.js` could not even print `--help`/`--dry-run`** in a
  source checkout because it hard-required the development-only `docker/context-profiles/`
  evaluation harness at import time. The provider plumbing is now loaded lazily.
- **`scripts/harness-audit.js` scored the repository 55/80** by looking for skills in a stale
  flat `skills/<name>` path (skills live in `skills/<category>/<name>` or the catalog tree).
  It resolves every candidate layout now: 75/80, and only genuinely absent artifacts remain.
- **Broken quick-start and CLI contract**: the README told users to run `all-skills setup`,
  `allskills explain` and `allskills run <skill> --safe`, none of which existed. `allskills`
  now ships `setup` (alias of `init`), `explain` (9-signal rationale, human and `--json`
  output) and `--safe` on `execute`/`run`, and the quick start documents commands that run.
- **`--safe` was declared but ignored**: `src/skills/cli.py` parsed the flag and never used it.
  Safe mode is now implemented in the policy engine (`apply_safe_mode`): `ALLOW` capabilities at
  `MEDIUM_RISK` and above are escalated to `ASK`, `ASK`/`DENY` are never relaxed, and the run
  returns an approval request bound to skill + capabilities + inputs. Wired through
  `ExecutionRuntime.execute`, `simulate`, `skills.py` and `allskills.py`.
- **102 catalog `SKILL.md` files had unparseable frontmatter** (48 with `---name:` glued to the
  fence, 54 with unquoted `key: value` colons or broken quotes). All are now valid YAML, so the
  catalog passes the JSON Schema with **0** violations and CI enforces `--max-catalog-errors 0`
  instead of tolerating 102.
- **Stale catalog index**: `awesome_skills/CATALOG.md` and `skills_index.json` were 291 skills
  behind the tree (14,855 vs 15,146). Regenerated, together with `stats.json` and the baselines.
- **Broken relative links in documentation**: 30 `file:///…` links (which never resolve on
  GitHub) in `docs/` now point at the right relative paths; `TROUBLESHOOTING.md` links in three
  `docs/` pages, `.kiro/README.md`'s licence link, `rules/ECC_RULES.md` and the `react-patterns`
  / `react-testing` rule links no longer 404.
- **Missing roadmaps**: `roadmaps/README.md` advertised `cybersecurity-specialist.md`,
  `data-engineer.md` and `system-architect.md`, which did not exist. All three are written.
- **`provenance/` documented a directory tree that did not exist** (and `THIRD_PARTY_NOTICES.md`
  linked to a non-existent `provenance/licenses/`). Both now describe the real record locations
  (`registry/provenance.json`, `registry/sbom.json`, `catalog/provenance/sources.json`).
- **Context-pack discovery rejected `skills/_quarantine`** as an "Invalid canonical skill ID",
  which broke profile inspection (`ecc profile`), context-profile validation and trigger
  generation. Reserved `_`/`.` directories and directories without a `SKILL.md` are skipped, as
  the Python loaders already did.
- **CLIs crashed on a closed pipe**: `allskills sources | head` exited 120 and
  `skills.py list | head` raised a `BrokenPipeError` traceback. Both now exit 0, while real
  failures keep their exit codes.
- **`package.json` shipped a `.gemini/` entry** for a directory that never exists; removed.
- **Stale documented stack sizes**: the discovery pyramid (124 canonical / 72 active / 500
  handlers / 3,200 vetted), `docs/LIMITATIONS.md` (122 / 72), the repository tree (187/146/129/82/65
  catalog counts, "10 Categories", "75+ adapters", "14 tool domains"), the voice OS box
  ("714+ skills", "12 language packs") and "70 pre-loaded playbooks" now match the repository:
  398 canonical, 89 active, 142 handlers, 15,140 schema-vetted catalog files, 29 categories,
  12 adapters, 18 tool domains, 405 native voice packages, 1 locale pack, 89 playbooks.
- **Dependabot** grouped security updates separately, keeps `increase-if-necessary` for pip and
  adds npm coverage.
- **`awesome_skills.lock` was unverifiable**: it pinned 14,849 entries with per-file digests that
  matched only 1,420 files (and no tree hash), so it could never be verified. It is regenerated by
  the new `scripts/build_awesome_lock.py` for all 15,140 catalog `SKILL.md` files with LF-normalised
  SHA-256 digests, and `--verify` now runs in CI, `allskills verify` and the 11-layer doctor.
- **`scripts/ci/catalog.js` could not see the canonical library**: it counted skills as flat
  `skills/<slug>/SKILL.md`, which is the upstream ECC layout, so this repository reported 0 skills
  and rejected the README for a missing quick-start summary. It now counts
  `skills/<category>/<slug>/SKILL.md` as well, and every tracked document marker exists.
- **`scripts/ci/validate-skills.js` reported 65 false "Missing SKILL.md" errors** because it treated
  each category directory as a skill. It now recognises the categorised layout and skips
  `_`-prefixed boundaries and code-backed skills (which the Python registry validates).
- **`manifests/install-modules.json` pointed at 291 paths that do not exist** (`skills/<name>` for
  skills that live in `skills/<category>/` or `awesome_skills/ecc/`, plus the generated `.gemini/`),
  so every selective install and the install-manifest validator failed. All paths now resolve.
- **Dead links across the documentation set**: 336 relative links pointed at files that do not
  exist (missing `assets/images/**` media, `TROUBLESHOOTING.md`, `rules/README.md`, localized asset
  copies, flat `skills/<slug>` references). The referenced media was restored, the shared assets
  moved to `assets/`, and markdown/HTML links were repointed, leaving only intentional placeholders.

- **CI was red on every workflow**: `pip install -e .` crashed in modern setuptools because `setup.py` duplicated metadata that the PEP 621 `[project]` table did not declare. `pyproject.toml` is now the single source of packaging metadata (readme, SPDX license, authors, URLs, classifiers) and `setup.py` is a thin shim.
- **Missing catalog skill**: an unanchored `build/` rule in `.gitignore` kept `awesome_skills/automation/build/` out of Git, so catalog statistics could never verify on a fresh clone. Build-output rules are now root-anchored and the skill is restored byte-for-byte (verified against its `awesome_skills.lock` digest).
- **Unimportable skill handlers**: 158 `skills/**/__init__.py` files contained literal `\n` escapes (`SyntaxError`) and all 142 `handler.py` modules subclassed `BaseSkill` before importing it (`NameError`). Every handler now imports and instantiates.
- **Platform-dependent lockfile**: `skills.lock` digests changed with the OS (CRLF checkouts, `Path` sort order, `__pycache__` files), so a lock generated on Windows reported every skill as "tampered" on Linux. Hashing now normalises line endings and ordering; `skills.lock` is regenerated.
- **Stale generated files**: `skills/registry.json` / `dependencies.json` were regenerated — two canonical skills (`architecture/architecture-decision-records`, `healthcare/health-economist`) were missing from the registry.
- **Machine-dependent `dependencies.json`**: the committed index recorded which tools were installed where it was generated, so `refresh_registry.py --check` could only pass on that machine. It now records declared dependencies only (index `version: 2`); live availability stays in `skills.py doctor`.
- **Python-version-dependent quality scores**: overall scores used float `sum()`, whose algorithm changed in Python 3.12, so boundary values (e.g. 6.45) rounded differently per interpreter. Scores now use exact decimal arithmetic, rounded half-up.
- **Packaged CLI `doctor`** crashed with `TypeError` (wrong `Validator` call); `skills/_quarantine/` was missing from Git; `skills.py lock` printed a hard-coded skill count.
- **Docker**: the image's default command crashed (`ModuleNotFoundError: core`), the compose service restart-looped, and the build context had no `.dockerignore` (copying `.git` and any local `.env`).
- 60 mypy errors and 3 undefined names in first-party code.

### Added
- **Universal MCP layer** (`mcps/catalog.json`, `src/skills/mcp.py`, `scripts/mcp_catalog.py`):
  a verified catalog of **64 MCP servers across 27 categories** that installs into **18 agent
  harnesses** with one command — `allskills mcp install --harness <h> --profile core|standard|full`.
  Installs are additive, idempotent and backed up; OpenCode/Zed/VS Code get their native dialects,
  Codex gets a TOML fragment and Goose a YAML fragment. Includes `list`, `doctor`, `verify`,
  `generate` (docs + per-harness bundles), `sync-optin` and 15 unit tests. `docs/MCP-CATALOG.md`
  is generated from the catalog and CI fails on a stale or incoherent one.
- **`integration` skill suite** (12 canonical skills): `mcp-server-install`, `mcp-gateway`,
  `mcp-server-author`, `mcp-security-review`, `agent-harness-onboarding`, `skill-pack-install`,
  `connector-github`, `connector-databases`, `connector-browser-automation`,
  `connector-observability`, `connector-cloud-infrastructure`, `universal-skill-discovery` —
  the "install anything, connect everything" front door, generated by
  `scripts/generate_integration_skills.py` and checked in CI.
- **`scripts/build_awesome_lock.py`** — generates/verifies `awesome_skills.lock` (catalog digests).
- **`README.zh-CN.md`** — Chinese landing page with the three-minute install, harness setup and MCP
  quick start, so the localized docs are reachable from the repository root.
- README sections **“Explain why this skill was selected”** and **“Safe Mode & Explicit Approval”**
  — both were linked from the table of contents but missing from the document.
- Safe-mode regression tests (`tests/test_runtime.py`): escalation, read-only pass-through,
  approval round-trip and the "never relaxes a DENY" invariant.
- `docs/LIMITATIONS.md` §8 documents the vendored ECC tooling layout gap that `npm run test:ecc`
  reports, so a failing ECC file is read as an unported feature rather than a platform regression.
- Consolidated **CI** workflow: Ruff, mypy, actionlint; tests with coverage on Python 3.10–3.12; library/registry/lockfile integrity; package build + wheel smoke test; Docker build (hadolint) + smoke test.
- **Security** workflow (skill scans, Gitleaks secret scanning, dependency review), **CodeQL** code scanning and **Dependabot** (Actions, pip, Docker).
- `tests/test_regressions.py` — permanent regression tests for every fix above (No-Regression Policy §3).
- `.editorconfig`, `.gitattributes` (LF everywhere, CRLF for `.bat`), `.pre-commit-config.yaml`, `.gitleaks.toml`, `.dockerignore`.
- Full Contributor Covenant 2.1, issue-template chooser with a feature-request form, refreshed PR template.
- README table of contents, live status badges, Mermaid architecture diagrams, "Quick Start" and "Development, CI & Quality Gates" sections; how-to-run READMEs for `src/`, `scripts/`, `tests/`, `skills/`, `docker/`, `hooks/`, `evals/`, `adapters/`, `schemas/` and `docs/`.

### Changed
- README now documents the MCP catalog, the surface-parity inventory table (68 agents / 410 skills /
  94 commands) and the `integration` suite; counts follow `stats.json` (410 canonical skills in
  30 categories, 499 lockfile entries).
- `npm` packaging ships `mcps/`, `README.zh-CN.md` and `scripts/profile.js` (previously missing) and
  keeps documentation media out of the tarball.
- All GitHub Actions upgraded to current Node 24 releases (pinned by commit SHA) on `ubuntu-24.04`; the release workflow now runs on tags or manual dispatch only and attaches built distributions.
- Docker image runs as a non-root user on Python 3.12, exposes the `all-skills` CLI and makes audio libraries opt-in.

### Security
- Removed the `security@allskills.dev` contact from `SECURITY.md` — the domain is not registered, so reports would have been lost (or received by whoever registers it).
- `.gitignore` now covers `.env.*` variants and `config/api_keys.yml`, which the setup docs instruct users to fill with real keys.

### Removed
- Redundant workflows `test.yml`, `validate.yml`, `validate-skills.yml`, `skill-integrity.yml` and `registry.yml` (every command they ran is now in `ci.yml`), and the duplicate `skill_request.yml` issue form (superseded by `skill_proposal.yml`).

---

## [3.0.0] - 2026-09-21

### Added
- **Single Source of Truth (`VERSION`)**: Established canonical root `VERSION` file (`3.0.0`) synchronizing `pyproject.toml`, `package.json`, `config.yaml`, `manifest.json`, and `stats.json`.
- **Registry & Stats Integrity Engine (`scripts/verify_registry_integrity.py`)**: Automated verification command (`allskills verify-registry`) recalculating all repository numbers and asserting zero metadata drift.
- **Fail-Closed Security Hooks (`scripts/run_hook.py`)**: Guaranteed non-zero exit codes when required or security-critical hook scripts are missing or fail.
- **AST Code Verification (`src/skills/security.py`)**: Added semantic AST parsers for Python scripts and YAML documents.
- **Skill Revocation Registry (`registry/revocations.json`)**: Cryptographic revocation list with advisory IDs and immediate router kill-switch blocking.
- **Skill Verification Matrix (`registry/verification_matrix.json`)**: Comprehensive verification tracking across schema, security, provenance, and license compliance for all skills.
- **STRIDE Threat Model (`docs/security/threat-model.md`)**: Formal threat model documenting attack vectors, mitigations, and residual risks for autonomous agent skills.
- **Network Security Policy (`docs/security/network-security.md`)**: Strict localhost binding in development (`127.0.0.1`), reverse proxy with TLS 1.3, rate limiting, and egress whitelisting in production.
- **SPDX License Compliance Policy (`docs/security/license-policy.yaml`)**: Permitted permissive inbound licenses, banned copyleft/proprietary licenses, and provenance validation rules.
- **Repository Architecture Inventory (`docs/architecture/repository-map.md`)**: Taxonomy table delineating source, generated, runtime, and experimental boundaries.
- **Code Ownership Governance (`CODEOWNERS`)**: Strict review assignments for security scanners, hooks, schemas, and adapters.
- **Out-of-Distribution Routing Benchmarks (`evals/routing/ood_cases.json`)**: Versioned dataset of 25 ambiguous, out-of-domain, and deceptive prompt test cases.

### Changed
- **Removed Security Scanner Line Bypass**: Eliminated dangerous substring check (`if any(k in line for k in ["input:", "payload:", "test_"]): continue`) in `src/skills/security.py`, preventing malicious payloads from disguising themselves as test cases.
- **Updated Production Host Binding**: Changed default `web.host` in `config.yaml` from `0.0.0.0` to `127.0.0.1` for safe default deployment.
- **Synchronized Workflows Counting**: `stats.json` explicitly distinguishes between 5 autonomous agent workflows (`workflows/`) and 8 CI/CD GitHub Actions workflows (`.github/workflows/`).
- **Standardized Documentation**: Reconciled all prose counts in `README.md` and `CONTRIBUTING.md` with authoritative platform metrics (14,855 catalog skills, 143 tests, 12 adapters, 20 profiles).

### Fixed
- Fixed trailing literal backslash in 23 `skills/*/__init__.py` files that caused `SyntaxError` on import.
- Fixed fail-open security bypass in lifecycle hook runner.
- Added console UTF-8 reconfigure across CLI entry points to prevent Windows `cp1252` encoding exceptions on emojis.

---

## [2.0.0] - 2026-09-20

### Added
- Hub-and-Spoke universal multi-agent harness linking `.agents/skills/` to `.claude/skills/`, `.cursor/skills/`, and `.codex/skills/`.
- 11-layer comprehensive diagnostic system (`allskills doctor --full`).
- 20 standardized role profiles in `profiles/` and `registry/profiles.json`.
- 12 platform adapters (`claude.yaml`, `cursor.yaml`, `codex.yaml`, `gemini.yaml`, `copilot.yaml`, `windsurf.yaml`, `cline.yaml`, etc.).
- Non-destructive setup scripts (`scripts/setup_tools.py`, `scripts/setup_skills.py`).
- Evaluation and behavioral benchmarks in `evals/`.
- SkillHub specification validation engine (`scripts/validate_skillhub_spec.py`).

---

## [1.0.0] - 2026-09-15

### Added
- Initial release with 122 canonical skills and 8 core categories.
- Basic intent routing engine with keyword and trigger phrase scoring.
- JSON Schema frontmatter validation (`schemas/skill-frontmatter.schema.json`).
- Static regex security scanner in `src/skills/security.py`.
- Dependency conflict resolver and import queue.
