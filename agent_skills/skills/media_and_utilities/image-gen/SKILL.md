---
name: image-gen
description: Create precise, safe image-generation prompts and iterate against visual requirements.
category: media_and_utilities
aliases: [image, generation, dalle, midjourney, stable-diffusion, art]
triggers:
  - Generate an image
  - Create artwork
  - Make a picture
  - AI art
  - Image generation
keywords: [image, generation, ai, art, dalle, midjourney, illustration]
required_tools: [image-generator]
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

# Image Prompt Generator

## Purpose

Create precise, effective prompts for AI image generation models and iterate
against visual requirements. The skill ensures generated images match user
intent through structured prompt refinement.

## When to Use

- The user wants to create AI-generated imagery
- Visual assets are needed for projects
- Prototyping visual concepts

## When NOT to Use

- For photography that requires real-world capture
- When stock imagery would be more appropriate
- For content requiring precise technical accuracy

## Capabilities

- Prompt writing and refinement
- Style specification (photorealistic, illustrative, abstract, etc.)
- Aspect ratio and resolution selection
- Negative prompt crafting
- Iteration based on feedback
- Multiple model support (DALL-E, Midjourney, Stable Diffusion, etc.)

## Inputs

- `description` (required) â€” what the image should depict
- `style` (optional) â€” artistic style preference
- `aspect_ratio` (optional) â€” 1:1, 16:9, 9:16, etc.
- `mood` (optional) â€” tone or atmosphere
- `reference` (optional) â€” reference image URL or upload
- `model` (optional) â€” preferred generation model

## Workflow

1. **Analyze** â€” Understand user requirements
2. **Draft** â€” Create initial prompt
3. **Refine** â€” Add style, quality, and specificity modifiers
4. **Generate** â€” Submit to image generation API
5. **Iterate** â€” Refine based on user feedback
6. **Deliver** â€” Provide image file and prompt used

## Tools

- Image generation APIs (DALL-E, Midjourney, Stable Diffusion, etc.)
- Image editing tools for post-processing

## Examples

**User:** "Create a logo for my tech startup"
**Response:**
```
Prompt: "Minimalist tech startup logo, geometric fox silhouette, 
gradient blue to purple, clean lines, modern, professional, white 
background, vector style, scalable"

Generating... [â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆ] 100%
Output: logo-startup-2026-02-09.png (1024x1024)
Prompt saved for reproducibility.
```

## Safety

- Never generate harmful, violent, or deceptive imagery
- Respect copyright and trademark considerations
- Avoid generating content that could be mistaken for real people
- Label AI-generated images appropriately

## Source

Auto-generated from openclawskills.net description.

## Pairs Well With

- `avatar-creator` (consistent character assets)
- `veo-video-generator` (storyboarding)
- `frontend-design` (UI asset generation)
