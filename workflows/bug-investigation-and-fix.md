# Bug Investigation & Fix Workflow Playbook

> **Target Objective**: Eliminate bugs systematically without guess-and-check edits or introducing regression side-effects.

---

## Workflow Sequence

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              BUG INVESTIGATION & RESOLUTION                            │
├─────────────────┬──────────────────┬─────────────────┬────────────────┬────────────────┤
│ 1. ROOT-CAUSE   │ 2. MINIMAL REPRO │ 3. AST SAFE FIX │ 4. REGRESSION  │ 5. POST-FIX    │
│    ISOLATION    │    TEST HARNESS  │    APPLICATION  │    VERIFICATION│    SELF-AUDIT  │
├─────────────────┼──────────────────┼─────────────────┼────────────────┼────────────────┤
│ systematic-     │ scratch/         │ ast-code-       │ verify_tests   │ requesting-    │
│ debugging       │ repro.py         │ transformation  │ & skills test  │ code-review    │
└─────────────────┴──────────────────┴─────────────────┴────────────────┴────────────────┘
```

---

## Phase 1: 4-Phase Root-Cause Analysis
- **Primary Skill**: [`.agents/skills/code-showcase-systematic-debugging/SKILL.md`](../.agents/skills/code-showcase-systematic-debugging/SKILL.md)
- **Rule**: NO FIXES WITHOUT ROOT CAUSE FIRST. Do not blindly edit lines hoping tests pass.
- **Actions**:
  1. Initialize bug fix state: `python scripts/manage_state.py init bug-fix`.
  2. **Isolate**: Identify the exact failing boundary, inputs, and error stack trace.
  3. **Trace**: Trace backward from error site through call graph to find where state diverged.
  4. **Hypothesize**: Formulate a falsifiable hypothesis explaining why the bug occurs.
- **Exit Gate**: Hypothesis validated with trace evidence.

---

## Phase 2: Isolated Minimal Reproduction
- **Rule**: Build a standalone reproduction script or failing unit test before modifying production code.
- **Actions**:
  1. Write a minimal reproduction script under `scratch/reproduce_issue.py`.
  2. Run script and confirm it reproduces the exact reported failure.
  3. Convert script into a permanent automated regression test in `tests/`.
- **Exit Gate**: A failing test that asserts the bug cleanly.

---

## Phase 3: AST-Safe Code Modification
- **Primary Skill**: [`.agents/skills/ast-code-transformation/SKILL.md`](../.agents/skills/ast-code-transformation/SKILL.md)
- **Actions**:
  1. Apply the targeted fix using AST-aware tools or block replacement with $\ge 3$ lines of surrounding unique syntactic context.
  2. Run AST validation check immediately:
     ```bash
     python -m py_compile <modified_file.py>
     ```
- **Exit Gate**: Bug is fixed, syntax checks pass, and reproduction test now passes (Green).

---

## Phase 4: Full Regression Testing
- **Actions**:
  1. Run the entire platform test suite:
     ```bash
     python scripts/run_hook.py post active.tdd
     ```
  2. Verify edge cases (null values, network timeouts, invalid types).
- **Exit Gate**: 100% of existing tests continue to pass.

---

## Phase 5: Self-Audit & Patch Summary
- **Primary Skill**: [`.agents/skills/requesting-code-review/SKILL.md`](../.agents/skills/requesting-code-review/SKILL.md)
- **Actions**:
  1. Summarize:
     - Root cause explanation.
     - Files modified and rationale.
     - Reproduction test added.
  2. Update `aas-stack.json`:
     ```bash
     python scripts/manage_state.py step 5 --status completed
     python scripts/manage_state.py sync-context
     ```
