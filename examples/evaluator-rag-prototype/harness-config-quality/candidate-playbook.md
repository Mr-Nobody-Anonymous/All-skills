# Candidate Playbook: Harness Config Quality

Status: promoted by the evaluator verifier as `adapter-matrix-backed-drift-check`.
Scenario: `harness-config-quality` (read-only run, 2026-05-14).

## Operating rules

1. Retrieve adapter state from the matrix first
   (`npm run harness:adapters -- --check`).
2. Name the install or onramp path per harness; never recommend a path the
   matrix does not list.
3. Name a verification command per recommendation
   (`node tests/docs/mcp-management-docs.test.js` for MCP surfaces).
4. Preserve existing user config: merge into MCP, hook, plugin, command, and
   rule files without overwriting entries the tool did not create; write a
   `.bak` backup on first mutation.
5. Label instruction-backed and reference-only harnesses as such; do not claim
   native support without adapter evidence.

## Verification

- Matrix check passes and its output is linked.
- Generated bundles match `mcps/generated/`.
- A dry-run install shows zero unexpected mutations.

## Rollback

Revert the recommendation document. User config untouched.
