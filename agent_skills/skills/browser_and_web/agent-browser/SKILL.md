---
name: agent-browser
description: Operate an agent-browser CLI for auditable navigation, extraction, screenshots, and UI checks.
category: browser_and_web
aliases: [browser, headless-browser, puppeteer, playwright]
triggers:
  - Navigate to this URL
  - Take a screenshot
  - Extract data from a webpage
  - Fill out a web form
  - Click a button on a page
keywords: [browser, automation, navigation, scrape, screenshot, click, type, extract]
required_tools: [agent-browser, http-client]
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

# Agent Browser

## Purpose

Operate a headless browser CLI (agent-browser) for AI agents to interact with websites.
The skill enables navigation, clicking, typing, screenshot capture, and structured data
extraction with full auditability.

## When to Use

- The user wants to interact with a website programmatically
- Screenshot or visual verification is needed
- Form submission or data extraction is required
- Accessibility tree inspection is needed

## When NOT to Use

- The website blocks automated access (check robots.txt first)
- The action requires human interaction for CAPTCHAs
- The task is read-only but the website requires login

## Capabilities

- Navigate to URLs with configurable viewport and headers
- Click, type, scroll, and hover interactions
- Screenshot capture (full page or viewport)
- Accessibility tree extraction for LLM-readable content
- DOM extraction with CSS selectors
- Wait for elements, network idle, or custom conditions
- Proxy and authentication support

## Inputs

- `url` (required) â€” target URL
- `action` (required) â€” one of: navigate, click, type, screenshot, extract, wait
- `selector` (optional) â€” CSS selector for element targeting
- `value` (optional) â€” text to type or other action parameter
- `timeout` (optional, default 30s)

## Workflow

1. **Validate** â€” URL format, selector validity, required tools available
2. **Execute** â€” Run the browser action via agent-browser CLI
3. **Capture** â€” Store output (screenshot path, extracted text, error)
4. **Report** â€” Present results to user

## Tools

- `agent-browser` CLI
- Optional: screenshot storage, file system for outputs

## Examples

**User:** "Take a screenshot of example.com"
**Response:** Navigating to example.com... Screenshot saved to `screenshots/example-2026-02-09.png`

**User:** "Click the login button and extract the form fields"
**Response:** Clicked #login-btn. Extracted form fields: username, password, remember_me

## Safety

- Never store credentials in logs
- Respect robots.txt and terms of service
- Confirm before submitting forms or making changes

## Source

Auto-generated from openclawskills.net description.

## Pairs Well With

- `web-scraper` (structured data extraction)
- `form-filler` (multi-field form automation)
- `search-synthesizer` (research workflows)
