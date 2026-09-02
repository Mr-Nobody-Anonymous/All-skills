---
name: media-downloader
description: Download user-authorized public media while respecting rights, terms, and safe filenames.
category: browser_and_web
aliases: [download, media, youtube, video, audio]
triggers:
  - Download this video
  - Save this audio
  - Download the image
  - Get this media file
keywords: [download, media, video, audio, image, youtube, mp3]
required_tools: [media-downloader, http-client]
risk: medium
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

# Media Downloader

## Purpose

Download publicly available media files (videos, audio, images) from the web with
proper respect for copyright, terms of service, and safe filename handling. The skill
ensures users have appropriate rights before downloading and provides proper attribution.

## When to Use

- The user explicitly requests to download a media file they have rights to
- Backing up content the user owns (e.g., their own YouTube videos)
- Downloading Creative Commons licensed content

## When NOT to Use

- Downloading copyrighted content without user authorization
- Circumventing paywalls or access controls
- Bulk downloading that violates terms of service
- Content the user doesn't have rights to

## Capabilities

- Support for common platforms (YouTube, Vimeo, SoundCloud, etc.)
- Format conversion (video to audio, different resolutions)
- Progress tracking for large files
- Filename sanitization
- Checksum verification
- Respect robots.txt and platform terms

## Inputs

- `url` (required) â€” media URL
- `format` (optional) â€” desired format (mp4, mp3, wav, jpg, etc.)
- `quality` (optional) â€” resolution/quality preference
- `output_dir` (optional) â€” destination directory

## Workflow

1. **Validate** â€” Check URL accessibility and format support
2. **Verify** â€” Confirm user has rights to this content
3. **Download** â€” Fetch media with progress tracking
4. **Convert** â€” Apply format conversion if requested
5. **Verify** â€” Check file integrity with checksum
6. **Report** â€” Confirm download with file details

## Tools

- yt-dlp or similar media downloader
- FFmpeg for format conversion
- HTTP client for direct downloads

## Examples

**User:** "Download this video: https://youtube.com/watch?v=..."
**Response:** Downloading video... [â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆ] 100%
Saved: `media/video-title-2026-02-09.mp4` (256MB, sha256:abc123...)

## Safety

- ALWAYS verify user authorization before downloading
- Check terms of service for target platform
- Never download copyrighted content without explicit permission
- Respect rate limits and robots.txt
- Store download receipts for provenance

## Source

Auto-generated from openclawskills.net description.

## Pairs Well With

- `audio-transcribe` (transcribe downloaded audio)
- `context-summarize` (summarize video content)
