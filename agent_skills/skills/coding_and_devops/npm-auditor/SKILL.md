---
name: npm-auditor
description: Audit an npm / pnpm / yarn project for vulnerabilities, outdated dependencies, license risks, and supply-chain issues, with an actionable fix plan.
category: coding_and_devops
aliases: [npm, audit, pnpm, yarn, dependency, supply-chain, vulnerabilities]
triggers:
  - Audit my dependencies
  - Run npm audit
  - Check for CVEs
  - Are my packages up to date
  - License check
keywords: [npm, pnpm, yarn, audit, dependency, vulnerability, cve, license, supply, chain]
required_tools: [node, npm-or-pnpm-or-yarn]
risk: medium
version: 1.0.0
source: openclawskills.net
enabled: true
metadata:
  openclaw:
    requires:
      env: []
      bins: []
    primaryEnv: null
---

# NPM & Dependency Audit

## Purpose

Run a layered audit of a Node.js project's dependencies â€” **vulnerabilities** (CVEs),
**outdated packages**, **license risks**, and **supply-chain red flags** (typosquats,
unmaintained packages, postinstall scripts) â€” and turn the result into a single,
actionable fix plan.

## When to Use

- A new dependency is being added
- A routine security check is requested
- After a major version bump or lockfile change
- Before a release

## When NOT to Use

- The project has no `package.json`
- The user is offline and the lockfile cannot be validated against the registry
- The user wants a license *enforcement* rule (this skill only reports)

## Capabilities

- `npm audit --json` (or pnpm/yarn equivalent), grouped by severity
- `npm outdated --json`, grouped by major/minor/patch
- License scan: list of SPDX expressions, flag unknown / GPL / AGPL
- Postinstall scan: list packages with `scripts.postinstall`
- Typosquat / maintenance check against a curated list
- Suggest a fix plan: `npm audit fix`, then a list of manual bumps

## Inputs

- `mode`: `cves` | `outdated` | `licenses` | `all` (default `all`)
- `severity`: `low|moderate|high|critical` filter (default `moderate+`)
- `prod-only`: include only production dependencies (default false)
- `apply`: actually run `npm audit fix` (default false â€” report only)

## Workflow

1. **Detect** package manager (`package-lock.json` â†’ npm, `pnpm-lock.yaml` â†’ pnpm, `yarn.lock` â†’ yarn).
2. **Run audit** in the chosen mode; parse JSON.
3. **Group** findings by severity and by package.
4. **Cross-check** postinstall scripts and license expressions.
5. **Compose the fix plan** â€” small, ordered, with the exact command per step.
6. **Print** a table: package | current | target | severity | license | action.
7. **Optionally apply** `npm audit fix` (non-breaking) if `--apply`.

## Tools

- `npm` / `pnpm` / `yarn` (whichever the project uses)
- `jq` for JSON shaping
- Optional: `license-checker` for richer license reports

## Examples

**User:** "Audit my project for CVEs."
**Response:**

| package | severity | via | fix |
|---|---|---|---|
| `lodash` | high | `^4.17.20` | `npm audit fix` |
| `axios` | moderate | `^0.27.0` | bump to `^1.7.0` (manual) |

**User:** "What packages are out of date?"
**Response:** 3 majors behind (breaking), 7 minors, 12 patches. List grouped.

## Safety

- Never run `npm audit fix --force` automatically
- Never modify the lockfile without a dry-run preview first
- Surface postinstall scripts to the user; require approval to install
- Skip `optionalDependencies` and `devDependencies` unless asked

## Source

Auto-generated from openclawskills.net description.

## Pairs Well With

- `git-workflow` (commit the lockfile bump)
- `security-scanner` (deeper source scan)
- `github-cli` (open an issue for the audit findings)
