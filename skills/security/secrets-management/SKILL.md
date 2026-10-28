---
name: secrets-management
description: "Handle application secrets correctly: vault and KMS-backed storage, rotation, least-privilege access, detection of leaks and emergency response."
type: procedural
category: security
domain: security
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: high
level: advanced
triggers:
  - secret rotation plan
  - vault integration
  - kms envelope encryption
  - leaked api key response
  - secrets in ci pipeline
keywords:
  - secrets
  - vault
  - kms
  - rotation
  - leak
  - least-privilege
source: custom
enabled: true
---

# Secrets Management

## Purpose

Handle application secrets correctly: vault and KMS-backed storage, rotation, least-privilege access, detection of leaks and emergency response.

## When to Use

- An application needs credentials that must not live in code or plain config.
- A key leaked into a repository, log or image and needs an incident response.
- Rotation policy must be defined and proven.

## When NOT to Use

- The value is public configuration, not a secret.
- You only need to scan for secrets (use the secret-detection skill).
- The credential cannot be rotated and belongs to a legacy system you do not control.

## Capabilities

- Design storage tiers: vault, KMS-backed envelope encryption, short-lived tokens.
- Automate rotation with overlap windows and verification.
- Scope access by workload identity rather than shared static keys.
- Run a leak response: revoke, rotate, audit, and prevent recurrence.

## Inputs

- The secret inventory: name, owner, consumers, rotation cadence.
- The platform's identity mechanism (OIDC, IAM role, workload identity).
- The incident details if a leak already happened.

## Workflow

1. Inventory secrets and classify by blast radius.
2. Prefer short-lived, workload-issued credentials over static strings.
3. Store long-lived secrets in a vault; grant read by identity, never by file copy.
4. Automate rotation with an overlap window so both versions work briefly.
5. Add pre-commit and CI scanning so the next leak is caught at the door.

## Tools

- HashiCorp Vault / cloud KMS / external secrets operator
- gitleaks or trufflehog
- OIDC federation

## Examples

- `vault kv put secret/app db_password="$NEW"`
- `gitleaks detect --source . --redact`
- `aws kms encrypt --key-id alias/app --plaintext fileb://secret.txt`

## Safety

- Deleting a vault path without a rotation plan locks you out of production.
- Mask secrets in logs and CI output; a redacted log is not proof of safety.
- After a leak, revoke first and investigate second.

## Source

All-Skills canonical library (`skills/security/secrets-management`). First-party skill, maintained in this repository.

## Notes

- Rotation must be tested: an untested rotation path is a future outage.
- Envelope encryption limits exposure to the data key, not the master key.
- Pairs with: `security/secret-detection`, `security/oauth2-oidc-integration`.
