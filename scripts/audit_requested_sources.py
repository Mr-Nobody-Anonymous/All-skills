#!/usr/bin/env python3
"""Resolve requested skill slugs against ClawHub's public catalog."""
from __future__ import annotations
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUGS = [
"git-workflow","summarize-repo","npm-auditor","docker-manager","adhd-task-breakdown",
"obsidian-sync","context-summarize","time-blocking","daily-journal","focus-guard",
"voice-to-action","web-scraper","form-filler","search-synthesizer","media-downloader",
"telegram-actions","whatsapp-router","email-inbox-zero","slack-synthesizer",
"calendar-assistant","meeting-action-extractor","image-gen","audio-transcribe",
"avatar-creator","system-monitor","cmd-safety-check","cf-worker-deploy","db-inspector",
"api-mock-generator","weather-now","sonos-cli","expense-parser","unit-converter",
"security-scanner","coding-agent","cursor-agent","github-cli","dokploy",
"remotion-best-practices","agent-browser","veo-video-generator",
]

def get_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "agent-skills-library-audit/1.0"})
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.load(response)

def main() -> int:
    report = {"registry": "https://clawhub.ai", "queried_at": "2026-09-01", "skills": []}
    for slug in SLUGS:
        url = "https://clawhub.ai/api/v1/search?q=" + urllib.parse.quote(slug)
        try:
            data = get_json(url)
            exact = [item for item in data.get("results", []) if item.get("slug") == slug]
            report["skills"].append({
                "requested_slug": slug,
                "status": "unique" if len(exact) == 1 else "missing" if not exact else "ambiguous",
                "matches": [{
                    "owner": item.get("ownerHandle"),
                    "slug": item.get("slug"),
                    "canonical_url": item.get("canonicalUrl"),
                    "summary": item.get("summary"),
                    "downloads": item.get("downloads"),
                    "installability": (item.get("trust") or {}).get("installability"),
                    "visibility": (item.get("trust") or {}).get("visibility"),
                    "source_identity": item.get("sourceIdentity"),
                } for item in exact],
            })
        except Exception as exc:
            report["skills"].append({"requested_slug": slug, "status": "error", "error": str(exc), "matches": []})
        time.sleep(0.05)
    out = ROOT / "skills" / "REQUESTED_SOURCES_AUDIT.json"
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for item in report["skills"]:
        owners = ",".join(match.get("owner") or "?" for match in item["matches"])
        print(f"{item['requested_slug']:<28} {item['status']:<10} {owners}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
