---
name: agol-search
description: "Search ArcGIS Online items and return clean, filtered results with safe defaults"
category: geospatial
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/danmaps/gis-agent-skills"
source_repository: "danmaps/gis-agent-skills"
source_path: "skills/agol-search/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---
# AGOL Search

Search ArcGIS Online for items and return a short, relevant list with actionable metadata.

## Inputs

- `query` (string)
- `item_types` (array, optional)
- `owner` (string, optional)
- `org_only` (bool, optional)
- `sort` (string, optional: relevance, modified, title)
- `limit` (int, optional, default 10)

## Output

List of items with:
- title
- type
- owner
- modified date
- url
- id

## Guidance

- Prefer exact matches when a title is provided
- If too many results, add filters: item type, owner, or org_only
- Do not expose credentials or tokens

## Example

**User:** “Find county parcels feature layers.”

**Output:** 5–10 items with URLs and owners, filtered to Feature Layer.

## Intent

State the operational goal of the skill and what good output should accomplish.

## Outputs

Return a concise, usable result with the key artifacts or recommendations.

## Safety

Do not invent data, credentials, or system context. Flag uncertainty and risky operations clearly.

