# Candidate Playbook: CI Failure Diagnosis

Status: promoted by the evaluator verifier as `log-backed-minimal-fix`.
Scenario: `ci-failure-diagnosis` (read-only run, 2026-05-14).

## Operating rules

1. Read the failing job and step before anything else:
   `gh run view <run-id> --log-failed`.
2. Capture or summarize the failing log excerpt; a screenshot of a red badge
   is not evidence.
3. Compare the changed-file context against the failing step; fix the cause,
   not the symptom.
4. Name a local reproduction or regression command and run it before pushing.
5. Never weaken, delete, or skip tests or checks to silence the failure.
6. Keep the Full required GitHub Actions matrix before merge; a green rerun
   of one job is not the matrix.

## Verification

- The regression command passes locally and in CI.
- The failing step passes on a fresh run, not a re-run.
- No test or gate was weakened.

## Rollback

Revert the fix commit. The original gate stays enforced.
