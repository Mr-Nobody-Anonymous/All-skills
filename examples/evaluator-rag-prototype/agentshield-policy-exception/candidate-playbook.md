# Candidate Playbook: AgentShield Policy Exception Review

Status: promoted by the evaluator verifier as `sarif-backed-timeboxed-exception-review`.
Scenario: `agentshield-policy-exception` (read-only run, 2026-05-14).

## Operating rules

1. Start from evidence: `npx ecc-agentshield scan --format json` or the
   SARIF report attached to the finding.
2. Bind every exception to the policy pack it scopes, e.g.
   `agentshield-policy/*`, never to the whole gate.
3. Record owner, ticket, scope, expiry for each exception; expiry is
   mandatory and enforced.
4. Expired exceptions stay rejected until renewed with fresh evidence.
5. Decide remediation versus time-boxed exception explicitly; prefer
   remediation when a fix exists.

## Verification

- SARIF/rule IDs are linked in the exception ticket.
- The org-policy gate passes with the exception active, and fails closed at
  expiry (test with a dry-run scan).

## Rollback

Withdraw the exception; the gate re-enforces immediately.
