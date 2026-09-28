"""CLI and Orchestration Manager for the 9-Stage Ingestion Pipeline."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import List

from .pipeline import IngestionPipeline, REPO_ROOT


def run_batch_ingest(source_id: str, repo_url: str, branch: str, category: str, license_spdx: str = "MIT") -> None:
    pipeline = IngestionPipeline()
    print(f"[*] Registering upstream source: {source_id} ({repo_url})")
    pipeline.discover(source_id, repo_url, branch, license_spdx)
    print(f"[*] Source {source_id} successfully recorded in 00_discovered")


def inspect_status() -> None:
    pipeline = IngestionPipeline()
    root = pipeline.ingestion_root
    print("\n--- Ingestion Pipeline Status ---")
    for stage in pipeline.STAGES:
        p = root / stage
        count = sum(1 for _ in p.rglob("*") if _.is_file() and _.name != ".gitkeep")
        print(f"  {stage:22}: {count} artifacts")
    quarantine_count = sum(1 for _ in (root / "quarantine").rglob("*") if _.is_file())
    print(f"  {'quarantine':22}: {quarantine_count} flagged")
    print("---------------------------------\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="All-Skills Federated Ingestion Manager")
    subparsers = parser.add_subparsers(dest="command")

    status_cmd = subparsers.add_parser("status", help="Display pipeline stage artifact counts")

    discover_cmd = subparsers.add_parser("discover", help="Discover and register an upstream repository")
    discover_cmd.add_argument("--source-id", required=True, help="Short source slug (e.g. anthropics-skills)")
    discover_cmd.add_argument("--repo-url", required=True, help="Git clone URL")
    discover_cmd.add_argument("--branch", default="main", help="Git branch or commit SHA")
    discover_cmd.add_argument("--category", default="development", help="Default target category")
    discover_cmd.add_argument("--license", default="MIT", help="SPDX license")

    args = parser.parse_args()

    if args.command == "status":
        inspect_status()
        return 0
    elif args.command == "discover":
        run_batch_ingest(args.source_id, args.repo_url, args.branch, args.category, args.license)
        return 0
    else:
        inspect_status()
        return 0


if __name__ == "__main__":
    sys.exit(main())
