---
name: docker-manager
description: Inspect, run, build, and clean up Docker containers, images, networks, and volumes from a shell or agent with safe defaults.
category: coding_and_devops
aliases: [docker, container, image, compose, podman]
triggers:
  - List docker containers
  - Tail container logs
  - Restart this container
  - Prune docker
  - Build this image
keywords: [docker, container, image, compose, podman, volume, network, prune, build]
required_tools: [docker]
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

# Docker Manager

## Purpose

Make common Docker operations safe and scriptable for an agent: list, inspect, run,
build, prune, and (with explicit confirmation) destroy. The skill defaults to **read
or report** mode; any state change is gated by an `--apply` flag.

## When to Use

- The user wants to inspect or control Docker resources
- A dev environment needs to be brought up or torn down
- A build is failing and the user needs the logs

## When NOT to Use

- The user has no Docker daemon access
- The user wants Kubernetes operations (use a different skill)
- The user wants production orchestration

## Capabilities

- `ps`, `images`, `networks`, `volumes` (all read-only)
- `logs <container>` (tail with timestamp)
- `exec <container> <cmd>` (interactive shell)
- `restart`, `start`, `stop` (gated)
- `compose up/down/ps/logs` (gated)
- `build` (gated, with `--no-cache` opt-in)
- `system prune` (gated, with size preview)
- `rm` / `rmi` (gated, never default)

## Inputs

- subcommand (`ps`, `logs`, `exec`, â€¦)
- target (container / image / volume / network id or name)
- `--apply` for any state-changing operation (default false)
- `--dry-run` to print the command without running it

## Workflow

1. **Detect** Docker (or Podman, via `DOCKER_HOST` or alias).
2. **Validate** the subcommand against the allowlist.
3. **For read-only ops**: run, parse, format (table or JSON).
4. **For state-changing ops**: print the exact command, ask for `--apply` confirmation.
5. **For destructive ops** (`rm`, `rmi`, `system prune`): require `--apply --force` and a
   5-second grace period with a clear "type YES to continue" prompt.
6. **Report** what changed, with IDs, before and after.

## Tools

- `docker` (or `podman`)
- `jq` for JSON shaping
- `less` / `tail` for log streaming

## Examples

**User:** "Show running containers."
**Response:** `docker ps --format '{{.ID}}\t{{.Image}}\t{{.Status}}\t{{.Names}}'`.

**User:** "Tail the api logs."
**Response:** `docker logs -f --tail 200 --timestamps api`.

**User:** "Prune everything not in use."
**Response:** Will free ~3.2 GB across 14 images, 3 networks. Type `YES` to proceed.

## Safety

- All destructive ops require explicit `--apply` confirmation
- `system prune` requires `--apply --force` and a typed confirmation
- Never `rm` a container with status `Up` without a stop first
- Never `rmi` an image that has child images (warn first)
- Cap log tail at 10 MB per request

## Source

Auto-generated from openclawskills.net description.

## Pairs Well With

- `dokploy` (Dokploy runs Docker underneath)
- `security-scanner` (scan images before deploy)
- `system-monitor` (correlate container stats with host load)
