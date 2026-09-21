# ADR-[NUMBER]: Deprecate [SYSTEM/COMPONENT] in Favor of [NEW_SYSTEM]

## Status
Accepted (Supersedes ADR-[OLD_NUMBER])

## Context & Motivation
[Explain why the previously accepted architecture (from ADR-XXXX) is no longer adequate. What technical debt, operational friction, or scaling limits have been reached?]

## Decision
Deprecate [OLD_SYSTEM] and migrate all workloads to [NEW_SYSTEM].

## Migration Phases & Rollout
1. **Phase 1 (Dual-Write/Read-Through)**: [Strategy and milestone dates]
2. **Phase 2 (Backfill & Data Parity)**: [Verification and reconciliation tests]
3. **Phase 3 (Primary Cutover)**: [Traffic routing and rollback trigger]
4. **Phase 4 (Decommissioning)**: [Removal of legacy code and tear-down of infrastructure]

## Consequences & Mitigations
- **Positive**: [Reduced maintenance, performance improvement]
- **Risks**: [Migration downtime, data sync race conditions]
- **Rollback Plan**: [Steps to revert if Phase 3 validation fails]
