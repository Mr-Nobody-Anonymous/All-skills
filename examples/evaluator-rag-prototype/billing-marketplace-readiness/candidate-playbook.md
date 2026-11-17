# Candidate Playbook: Billing / Marketplace Readiness

Status: promoted by the evaluator verifier as `evidence-backed-billing-check`.
Scenario: `billing-marketplace-readiness` (read-only run, 2026-05-14).

## Goal

Prevent launch copy from presenting dry-run release evidence or roadmap intent
as live billing state for ECC Tools.

## Operating rules

1. Treat the billing audit (plans, seats, subscriptions, entitlements,
   overage, downgrade/cancel, failure modes) as the source of truth, not the
   roadmap.
2. Cross-check the draft Marketplace listing at
   https://github.com/marketplace/ecc-tools before approving any claim.
3. Mark every unverified claim remove-before-publication until the audit
   closes; announcement copy waits for sign-off.
4. Never edit plans, limits, seats, subscriptions, or entitlements from this
   run; those changes go through the normal billing review.
5. Record which dry-run artifacts are being relied on and which live checks
   remain outstanding.

## Verification

- Billing audit checklist is complete and linked.
- Listing draft matches the audited state; nothing is published.
- Launch copy carries remove-before-publication markers for open items.

## Rollback

Revert the checklist document. No Marketplace, plan, or subscription state was
changed by this run.
