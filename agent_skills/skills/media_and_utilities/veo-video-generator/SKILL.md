---
name: veo-video-generator
description: Plan and generate Google Veo videos from approved prompts, assets, and output constraints.
category: media_and_utilities
aliases: [video, generation, veo, google-veo, ai-video]
triggers:
  - Generate a video
  - Create a video from this prompt
  - Make an AI video
  - Veo video
keywords: [video, generation, ai, veo, google, animation]
required_tools: [GOOGLE_API_KEY]
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

# Veo Video Generator

## Purpose

Plan and generate videos using Google Veo (Veo 3.1 / Veo 3.0) through approved prompts,
provided assets, and explicit output constraints. The skill ensures video generation
requests are well-formed and meet quality standards.

## When to Use

- The user wants to create an AI-generated video
- Video content is needed for presentations or social media
- Prototyping video concepts before full production

## When NOT to Use

- For real-world footage that requires human filming
- When video generation costs are prohibitive
- For content requiring photorealistic accuracy

## Capabilities

- Prompt refinement for optimal video generation
- Style and aspect ratio selection
- Duration configuration (up to platform limits)
- Seed and consistency controls
- Asset upload integration
- Output format selection (MP4, WebM)

## Inputs

- `prompt` (required) â€” video description
- `duration` (optional) â€” video length in seconds
- `aspect_ratio` (optional) â€” 16:9, 9:16, 1:1, etc.
- `style` (optional) â€” cinematic, realistic, animated, etc.
- `seed` (optional) â€” for reproducibility
- `assets` (optional) â€” uploaded reference images or videos

## Workflow

1. **Refine** â€” Improve prompt for best results
2. **Configure** â€” Set parameters and constraints
3. **Generate** â€” Submit to Veo API
4. **Monitor** â€” Track generation status
5. **Deliver** â€” Provide video file and metadata
6. **Review** â€” Present for user approval

## Tools

- Google Veo API
- Video processing tools (FFmpeg for format conversion)

## Examples

**User:** "Create a cinematic video of a sunset over the ocean"
**Response:**
```
Refined prompt: "Aerial view of golden hour sunset over calm Pacific Ocean, 
waves gently rolling, clouds painted in orange and pink hues, cinematic 
lighting, slow motion, 4K quality"

Generating... [â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆ] 100%
Output: video-sunset-2026-02-09.mp4 (1080p, 10s)
```

## Safety

- Never generate harmful, misleading, or deceptive content
- Respect content policies for AI-generated video
- Label AI-generated content appropriately
- Obtain necessary rights for reference assets

## Source

Auto-generated from openclawskills.net description.

## Pairs Well With

- `image-gen` (storyboarding and reference images)
- `media-downloader` (download generated content)
- `audio-transcribe` (add subtitles or narration)
