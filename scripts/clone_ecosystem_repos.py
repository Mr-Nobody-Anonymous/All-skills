"""
Automated Ecosystem Repository Cloner and Synchronizer.
Reads resources/master_clone_list.yaml (155+ upstream repositories)
and clones/syncs them into the proper format under upstream/<category>/<repo_name>.
Enforces:
- Zero deletions
- Free disk space threshold protection
- Shallow depth-1 single-branch clones
- Dry-run capability
"""

import sys
import os
import shutil
import subprocess
import argparse
from pathlib import Path
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
LIST_FILE = REPO_ROOT / "resources" / "master_clone_list.yaml"

def check_disk_safety(min_free_mb=500):
    total, used, free = shutil.disk_usage(REPO_ROOT)
    free_mb = free / (1024 * 1024)
    if free_mb < min_free_mb:
        print(f"[DISK GUARD] Critical: Only {free_mb:.1f}MB free on drive, minimum {min_free_mb}MB required.")
        return False, free_mb
    return True, free_mb

def load_catalog():
    if not LIST_FILE.exists():
        print(f"[ERROR] Catalog file not found at: {LIST_FILE}")
        sys.exit(1)
    with open(LIST_FILE, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def main():
    parser = argparse.ArgumentParser(description="Clone or sync ecosystem repositories across 24 categories")
    parser.add_argument("--dry-run", action="store_true", help="Inspect repositories and destination paths without cloning")
    parser.add_argument("--category", type=str, default="all", help="Target specific category (or 'all')")
    parser.add_argument("--repo", type=str, default=None, help="Target specific repository by name")
    parser.add_argument("--depth", type=int, default=1, help="Git clone depth (default 1 for space efficiency)")
    parser.add_argument("--dest-dir", type=str, default="upstream", help="Base destination folder (default: upstream)")
    parser.add_argument("--min-free-mb", type=int, default=300, help="Minimum free disk space threshold in MB")
    args = parser.parse_args()

    safe, free_mb = check_disk_safety(min_free_mb=args.min_free_mb)
    print(f"[All-Skills] Ecosystem Clone Engine initialized.")
    print(f"  Drive Free Space : {free_mb:.1f} MB (Threshold: {args.min_free_mb} MB)")
    print(f"  Target Category  : {args.category}")
    print(f"  Target Repo      : {args.repo or 'ALL'}")
    print(f"  Dry-run Mode     : {args.dry_run}")
    print(f"  Base Destination : {args.dest_dir}")
    print(f"  Clone Depth      : {args.depth}\n")

    if not args.dry_run and not safe:
        print("[ABORT] Exiting to protect local disk space. Use --dry-run to preview actions.")
        sys.exit(1)

    catalog = load_catalog()
    categories = catalog.get("categories", {})

    total_repos = 0
    cloned_repos = 0
    existing_repos = 0

    base_dest = REPO_ROOT / args.dest_dir

    for cat_key, cat_data in categories.items():
        if args.category != "all" and args.category.lower() != cat_key.lower():
            continue

        repos = cat_data.get("repos", [])
        print(f"=== Category: {cat_key.upper()} ({len(repos)} repositories) ===")

        for r in repos:
            name = r.get("name")
            url = r.get("url")
            desc = r.get("description", "")

            if args.repo and args.repo.lower() != name.lower():
                continue

            total_repos += 1
            target_path = base_dest / cat_key / name

            if target_path.exists():
                existing_repos += 1
                print(f"  [EXISTS] {name:<25} -> {target_path.relative_to(REPO_ROOT)}")
                continue

            if args.dry_run:
                print(f"  [DRY-RUN] Would clone {name:<25} ({url})")
                print(f"            Destination: {target_path.relative_to(REPO_ROOT)}")
                print(f"            Description: {desc[:80]}...")
            else:
                safe, free_mb = check_disk_safety(min_free_mb=args.min_free_mb)
                if not safe:
                    print(f"  [HALT] Remaining disk space ({free_mb:.1f}MB) reached safety threshold. Stopping.")
                    break

                print(f"  [CLONING] {name} from {url}...")
                target_path.parent.mkdir(parents=True, exist_ok=True)
                try:
                    cmd = ["git", "clone", "--depth", str(args.depth), "--single-branch", url, str(target_path)]
                    subprocess.run(cmd, check=True)
                    cloned_repos += 1
                    print(f"  [SUCCESS] Cloned {name} to {target_path.relative_to(REPO_ROOT)}")
                except Exception as e:
                    print(f"  [WARN] Failed to clone {name}: {e}")

    print(f"\n==========================================")
    print(f"Ecosystem Sync Summary:")
    print(f"  Total Repositories Processed : {total_repos}")
    print(f"  Already Existing             : {existing_repos}")
    print(f"  Cloned in This Session       : {cloned_repos}")
    print(f"==========================================\n")

if __name__ == "__main__":
    main()
