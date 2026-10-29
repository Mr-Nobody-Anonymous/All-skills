#!/usr/bin/env python3
"""Round-4 connectors: the integrations an external audit of this repo named as missing.

Each entry was verified before being written here:

* the distribution resolves on PyPI / npm,
* the console script name comes from the wheel's ``entry_points.txt`` (not guessed),
* the licence comes from the PyPI metadata or the upstream GitHub API,
* the required env var is documented in the package's own metadata/README.

Already present and therefore NOT re-added: ``github``, ``playwright``, ``context7``,
``supabase``, ``sentry``, ``figma``, ``linear``, ``atlassian``, ``brave-search``,
``firecrawl``, ``notion``, ``slack``, ``grafana``, ``cloudflare``, ``stripe``,
``google-drive``, ``hubspot``, ``huggingface``, ``exa``, ``docker``. ``zapier`` has
no verifiable public package (npm ``zapier-mcp`` is UNLICENSED 0.0.1), so it is
recorded as a gap in ``docs/AUDIT-RESPONSE.md`` instead of invented here.

Idempotent: existing ids are skipped.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "mcps" / "catalog.json"

HARNESSES = [
    "claude", "cursor", "codex", "vscode", "gemini", "windsurf", "cline", "roo",
    "goose", "opencode", "zed", "qwen", "kimi", "hermes", "openclaw", "trae",
    "codebuddy", "continue",
]


def entry(server_id, name, description, *, tier, category, risk, docs, license_,
          vendor, command="uvx", args=(), env=(), official=False, transport="stdio", url=None):
    block = {
        "id": server_id, "name": name, "description": description,
        "vendor": vendor, "official": official, "tier": tier, "category": category,
        "transport": transport,
    }
    if transport == "stdio":
        block["command"] = command
        block["args"] = list(args)
    else:
        block["url"] = url
    block["required_env"] = list(env)
    block.update({"risk": risk, "license": license_, "docs": docs, "harnesses": list(HARNESSES)})
    return block


SERVERS = [
    entry(
        "serena", "Serena",
        "Symbol-aware code intelligence: find and edit by symbol instead of by text, across many languages, with semantic retrieval over a repository.",
        tier="full", category="development", risk="medium",
        docs="https://github.com/oraios/serena", license_="GPL-3.0-or-later", vendor="oraios",
        command="uvx", args=["--from", "serena-agent", "serena", "start-mcp-server"],
    ),
    entry(
        "deepwiki", "DeepWiki",
        "Ask questions about an unfamiliar public repository and get answers grounded in its wiki-style documentation.",
        tier="full", category="knowledge", risk="low",
        docs="https://www.npmjs.com/package/deepwiki-mcp", license_="MIT", vendor="deepwiki",
        command="npx", args=["-y", "deepwiki-mcp@latest"],
    ),
    entry(
        "prometheus", "Prometheus",
        "Run PromQL against a Prometheus server: query metrics, inspect targets and labels, and pull range data for triage.",
        tier="full", category="observability", risk="medium",
        docs="https://github.com/pab1it0/prometheus-mcp-server", license_="MIT",
        vendor="pab1it0", command="uvx", args=["prometheus-mcp-server"],
        env=["PROMETHEUS_URL"],
    ),
    entry(
        "opentelemetry", "OpenTelemetry traces",
        "Query distributed traces from an OpenTelemetry backend (Jaeger, Phoenix, Traceloop) to explain latency and failures across services and LLM calls.",
        tier="full", category="observability", risk="medium",
        docs="https://github.com/traceloop/opentelemetry-mcp-server", license_="Apache-2.0",
        vendor="traceloop", command="uvx", args=["opentelemetry-mcp"],
        env=["BACKEND_TYPE", "BACKEND_URL"],
    ),
]


def main() -> int:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    existing = {server["id"] for server in catalog["servers"]}
    added = [server for server in SERVERS if server["id"] not in existing]
    catalog["servers"].extend(added)
    catalog["servers"].sort(key=lambda server: server["id"])
    CATALOG.write_text(json.dumps(catalog, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"added {len(added)} servers; catalog now has {len(catalog['servers'])}")
    print("  " + ", ".join(server["id"] for server in added))
    return 0


if __name__ == "__main__":
    sys.exit(main())
