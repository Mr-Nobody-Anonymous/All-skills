---
name: frontend-design
description: Generate distinctive, production-grade frontend interfaces with high design quality, including layout, typography, motion, and component composition.
category: coding_and_devops
aliases: [frontend, ui, design, components, interface]
triggers:
  - Build a UI for this
  - Make a landing page
  - Design a dashboard
  - Create a React component
  - Style this view
keywords: [frontend, design, ui, ux, react, tailwind, css, motion, typography, layout]
required_tools: []
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

# Frontend Design Patterns

## Purpose

Produce frontend code (HTML, CSS, React, Vue, Svelte) that is *unmistakably designed*:
strong typography, considered spacing, intentional motion, real hierarchy, and a
coherent visual language. The skill is opinionated: it refuses generic "AI-slop"
layouts and aims for production-grade interfaces a senior designer would sign off on.

## When to Use

- The user wants a new page, screen, or component
- The user wants an existing screen redesigned or refreshed
- The user wants a design system update

## When NOT to Use

- The user wants a wireframe (use a different, lo-fi skill)
- The user only wants CSS tweaks to an existing stylesheet
- The user explicitly wants "plain" or "minimal" â€” respect that, but do not ship slop

## Capabilities

- Choose a typographic system (serif/sans, scale, line-height) that fits the brand
- Build a layout grid that earns its complexity
- Add motion that is purposeful (entrance, hover, state change)
- Use real spacing scale, not random pixel values
- Use real color systems (semantic tokens, contrast checks)
- Compose with existing component libraries (shadcn, Radix, MUI) when the user has one
- Output responsive code that works at 320 px, 768 px, 1280 px

## Inputs

- The screen or component (one to several sentences)
- The brand or mood ("Stripe-clean", "Brutalist", "Apple-store")
- The stack (default: React + Tailwind; switchable)
- Any constraints (must use `data-testid`, must work in IE11, etc.)

## Workflow

1. **Read the brief** and pick a single visual concept (one word: "ledger", "observatory", "atelier").
2. **Define the type system** â€” one display face, one body face, one mono.
3. **Define the color tokens** â€” 1 brand, 1 surface, 1 ink, 1 accent, 1 success, 1 warn, 1 danger.
4. **Define the spacing scale** â€” 4 px or 8 px base, never raw values.
5. **Sketch the layout** â€” 3 to 7 regions, named, with hierarchy.
6. **Pick the components** â€” buttons, cards, tables, etc. â€” and their states.
7. **Add motion** â€” entrance (â‰¤ 200 ms), hover (â‰¤ 120 ms), state change (â‰¤ 160 ms).
8. **Ship the code** as a single file or per-component, with comments explaining choices.

## Tools

- None required.
- Optional: Figma plugin / Storybook for handoff.

## Examples

**User:** "Make a settings page for a developer tool."
**Response:** Mono headers, dense table layout, semantic tokens, keyboard hints
inline. Single-file React + Tailwind.

**User:** "Build a marketing landing page for an analytics product."
**Response:** Editorial typography, hero with real chart, three-tier pricing, full
marketing footer. Single-file HTML + Tailwind via CDN.

## Safety

- Respect the user's chosen stack and existing components
- Honor accessibility (contrast â‰¥ 4.5:1, focus states, reduced-motion media query)
- Do not invent fake testimonials, logos, or numbers
- Do not include tracking pixels without explicit consent

## Source

Auto-generated from openclawskills.net description.

## Pairs Well With

- `remotion-best-practices` (animated hero)
- `image-gen` (hero artwork)
- `coding-agent` (apply the result in a branch)
