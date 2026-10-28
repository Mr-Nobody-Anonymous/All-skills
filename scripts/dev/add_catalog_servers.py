#!/usr/bin/env python3
"""One-shot maintainer helper: append verified connectors to ``mcps/catalog.json``.

Every entry here was checked against the public registry before it was added:

* npm packages resolved from ``https://registry.npmjs.org/<name>`` (200),
* PyPI packages resolved from ``https://pypi.org/pypi/<name>/json`` (200),
* every ``docs`` URL was taken from the package's own ``repository``/``homepage``
  metadata, so it points at the project that ships the server.

The script is additive only: an entry whose id already exists is left untouched.
Run ``python scripts/mcp_catalog.py verify && python scripts/mcp_catalog.py generate``
afterwards; the generated bundles and ``docs/MCP-CATALOG.md`` are authoritative.
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


def npm(server_id, name, description, package, *, tier, category, risk,
        env=(), args=(), version="latest", docs, license_, vendor, official=False):
    return {
        "id": server_id, "name": name, "description": description,
        "vendor": vendor, "official": official, "tier": tier, "category": category,
        "transport": "stdio", "command": "npx",
        "args": ["-y", f"{package}@{version}"] if version else ["-y", package, *args],
        "required_env": list(env), "risk": risk, "license": license_,
        "docs": docs, "harnesses": list(HARNESSES),
    }


def npm_args(server_id, name, description, package, args, *, tier, category, risk,
             env=(), docs, license_, vendor, official=False):
    return {
        "id": server_id, "name": name, "description": description,
        "vendor": vendor, "official": official, "tier": tier, "category": category,
        "transport": "stdio", "command": "npx",
        "args": ["-y", package, *args],
        "required_env": list(env), "risk": risk, "license": license_,
        "docs": docs, "harnesses": list(HARNESSES),
    }


def uvx(server_id, name, description, package, *, tier, category, risk,
        env=(), args=(), docs, license_, vendor, official=False):
    return {
        "id": server_id, "name": name, "description": description,
        "vendor": vendor, "official": official, "tier": tier, "category": category,
        "transport": "stdio", "command": "uvx",
        "args": [package, *args],
        "required_env": list(env), "risk": risk, "license": license_,
        "docs": docs, "harnesses": list(HARNESSES),
    }


SERVERS = [
    # ---------------------------------------------------------------- databases
    uvx(
        "mysql", "MySQL",
        "Inspect schemas and run read-only SQL against MySQL or MariaDB with an explicit use-case allowlist.",
        "mysql-mcp-server", tier="standard", category="database", risk="medium",
        env=["MYSQL_HOST", "MYSQL_USER", "MYSQL_PASSWORD", "MYSQL_DATABASE"],
        docs="https://github.com/designcomputer/mysql_mcp_server", license_="MIT",
        vendor="designcomputer",
    ),
    uvx(
        "neo4j", "Neo4j",
        "Cypher queries, graph schema inspection and read-only analytics over a Neo4j database.",
        "mcp-neo4j-cypher", tier="full", category="database", risk="medium",
        env=["NEO4J_URL", "NEO4J_USERNAME", "NEO4J_PASSWORD"],
        docs="https://github.com/neo4j-contrib/mcp-neo4j", license_="Apache-2.0",
        vendor="neo4j-contrib", official=True,
    ),
    uvx(
        "qdrant", "Qdrant",
        "Semantic memory over a Qdrant collection: store, recall and search vectorized notes.",
        "mcp-server-qdrant", tier="standard", category="database", risk="medium",
        env=["QDRANT_URL", "QDRANT_API_KEY", "COLLECTION_NAME"],
        docs="https://github.com/qdrant/mcp-server-qdrant", license_="Apache-2.0",
        vendor="qdrant", official=True,
    ),
    uvx(
        "chroma", "Chroma",
        "Vector search and document storage over a local, HTTP or Chroma Cloud collection.",
        "chroma-mcp", tier="full", category="database", risk="medium",
        env=["CHROMA_CLIENT_TYPE", "CHROMA_API_KEY", "CHROMA_TENANT", "CHROMA_DATABASE"],
        docs="https://github.com/chroma-core/chroma-mcp", license_="Apache-2.0",
        vendor="chroma-core", official=True,
    ),
    npm(
        "pinecone", "Pinecone",
        "Create, upsert, query and inspect Pinecone indexes and their records.",
        "@pinecone-database/mcp", tier="standard", category="database", risk="medium",
        env=["PINECONE_API_KEY"],
        docs="https://docs.pinecone.io/guides/operations/mcp-server",
        license_="Apache-2.0", vendor="pinecone", official=True,
    ),
    uvx(
        "snowflake", "Snowflake",
        "Read-only SQL against Snowflake with warehouse, role and schema awareness; writes stay opt-in.",
        "mcp-server-snowflake", tier="full", category="database", risk="high",
        env=["SNOWFLAKE_ACCOUNT", "SNOWFLAKE_USER", "SNOWFLAKE_PASSWORD",
             "SNOWFLAKE_WAREHOUSE", "SNOWFLAKE_DATABASE"],
        docs="https://github.com/isaacwasserman/mcp-snowflake-server", license_="MIT",
        vendor="isaacwasserman",
    ),
    npm_args(
        "bigquery", "BigQuery",
        "Query BigQuery datasets and inspect table metadata with the BigQuery SQL dialect.",
        "@ergut/mcp-bigquery-server",
        ["--project", "${BIGQUERY_PROJECT}", "--location", "${BIGQUERY_LOCATION}"],
        tier="full", category="database", risk="high",
        env=["BIGQUERY_PROJECT", "BIGQUERY_LOCATION", "GOOGLE_APPLICATION_CREDENTIALS"],
        docs="https://github.com/ergut/mcp-bigquery-server", license_="MIT",
        vendor="ergut",
    ),
    uvx(
        "duckdb", "DuckDB / MotherDuck",
        "Local DuckDB files and MotherDuck databases: SQL, schema exploration and ad-hoc analytics.",
        "mcp-server-motherduck", tier="standard", category="database", risk="medium",
        env=["MOTHERDUCK_TOKEN"], args=["--db-path", "${DUCKDB_PATH}"],
        docs="https://github.com/motherduckdb/mcp-server-motherduck", license_="MIT",
        vendor="motherduck", official=True,
    ),
    npm_args(
        "neon", "Neon",
        "Create and manage Neon Postgres projects, branches, and run SQL against them.",
        "@neondatabase/mcp-server-neon", ["start", "${NEON_API_KEY}"],
        tier="standard", category="database", risk="high", env=["NEON_API_KEY"],
        docs="https://github.com/neondatabase/mcp-server-neon", license_="MIT",
        vendor="neon", official=True,
    ),
    # ------------------------------------------------------------------- cloud
    npm_args(
        "azure", "Azure",
        "Azure resource management, diagnostics and service tooling through the official Azure MCP server.",
        "@azure/mcp", ["server", "start"],
        tier="full", category="cloud", risk="high", env=[],
        docs="https://github.com/microsoft/mcp/tree/main/servers/Azure.Mcp.Server",
        license_="MIT", vendor="microsoft", official=True,
    ),
    npm(
        "digitalocean", "DigitalOcean",
        "Manage Droplets, App Platform apps, databases and Kubernetes clusters on DigitalOcean.",
        "@digitalocean/mcp", tier="full", category="cloud", risk="high",
        env=["DIGITALOCEAN_API_TOKEN"],
        docs="https://github.com/digitalocean-labs/mcp-digitalocean", license_="MIT",
        vendor="digitalocean", official=True,
    ),
    npm(
        "heroku", "Heroku",
        "Inspect and operate Heroku apps, dynos, add-ons and releases.",
        "@heroku/mcp-server", tier="full", category="cloud", risk="high",
        env=["HEROKU_API_KEY"], docs="https://github.com/heroku/heroku-mcp-server",
        license_="Apache-2.0", vendor="heroku", official=True,
    ),
    npm(
        "netlify", "Netlify",
        "Create and deploy Netlify sites, manage environment variables and read deploy logs.",
        "@netlify/mcp", tier="full", category="cloud", risk="high",
        env=["NETLIFY_PERSONAL_ACCESS_TOKEN"],
        docs="https://docs.netlify.com/welcome/build-with-ai/netlify-mcp-server/",
        license_="ISC", vendor="netlify", official=True,
    ),
    npm(
        "google-cloud-run", "Google Cloud Run",
        "Deploy container images to Cloud Run, read service logs and manage revisions.",
        "cloud-run-mcp", tier="full", category="cloud", risk="high", env=[],
        docs="https://github.com/GoogleCloudPlatform/cloud-run-mcp",
        license_="Apache-2.0", vendor="google", official=True,
    ),
    npm_args(
        "firebase", "Firebase",
        "Firebase project tooling: Firestore, Auth, Hosting and emulator workflows via firebase-tools.",
        "firebase-tools", ["experimental:mcp"],
        tier="full", category="cloud", risk="high", env=[],
        docs="https://github.com/firebase/firebase-tools", license_="MIT",
        vendor="firebase", official=True,
    ),
    npm(
        "pulumi", "Pulumi",
        "Inspect stacks, preview and apply infrastructure changes, and query Pulumi Cloud.",
        "@pulumi/mcp-server", tier="full", category="infrastructure", risk="high",
        env=["PULUMI_ACCESS_TOKEN"],
        docs="https://www.pulumi.com/docs/iac/using-pulumi/mcp-server/",
        license_="Apache-2.0", vendor="pulumi", official=True,
    ),
    # ------------------------------------------------------- project & knowledge
    npm(
        "clickup", "ClickUp",
        "Tasks, lists, docs and comments in ClickUp workspaces.",
        "@taazkareem/clickup-mcp-server", tier="full", category="project-management",
        risk="medium", env=["CLICKUP_API_KEY", "CLICKUP_TEAM_ID"],
        docs="https://github.com/taazkareem/clickup-mcp-server", license_="Proprietary",
        vendor="taazkareem",
    ),
    npm(
        "trello", "Trello",
        "Boards, lists and cards: read and update Trello workflows.",
        "@delorenj/mcp-server-trello", tier="full", category="project-management",
        risk="medium", env=["TRELLO_API_KEY", "TRELLO_TOKEN"],
        docs="https://github.com/delorenj/mcp-server-trello", license_="MIT",
        vendor="delorenj",
    ),
    npm(
        "airtable", "Airtable",
        "Read and write Airtable bases, tables, records and schema.",
        "airtable-mcp-server", tier="standard", category="knowledge", risk="medium",
        env=["AIRTABLE_API_KEY"],
        docs="https://github.com/domdomegg/airtable-mcp-server", license_="MIT",
        vendor="domdomegg",
    ),
    npm(
        "todoist", "Todoist",
        "Tasks, projects, labels and comments in Todoist.",
        "@abhiz123/todoist-mcp-server", tier="standard", category="productivity",
        risk="medium", env=["TODOIST_API_TOKEN"],
        docs="https://github.com/abhiz123/todoist-mcp-server", license_="MIT",
        vendor="abhiz123",
    ),
    npm(
        "google-calendar", "Google Calendar",
        "List, create and update Google Calendar events across accounts.",
        "@cocal/google-calendar-mcp", tier="full", category="productivity", risk="medium",
        env=["GOOGLE_OAUTH_CREDENTIALS"],
        docs="https://github.com/nspady/google-calendar-mcp", license_="MIT",
        vendor="nspady",
    ),
    uvx(
        "google-sheets", "Google Sheets",
        "Read and write Google Sheets cells, sheets and Drive metadata.",
        "mcp-google-sheets", tier="full", category="productivity", risk="medium",
        env=["GOOGLE_APPLICATION_CREDENTIALS"],
        docs="https://github.com/xing5/mcp-google-sheets", license_="MIT",
        vendor="xing5",
    ),
    # --------------------------------------------------------------- automation
    npm(
        "n8n", "n8n",
        "Search, inspect and validate n8n workflow nodes and build automations from the catalog.",
        "n8n-mcp", tier="full", category="automation", risk="high",
        env=["N8N_API_URL", "N8N_API_KEY"], docs="https://github.com/czlonkowski/n8n-mcp",
        license_="MIT", vendor="czlonkowski",
    ),
    npm(
        "apify", "Apify",
        "Run Apify actors (scrapers, crawlers, extractors) and read their datasets.",
        "@apify/actors-mcp-server", tier="standard", category="automation", risk="high",
        env=["APIFY_TOKEN"], docs="https://github.com/apify/apify-mcp-server",
        license_="MIT", vendor="apify", official=True,
    ),
    npm(
        "e2b", "E2B Sandbox",
        "Spin up disposable cloud sandboxes and run code inside them.",
        "@e2b/mcp-server", tier="standard", category="execution", risk="high",
        env=["E2B_API_KEY"], docs="https://github.com/e2b-dev/mcp-server",
        license_="Apache-2.0", vendor="e2b", official=True,
    ),
    # ------------------------------------------------------- CI, QA and API tools
    npm(
        "circleci", "CircleCI",
        "Pipeline health, failed job logs and build configuration for CircleCI projects.",
        "@circleci/mcp-server-circleci", tier="full", category="ci-cd", risk="medium",
        env=["CIRCLECI_TOKEN"], docs="https://github.com/CircleCI-Public/mcp-server-circleci",
        license_="Apache-2.0", vendor="circleci", official=True,
    ),
    npm(
        "sonarqube", "SonarQube",
        "Code quality gates, issues and coverage from a SonarQube or SonarCloud instance.",
        "sonarqube-mcp-server", tier="full", category="testing", risk="medium",
        env=["SONARQUBE_URL", "SONARQUBE_TOKEN"],
        docs="https://github.com/SapientPants/sonarqube-mcp-server", license_="MIT",
        vendor="sapientpants",
    ),
    npm(
        "postman", "Postman",
        "Browse Postman collections, run API requests and inspect mock servers and workspaces.",
        "@postman/postman-mcp-server", tier="full", category="integration", risk="medium",
        env=["POSTMAN_API_KEY"], docs="https://github.com/postmanlabs/postman-mcp-server",
        license_="Apache-2.0", vendor="postman", official=True,
    ),
    # --------------------------------------------------- payments & communication
    npm(
        "paypal", "PayPal",
        "PayPal orders, payments, invoices and disputes for sandbox or live accounts.",
        "@paypal/mcp", tier="full", category="payments", risk="high",
        env=["PAYPAL_ACCESS_TOKEN", "PAYPAL_ENVIRONMENT"],
        docs="https://github.com/paypal/paypal-mcp-server", license_="Apache-2.0",
        vendor="paypal", official=True,
    ),
    npm(
        "resend", "Resend",
        "Send transactional email, manage audiences and inspect deliveries with Resend.",
        "resend-mcp", tier="full", category="communication", risk="high",
        env=["RESEND_API_KEY"], docs="https://github.com/resend/resend-mcp",
        license_="MIT", vendor="resend", official=True,
    ),
    npm_args(
        "twilio", "Twilio",
        "Send SMS and WhatsApp messages and inspect Twilio account resources.",
        "@twilio-alpha/mcp",
        ["${TWILIO_ACCOUNT_SID}/${TWILIO_API_KEY}/${TWILIO_API_SECRET}"],
        tier="full", category="communication", risk="high",
        env=["TWILIO_ACCOUNT_SID", "TWILIO_API_KEY", "TWILIO_API_SECRET"],
        docs="https://github.com/twilio-labs/mcp", license_="MIT", vendor="twilio",
    ),
    uvx(
        "elevenlabs", "ElevenLabs",
        "Text-to-speech, voice design and audio generation with the ElevenLabs API.",
        "elevenlabs-mcp", tier="standard", category="media", risk="medium",
        env=["ELEVENLABS_API_KEY"],
        docs="https://github.com/elevenlabs/elevenlabs-mcp", license_="MIT",
        vendor="elevenlabs", official=True,
    ),
]

# Standard profile additions: keyless, or a single token on a common workflow.
STANDARD_ADDS = [
    "duckdb", "pinecone", "qdrant", "airtable",
    "todoist", "apify", "e2b", "elevenlabs",
]


def main() -> int:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    existing = {server["id"] for server in catalog["servers"]}
    added = [server for server in SERVERS if server["id"] not in existing]
    catalog["servers"].extend(added)
    catalog["servers"].sort(key=lambda server: server["id"])

    standard = catalog["profiles"]["standard"]
    for server_id in STANDARD_ADDS:
        if server_id in {server["id"] for server in SERVERS} and server_id not in standard:
            standard.append(server_id)
    catalog["profiles"]["standard"] = standard

    CATALOG.write_text(json.dumps(catalog, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"added {len(added)} servers; catalog now has {len(catalog['servers'])}")
    print("  " + ", ".join(server["id"] for server in added))
    return 0


if __name__ == "__main__":
    sys.exit(main())
