# Candidate Playbook: Skill Quality Amendment

Status: promoted by the evaluator verifier as `evidence-backed-skill-amendment`.
Scenario: `skill-quality-evidence` (read-only run, 2026-05-14).

## Operating rules

1. Read docs/SKILL-DEVELOPMENT-GUIDE.md before touching the skill; follow its
   frontmatter and focus contract.
2. Record the observed skill-run failure or user-feedback excerpt that
   motivates the change.
3. Keep the amendment focused: one surface, one example, one validation
   command (`node scripts/ci/validate-skills.js`).
4. Attach a worked example that fails before and passes after the amendment.
5. Never copy private operator context, secrets, tokens, or personal paths
   into a skill.
6. Check the reference set for duplicates before adding anything broad.

## Verification

- Validator passes on the amended skill.
- Lock digest refreshed via `python scripts/skills/skills.py lock` if
  SKILL.md changed.
- Example output attached to the PR.

## Rollback

Revert the amendment; refresh skills.lock.
