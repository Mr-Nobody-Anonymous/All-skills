# 🧠 Agent State Management & Memory Hierarchy (`state/`)

Separates short-term working context from persistent episodic and semantic knowledge:

```
state/
├── session/    # Current execution session variables and ephemeral scratchpads
├── project/    # Workspace-level settings, technology stacks, and invariants
├── task/       # Atomic task goals, checklists, and active execution step
├── workflow/   # Multi-stage DAG progress, checkpoints, and resume tokens
├── agent/      # Agent persona, assigned role, and tool permission scopes
├── user/       # User preferences, autonomy confirmations, and feedback history
├── memory/     # Long-term semantic knowledge and episodic interaction records
└── audit/      # Immutable audit trail of completed tool calls and file mutations
```
