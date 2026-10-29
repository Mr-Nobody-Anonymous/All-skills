# Agents Skills

_Generated: 2026-10-29T14:02:53+00:00_



**4 skills in this category.**

## Skills

### `agents.agent-observability`

Instrument agent runs: trace structure for tool calls and model turns, token and cost accounting, latency budgets, and searchable logs that explain a bad answer.

- **Risk:** low
- **Path:** `agents/agent-observability`
- **Aliases:** `agent-tracing`
- **Triggers:**
  - trace agent tool calls
  - agent token cost tracking
  - agent latency budget
  - log llm agent run
  - debug agent failure
- **Source:** custom
- **Version:** 1.0.0

Instrument agent runs: trace structure for tool calls and model turns, token and cost accounting, latency budgets, and searchable logs that explain a bad answer.

### `agents.agent-reliability`

Make agents reliable under failure: retries with jitter, timeouts per tool, idempotency, checkpointing, loop detection and graceful degradation.

- **Risk:** medium
- **Path:** `agents/agent-reliability`
- **Aliases:** `agent-resilience`
- **Triggers:**
  - agent stuck in loop
  - tool call retry policy
  - agent timeout handling
  - agent partial failure recovery
  - make agent deterministic
- **Source:** custom
- **Version:** 1.0.0

Make agents reliable under failure: retries with jitter, timeouts per tool, idempotency, checkpointing, loop detection and graceful degradation.

### `agents.human-in-the-loop-design`

Design human approval into agent workflows: risk-tiered gates, reviewable diffs, timeout and escalation policy, audit trail and reversible actions.

- **Risk:** medium
- **Path:** `agents/human-in-the-loop-design`
- **Aliases:** `hitl`
- **Triggers:**
  - agent approval gate
  - human in the loop design
  - agent escalation policy
  - approve before destructive action
  - agent audit trail
- **Source:** custom
- **Version:** 1.0.0

Design human approval into agent workflows: risk-tiered gates, reviewable diffs, timeout and escalation policy, audit trail and reversible actions.

### `agents.mcp-integration-testing`

Test MCP servers and their integrations: tool-schema contracts, transport handshakes, failure and timeout behaviour, permission scoping and end-to-end agent runs.

- **Risk:** medium
- **Path:** `agents/mcp-integration-testing`
- **Aliases:** `mcp-testing`
- **Triggers:**
  - test mcp server
  - mcp tool schema validation
  - mcp server timeout handling
  - mcp integration test harness
  - verify mcp connector works
- **Source:** custom
- **Version:** 1.0.0

Test MCP servers and their integrations: tool-schema contracts, transport handshakes, failure and timeout behaviour, permission scoping and end-to-end agent runs.

