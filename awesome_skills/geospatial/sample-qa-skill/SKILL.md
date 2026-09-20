---
name: sample-qa-skill
description: "Minimal Q&A skill example with clear inputs and outputs"
category: geospatial
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/danmaps/gis-agent-skills"
source_repository: "danmaps/gis-agent-skills"
source_path: "skills/sample-qa-skill/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---
# Sample QA Skill

A tiny example skill that answers a question succinctly.

## Inputs

- `question` (string)

## Output

- `answer` (string)

## Example

**User:** “What is a geodatabase?”

**Output:** “A geodatabase is Esri’s container format for storing spatial data, tables, and relationships.”

## Intent

State the operational goal of the skill and what good output should accomplish.

## Outputs

Return a concise, usable result with the key artifacts or recommendations.

## Safety

Do not invent data, credentials, or system context. Flag uncertainty and risky operations clearly.

