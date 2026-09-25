# syntax=docker/dockerfile:1
#
# All-Skills CLI image.
#
#   docker build -f docker/Dockerfile -t all-skills .
#   docker run --rm all-skills                      # platform health check (doctor)
#   docker run --rm all-skills search "kubernetes"  # any `all-skills` sub-command
#   docker run --rm -it --entrypoint python all-skills -m interfaces.cli.terminal_interface
#
# Optional audio/voice system libraries (only needed for voice skills that use
# requirements-optional.txt):  --build-arg INSTALL_AUDIO_DEPS=true

FROM python:3.12-slim

ARG INSTALL_AUDIO_DEPS=false

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# git is used by the skill installer/updater; audio libraries are opt-in.
# The unprivileged `app` user (UID/GID 10001) owns /app so the runtime can
# write audit logs. Distro package versions are intentionally not pinned: the
# Debian archive drops old versions, which would break rebuilds.
# hadolint ignore=DL3008
RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && if [ "$INSTALL_AUDIO_DEPS" = "true" ]; then \
         apt-get install -y --no-install-recommends build-essential portaudio19-dev libasound2-dev ffmpeg; \
       fi \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd --system --gid 10001 app \
    && useradd --system --uid 10001 --gid app --create-home --home-dir /home/app --shell /usr/sbin/nologin app \
    && chown 10001:10001 /app

# Install dependencies first so this layer is cached across source changes.
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy the source tree (see .dockerignore) and install the package in editable
# mode: the `all-skills` entry point locates scripts/ relative to src/, so the
# full CLI is only available from a source checkout. `--chown` avoids a costly
# recursive chown layer.
COPY --chown=10001:10001 . .
RUN pip install --no-deps -e .

# Never run as root.
USER 10001:10001

ENTRYPOINT ["all-skills"]
CMD ["doctor"]
