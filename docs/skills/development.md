# Development Skills

_Generated: 2026-09-19T17:27:28+00:00_

Skills for software engineering work — coding, debugging, refactoring, code review, testing, TDD, architecture, frontend, backend, databases, Git, GitHub, performance optimization, and DevOps. These skills produce structured output (checklists, prompts, plans) rather than execute code.

**38 skills in this category.**

## Skills

### `development.api-mock-generator`

Derive API mocks and contract tests from schemas or observed interfaces without inventing behavior.

- **Risk:** low
- **Path:** `development/api-mock-generator`
- **Aliases:** `api`, `mock`, `test`, `contract`, `openapi`, `swagger`
- **Triggers:**
  - Generate API mocks
  - Create mock API
  - API testing
  - Mock endpoints
- **Source:** custom
- **Version:** 1.0.0

Generate API mocks and contract tests from OpenAPI schemas or observed interfaces. The skill ensures mocks accurately reflect the API contract without inventing behavior beyond the specification.

### `development.architecture`

Design and review software architecture — modules, boundaries, data flow, dependencies, and trade-offs.

- **Risk:** low
- **Path:** `development/architecture`
- **Aliases:** `system-design`, `design`, `architect`, `modular`
- **Triggers:**
  - how should I structure this
  - design the architecture
  - system design
  - architect this
  - pick a tech stack
  - module boundaries
- **Source:** custom
- **Version:** 1.0.0

Help the user make structural decisions about software: module boundaries, data flow, dependency choices, and trade-offs. Produce diagrams-in-prose and concrete recommendations.

### `development.autoreview`

Run an explicitly requested structured second-model code review and verify findings before changes.

- **Risk:** low
- **Path:** `development/autoreview`
- **Aliases:** —
- **Triggers:**
  - use autoreview
  - run autoreview
- **Source:** custom
- **Version:** 1.0.0

Run an explicitly requested structured second-model code review and verify findings before changes.

### `development.backend`

Build backend services — APIs, server logic, persistence, queues, and integration with other systems.

- **Risk:** low
- **Path:** `development/backend`
- **Aliases:** `server`, `api-server`, `backend-dev`
- **Triggers:**
  - build a backend
  - backend dev
  - write an API
  - server side
- **Source:** custom
- **Version:** 1.0.0

Build and reason about backend services: HTTP APIs, persistence, async work, authentication, and integration with other systems.

### `development.behavior-validator`

Validate user-visible behavior against a written contract without inspecting implementation source.

- **Risk:** low
- **Path:** `development/behavior-validator`
- **Aliases:** —
- **Triggers:**
  - use behavior-validator
  - run behavior-validator
- **Source:** custom
- **Version:** 1.0.0

Validate user-visible behavior against a written contract without inspecting implementation source.

### `development.brainstorming`

Clarify intent and turn software ideas into approved designs before implementation.

- **Risk:** low
- **Path:** `development/brainstorming`
- **Aliases:** `design-first`, `requirements-discovery`, `software-ideation`
- **Triggers:**
  - brainstorm this feature
  - help design this change
- **Source:** obra/superpowers
- **Version:** 1.0.0

Clarify intent and turn software ideas into approved designs before implementation. The reviewed upstream workflow is preserved in `references/upstream-SKILL.md`.

### `development.cf-worker-deploy`

Validate and deploy Cloudflare Workers with preview, secret, and rollback safeguards.

- **Risk:** high
- **Path:** `development/cf-worker-deploy`
- **Aliases:** `cloudflare`, `worker`, `cf`, `edge`
- **Triggers:**
  - Deploy to Cloudflare Workers
  - Publish worker
  - Cloudflare deployment
  - Update worker
- **Source:** custom
- **Version:** 1.0.0

Validate and deploy Cloudflare Workers with proper preview testing, secret management, and rollback capabilities. The skill ensures safe deployments with minimal disruption.

### `development.ci-cd-pipeline`

Design, audit, and optimize CI/CD pipelines with build caching, test parallelism, secret boundaries, and automated gates.

- **Risk:** low
- **Path:** `development/ci-cd-pipeline`
- **Aliases:** `github-actions-pipeline`, `ci-cd-workflow`, `continuous-integration`, `pipeline-builder`
- **Triggers:**
  - build a CI/CD pipeline
  - create GitHub Actions workflow
  - optimize build pipeline caching
  - audit CI security and test stages
  - automate deployment pipeline
- **Source:** custom
- **Version:** 1.0.0

Designs, implements, audits, and accelerates Continuous Integration and Continuous Deployment (CI/CD) pipelines. Maximizes test parallelism and build caching while strictly preserving secret isolation and deployment gates.

### `development.code-review`

Review code for correctness, readability, design, tests, security, and style. Produce actionable, kind, prioritized feedback.

- **Risk:** low
- **Path:** `development/code-review`
- **Aliases:** `review`, `pr-review`, `peer-review`
- **Triggers:**
  - review this code
  - review my PR
  - code review
  - look at this diff
  - is this code good
- **Source:** custom
- **Version:** 1.0.0

Provide a thorough, prioritized, kind code review covering correctness, design, readability, tests, and security. Output is structured, actionable feedback — not a rewrite.

### `development.coding`

General-purpose software engineering assistant: implement features, write functions, scaffold projects, and produce idiomatic code in many languages.

- **Risk:** low
- **Path:** `development/coding`
- **Aliases:** `programming`, `software-engineering`, `implement`, `write-code`, `build-feature`
- **Triggers:**
  - write this code
  - implement this
  - code this up
  - help me code
  - build a function
  - write a script
  - implement this feature
- **Source:** custom
- **Version:** 1.0.0

Help the user write, modify, and reason about code in any language. Focus on idiomatic, testable, readable code with clear interfaces.

### `development.coding-agent`

Delegate bounded coding work to an installed coding-agent CLI with explicit scope and verification.

- **Risk:** medium
- **Path:** `development/coding-agent`
- **Aliases:** `codex`, `claude-code`, `headless-agent`, `ai-coding`, `autopilot`
- **Triggers:**
  - Run the coding agent
  - Use Codex
  - Use Claude Code
  - Spin up an agent to fix this
  - Hand this off to an agent
- **Source:** custom
- **Version:** 1.0.0

Launch, monitor, and inspect a headless coding agent (Codex CLI, Claude Code, OpenCode, or Pi) as a managed background process. The skill turns "do this fix in another process" into a single call with deterministic start, streaming output, and clean shutdown.

### `development.crabbox`

Coordinate isolated remote or clean-machine validation while preserving trust and credential boundaries.

- **Risk:** low
- **Path:** `development/crabbox`
- **Aliases:** —
- **Triggers:**
  - use crabbox
  - run crabbox
- **Source:** custom
- **Version:** 1.0.0

Coordinate isolated remote or clean-machine validation while preserving trust and credential boundaries.

### `development.cursor-agent`

Use Cursor Agent safely for bounded software tasks without unattended destructive actions.

- **Risk:** medium
- **Path:** `development/cursor-agent`
- **Aliases:** `cursor`, `cursor-cli`, `ai-ide`, `agent`
- **Triggers:**
  - Use Cursor
  - Run the Cursor agent
  - Hand this to Cursor
  - Cursor CLI
- **Source:** custom
- **Version:** 1.0.0

Drive the **Cursor CLI agent** (`agent`, formerly `cursor-agent`) from a non-interactive shell, using tmux so the same session can be inspected, taken over, or detached. The skill wraps prompt construction, model selection, and result capture in a single operation that any other skill or tool can call.

### `development.databases`

Work with databases — schema design, queries, indexing, migrations, and selecting the right store.

- **Risk:** medium
- **Path:** `development/databases`
- **Aliases:** `sql`, `nosql`, `schema`, `migrations`
- **Triggers:**
  - design a database schema
  - write a migration
  - optimize this query
  - pick a database
- **Source:** custom
- **Version:** 1.0.0

Help the user with databases: design schemas, write queries, plan migrations, optimize performance, and choose the right store for the workload.

### `development.db-inspector`

Inspect database schemas and queries read-only by default and explain performance or safety risks.

- **Risk:** medium
- **Path:** `development/db-inspector`
- **Aliases:** `database`, `db`, `query`, `inspect`, `mysql`, `postgres`
- **Triggers:**
  - Check database schema
  - Inspect this database
  - Run a query
  - Database structure
  - Explain this query
- **Source:** custom
- **Version:** 1.0.0

Inspect database schemas, run queries, and explain execution plans with read-only defaults and clear risk indicators. The skill helps developers understand database structure and optimize queries while preventing accidental modifications.

### `development.debugging`

Systematically diagnose and fix bugs using reproduction, isolation, root-cause analysis, and verification.

- **Risk:** low
- **Path:** `development/debugging`
- **Aliases:** `debug`, `fix-bug`, `troubleshoot`, `diagnose`
- **Triggers:**
  - this isn't working
  - help me debug
  - find the bug
  - why is this failing
  - I have a bug
  - something is broken
  - trace this error
- **Source:** custom
- **Version:** 1.0.0

Move from "this is broken" to a verified fix via structured debugging: reproduce, isolate, form a hypothesis, test it, and verify.

### `development.devops`

DevOps practices — CI/CD, infrastructure, deployment, observability, and incident response.

- **Risk:** medium
- **Path:** `development/devops`
- **Aliases:** `ci-cd`, `deploy`, `sre`, `ops`
- **Triggers:**
  - set up CI
  - deploy this
  - infrastructure help
  - CI/CD
  - devops
- **Source:** custom
- **Version:** 1.0.0

Help the user with DevOps: CI/CD pipelines, infrastructure-as-code, deployments, observability, and incident response.

### `development.docker-manager`

Inspect and manage Docker resources with read-only defaults and confirmation for mutations.

- **Risk:** high
- **Path:** `development/docker-manager`
- **Aliases:** `docker`, `container`, `image`, `compose`, `podman`
- **Triggers:**
  - List docker containers
  - Tail container logs
  - Restart this container
  - Prune docker
  - Build this image
- **Source:** custom
- **Version:** 1.0.0

Make common Docker operations safe and scriptable for an agent: list, inspect, run, build, prune, and (with explicit confirmation) destroy. The skill defaults to **read or report** mode; any state change is gated by an `--apply` flag.

### `development.dokploy`

Inspect and manage Dokploy deployments through its API with explicit confirmation for mutations.

- **Risk:** high
- **Path:** `development/dokploy`
- **Aliases:** `hosting`, `self-host`
- **Triggers:**
  - Deploy to Dokploy
  - Restart the app on Dokploy
  - Add a domain
  - List projects on Dokploy
- **Source:** custom
- **Version:** 1.0.0

Drive a **Dokploy** instance (self-hosted PaaS) through its REST API: list, create, update, deploy, and roll back projects, applications, and domains. The skill is careful to surface every destructive operation and never assume a default environment.

### `development.frontend`

Build frontend applications — frameworks, state management, routing, data fetching, and integration with APIs.

- **Risk:** low
- **Path:** `development/frontend`
- **Aliases:** `frontend-dev`, `web-app`, `react-vue-svelte`
- **Triggers:**
  - build a frontend
  - frontend dev
  - build a web app
  - help with react
- **Source:** custom
- **Version:** 1.0.0

Build and reason about frontend applications: framework choice, state management, routing, data fetching, performance, and accessibility.

### `development.git`

Use git effectively — commits, branches, rebases, merges, conflict resolution, history surgery, and common workflows.

- **Risk:** medium
- **Path:** `development/git`
- **Aliases:** `version-control`, `source-control`, `vcs`
- **Triggers:**
  - git help
  - how do I use git
  - help me commit
  - resolve this merge conflict
  - git rebase
  - git workflow
  - undo this commit
- **Source:** custom
- **Version:** 1.0.0

Help the user with git: commits, branching strategies, history, conflict resolution, and recovery from mistakes.

### `development.git-workflow`

Guide safe commits, branches, pushes, and pull requests while preserving uncommitted work.

- **Risk:** medium
- **Path:** `development/git-workflow`
- **Aliases:** `git`, `commit`, `conventional-commits`, `push`
- **Triggers:**
  - Commit this
  - Open a PR
  - Push my branch
  - Use a conventional commit message
  - Sign my commits
- **Source:** custom
- **Version:** 1.0.0

Wrap the local Git cycle (stage â†’ commit â†’ push â†’ PR) into a single, opinionated operation. The skill enforces **conventional commits**, optional GPG/SSH signing, and assembles a useful PR body from the commit log and any issue context.

### `development.git-worktrees`

Create isolated Git workspaces safely while preserving current work and verifying a clean baseline.

- **Risk:** medium
- **Path:** `development/git-worktrees`
- **Aliases:** `worktree`, `isolated-branch`, `parallel-branch`
- **Triggers:**
  - create a git worktree
  - work in an isolated branch
- **Source:** obra/superpowers
- **Version:** 1.0.0

Create isolated Git workspaces safely while preserving current work and verifying a clean baseline. The reviewed upstream workflow is preserved in `references/upstream-SKILL.md`.

### `development.github`

Work with GitHub — pull requests, issues, Actions, code review, project boards, releases.

- **Risk:** medium
- **Path:** `development/github`
- **Aliases:** `pr`, `pull-request`, `issue`, `gh`, `github-actions`
- **Triggers:**
  - open a PR
  - create an issue
  - github actions
  - help with GitHub
  - review a PR
- **Source:** custom
- **Version:** 1.0.0

Operate on GitHub: pull requests, issues, Actions workflows, releases, project boards, and code review etiquette.

### `development.github-cli`

Use GitHub CLI for issues, pull requests, Actions, and API queries with confirmation for writes.

- **Risk:** medium
- **Path:** `development/github-cli`
- **Aliases:** `github`, `gh-cli`
- **Triggers:**
  - Open a PR
  - List my issues
  - Check the CI run
  - Create a release
  - Use the GitHub API
- **Source:** custom
- **Version:** 1.0.0

Run common GitHub operations through the `gh` CLI in a way that is safe, scriptable, and ergonomic for an agent. The skill wraps `gh issue`, `gh pr`, `gh run`, `gh release`, and `gh api` into named, audited operations.

### `development.issue-triage`

Classify, deduplicate, label, and prioritize incoming issues with reproduction checklists and routing rules.

- **Risk:** low
- **Path:** `development/issue-triage`
- **Aliases:** `triage-issues`, `bug-triage`, `issue-classifier`, `issue-routing`
- **Triggers:**
  - triage incoming issues
  - classify this bug report
  - prioritize GitHub issues
  - label and route this issue
  - check issue for reproduction steps
- **Source:** custom
- **Version:** 1.0.0

Systematically triages, validates, categorizes, and routes incoming GitHub issues and bug reports. Ensures reproducible bugs are fast-tracked, duplicates are consolidated, and missing environment details are immediately requested.

### `development.mcp-builder`

Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. Use when building MCP servers to integrate external APIs or services, whether in Python (FastMCP) or Node/TypeScript (MCP SDK).

- **Risk:** medium
- **Path:** `development/mcp-builder`
- **Aliases:** `mcp-scaffold`, `mcp-sdk`, `custom-mcp`
- **Triggers:**
  - build an MCP server
  - create MCP tools
  - integrate an API as MCP
  - MCP server
  - model context protocol
- **Source:** anthropics/skills
- **Version:** 1.1.0

Create MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. The quality of an MCP server is measured by how well it enables LLMs to accomplish real-world tasks.

### `development.mcp-server-development`

Design and implement discoverable, safe Model Context Protocol servers and evaluations.

- **Risk:** medium
- **Path:** `development/mcp-server-development`
- **Aliases:** `mcp-builder`, `model-context-protocol`, `mcp-server`
- **Triggers:**
  - build an MCP server
  - create MCP tools for this API
- **Source:** anthropics/skills
- **Version:** 1.0.0

Design and implement discoverable, safe Model Context Protocol servers and evaluations. The reviewed upstream workflow is preserved in `references/upstream-SKILL.md`.

### `development.performance-optimization`

Find and fix performance bottlenecks — profiling, measurement, and targeted optimization.

- **Risk:** low
- **Path:** `development/performance-optimization`
- **Aliases:** `perf`, `profiling`, `bottleneck`, `speed-up`
- **Triggers:**
  - this is slow
  - profile this
  - find the bottleneck
  - speed this up
  - performance optimization
- **Source:** custom
- **Version:** 1.0.0

Identify performance bottlenecks via measurement and fix them with targeted changes.

### `development.pr-splitter`

Decompose large, complex pull requests into atomic, logically isolated, reviewable PR branches.

- **Risk:** low
- **Path:** `development/pr-splitter`
- **Aliases:** `split-pr`, `atomic-pr`, `decompose-pr`, `pr-slice`
- **Triggers:**
  - split this PR
  - break down large pull request
  - decompose PR into smaller chunks
  - make this PR reviewable
  - slice this diff
- **Source:** custom
- **Version:** 1.0.0

Decomposes large, monolithic diffs and pull requests into small, atomic, reviewable PR branches. This accelerates code review velocity, reduces merge conflicts, and isolates regression risks.

### `development.receiving-code-review`

Evaluate code-review feedback technically before accepting, rejecting, or implementing it.

- **Risk:** low
- **Path:** `development/receiving-code-review`
- **Aliases:** `review-feedback`, `address-review`, `respond-to-review`
- **Triggers:**
  - address this review feedback
  - is this reviewer correct
- **Source:** obra/superpowers
- **Version:** 1.0.0

Evaluate code-review feedback technically before accepting, rejecting, or implementing it. The reviewed upstream workflow is preserved in `references/upstream-SKILL.md`.

### `development.refactoring`

Improve the internal structure of existing code without changing external behavior — naming, decomposition, clarity, duplication removal.

- **Risk:** low
- **Path:** `development/refactoring`
- **Aliases:** `refactor`, `clean-up`, `simplify`, `restructure`
- **Triggers:**
  - refactor this
  - clean up this code
  - simplify this
  - rename this
  - extract a function
  - make this clearer
- **Source:** custom
- **Version:** 1.0.0

Improve code structure without changing behavior. Extract functions, rename for clarity, remove duplication, and reorganize for the next reader.

### `development.release-management`

Coordinate end-to-end software releases with semantic versioning, automated changelogs, tag verification, and rollbacks.

- **Risk:** low
- **Path:** `development/release-management`
- **Aliases:** `release-workflow`, `release-coordinator`, `semantic-release`, `cut-release`
- **Triggers:**
  - cut a new release
  - manage release workflow
  - generate release notes and tag
  - prepare semantic version bump
  - coordinate production release
- **Source:** custom
- **Version:** 1.0.0

Orchestrates disciplined, repeatable software release lifecycles. Automates semantic version calculation, changelog generation, release tagging, artifact verification, and deployment rollback checklists.

### `development.requesting-code-review`

Prepare a focused, evidence-based request for code review before integration.

- **Risk:** low
- **Path:** `development/requesting-code-review`
- **Aliases:** `request-review`, `pre-merge-review`, `review-request`
- **Triggers:**
  - request a code review
  - prepare this for review
- **Source:** obra/superpowers
- **Version:** 1.0.0

Prepare a focused, evidence-based request for code review before integration. The reviewed upstream workflow is preserved in `references/upstream-SKILL.md`.

### `development.summarize-repo`

Produce an evidence-based codebase map covering architecture, entry points, dependencies, and risks.

- **Risk:** low
- **Path:** `development/summarize-repo`
- **Aliases:** `summarize`, `repo-overview`, `codebase-summary`, `on boarding`
- **Triggers:**
  - Summarize this repo
  - What is this project
  - Give me an overview
  - Onboard me to this codebase
- **Source:** custom
- **Version:** 1.0.0

Read a repository and produce a **single, scannable summary** that answers: *what is this, what stack, where is the entry point, where is the work done, and how do I run it*. The output is shaped to onboard a new contributor in five minutes.

### `development.tdd`

Test-Driven Development discipline — red/green/refactor cycles for designing code from tests outward.

- **Risk:** low
- **Path:** `development/tdd`
- **Aliases:** `test-driven`, `red-green-refactor`
- **Triggers:**
  - let's do TDD
  - test first
  - red green refactor
  - write the test first
- **Source:** custom
- **Version:** 1.0.0

Apply TDD discipline: write a failing test first, make it pass with the simplest code, then refactor. Use TDD when it improves design feedback, not as religion.

### `development.testing`

Design and write automated tests (unit, integration, end-to-end) using TDD where appropriate.

- **Risk:** low
- **Path:** `development/testing`
- **Aliases:** `tdd`, `unit-test`, `integration-test`, `write-tests`, `test-coverage`
- **Triggers:**
  - write tests for this
  - add tests
  - how do I test this
  - TDD
  - test coverage
  - unit test this
- **Source:** custom
- **Version:** 1.0.0

Design and write automated tests that catch real bugs and document intended behavior. Choose the right level of test for each concern.

### `development.verification-before-completion`

Require fresh evidence before claiming that implementation work is complete or correct.

- **Risk:** low
- **Path:** `development/verification-before-completion`
- **Aliases:** `verify-completion`, `evidence-before-claims`, `done-check`
- **Triggers:**
  - verify this is done
  - can I call this complete
- **Source:** obra/superpowers
- **Version:** 1.0.0

Require fresh evidence before claiming that implementation work is complete or correct. The reviewed upstream workflow is preserved in `references/upstream-SKILL.md`.

