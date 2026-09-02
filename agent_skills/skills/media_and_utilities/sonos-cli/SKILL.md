---
name: sonos-cli
description: Inspect and control Sonos playback with room validation and confirmation for disruptive actions.
category: media_and_utilities
aliases: [sonos, music, speaker, playback, audio]
triggers:
  - Control Sonos
  - Play music on Sonos
  - Sonos speaker
  - Pause Sonos
keywords: [sonos, music, speaker, playback, audio, streaming]
required_tools: [sonos-cli]
risk: low
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

# Sonos CLI Controller

## Purpose

Inspect and control Sonos speakers through the CLI with room validation and
confirmation required for disruptive actions like volume changes or playback
interruption. The skill enables hands-free speaker management.

## When to Use

- Controlling Sonos playback (play, pause, skip)
- Adjusting volume across rooms
- Checking what's currently playing
- Grouping or ungrouping speakers

## When NOT to Use

- For professional audio equipment
- When Sonos is unavailable on the network
- For streaming service configuration (use app)

## Capabilities

- Playback control (play, pause, skip, previous)
- Volume adjustment (per room or group)
- Queue management
- Room status and current track info
- Group management (add/remove rooms)
- Preset recall (favorites, playlists)
- Power control (standby, wake)

## Inputs

- `action` (required) â€” one of: status, play, pause, volume, skip, group
- `room` (required) â€” speaker or group name
- `value` (optional) â€” volume level, target room for grouping

## Workflow

1. **Discover** â€” Find available Sonos devices
2. **Validate** â€” Confirm room exists
3. **Execute** â€” Perform requested action
4. **Confirm** â€” Report result
5. **Interrupt** â€” Ask for disruptive actions first

## Tools

- Sonos CLI (sonos-cli, soco, or similar)
- Network access to Sonos devices

## Examples

**User:** "What's playing in the living room?"
**Response:**
```
Living Room:
- Status: Playing
- Track: Bohemian Rhapsody - Queen
- Artist: Queen
- Album: A Night at the Opera
- Duration: 5:55 / 5:54
- Volume: 35%
```

## Safety

- Always validate room name exists
- Confirm before disruptive volume changes
- Never auto-adjust to max volume
- Warn before grouping/ungrouping

## Source

Auto-generated from openclawskills.net description.

## Pairs Well With

- `audio-transcribe` (transcribe playing audio)
- `calendar-assistant` (music for events)
- `system-monitor` (network speaker diagnostics)
