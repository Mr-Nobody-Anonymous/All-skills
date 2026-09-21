# All-Skills Forensic Quarantine Vault

**Status:** Enforced  
**Policy:** Zero-Deletion Forensic Retention  

---

## 1. Overview

The All-Skills platform enforces a strict **preservation and quarantine** policy:
- Skills suspected of containing malicious instructions, prompt injection, or severe vulnerabilities are **never silently deleted**.
- Instead, skills are immediately quarantined, preventing runtime execution and removing them from candidate router scoring, while preserving complete forensic evidence.

---

## 2. Directory Structure

```
quarantine/
├── README.md               # Policy and workflow documentation
├── quarantine_log.jsonl    # Append-only ledger of quarantine actions
└── evidence/               # Forensic snapshots and vulnerability audit reports
```

---

## 3. Quarantine Lifecycle

1. **Detection**: The static scanner, instruction scanner, or external report flags an issue.
2. **Quarantine Trigger**: `quarantine_skill(skill_id, reason, reporter)` is invoked:
   - Skill ID is added to `skills/revocations.json` (kill-switch).
   - An immutable record is appended to `quarantine/quarantine_log.jsonl`.
   - A forensic snapshot is saved in `quarantine/evidence/{skill_id}.json`.
3. **Execution Denial**: Both `Router.route()` and `ExecutionRuntime.execute()` immediately block execution of any quarantined skill with a fail-closed error.
4. **Appeals & Remediation**: A quarantined skill can only be reinstated after passing all static and behavioral evaluation gates via `unquarantine_skill()`.
