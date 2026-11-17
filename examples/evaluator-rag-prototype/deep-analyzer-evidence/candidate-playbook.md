# Candidate Playbook: Deep Analyzer Evidence

Status: promoted by the evaluator verifier as `corpus-backed-analyzer-change`.
Scenario: `deep-analyzer-evidence` (read-only run, 2026-05-14).

## Operating rules

1. Start from the corpus: `../ECC-Tools/src/analyzers/fixtures/deep-analyzer-corpus.ts`.
2. Add or extend a corpus case before changing analyzer behavior; commit the
   expected output with it.
3. Compare expected outputs for every touched classification — no diff means
   no change.
4. Describe a representative repository shape or commit history for the case.
5. Name the regression command and run it:
   `npm test -- src/analyzers/deep-analyzer-corpus.test.ts src/lib/analyzer.compare.test.ts`
6. Do not suppress the Deep Analyzer Evidence risk bucket without co-located
   corpus, snapshot, fixture, or benchmark evidence.

## Verification

- All corpus cases pass with expected outputs.
- Golden traces show no unintended classification drift.

## Rollback

Revert the analyzer and corpus commits together.
