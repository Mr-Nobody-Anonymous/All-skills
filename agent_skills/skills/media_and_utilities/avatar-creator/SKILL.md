---
name: avatar-creator
description: Design consistent avatar and asset specifications across required formats and sizes.
category: media_and_utilities
aliases: [avatar, profile-image, icon, character-design]
triggers:
  - Create an avatar
  - Design a profile image
  - Generate character art
  - Make an icon
keywords: [avatar, profile, image, icon, character, design, art]
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

# Avatar & Asset Creator

## Purpose

Design consistent avatars and visual assets across multiple formats and sizes.
The skill ensures brand consistency and provides properly sized assets for
different platforms and use cases.

## When to Use

- Creating user profile avatars
- Designing character illustrations
- Generating consistent asset sets
- Updating visual identity materials

## When NOT to Use

- For professional photography or detailed portraits
- When existing brand assets should be used
- For trademarked or copyrighted imagery

## Capabilities

- Avatar design with style consistency
- Multiple format export (PNG, SVG, WebP)
- Size variants (profile, thumbnail, full resolution)
- Color palette adherence
- Background removal
- Batch generation for consistency
- Platform-specific sizing (social media, websites, apps)

## Inputs

- `description` (required) â€” avatar concept or reference
- `style` (optional) â€” illustration style (realistic, cartoon, abstract, etc.)
- `palette` (optional) â€” color constraints
- `formats` (optional) â€” desired output formats
- `sizes` (optional) â€” required dimensions

## Workflow

1. **Design** â€” Create base avatar concept
2. **Generate** â€” Produce primary avatar image
3. **Export** â€” Create format variants
4. **Size** â€” Generate required dimension variants
5. **Package** â€” Deliver as zip or organized folder
6. **Document** â€” Provide usage guidelines

## Tools

- Image generation (DALL-E, Stable Diffusion, etc.)
- Image editing (background removal, resizing)

## Examples

**User:** "Create an avatar for my user profile: friendly robot"
**Response:**
```
Design: Friendly robot avatar, blue and white palette, rounded design
Generating base avatar... [â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆ] 100%

Exporting variants:
- avatar-full.png (512x512)
- avatar-thumb.png (128x128)  
- avatar-social.png (256x256)
- avatar-bg-removed.png (512x512)

Package: avatar-set-2026-02-09.zip
```

## Safety

- Never generate avatars resembling real people without consent
- Respect intellectual property in reference images
- Ensure consistency for brand applications
- Consider accessibility (color contrast, alt text)

## Source

Auto-generated from openclawskills.net description.

## Pairs Well With

- `image-gen` (related image generation)
- `frontend-design` (integrate assets into designs)
- `branding` (maintain visual identity)
