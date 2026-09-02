---
name: voice-to-action
description: Parse a voice memo (or live dictation) into a structured action: a task, calendar event, note, or follow-up message, with a verbatim transcript.
category: adhd_and_productivity
aliases: [voice, dictation, memo, transcribe, action]
triggers:
  - From my voice memo
  - Transcribe this audio
  - What did I just say
  - Convert this to a task
keywords: [voice, audio, transcribe, dictation, memo, action, task, whisper]
required_tools: [audio-transcribe, calendar, todo]
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

# Voice-to-Action Parser

## Purpose

Take a voice memo (or live audio stream) and turn it into a **single concrete
action** plus a verbatim transcript and a confidence score. The skill assumes the
user spoke quickly, was distracted, and meant something specific.

## When to Use

- The user has just finished a voice memo and wants it processed
- The user is dictating a task, a calendar event, or a note
- A live transcription should be paired with intent classification

## When NOT to Use

- The audio contains many speakers (use a meeting-specific skill)
- The user wants high-fidelity word-for-word transcription only (use `audio-transcribe`)
- The user is in a setting where the device microphone is unavailable

## Capabilities

- Transcribe audio via `whisper` (local or API)
- Classify the *intent* of the memo:
  - `task` â€” needs to land in a todo list
  - `event` â€” has a time and a date
  - `note` â€” wants to be saved as-is
  - `message` â€” needs to be sent to a person
  - `idea` â€” capture only, no action
- Extract entities (people, dates, places) and link to the action
- Output a one-line action plus a short transcript with timestamps

## Inputs

- An audio file path **or** a live mic stream id
- Optional `intent_hint` (one of `task|event|note|message|idea`)
- Optional `target` (a todo app, calendar, or person)

## Workflow

1. **Acquire** the audio (file or live chunk).
2. **Transcribe** with `whisper` (or a cloud STT API), capturing word-level timestamps.
3. **Classify intent** with a small model prompt + the transcript.
4. **Extract entities** (dates â†’ ISO, people â†’ contacts, places â†’ maps).
5. **Build the action**:
   - For `task`: short verb phrase + due date.
   - For `event`: title + start time + duration.
   - For `note`: a clean markdown body, with `[...]` for uncertain words.
   - For `message`: the message text + recipient (ask if ambiguous).
   - For `idea`: title + one-line summary.
6. **Confirm** with the user before performing the action (`add to todo`, `create event`).
7. **Append** the verbatim transcript to a log if the user opted in.

## Tools

- `whisper` (local `whisper.cpp` / `whisper-cli`, or OpenAI Whisper API)
- `ffmpeg` for audio prep (16 kHz mono PCM)
- Optional: `calendar` / `todo` / `telegram-actions` for execution

## Examples

**User:** "Process this voice memo."
**Response:** Intent: `task`. "Email Sam about the launch date, by Friday."
Confirmed: adding to your todo with due date 2026-02-13.

**User:** "Capture this idea."
**Response:** Intent: `idea`. Saved to `notes/ideas/2026-02-09-001.md`. Transcript
appended.

## Safety

- Never send a `message` action without explicit user confirmation
- Strip the recording from the device once processed, unless the user opts in
- Honor a "private" flag (no log, no cloud STT)
- Surface a confidence score; ask when below 0.7

## Source

Auto-generated from openclawskills.net description.

## Pairs Well With

- `audio-transcribe` (the underlying engine)
- `calendar-assistant` (when intent is `event`)
- `telegram-actions` (when intent is `message`)
- `obsidian-sync` (when intent is `note`)
