# Response to the external audit

An external review of this repository (October 2026) listed MCP servers and skills it believed were
missing, then flagged internal inconsistencies: `124` canonical skills against `122`, `72` active
skills against `70`, `4` core MCP servers against `12`, `264` tests against `94`, and a `SKILLS.md`
architecture that did not match `README.md`.

This page answers that review item by item, from the repository itself rather than from indexed
documentation. Every claim below is checkable with the command in the *Evidence* column; nothing here
is asserted from memory.

---

## 1. The headline finding was right, and the fix was structural

> "Its default MCP configuration is much smaller than its catalog and ambitions suggest."

Correct at the time of writing, in two ways:

1. **Two inventories existed.** `mcps/catalog.json` drives the installer; a second, hand-maintained
   `mcp/` tree shipped alongside it with 12 server stubs and a `registry.json` claiming 12 servers
   and 9 profiles, some naming servers that did not exist (`bitbucket`, `asana`, `monday`, `canva`,
   `datadog`, `quickbooks`). Two hand-edited inventories always drift.
2. **Counts were prose.** "96 MCP servers", "448 skills", "94 tests" lived as literal text in
   `README.md`, `SKILLS.md` and `docs/`, refreshed by hand. That is exactly why the review found
   `README.md` and `SKILLS.md` disagreeing.

Both are now fixed at the root:

| Before | After |
| :--- | :--- |
| `mcp/` hand-maintained, 12 servers, partly fictional | generated from `mcps/catalog.json` — 117 server files, real categories, validated role profiles (`scripts/dev/generate_mcp_registry.py --check`) |
| MCP counts only in prose | `mcp_servers`, `mcp_categories`, `mcp_harnesses`, `mcp_profiles`, `mcp_role_profiles` are computed into `stats.json` and synced into every document by `scripts/compute_stats.py` |
| `SKILLS.md` said 122 skills / 70 active / 12 servers | generated from the same `stats.json`; `compute_stats --verify` fails CI on any drift |
| Skill → connector requirements undocumented | `registry/skill-mcp-map.json` + `docs/MCP-SKILL-MAP.md` + an `## MCP Requirements` table inside each skill that declares servers (`scripts/dev/generate_skill_mcp_map.py --check`) |

*Evidence*: `python scripts/dev/generate_mcp_registry.py --check`,
`python scripts/dev/generate_skill_mcp_map.py --check`, `python scripts/compute_stats.py --verify`,
and `tests/test_catalog_coverage.py::test_generated_mcp_tree_matches_the_catalog` (plus four sibling
tests) which fail if any of it drifts again.

**The default config is still deliberately small.** `mcp_config.json` at the repository root carries
only the five keyless `core` servers, because writing 117 servers into every agent's config is a
denial-of-service against its context window, not a feature. The catalog is what you install *from*:
`allskills mcp install --harness <h> --profile full` writes all 117, `--profile standard` writes the
20 keyless/single-token ones.

---

## 2. The ten "add first" servers: nine were already there

| Proposed | Status in this repository |
| :--- | :--- |
| GitHub MCP | **already present** — `github` (official, in `standard`) |
| Playwright MCP | **already present** — `playwright` (official, in `standard`) |
| Context7 | **already present** — `context7` (in `standard`) |
| Supabase / database MCP | **already present** — `supabase` plus `postgres`, `sqlite`, `mysql`, `mongodb`, `redis`, `duckdb`, `bigquery`, `snowflake`, `clickhouse`, `elasticsearch`, `neo4j`, `qdrant`, `chroma`, `pinecone` |
| Sentry MCP | **already present** — `sentry` |
| Figma MCP | **already present** — `figma` |
| Linear / Atlassian | **already present** — `linear`, `atlassian` (Jira), `jira`, `confluence` |
| Brave Search / Firecrawl | **already present** — `brave-search`, `firecrawl`, plus `exa`, `tavily`, `perplexity` |
| Notion / Slack | **already present** — `notion`, `slack` |
| Grafana | **already present** — `grafana` |

The review was reading an older revision of the README. The gap it identified was real in *documentation*
(the catalog section was not prominent), which the README's MCP section now leads with.

## 3. The second list: four more were already present, two were genuinely missing

| Proposed | Status |
| :--- | :--- |
| Serena (code intelligence) | **added** — `serena` (`uvx --from serena-agent serena start-mcp-server`) |
| DeepWiki | **added** — `deepwiki` (`npx -y deepwiki-mcp@latest`) |
| Cloudflare | already present — `cloudflare` |
| Stripe | already present — `stripe` |
| Google Workspace | already present — `google-drive`, `gmail`, `google-calendar`, `google-sheets` |
| HubSpot | already present — `hubspot` |
| Zapier | **not added — no verifiable package.** npm `zapier-mcp@0.0.1` is `UNLICENSED` with no repository metadata. Recorded here rather than invented. |
| Hugging Face | already present — `huggingface` |
| Exa | already present — `exa` |
| Docker | already present — `docker` |
| Prometheus / OpenTelemetry (implied by the Grafana gap) | **added** — `prometheus`, `opentelemetry` |

Catalog total: **117 servers across 36 categories, 18 harnesses, 3 install profiles, 10 role profiles.**

---

## 4. The proposed skills: most already existed under a different name

The review was careful to say these were "gaps in the visible, active skill suite, not verified
absences" — and it was right to hedge. Of 55 proposals, **26 already existed** and were not duplicated:

| Proposed | Existing equivalent |
| :--- | :--- |
| `graphql-engineering` | `development/graphql-api-design` |
| `grpc-api-design` | `development/grpc-service-design` |
| `websocket-engineering` | `development/websocket-realtime` |
| `dbt-expert` | `data/dbt` |
| `data-quality-testing` | `data/data-quality` |
| `vector-database-engineering` | `data/vector-database` |
| `llm-fine-tuning` | `ai/fine-tuning` |
| `llm-serving-vllm` | `ai/vllm` |
| `multimodal-ai` | `ai/multimodal` |
| `ai-cost-optimization` | `finops/ai-inference-cost` |
| `mcp-security-audit` | `integration/mcp-security-review` |
| `sre-slos-error-budgets` | `observability/slo-sli` |
| `dependency-supply-chain-security` | `security/dependency-audit` + `legal/sbom-analysis` |
| `privacy-compliance` | `legal/gdpr` + `legal/ccpa` + `legal/data-retention` |
| `release-engineering` | `development/release-management` |
| `statistical-analysis` | `scientific/statistics` |
| `react-native-expert` | `mobile/react-native` |
| `flutter-development` | `mobile/flutter` |
| `ios-swift` | `mobile/swift-development` + `mobile/swiftui-development` |
| `android-kotlin` | `mobile/kotlin-development` + `mobile/android-compose` |
| `image-generation-workflows` | `design/image-gen` |
| `video-editing-automation` | `video/video-editing-workflow` |
| `3d-content-pipelines` | `3d/three-d-asset-pipeline` |
| `presentation-design` | `design/presentations` |
| `load-testing` | `testing/load-testing` |
| `threat-modeling`, `container-security`, `incident-response`, `experiment-design` | identical names already existed |

**29 genuinely missing skills were written** (`scripts/dev/domain_skills_eng.py`), each a full
playbook with workflow, inputs, safety and failure modes:

| Area | Added |
| :--- | :--- |
| Frontend | `web/nextjs-app-router`, `web/react-performance`, `web/typescript-advanced` |
| Quality | `testing/component-testing`, `testing/visual-regression-testing`, `testing/mutation-testing`, `testing/contract-testing`, `testing/accessibility-automation` |
| Backend | `development/fastapi-expert`, `development/nestjs-expert` |
| Data | `databases/postgresql-performance`, `databases/database-query-optimization` |
| AI | `ai/rag-evaluation`, `ai/mlops`, `ai/model-drift-monitoring` |
| Agents (new category) | `agents/mcp-integration-testing`, `agents/agent-observability`, `agents/agent-reliability`, `agents/human-in-the-loop-design` |
| Cloud / ops | `cloud/cloudflare-workers`, `devops/platform-engineering`, `devops/disaster-recovery` |
| Security | `security/api-security-testing` |
| Data science | `scientific/causal-inference` |
| Product | `product/user-research`, `product/product-analytics`, `product/conversion-rate-optimization`, `product/pricing-strategy`, `communication/customer-support-automation` |

Skills: **448 → 533**, categories **44 → 45**. Every new skill that needs a connector declares it in
frontmatter and carries a generated `## MCP Requirements` table.

---

## 5. The five architectural gaps: what was done about each

| Gap the review raised | What this repository now does |
| :--- | :--- |
| **MCP security and permissions** | Per-server `risk` and `required_env` in the catalog; `mcp/policies/default-policy.json` (`least-privilege`, read-only default, approval for destructive); `mcp/permissions/permissions-schema.json`; the generated `mcp/servers/*.json` carry the policy inline; `scripts/dev/generate_skill_mcp_map.py` fails on a skill declaring a server that does not exist; `security/prompt-injection-defense` and `integration/mcp-security-review` cover tool-result injection. |
| **Skill deduplication and provenance** | `registry/provenance.json`, `registry/licenses.json`, `registry/trust.json` and `skills.lock` (622 pinned hashes) are generated for every canonical skill; `scripts/deduplicate.py` and `tests/` guard duplicates; section 4 above is the worked example of de-duplicating against names rather than filenames. |
| **Capability verification** | `allskills doctor --full` runs 11 layers; `run_evals.py` runs 8 suites; `pytest` 364 tests; `scripts/scan_skills_security.py` scans every skill file; `scripts/ci/*.js` validate catalog, skills, manifests, context profiles, agents and commands. A skill existing is not treated as evidence; the gates are in CI. |
| **Skill → MCP dependency mapping** | **New**: declared `mcp_servers` frontmatter, `registry/skill-mcp-map.json` (both directions: skill → servers and server → skills), `docs/MCP-SKILL-MAP.md`, per-skill requirements tables, and five tests. 63 skills declare servers, 37 servers are required by at least one skill, and the remaining 80 servers are listed as the backlog for future coverage. |
| **Observability and evaluation** | `evals/` (behavioural, routing, OOD, adversarial, security, baseline), `scripts/benchmark_skills.py`, `scripts/eval-harness.js`, `tests/` for tool-failure and executor limits, plus `agents/agent-observability` for instrumenting agents themselves. |

---

## 6. The specific inconsistencies the review listed

| Finding | Verdict |
| :--- | :--- |
| "Conflicting architecture inventories (`README.md` vs `SKILLS.md`)" | **Real, fixed.** `SKILLS.md` quoted 122/70/12/13,333 and listed an `mcp/` layout that no longer matched. It is now synced from `stats.json` by rule, and `mcp/` is generated. |
| "Canonical skill count differs: 124 vs 122" | **Stale on both sides.** The catalog holds **533** curated skills in 45 categories; both documents now derive the number. |
| "Active skill count differs: 72 vs 70" | **Stale.** 89 active harness skills; derived, not typed. |
| "MCP servers: 4 documented core vs 12 in `SKILLS.md`" | **Real, fixed.** 5 keyless `core` (by design), 20 `standard`, 117 `full`; the 12-server tree is gone, replaced by 117 generated files. |
| "Test counts differ: 264 vs 94" | **Real, fixed.** The suite is discovered, not hardcoded: `compute_stats` counts test cases (280) and `pytest` reports 364 collected tests including subtests. `SKILLS.md` no longer claims a "passing" ratio — CI badges report status, documents do not. |
| "Catalog counts differ: 14,855 vs 12,757" | **Both numbers are correct and measure different things** — 15,146 catalog *entries* versus 13,321 *unique* skill identities. `compute_stats.py` enforces the distinction with separate rules (`catalog_skills` vs `total_unique_skills`) and a test asserts no rule may conflate them. |
| "Agent compatibility claims vary by platform" | Partly addressed: `adapters/` (12 YAML), `platforms/platforms.yaml`, and `tests/` exercise discovery and install for each target; `allskills doctor --full` verifies 11 agent adapters. Runtime execution differs per vendor and is not claimed beyond what CI exercises. |
| "Feature claims need runtime evidence" | Agreed and applied: sandboxing, approval gates, hooks and dependency resolution each have executable tests; `docs/LIMITATIONS.md` records what is **not** covered (including the vendored ECC installer mapping gap) instead of implying it works. |

---

## 7. What is still missing — and why it is not being invented

- **Zapier MCP** — no verifiable public package (npm entry is `UNLICENSED` 0.0.1, no repo). Open.
- **Photoshop MCP** — does not exist in any registry as of this writing; checked PyPI and npm.
- **OBS, Pro Tools, LightBurn, MuseScore, Scribus, Argyll CMS** — all CLI-drivable but no published
  MCP server. An MCP wrapper would be a new project, not a catalog entry.
- **A real `full`-profile smoke test per server.** Every entry is verified to *resolve* (PyPI/npm,
  console-script name, licence, docs) but not to *run* — running 117 third-party servers with real
  credentials in CI is out of scope. `mcp_catalog.py doctor` reports which are installable locally.
- **Domain gaps** (welding, textiles, structural/MEP engineering, clinical coding, agriculture,
  aviation, insurance) are enumerated with their prerequisites in [`DOMAIN-COVERAGE.md`](DOMAIN-COVERAGE.md) §3.

The honest summary of the review's central limitation — *"not enough to certify every proposed skill is
absent without inspecting the files"* — is exactly why section 4 above lists the 26 proposals that were
already present. De-duplicating against the tree is the first step of every addition in this repository,
and it is now enforced by the generator rather than by reviewer diligence.
