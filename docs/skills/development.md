# Development Skills

_Generated: 2026-09-02T04:38:48+00:00_

Skills for software engineering work — coding, debugging, refactoring, code review, testing, TDD, architecture, frontend, backend, databases, Git, GitHub, performance optimization, and DevOps. These skills produce structured output (checklists, prompts, plans) rather than execute code.

**21 skills in this category.**

## Skills

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

### `development.brainstorming`

Clarify intent and turn software ideas into approved designs before implementation.

- **Risk:** low
- **Path:** `development/brainstorming`
- **Aliases:** `design-first`, `requirements-discovery`, `ideation`
- **Triggers:**
  - brainstorm this feature
  - help design this change
- **Source:** obra/superpowers
- **Version:** 1.0.0

Clarify intent and turn software ideas into approved designs before implementation. The reviewed upstream workflow is preserved in `references/upstream-SKILL.md`.

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

### `development.mcp-builder`

Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. Use when building MCP servers to integrate external APIs or services, whether in Python (FastMCP) or Node/TypeScript (MCP SDK).

- **Risk:** medium
- **Path:** `development/mcp-builder`
- **Aliases:** `mcp`, `model-context-protocol`, `mcp-server`
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

