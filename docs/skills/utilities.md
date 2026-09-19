# Utilities Skills

_Generated: 2026-09-19T17:27:28+00:00_

General-purpose skills for working with files, text, images, and writing. Includes summarization, documentation generation, automation, and file management.

**20 skills in this category.**

## Skills

### `utilities.agent-transcript`

Create a redacted, consent-gated agent transcript for a pull request or issue.

- **Risk:** low
- **Path:** `utilities/agent-transcript`
- **Aliases:** —
- **Triggers:**
  - use agent-transcript
  - run agent-transcript
- **Source:** custom
- **Version:** 1.0.0

Create a redacted, consent-gated agent transcript for a pull request or issue.

### `utilities.audio-transcribe`

Transcribe audio into timestamped text and optionally extract speakers and actions.

- **Risk:** low
- **Path:** `utilities/audio-transcribe`
- **Aliases:** `speech-to-text`, `transcription`
- **Triggers:**
  - Transcribe this audio
  - Convert speech to text
  - Get a transcript
  - Speech recognition
- **Source:** custom
- **Version:** 1.0.0

Transcribe audio files into timestamped text with speaker identification and action extraction. The skill processes various audio formats and produces clean, usable transcripts for documentation or analysis.

### `utilities.automation`

Automate repetitive workflows — scripts, scheduled jobs, glue code, and "do this every time" tasks.

- **Risk:** medium
- **Path:** `utilities/automation`
- **Aliases:** `script`, `workflow-automation`, `glue`
- **Triggers:**
  - automate this
  - run this every day
  - write a script for
  - glue this together
- **Source:** custom
- **Version:** 1.0.0

Help the user automate repetitive tasks. Identify the trigger, write the script, and wire up scheduling where appropriate.

### `utilities.beam`

Publish a locally redacted coding-session snapshot only when explicitly requested.

- **Risk:** low
- **Path:** `utilities/beam`
- **Aliases:** —
- **Triggers:**
  - use beam
  - run beam
- **Source:** custom
- **Version:** 1.0.0

Publish a locally redacted coding-session snapshot only when explicitly requested.

### `utilities.documentation`

Write and structure documentation — READMEs, API docs, guides, and reference material.

- **Risk:** low
- **Path:** `utilities/documentation`
- **Aliases:** `docs`, `readme`, `api-docs`
- **Triggers:**
  - write docs for this
  - document this API
  - write a README
  - help me document
- **Source:** custom
- **Version:** 1.0.0

Help the user produce documentation that future readers will actually use. Focus on audience, structure, and accuracy.

### `utilities.file-management`

Safely and predictably manage files and directories — read, write, copy, move, rename, organize.

- **Risk:** medium
- **Path:** `utilities/file-management`
- **Aliases:** `fs`, `filesystem`, `file-ops`
- **Triggers:**
  - organize my files
  - rename these files
  - move files
  - clean up the folder
- **Source:** custom
- **Version:** 1.0.0

Help the user manage files and folders: organize, rename, copy, move, and clean up — with safety against accidental data loss.

### `utilities.handoff`

Prepare a portable context-rich handoff prompt for another coding agent.

- **Risk:** low
- **Path:** `utilities/handoff`
- **Aliases:** —
- **Triggers:**
  - use handoff
  - run handoff
- **Source:** custom
- **Version:** 1.0.0

Prepare a portable context-rich handoff prompt for another coding agent.

### `utilities.image`

Work with images — read, resize, convert, OCR, and inspect metadata.

- **Risk:** low
- **Path:** `utilities/image`
- **Aliases:** `images`, `ocr`, `image-processing`
- **Triggers:**
  - read this image
  - OCR this
  - resize image
  - convert image format
- **Source:** custom
- **Version:** 1.0.0

Work with image files: read metadata, resize, convert formats, OCR text from images.

### `utilities.parallel-agents`

Split independent work into isolated agent tasks and coordinate them concurrently.

- **Risk:** low
- **Path:** `utilities/parallel-agents`
- **Aliases:** `parallel-work`, `delegate-agents`, `multi-agent`
- **Triggers:**
  - run these independent tasks in parallel
  - delegate this work
- **Source:** obra/superpowers
- **Version:** 1.0.0

Split independent work into isolated agent tasks and coordinate them concurrently. The reviewed upstream workflow is preserved in `references/upstream-SKILL.md`.

### `utilities.readme-standard`

Write and review concise, progressive READMEs with executable examples and verified links.

- **Risk:** low
- **Path:** `utilities/readme-standard`
- **Aliases:** —
- **Triggers:**
  - use readme-standard
  - run readme-standard
- **Source:** custom
- **Version:** 1.0.0

Write and review concise, progressive READMEs with executable examples and verified links.

### `utilities.slack-synthesizer`

Summarize Slack threads into decisions, evidence, disagreements, and action items.

- **Risk:** low
- **Path:** `utilities/slack-synthesizer`
- **Aliases:** `slack`, `thread`
- **Triggers:**
  - Summarize this Slack thread
  - What was decided in this channel
  - Extract action items from Slack
  - Slack summary
- **Source:** custom
- **Version:** 1.0.0

Summarize Slack threads and channels into structured information: decisions made, key evidence and arguments, disagreements noted, and action items with owners. The skill helps users catch up on conversations without reading everything.

### `utilities.sonos-cli`

Inspect and control Sonos playback with room validation and confirmation for disruptive actions.

- **Risk:** low
- **Path:** `utilities/sonos-cli`
- **Aliases:** `sonos`, `music`, `speaker`, `playback`
- **Triggers:**
  - Control Sonos
  - Play music on Sonos
  - Sonos speaker
  - Pause Sonos
- **Source:** custom
- **Version:** 1.0.0

Inspect and control Sonos speakers through the CLI with room validation and confirmation required for disruptive actions like volume changes or playback interruption. The skill enables hands-free speaker management.

### `utilities.summarization`

Summarize long content — articles, documents, transcripts — at various lengths and for various audiences.

- **Risk:** low
- **Path:** `utilities/summarization`
- **Aliases:** `summary`, `tldr`, `abstract`
- **Triggers:**
  - summarize this
  - tldr
  - give me the summary
  - shorten this
- **Source:** custom
- **Version:** 1.0.0

Produce useful summaries at the right length and angle for the user. Different audiences and purposes need different summaries.

### `utilities.system-monitor`

Inspect system telemetry and summarize CPU, memory, disk, process, and network anomalies.

- **Risk:** low
- **Path:** `utilities/system-monitor`
- **Aliases:** `system`, `monitor`, `telemetry`, `metrics`, `performance`
- **Triggers:**
  - Check system status
  - System health
  - Server metrics
  - CPU usage
  - Memory check
- **Source:** custom
- **Version:** 1.0.0

Inspect system telemetry and provide clear summaries of CPU usage, memory allocation, disk space, running processes, and network activity. The skill highlights anomalies and helps diagnose performance issues.

### `utilities.telegram-actions`

Draft and perform user-approved Telegram actions without exposing bot credentials.

- **Risk:** medium
- **Path:** `utilities/telegram-actions`
- **Aliases:** `telegram`, `bot`, `message`, `telegram-bot`
- **Triggers:**
  - Send a Telegram message
  - Post to Telegram
  - Telegram notification
  - Message via Telegram
- **Source:** custom
- **Version:** 1.0.0

Draft and send messages through a Telegram bot without exposing bot tokens or credentials. The skill ensures all Telegram actions are explicitly approved by the user before execution.

### `utilities.text-processing`

Process text — search, replace, transform, dedupe, slice, and convert between common formats.

- **Risk:** low
- **Path:** `utilities/text-processing`
- **Aliases:** `text-utils`, `string-manipulation`
- **Triggers:**
  - process this text
  - find and replace
  - clean this text
  - transform this
- **Source:** custom
- **Version:** 1.0.0

Operate on text: search/replace, transformation, deduping, slicing, and format conversion.

### `utilities.unit-converter`

Convert units and currencies while showing assumptions, precision, and exchange-rate timestamps.

- **Risk:** low
- **Path:** `utilities/unit-converter`
- **Aliases:** `convert`, `units`, `currency`, `conversion`, `calculator`
- **Triggers:**
  - Convert units
  - Currency conversion
  - How many miles in a km
  - Convert this measurement
- **Source:** custom
- **Version:** 1.0.0

Convert between units of measurement and currencies with full transparency on assumptions, precision levels, and data freshness. The skill ensures accurate conversions with appropriate uncertainty indicators.

### `utilities.weather-now`

Retrieve current weather and local conditions with location, timestamp, and source clarity.

- **Risk:** low
- **Path:** `utilities/weather-now`
- **Aliases:** `weather`, `forecast`, `temperature`, `conditions`
- **Triggers:**
  - What's the weather
  - Weather forecast
  - Current conditions
  - Temperature
- **Source:** custom
- **Version:** 1.0.0

Retrieve current weather conditions and forecasts with clear location identification, timestamps, and data source attribution. The skill provides accurate weather information for planning and decision-making.

### `utilities.whatsapp-router`

Classify and route WhatsApp messages with consent, privacy, and escalation boundaries.

- **Risk:** high
- **Path:** `utilities/whatsapp-router`
- **Aliases:** `whatsapp`, `route`, `classify`
- **Triggers:**
  - Route this WhatsApp message
  - Categorize WhatsApp message
  - Process WhatsApp input
- **Source:** custom
- **Version:** 1.0.0

Classify incoming WhatsApp messages and route them to appropriate handlers based on content type, sender, and intent. The skill ensures proper consent verification and privacy boundaries are maintained.

### `utilities.writing`

Help the user write clearly — drafts, edits, tone, structure. Apply principles of clear writing.

- **Risk:** low
- **Path:** `utilities/writing`
- **Aliases:** `draft`, `edit`, `copywriting`
- **Triggers:**
  - help me write
  - edit this
  - draft an email
  - make this clearer
- **Source:** custom
- **Version:** 1.0.0

Help the user write clearly — for the audience, in the right tone, with the right structure.

