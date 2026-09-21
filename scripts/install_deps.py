#!/usr/bin/env python3
"""
Install dependencies for selected skill categories.
Usage: python scripts/install_deps.py [--category CATEGORY] [--all] [--dry-run]
"""
import subprocess
import sys
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CATEGORY_REQS = {
    "nlp": ROOT / "skills/nlp/requirements.txt",
    "speech": ROOT / "skills/speech/requirements.txt",
    "vision": ROOT / "skills/vision/requirements.txt",
    "knowledge": ROOT / "skills/knowledge/requirements.txt",
    "system": ROOT / "skills/system/requirements.txt",
    "smart_home": ROOT / "skills/smart_home/requirements.txt",
    "communication": ROOT / "skills/communication/requirements.txt",
    "media": ROOT / "skills/media/requirements.txt",
    "productivity": ROOT / "skills/productivity/requirements.txt",
    "devtools": ROOT / "skills/devtools/requirements.txt",
    "security": ROOT / "skills/security/requirements.txt",
    "data_science": ROOT / "skills/data_science/requirements.txt",
    "navigation": ROOT / "skills/navigation/requirements.txt",
    "health": ROOT / "skills/health/requirements.txt",
    "finance": ROOT / "skills/finance/requirements.txt",
    "core": ROOT / "requirements-core.txt",
}

def install(req_file: Path, dry_run: bool = False):
    if not req_file.exists():
        print(f"  [SKIP] {req_file} not found")
        return
    print(f"  Installing from {req_file.name}...")
    if not dry_run:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(req_file)], check=True)
    else:
        print(f"  [DRY-RUN] Would run: pip install -r {req_file}")

def main():
    parser = argparse.ArgumentParser(description="Install All-Skills dependencies")
    parser.add_argument("--category", help="Specific category to install")
    parser.add_argument("--all", action="store_true", help="Install all categories")
    parser.add_argument("--dry-run", action="store_true", help="Preview without installing")
    args = parser.parse_args()

    if args.all:
        for cat, req in CATEGORY_REQS.items():
            print(f"\n[{cat}]")
            install(req, args.dry_run)
    elif args.category:
        req = CATEGORY_REQS.get(args.category)
        if req:
            install(req, args.dry_run)
        else:
            print(f"Unknown category: {args.category}")
            print(f"Available: {list(CATEGORY_REQS.keys())}")
    else:
        install(ROOT / "requirements-core.txt", args.dry_run)

if __name__ == "__main__":
    main()
