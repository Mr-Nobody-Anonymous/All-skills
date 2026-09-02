# Web Skills

_Generated: 2026-09-02T04:38:48+00:00_

Skills that interact with the live web: browser automation, web scraping, web extraction, SEO audits, accessibility testing, and end-to-end website testing. These skills are wrappers around concrete tools (Playwright, Lighthouse-style checks, a11y linters) but the library itself is tooling-light — the skills describe the workflow.

**6 skills in this category.**

## Skills

### `web.accessibility`

Accessibility (a11y) testing — WCAG checks, keyboard navigation, screen-reader semantics, color contrast.

- **Risk:** low
- **Path:** `web/accessibility`
- **Aliases:** `a11y`, `wcag`, `accessibility-testing`
- **Triggers:**
  - accessibility check
  - a11y audit
  - WCAG
  - is this accessible
  - keyboard navigation
- **Source:** custom
- **Version:** 1.0.0

Audit UI / web content for accessibility. Check against WCAG principles, keyboard navigation, screen-reader semantics, and color contrast.

### `web.browser-automation`

Drive a headless browser to interact with web pages — fill forms, click, screenshot, scrape, test, and verify UI behavior.

- **Risk:** medium
- **Path:** `web/browser-automation`
- **Aliases:** `playwright`, `puppeteer`, `headless-browser`, `browser-driver`
- **Triggers:**
  - automate this website
  - drive the browser
  - browser automation
  - click this button
  - fill this form
  - take a screenshot
- **Source:** custom
- **Version:** 1.0.0

Use a headless or visible browser to interact with web pages. Drive navigation, form interaction, scraping, and end-to-end UI tests.

### `web.seo`

Search engine optimization audits — on-page, technical, content, and link analysis with prioritized recommendations.

- **Risk:** low
- **Path:** `web/seo`
- **Aliases:** `search-engine-optimization`, `site-audit`
- **Triggers:**
  - SEO audit
  - check this page for SEO
  - improve SEO
  - meta tags
  - search rankings
- **Source:** custom
- **Version:** 1.0.0

Audit a site or page for SEO: on-page elements, technical issues, content quality, and links. Produce a prioritized list of recommendations.

### `web.web-extraction`

Extract specific information from a URL — main content, article text, structured fields — without full scraping infrastructure.

- **Risk:** low
- **Path:** `web/web-extraction`
- **Aliases:** `extract-from-url`, `article-extraction`, `main-content`
- **Triggers:**
  - extract the main content from this page
  - pull the article text
  - get the text from this URL
- **Source:** custom
- **Version:** 1.0.0

Pull the main textual content (or specific fields) from a single URL quickly. Lightweight alternative to full scraping for one-off needs.

### `web.web-scraping`

Extract structured data from websites — list pages, parse DOM, normalize records, and write to CSV / JSON.

- **Risk:** medium
- **Path:** `web/web-scraping`
- **Aliases:** `scrape`, `extraction`, `data-extraction`
- **Triggers:**
  - scrape this site
  - extract data from
  - pull all the X from this website
  - get me a list of
- **Source:** custom
- **Version:** 1.0.0

Extract structured data from one or more web pages. Discover pages, parse the relevant DOM, normalize the records, and write to a useful output format.

### `web.website-testing`

End-to-end testing of websites — happy paths, edge cases, browser matrix, and visual regressions.

- **Risk:** low
- **Path:** `web/website-testing`
- **Aliases:** `e2e-testing`, `end-to-end`, `visual-regression`
- **Triggers:**
  - test this website
  - e2e tests
  - end-to-end test
  - visual regression
- **Source:** custom
- **Version:** 1.0.0

End-to-end test a website's user flows across browsers. Catch regressions and ensure core flows work.

