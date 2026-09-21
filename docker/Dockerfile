# syntax=docker/dockerfile:1
FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# System dependencies for audio and system utilities
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    curl \
    portaudio19-dev \
    libasound2-dev \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

EXPOSE 8000 8080

CMD ["python", "interfaces/cli/terminal_interface.py"]
