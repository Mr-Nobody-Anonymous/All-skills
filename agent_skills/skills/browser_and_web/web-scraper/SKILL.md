---
name: web-scraper
description: Extract permitted public web data with rate limits, provenance, and robots/terms awareness.
category: browser_and_web
aliases: [scraper, crawl, extract, web-data]
triggers:
  - Scrape this webpage
  - Extract data from a website
  - Pull information from this URL
  - Parse web content
keywords: [scraping, extraction, crawl, data, parse, html, json]
required_tools: [http-client]
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

# Web Scraper

## Purpose

Extract structured data from public web pages with proper rate limiting, error handling,
and compliance with robots.txt and terms of service. The skill produces clean, usable data
with full provenance tracking.

## When to Use

- The user wants to extract specific data from a public website
- Research requires pulling information from multiple sources
- Data needs to be parsed from HTML into structured format

## When NOT to Use

- The website explicitly prohibits scraping (check terms of service)
- The data requires authentication or is behind a login
- The target is a single-page application that requires browser rendering

## Capabilities

- HTTP GET requests with proper headers (User-Agent, Accept)
- HTML parsing with CSS selectors or XPath
- JSON extraction from API endpoints
- Rate limiting (configurable requests per second)
- Retry logic with exponential backoff
- robots.txt compliance checking
- Output as JSON, CSV, or markdown tables

## Inputs

- `url` (required) â€” target URL or list of URLs
- `selectors` (required) â€” CSS selectors for data to extract
- `format` (optional) â€” one of: json, csv, markdown, table
- `rate_limit` (optional) â€” requests per second (default: 1)
- `respect_robots` (optional, default: true)

## Workflow

1. **Validate** â€” Check URL format, robots.txt compliance
2. **Fetch** â€” HTTP GET with proper headers
3. **Parse** â€” Extract data using specified selectors
4. **Format** â€” Convert to requested output format
5. **Store** â€” Save to file with provenance metadata

## Tools

- HTTP client (curl, wget, or Python requests)
- HTML parser (BeautifulSoup, lxml, or similar)

## Examples

**User:** "Extract all article titles from news.example.com"
**Response:**
```json
[
  {"title": "Article 1", "url": "https://news.example.com/1"},
  {"title": "Article 2", "url": "https://news.example.com/2"}
]
```

**User:** "Pull product prices from shop.example.com/products"
**Response:** Extracted 47 products. Saved to `data/shop-prices-2026-02-09.json`

## Safety

- Always check robots.txt before scraping
- Never bypass rate limits or authentication
- Store raw HTML alongside parsed data for verification
- Never store personally identifiable information

## Source

Auto-generated from openclawskills.net description.

## Pairs Well With

- `agent-browser` (for JavaScript-rendered pages)
- `search-synthesizer` (for multi-source research)
- `context-summarize` (to summarize scraped content)
