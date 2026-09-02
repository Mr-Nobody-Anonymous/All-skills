---
name: audio-transcribe
description: Transcribe audio into timestamped text and optionally extract speakers and actions.
category: media_and_utilities
aliases: [transcribe, speech-to-text, audio, transcription, voice]
triggers:
  - Transcribe this audio
  - Convert speech to text
  - Get a transcript
  - Speech recognition
keywords: [audio, transcription, speech, voice, text, whisper]
required_tools: [transcription-engine]
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

# Audio Transcription Processor

## Purpose

Transcribe audio files into timestamped text with speaker identification and action
extraction. The skill processes various audio formats and produces clean, usable
transcripts for documentation or analysis.

## When to Use

- Converting meeting recordings to text
- Transcribing voice memos or notes
- Creating captions for audio/video content
- Processing interview recordings

## When NOT to Use

- For real-time transcription (use specialized real-time tools)
- When audio quality is too poor for accurate transcription
- For languages without available transcription models

## Capabilities

- Multi-format audio support (MP3, WAV, M4A, FLAC, etc.)
- Timestamped output
- Speaker diarization (identify different speakers)
- Punctuation and formatting
- Confidence scores
- Multiple language support
- Action item extraction

## Inputs

- `audio` (required) â€” audio file URL or path
- `language` (optional) â€” source language (auto-detect if omitted)
- `speakers` (optional) â€” number of speakers (for diarization)
- `timestamps` (optional, default: true) â€” include timestamps
- `format` (optional) â€” one of: text, srt, vtt, json

## Workflow

1. **Validate** â€” Check audio format and accessibility
2. **Process** â€” Run transcription engine
3. **Format** â€” Apply formatting and timestamps
4. **Extract** â€” Identify speakers and actions (if requested)
5. **Deliver** â€” Provide transcript in requested format

## Tools

- Transcription engine (Whisper, DeepSpeech, or API)
- Audio preprocessing tools

## Examples

**User:** "Transcribe this meeting recording"
**Response:**
```
Transcribing meeting-audio.mp3...
[â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆ] 100%

00:00 - Speaker 1: "Let's start with the agenda..."
00:15 - Speaker 2: "I'll share my screen first."
00:42 - Speaker 1: "Action: Alice to follow up with vendor."

Transcript saved: transcript-meeting-2026-02-09.txt
```

## Safety

- Never store audio or transcripts without consent
- Respect speaker privacy
- Flag low-confidence transcriptions for review
- Handle sensitive content carefully

## Source

Auto-generated from openclawskills.net description.

## Pairs Well With

- `meeting-action-extractor` (extract action items from transcript)
- `context-summarize` (summarize transcript content)
- `media-downloader` (download audio for transcription)
