---
name: cf-worker-deploy
description: Validate and deploy Cloudflare Workers with preview, secret, and rollback safeguards.
category: media_and_utilities
aliases: [cloudflare, worker, deploy, cf, edge]
triggers:
  - Deploy to Cloudflare Workers
  - Publish worker
  - Cloudflare deployment
  - Update worker
keywords: [cloudflare, worker, deploy, edge, serverless, wrangler]
required_tools: [wrangler]
risk: high
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

# Cloudflare Worker Deployer

## Purpose

Validate and deploy Cloudflare Workers with proper preview testing, secret management,
and rollback capabilities. The skill ensures safe deployments with minimal disruption.

## When to Use

- Deploying or updating a Cloudflare Worker
- Managing worker secrets and environment variables
- Rolling back a problematic deployment
- Testing workers in preview mode before production

## When NOT to Use

- For non-Cloudflare deployments (use appropriate cloud skill)
- Without proper Cloudflare authentication
- When rollback isn't possible (stateless workers)

## Capabilities

- Local validation and linting
- Preview deployment to staging
- Production deployment with traffic splitting
- Secret management (set, update, rotate)
- Environment variable management
- Rollback to previous version
- Deployment history and logs
- Traffic percentage controls

## Inputs

- `action` (required) â€” one of: validate, preview, deploy, rollback, secrets
- `worker_name` (required) â€” target worker
- `environment` (optional) â€” production, staging, preview
- `traffic_percentage` (optional) â€” for gradual rollouts

## Workflow

1. **Validate** â€” Run linting and type checks
2. **Preview** â€” Deploy to preview environment
3. **Test** â€” Verify preview is functional
4. **Confirm** â€” User approval for production
5. **Deploy** â€” Push to production with monitoring
6. **Verify** â€” Confirm successful deployment
7. **Rollback** â€” If issues detected, revert

## Tools

- Wrangler CLI (wrangler.toml configuration)
- Cloudflare API

## Examples

**User:** "Deploy my worker to production"
**Response:**
```
Validating worker...
âœ“ Linting passed
âœ“ Type checks passed

Preview deployment: âœ“ Success
Preview URL: https://my-worker.preview.pages.dev

Deploy to production? Say "confirm" to proceed.

After deployment, I'll monitor for errors and can rollback if needed.
```

## Safety

- ALWAYS validate before deployment
- ALWAYS use preview mode first
- Require explicit confirmation for production
- Monitor for errors after deployment
- Keep rollback path available
- Never expose secrets in logs or responses

## Source

Auto-generated from openclawskills.net description.

## Pairs Well With

- `github-cli` (trigger deploy from CI/CD)
- `system-monitor` (post-deployment monitoring)
- `cmd-safety-check` (pre-deployment command validation)
