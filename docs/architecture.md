# All-Skills Universal Platform Architecture

This document outlines the complete architectural design of the **All-Skills Universal Platform**, integrating multi-turn conversational NLP, multimodal perception, system automation, agent reasoning, and deterministic priority execution.

---

## 1. System Topology

```
                                 ┌─────────────────────────┐
                                 │   MULTIMODAL INTERFACES │
                                 │ (CLI, Voice, Web, API)  │
                                 └────────────┬────────────┘
                                              │
                                              ▼
                                 ┌─────────────────────────┐
                                 │     INPUT ADAPTERS      │
                                 │ (Text, Audio, Vision)   │
                                 └────────────┬────────────┘
                                              │
                                              ▼
    ┌───────────────────────┐    ┌─────────────────────────┐    ┌───────────────────────┐
    │   MEMORY SUBSYSTEM    │◄───┤   COGNITIVE PIPELINE    │───►│    EVENT BUS & PUB    │
    │  Short-term / Buffer  │    │  (Intent → Skill → Out) │    │  Cross-skill messages │
    │  Long-term / Vectors  │    └────────────┬────────────┘    └───────────────────────┘
    │  Episodic / Events    │                 │
    └───────────────────────┘                 ▼
                                 ┌─────────────────────────┐
                                 │ SCRATCH PRIORITY IMPORT │
                                 │ Priority 1-100 & Cycles │
                                 └────────────┬────────────┘
                                              │
                                              ▼
                                 ┌─────────────────────────┐
                                 │   24 SKILL CATEGORIES   │
                                 │ (Conversational, Vision,│
                                 │  Speech, Robotics, etc.)│
                                 └────────────┬────────────┘
                                              │
                                              ▼
                                 ┌─────────────────────────┐
                                 │     OUTPUT ADAPTERS     │
                                 │ (Speech, Cards, Action) │
                                 └─────────────────────────┘
```

---

## 2. Seven Architectural Principles

1. **Self-Contained Modules**: Every skill exports `can_handle(intent)`, `handle(intent, context)`, and `get_priority()`.
2. **Zero Direct Imports**: Skills never import other skills directly; communication passes through the `EventBus` or `SkillManager`.
3. **Declared Dependencies**: Dependencies are formally tracked in `scratch_priority_import/skill_manifest.yaml` for topological sorting.
4. **Lazy Loading**: Heavy vision, STT, and LLM models load on first use rather than startup.
5. **Universal Fallback**: All skills feature graceful degradation if upstream APIs or weights are unavailable.
6. **Isolated Requirements**: Each skill category maintains an isolated `requirements.txt`.
7. **Priority Backbone**: `scratch_priority_import/` governs execution ranks, conflict resolution, and deterministic scheduling.
