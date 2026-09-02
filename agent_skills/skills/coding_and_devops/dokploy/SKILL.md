---
name: dokploy
description: Manage Dokploy deployments, projects, applications, and domains via the Dokploy REST API from a shell or agent.
category: coding_and_devops
aliases: [dokploy, deploy, hosting, self-host]
triggers:
  - Deploy to Dokploy
  - Restart the app on Dokploy
  - Add a domain
  - List projects on Dokploy
keywords: [dokploy, deploy, hosting, project, application, domain, server, docker]
required_tools: [http, dokploy-api-token]
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

# Dokploy Management

## Purpose

Drive a **Dokploy** instance (self-hosted PaaS) through its REST API: list, create,
update, deploy, and roll back projects, applications, and domains. The skill is
careful to surface every destructive operation and never assume a default environment.

## When to Use

- The user wants to deploy, redeploy, or roll back a service
- A new project / application / domain needs to be created
- Status of one or more Dokploy services is needed

## When NOT to Use

- The user has no Dokploy instance or no API token
- The action is to delete a service (require explicit `--destroy` confirmation)
- The user wants a UI walkthrough (route to the Dokploy web UI)

## Capabilities

- List, view, create, update, and delete projects
- List, view, create, update, redeploy, and stop applications
- Manage domains (add, remove, verify DNS)
- Pull and inspect deployment logs
- Trigger a redeploy of a specific commit / image tag
- Roll back to the previous deployment

## Inputs

- `--base-url https://dokploy.example.com` (required)
- `--api-token <token>` (required; or env `DOKPLOY_API_TOKEN`)
- subcommand + args (e.g. `app list --project myproj`)

## Workflow

1. **Resolve credentials** â€” `--api-token` flag or `DOKPLOY_API_TOKEN` env.
2. **Resolve base URL** â€” `--base-url` flag or `DOKPLOY_URL` env.
3. **Pre-flight**: `GET /api/health` (Dokploy 0.1+). On failure, abort.
4. **Build the request**: method, path, JSON body, headers (`x-api-key`, `Content-Type`).
5. **Send the request** with a 30 s timeout (60 s for deploys).
6. **Format the response** for chat â€” table for lists, JSON for detail.
7. **For `deploy` / `redeploy`**: poll `GET /api/application.deployments` until status is
   `done` or `error`, with a 5-min ceiling.

## Endpoints Used (subset)

- `GET /api/project.all`
- `POST /api/project.create`
- `GET /api/application.all?projectId=â€¦`
- `POST /api/application.deploy`
- `POST /api/application.redeploy`
- `POST /api/domain.create`
- `GET /api/application.logs?appId=â€¦`

## Examples

**User:** "Redeploy `web` in the `marketing` project."
**Response:** `POST /api/application.redeploy` with `{ applicationId: "â€¦" }`. Will
poll until `done`.

**User:** "Add `app.example.com` to the `api` app."
**Response:** `POST /api/domain.create` with `{ applicationId, host: "app.example.com", â€¦ }`.

## Safety

- **Always confirm** before: delete, rebuild (image reset), environment-variable change
- **Never** print the API token back to chat
- **Default to `dry-run`** for any mutating call; pass `--apply` to execute
- **Cap concurrent deploys** at 3; queue the rest

## Source

Auto-generated from openclawskills.net description.

## Pairs Well With

- `docker-manager` (inspect the underlying container)
- `cf-worker-deploy` (edge layer in front of Dokploy)
- `github-cli` (trigger deploy from a release tag)
