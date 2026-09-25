# `docker/` — container images

A self-contained image of the All-Skills CLI (Python 3.12, non-root user, full skill
library). Build context is the repository root; [`.dockerignore`](../.dockerignore)
keeps Git metadata, caches and secrets out of the image.

## How to run

```bash
# Build and run the platform health check (default command: `doctor`)
docker compose -f docker/docker-compose.yml up --build

# Run any `all-skills` sub-command
docker compose -f docker/docker-compose.yml run --rm all-skills search "kubernetes"
docker compose -f docker/docker-compose.yml run --rm all-skills route "review my pull request"

# Interactive terminal interface
docker compose -f docker/docker-compose.yml run --rm --entrypoint python all-skills -m interfaces.cli.terminal_interface
```

Plain Docker works too:

```bash
docker build -f docker/Dockerfile -t all-skills .
docker run --rm all-skills --help
docker run --rm --env-file .env all-skills doctor      # optional credentials, see .env.example
```

## Development container

`docker-compose.dev.yml` bind-mounts the repository so host edits are picked up
immediately:

```bash
docker compose -f docker/docker-compose.dev.yml run --rm dev          # run the test suite
docker compose -f docker/docker-compose.dev.yml run --rm dev doctor   # any skills.py command
```

## Options

| Build argument | Default | Effect |
| :--- | :--- | :--- |
| `INSTALL_AUDIO_DEPS` | `false` | Adds `ffmpeg`, `portaudio` and build tools for voice skills (`--build-arg INSTALL_AUDIO_DEPS=true`) |

The image is linted with hadolint, built and smoke-tested on every pull request
(`docker` job in [`ci.yml`](../.github/workflows/ci.yml)).
