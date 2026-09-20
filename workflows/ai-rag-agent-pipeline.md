# AI RAG & Agent Pipeline Workflow Playbook

> **Target Objective**: Architect, develop, test, and evaluate production-grade Model Context Protocol (MCP) servers, hybrid RAG pipelines, and multi-agent coordination graphs.

---

## Workflow Sequence

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              AI RAG & AGENT PIPELINE FLOW                              │
├─────────────────┬──────────────────┬─────────────────┬────────────────┬────────────────┤
│ 1. CONTEXT      │ 2. MCP TOOL      │ 3. MEMORY &     │ 4. MULTI-AGENT │ 5. EVALUATION  │
│    BUDGETING    │    BUILDING      │    RAG STORAGE  │    ORCHESTRATE │    HARNESS     │
├─────────────────┼──────────────────┼─────────────────┼────────────────┼────────────────┤
│ context-budget- │ mcp-builder &    │ agent-memory &  │ multi-agent-   │ agent-eval &   │
│ and-pruning     │ tool-developer   │ ai-engineer     │ architect      │ ai-engineering │
└─────────────────┴──────────────────┴─────────────────┴────────────────┴────────────────┘
```

---

## Phase 1: Context Budgeting & Token Limits
- **Primary Skills**: [`.agents/skills/context-budget-and-pruning/SKILL.md`](../.agents/skills/context-budget-and-pruning/SKILL.md) & [`.agents/skills/context-window-management/SKILL.md`](../.agents/skills/context-window-management/SKILL.md)
- **Actions**:
  1. Define token budget allocation: System Prompt (10%) + Retrieved Context (40%) + Tool Definitions (10%) + Scratchpad (40%).
  2. Implement truncation and sliding-window strategies for history persistence.
  3. Enforce scratchpad offloading for multi-turn workflows.
- **Exit Gate**: Context budget model validated against target LLM limits.

---

## Phase 2: MCP Server & Tool Development
- **Primary Skills**: [`.agents/skills/mcp-builder/SKILL.md`](../.agents/skills/mcp-builder/SKILL.md) & [`.agents/skills/mcp-tool-developer/SKILL.md`](../.agents/skills/mcp-tool-developer/SKILL.md)
- **Actions**:
  1. Define tools with strict JSON schemas, unambiguous argument descriptions, and required fields.
  2. Implement error handling that returns structured error strings rather than crashing the process.
  3. Register servers in `mcp_config.json`.
- **Exit Gate**: MCP server boots, passes inspector checks, and handles malformed parameters gracefully.

---

## Phase 3: Hybrid Memory & Vector RAG Pipeline
- **Primary Skills**: [`.agents/skills/agent-memory/SKILL.md`](../.agents/skills/agent-memory/SKILL.md) & [`.agents/skills/ai-engineer/SKILL.md`](../.agents/skills/ai-engineer/SKILL.md)
- **Actions**:
  1. Set up hybrid retrieval combining dense vector embeddings with sparse BM25 keyword matching.
  2. Implement reciprocal rank fusion (RRF) and reranking models.
  3. Configure persistent episodic memory and cross-session entity extraction.
- **Exit Gate**: Document ingestion verified, retrieval precision @ k > 85%.

---

## Phase 4: Multi-Agent Orchestration
- **Primary Skills**: [`.agents/skills/multi-agent-architect/SKILL.md`](../.agents/skills/multi-agent-architect/SKILL.md) & [`.agents/skills/multi-agent-patterns/SKILL.md`](../.agents/skills/multi-agent-patterns/SKILL.md)
- **Actions**:
  1. Design agent topology (Supervisor-Worker, Sequential Handoff, or Swarm).
  2. Enforce context isolation between child agents to prevent token explosion.
  3. Implement deterministic stopping conditions and loop guards.
- **Exit Gate**: End-to-end multi-agent run completes with deterministic handoffs.

---

## Phase 5: Evaluation Harness & Benchmark
- **Primary Skills**: [`.agents/skills/agent-evaluation/SKILL.md`](../.agents/skills/agent-evaluation/SKILL.md) & [`.agents/skills/ai-engineering-toolkit/SKILL.md`](../.agents/skills/ai-engineering-toolkit/SKILL.md)
- **Actions**:
  1. Run automated test suite against versioned gold-standard evaluation cases.
  2. Measure accuracy, latency, token consumption, and hallucination rate.
  3. Log evaluation scores into `aas-stack.json`:
     ```bash
     python scripts/manage_state.py step 5 --status completed
     python scripts/manage_state.py sync-context
     ```
- **Exit Gate**: Evaluation scores exceed quality threshold across all test suites.
