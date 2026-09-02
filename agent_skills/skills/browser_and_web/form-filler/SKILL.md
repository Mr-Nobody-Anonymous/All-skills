---
name: form-filler
description: Fill web forms from user-approved data while requiring confirmation before submission.
category: browser_and_web
aliases: [form, autofill, webform, submit]
triggers:
  - Fill out this form
  - Submit this application
  - Auto-fill the form
  - Complete this registration
keywords: [form, fill, submit, autofill, webform, input]
required_tools: [browser-automation, agent-browser]
risk: high
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

# Form Filler

## Purpose

Fill web forms from structured data provided by the user, with explicit confirmation
required before any submission. The skill ensures data accuracy and prevents accidental
or unauthorized form submissions.

## When to Use

- The user provides specific data to fill into a web form
- Registration or application forms need to be completed
- Multi-step forms require sequential field population

## When NOT to Use

- The form contains sensitive personal data the user hasn't explicitly approved
- The form submission has legal or financial implications without user review
- The target site uses bot detection that requires human-like behavior

## Capabilities

- Identify form fields from page structure or provided mapping
- Support text inputs, checkboxes, radio buttons, selects, and textareas
- Handle multi-step forms with navigation
- Preview filled form before submission
- Provide clear confirmation prompts for submission
- Handle captchas and bot detection gracefully

## Inputs

- `url` (required) â€” target form URL
- `data` (required) â€” mapping of field names to values
- `field_mapping` (optional) â€” explicit selector-to-field mapping
- `submit` (optional, default: false) â€” whether to submit after filling
- `preview` (optional, default: true) â€” show preview before action

## Workflow

1. **Navigate** â€” Open the form URL
2. **Analyze** â€” Identify form fields and types
3. **Map** â€” Match provided data to form fields
4. **Preview** â€” Show filled form state to user
5. **Confirm** â€” Wait for explicit user approval
6. **Submit** â€” Only if confirmed, submit the form
7. **Report** â€” Present submission result or error

## Tools

- Browser automation (agent-browser, playwright, puppeteer)

## Examples

**User:** "Fill out this contact form with: name=John, email=john@example.com"
**Response:**
```
Form fields detected:
- Name: John âœ“
- Email: john@example.com âœ“
- Message: [empty]

Preview ready. Say "submit" to send, or provide message text.
```

## Safety

- ALWAYS require explicit confirmation before submission
- Never auto-submit forms
- Preview all data before filling
- Never store submitted form responses without consent
- Warn about potential consequences (legal, financial)

## Source

Auto-generated from openclawskills.net description.

## Pairs Well With

- `agent-browser` (for page interaction)
- `email-inbox-zero` (for form submission confirmations)
