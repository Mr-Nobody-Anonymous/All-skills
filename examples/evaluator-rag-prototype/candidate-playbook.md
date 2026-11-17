# Candidate Playbook: Stale PR Salvage (Maintainer-Owned Branch)

Status: promoted by the evaluator verifier as `maintainer-salvage-branch`.
Scenario: `stale-pr-salvage-maintainer-branch` (read-only run, 2026-05-14).

## When to use

A previously closed or stale PR contains work that is still useful on current
`main`. The salvage lands through a maintainer-owned branch that ports the
subset onto today's architecture, with attribution and validation — never by
reopening the original PR blindly.

## Operating rules

1. Inspect the closed diff and the review thread before porting anything.
2. Open a maintainer-owned branch from current `main`; do not cherry-pick the
   old branch wholesale.
3. Preserve attribution: credit the source PR in the commit message, the PR
   body, and the ledger entry.
4. Copy no private operator context, tokens, personal paths, or raw local
   notes into the branch.
5. Keep bulk localization and generated churn out of the salvage; content that
   needs it waits for translator/manual review and lands separately.
6. Record the outcome in `docs/stale-pr-salvage-ledger.md` with the source
   PR, the port result, and the salvage state (Salvaged, Superseded, Skipped,
   Translator/manual review).
7. Run the same validation gates as any code/docs change, including
   `git diff --check`, the schema and lockfile gates, and the targeted test
   suites for the touched surface.

## Verification

- `git diff --check` is clean.
- The ledger gains or updates the matching rows with source PR links.
- `skills.lock` / catalog digests are refreshed only if skill files changed.
- Release publication, package publishing, and tagging remain explicitly
  approval-gated and are never part of the salvage.

## Rollback

Close the maintainer-owned branch/PR, annotate the ledger row as superseded,
and file the remainder for translator/manual review or a follow-up salvage.
