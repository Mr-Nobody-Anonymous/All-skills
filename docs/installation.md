# Installation Guide

This guide explains how to install and set up the All-Skills Universal Voice & Agent Operating System.

---

## Prerequisites

- **Python**: Version 3.10 or higher.
- **Git**: Installed and accessible in your system `PATH`.
- **Operating System**: Windows, Linux, or macOS.
- **Optional Audio Drivers**: PulseAudio/PipeWire or ALSA (Linux), PortAudio (macOS/Windows).

---

## 1. Quick Setup

Run the automated platform setup script:

```bash
# Windows
.\allskills.bat doctor
.\allskills.bat setup

# Linux / macOS
./setup.sh
```

---

## 2. Python Dependencies

Install the core dependencies:

```bash
pip install -r requirements.txt
```

---

## 3. Synchronizing Verified Upstream Skills

To inspect and synchronize the verified OpenVoiceOS and Neon skill repositories:

```bash
# Dry run inspection (safe preview)
python scripts/clone_all_repos.py --dry-run --verified-only

# Clone verified OpenVoiceOS and Neon repos into upstream/
python scripts/clone_all_repos.py --verified-only --depth 1

# Synchronize with OpenVoiceOS Skill Manager (OSM) catalog
python scripts/sync_osm_skills.py --stats
```

---

## 4. Validating the Installation

Verify that the platform and tests pass:

```bash
# Run unit and integration tests
python scripts/skills/skills.py test

# Validate all SKILL.md schemas
python scripts/validate_schema.py

# Run doctor diagnostic
.\allskills.bat doctor
```
