# Feature Development Workflow Playbook

> **Target Objective**: Guide an autonomous agent through the end-to-end development of a major feature, ensuring high architectural clarity, complete test coverage, zero regression, and polished documentation.

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   FEATURE DEVELOPMENT FLOW                                             │
├───────────────┬────────────────┬────────────────┬───────────────┬───────────────┬──────────────────────┤
│ 1. BRAINSTORM │ 2. GRANULAR    │ 3. API & TYPE  │ 4. TDD CYCLES │ 5. CODE REVIEW│ 6. CHANGELOG         │
│ & INVARIANTS  │    PLANNING    │    CONTRACTS   │    & AST FIX  │    & CLEANUP  │    & STAGE           │
├───────────────┼────────────────┼────────────────┼───────────────┼───────────────┼──────────────────────┤
│ brainstorming │concise-planning│api-and-        │ tdd &         │ code-reviewer │ changelog-automation │
│               │                │interface-design│ ast-transform │ & simplify    │                      │
└───────────────┴────────────────┴────────────────┴───────────────┴───────────────┴──────────────────────┘
```

---

## Phase 1: Requirements Refinement & Invariants
- **Primary Skill**: [`.agents/skills/brainstorming/SKILL.md`](../.agents/skills/brainstorming/SKILL.md)
- **Actions**:
  1. Initialize workflow state: `python scripts/manage_state.py init feature-development`.
  2. Snapshot baseline commit: `python scripts/run_hook.py pre active.brainstorming`.
  3. Formulate clarifying questions regarding scope, edge cases, performance budgets, and interface boundaries.
  4. Write architectural invariants to `aas-stack.json`:
     ```bash
     python scripts/manage_state.py decide "Feature Scope Bound" "Exclude legacy v1 endpoints"
     ```
- **Exit Gate**: Requirements confirmed and signed off.

---

## Phase 2: Granular Planning & Task Decomposition
- **Primary Skill**: [`.agents/skills/concise-planning/SKILL.md`](../.agents/skills/concise-planning/SKILL.md)
- **Actions**:
  1. Break down implementation into atomic tasks (each taking 2–5 minutes of execution).
  2. Order dependencies logically: Core models ➔ Business logic ➔ Public API ➔ Integration tests ➔ UI.
  3. Populate checklist in `aas-stack.json` and sync `CONTEXT.md`:
     ```bash
     python scripts/manage_state.py step 1 --status completed
     python scripts/manage_state.py sync-context
     ```
- **Exit Gate**: An atomic, ordered task list in `CONTEXT.md`.

---

## Phase 3: API & Contract Specification
- **Primary Skill**: [`.agents/skills/api-and-interface-design/SKILL.md`](../.agents/skills/api-and-interface-design/SKILL.md)
- **Actions**:
  1. Define explicit function signatures, data transfer objects (DTOs), or REST/GraphQL schema.
  2. Implement strict error models, input validation, and boundary contracts.
  3. Ensure backward compatibility and deprecation paths if altering existing endpoints.
- **Exit Gate**: Type definitions and endpoint contracts compiled without errors.

---

## Phase 4: Test-Driven Implementation (TDD) & AST Safety
- **Primary Skills**: [`.agents/skills/tdd/SKILL.md`](../.agents/skills/tdd/SKILL.md) & [`.agents/skills/ast-code-transformation/SKILL.md`](../.agents/skills/ast-code-transformation/SKILL.md)
- **Actions**:
  1. **Red**: Write failing unit tests specifying desired behavior. Run tests to observe explicit failure.
  2. **Green**: Implement the minimal clean code necessary to make tests pass.
  3. **Refactor**: Clean up duplication, enforce naming standards, and ensure zero code rot.
  4. **AST Verification**: Never save edits blindly; run AST checks:
     ```bash
     python -m py_compile <modified_file.py>
     ```
- **Exit Gate**: All new tests pass, zero regressions on existing suites.

---

## Phase 5: Verification & Safety Gates
- **Primary Skill**: [`.agents/skills/verification-before-completion/SKILL.md`](../.agents/skills/verification-before-completion/SKILL.md)
- **Actions**:
  1. Execute full project test suite:
     ```bash
     python scripts/run_hook.py post active.tdd
     ```
  2. Verify working tree status: `git status --porcelain`.
- **Exit Gate**: 100% test pass rate, syntax valid, no unhandled exceptions.

---

## Phase 6: Code Review & Simplification
- **Primary Skills**: [`.agents/skills/code-reviewer/SKILL.md`](../.agents/skills/code-reviewer/SKILL.md) & [`.agents/skills/review-and-simplify-changes/SKILL.md`](../.agents/skills/review-and-simplify-changes/SKILL.md)
- **Actions**:
  1. Inspect `git diff` against baseline commit SHA.
  2. Eliminate dead code, extraneous logs, and unneeded dependencies.
  3. Audit against performance regressions and N+1 query patterns.
- **Exit Gate**: Clean, readable patch ready for human signoff.

---

## Phase 7: Changelog & Release Staging
- **Primary Skill**: [`.agents/skills/changelog-automation/SKILL.md`](../.agents/skills/changelog-automation/SKILL.md)
- **Actions**:
  1. Generate Keep-a-Changelog entry under `[Unreleased]`.
  2. Finalize `aas-stack.json` progress:
     ```bash
     python scripts/manage_state.py step 7 --status completed
     python scripts/manage_state.py sync-context
     ```
  3. Format git commit message following Conventional Commits (`feat: ...`).
