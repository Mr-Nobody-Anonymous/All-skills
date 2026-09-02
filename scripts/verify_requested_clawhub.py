#!/usr/bin/env python3
"""Fetch ClawHub verification envelopes for uniquely resolved requested skills."""
from __future__ import annotations
import json
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "skills" / "REQUESTED_SOURCES_AUDIT.json"
OUT = ROOT / "skills" / "REQUESTED_VERIFICATION_AUDIT.json"

def get_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "agent-skills-library-audit/1.0"})
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.load(response)

def main() -> int:
    source = json.loads(AUDIT.read_text(encoding="utf-8"))
    report = {"registry": source["registry"], "verified_at": "2026-09-01", "skills": []}
    for item in source["skills"]:
        if item["status"] != "unique":
            continue
        match = item["matches"][0]
        slug, owner = item["requested_slug"], match["owner"]
        query = urllib.parse.urlencode({"ownerHandle": owner})
        url = f"https://clawhub.ai/api/v1/skills/{urllib.parse.quote(slug)}/verify?{query}"
        try:
            envelope = get_json(url)
            security = envelope.get("security") or {}
            report["skills"].append({
                "slug": slug, "owner": owner, "ok": envelope.get("ok", False),
                "decision": envelope.get("decision"), "version": envelope.get("version"),
                "reasons": envelope.get("reasons", []), "security_status": security.get("status"),
                "security_summary": security.get("summary"), "provenance": envelope.get("provenance"),
                "artifact": envelope.get("artifact"), "page_url": envelope.get("pageUrl"),
            })
        except Exception as exc:
            report["skills"].append({"slug": slug, "owner": owner, "ok": False, "error": str(exc)})
    OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for item in report["skills"]:
        print(f"{item['slug']:<28} ok={str(item.get('ok')):<5} security={item.get('security_status')} version={item.get('version')} owner={item['owner']}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
