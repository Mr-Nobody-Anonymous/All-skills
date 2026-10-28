# Integration Skills

_Generated: 2026-10-28T05:29:45+00:00_



**14 skills in this category.**

## Skills

### `integration.agent-harness-onboarding`

Install the All-Skills library into any supported agent harness (Claude Code, Cursor, Codex, Gemini, Copilot, VS Code, Windsurf, OpenCode, Cline, Roo, Goose and more) and verify the links.

- **Risk:** low
- **Path:** `integration/agent-harness-onboarding`
- **Aliases:** `harness-setup`, `install-agent-skills`, `onboard-agent`
- **Triggers:**
  - install skills into my agent
  - set up my harness
  - connect all agents
- **Source:** custom
- **Version:** 1.0.0

Each harness discovers skills from a different directory. Rather than copying 89 active skills into eleven places (and letting them drift), All-Skills links every harness to one canonical source, records exactly what it created, and can verify or undo the whole thing.

### `integration.connector-browser-automation`

Choose and wire the right browser connector — Chrome DevTools for live debugging, Playwright for scripted end-to-end checks, Browserbase for remote sessions — and keep context cost bounded.

- **Risk:** medium
- **Path:** `integration/connector-browser-automation`
- **Aliases:** `browser-mcp`, `playwright-connector`, `devtools-mcp`
- **Triggers:**
  - drive a browser from the agent
  - debug my page with devtools
  - end-to-end test the UI
- **Source:** custom
- **Version:** 1.0.0

Browser tools are the most context-expensive connectors available, and they differ in kind: a held-open DevTools session, a scripted Playwright run and a remote Browserbase session solve different problems. This skill picks deliberately and keeps step-by-step accessibility dumps out of the context window.

### `integration.connector-cloud-infrastructure`

Wire AWS, Cloudflare, Vercel, Railway, Kubernetes and Terraform connectors with least-privilege credentials, dry-run discipline and explicit approval gates for mutations.

- **Risk:** high
- **Path:** `integration/connector-cloud-infrastructure`
- **Aliases:** `cloud-mcp`, `kubernetes-mcp`, `infra-connectors`
- **Triggers:**
  - deploy from the agent
  - check cluster state
  - provision infrastructure
- **Source:** custom
- **Version:** 1.0.0

Infrastructure connectors can destroy in one call what took months to build. This skill keeps read paths open for investigation and requires a reviewed plan, an explicit approval and a rollback path before any mutation.

### `integration.connector-databases`

Connect an agent to PostgreSQL, SQLite, MySQL, MongoDB, Redis or ClickHouse through MCP, with read-only enforcement, schema discovery and cost-aware query habits.

- **Risk:** high
- **Path:** `integration/connector-databases`
- **Aliases:** `database-mcp`, `connect-postgres`, `sql-connector`
- **Triggers:**
  - query my database from the agent
  - connect postgres to claude
  - analyse data with the agent
- **Source:** custom
- **Version:** 1.0.0

A database connector is the fastest way to turn a helpful agent into an outage. This skill defaults to read-only credentials, requires an explicit schema scope, and makes the agent read execution plans before proposing index or query changes.

### `integration.connector-github`

Wire GitHub access into an agent (GitHub MCP server or the gh CLI skill) and run review, triage and release operations with least-privilege tokens.

- **Risk:** medium
- **Path:** `integration/connector-github`
- **Aliases:** `github-connector`, `github-mcp`, `gh-ops`
- **Triggers:**
  - connect github to my agent
  - review pull requests automatically
  - triage github issues
- **Source:** custom
- **Version:** 1.0.0

GitHub work is where an agent's autonomy is most visible and most dangerous. This skill picks the right access path — `gh` CLI for one-shot operations, the MCP server only when session state matters — and keeps the token scoped to exactly the repositories in play.

### `integration.connector-observability`

Wire error tracking, metrics and log search into an agent session so incidents are investigated from evidence rather than speculation.

- **Risk:** medium
- **Path:** `integration/connector-observability`
- **Aliases:** `sentry-mcp`, `grafana-mcp`, `observability-connectors`
- **Triggers:**
  - investigate a production error
  - check our dashboards
  - search logs for the failure
- **Source:** custom
- **Version:** 1.0.0

Incident work is where an agent's tendency to invent plausible causes does the most damage. This skill forces the investigation to start from a real error record, a real metric window and real log lines, and to cite them in the write-up.

### `integration.mcp-gateway`

Aggregate a large MCP catalog behind a single gateway endpoint so an agent can reach every connector without loading dozens of tool schemas into every session.

- **Risk:** medium
- **Path:** `integration/mcp-gateway`
- **Aliases:** `mcp-proxy`, `mcp-router`, `tool-gateway`
- **Triggers:**
  - too many MCP servers
  - context window blown by tools
  - single MCP endpoint for all tools
- **Source:** custom
- **Version:** 1.0.0

Every MCP server you enable injects its tool schemas into every session. Past a handful of servers the agent spends more context on tool descriptions than on the task. A gateway exposes one endpoint and lets tools be discovered on demand, so a 60-connector catalog costs roughly what a 3-connector catalog costs.

### `integration.mcp-security-review`

Audit MCP servers and their tool contracts for tool poisoning, prompt injection, over-broad scopes, unbounded execution and credential exfiltration paths before enabling them.

- **Risk:** low
- **Path:** `integration/mcp-security-review`
- **Aliases:** `mcp-audit`, `tool-poisoning-review`, `connector-risk-review`
- **Triggers:**
  - is this MCP server safe
  - review connectors for risk
  - tool poisoning
- **Source:** custom
- **Version:** 1.0.0

An MCP server inherits the agent's trust. A malicious or careless tool description can instruct the model, a permissive token can rewrite production, and a shell tool can bypass every other guardrail. This skill makes the trust boundary explicit before the connector is enabled.

### `integration.mcp-server-author`

Design and implement a new Model Context Protocol server with well-scoped tools, validated schemas, resource/prompt support and tests that exercise the protocol surface.

- **Risk:** medium
- **Path:** `integration/mcp-server-author`
- **Aliases:** `build-mcp-server`, `custom-connector`, `fastmcp`
- **Triggers:**
  - write an MCP server
  - expose our internal API to agents
  - add tools to our agent
- **Source:** custom
- **Version:** 1.0.0

Most agent-facing servers fail on tool design, not on transport. This skill enforces the parts that decide whether an agent can actually use the server: unambiguous tool names, strictly validated inputs, bounded output size, explicit error shapes and a documented auth model.

### `integration.mcp-server-install`

Install Model Context Protocol servers from the curated All-Skills catalog into any agent harness, with a preview, an idempotent merge and a verification step.

- **Risk:** medium
- **Path:** `integration/mcp-server-install`
- **Aliases:** `mcp-install`, `add-mcp-server`, `connect-mcp`
- **Triggers:**
  - install an MCP server
  - add a connector to my agent
  - wire MCP into Cursor
- **Source:** custom
- **Version:** 1.0.0

Wiring a connector by hand means remembering a different config path, key name and dialect for every harness. This skill replaces that with one catalog and one command, and refuses to guess: it previews the diff, keeps unmanaged entries byte-identical, and tells you exactly which environment variables the server needs before you start it.

### `integration.skill-pack-install`

Install a role profile or curated skill pack with dependency resolution, destination control and a dry-run preview.

- **Risk:** low
- **Path:** `integration/skill-pack-install`
- **Aliases:** `install-profile`, `install-pack`, `role-bundle`
- **Triggers:**
  - install the backend profile
  - add the ai engineer pack
  - give this agent a role bundle
- **Source:** custom
- **Version:** 1.0.0

A role needs a coherent set of skills, not a directory dump. Packs and profiles resolve to a minimal, dependency-closed set, so an agent gets exactly the playbooks its job needs and nothing else competing for context.

### `integration.third-party-api-resilience`

Harden integrations with external APIs: timeouts, retry budgets, circuit breaking, rate-limit awareness, caching and graceful degradation.

- **Risk:** medium
- **Path:** `integration/third-party-api-resilience`
- **Aliases:** —
- **Triggers:**
  - third party api timeout
  - retry storm
  - circuit breaker design
  - rate limit handling
  - external api degradation
- **Source:** custom
- **Version:** 1.0.0

Harden integrations with external APIs: timeouts, retry budgets, circuit breaking, rate-limit awareness, caching and graceful degradation.

### `integration.universal-skill-discovery`

Find the right skill across canonical skills, the 15k-entry catalog and imported upstream sources, then install it or publish a new one with provenance intact.

- **Risk:** low
- **Path:** `integration/universal-skill-discovery`
- **Aliases:** `find-a-skill`, `skill-search`, `publish-skill`
- **Triggers:**
  - is there a skill for this
  - find a skill that does X
  - publish my skill
- **Source:** custom
- **Version:** 1.0.0

There are three layers to search — 492 canonical skills, the active harness set, and a 15k catalog of imported skills — and they answer different questions. This skill routes a task, explains why a skill won, and installs it with its provenance and license intact.

### `integration.webhook-delivery-design`

Design reliable outbound webhooks: signed payloads, retries with backoff, idempotent consumers, replay and delivery observability.

- **Risk:** medium
- **Path:** `integration/webhook-delivery-design`
- **Aliases:** —
- **Triggers:**
  - webhook signature verification
  - webhook retry backoff
  - webhook idempotency
  - webhook replay
  - webhook delivery monitoring
- **Source:** custom
- **Version:** 1.0.0

Design reliable outbound webhooks: signed payloads, retries with backoff, idempotent consumers, replay and delivery observability.

