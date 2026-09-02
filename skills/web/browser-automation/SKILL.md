---
name: browser-automation
description: Drive a headless browser to interact with web pages — fill forms, click, screenshot, scrape, test, and verify UI behavior.
category: web
aliases: [playwright, puppeteer, headless-browser, browser-driver]
triggers:
  - automate this website
  - drive the browser
  - browser automation
  - click this button
  - fill this form
  - take a screenshot
keywords: [browser, automation, playwright, puppeteer, headless, click, screenshot, scrape]
dependencies: [optional:playwright-or-similar]
risk: medium
version: 1.0.0
source: custom
enabled: true
---

# Browser Automation

## Purpose

Use a headless or visible browser to interact with web pages. Drive navigation, form
interaction, scraping, and end-to-end UI tests.

## When to Use

- User wants to automate a web flow
- User wants screenshots / visual verification
- User wants end-to-end testing of a UI

## When NOT to Use

- User wants static data only and the site exposes an API (use that instead)
- The target site forbids automation in its TOS — confirm with the user

## Capabilities

- Navigate and wait for elements
- Click, type, fill forms
- Extract structured data from the DOM
- Take screenshots for verification
- Run multi-step flows

## Inputs

- Target URL
- Desired actions or data

## Safety

- Respect robots.txt where relevant
- Don't bypass CAPTCHAs or auth walls
- Don't auto-submit forms to third parties without explicit user intent
- Rate-limit requests

## Source

Custom skill, written for this library.

## Notes

Pairs with:
- `web-scraping`
- `accessibility-testing`
- `website-testing`

## Workflow

1. Confirm the goal, scope, and constraints.
2. Inspect the available context before acting.
3. Apply the skill-specific guidance in this document.
4. Verify the result and report limitations or next steps.

## Tools

- No mandatory tool unless declared in frontmatter.
- Use only project-approved tools and documented optional dependencies.

## Examples

Requests that should activate this skill include: "automate this website"; "drive the browser"; "browser automation".
