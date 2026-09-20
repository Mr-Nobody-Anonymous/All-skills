"""
Automated repository cloner and manifest synchronization script.
Supports:
- Verified OpenVoiceOS repos (39 active)
- Verified NeonGeckoCom repos (28 active)
- Archived MycroftAI reference repos (22)
- Official OpenVoiceOS Skills Manager (OSM) catalog
- Safety disk quota checks to prevent disk overflow
- Manifest synchronization with zero deletions
"""

import sys
import os
import shutil
import subprocess
import argparse
from pathlib import Path
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent

def check_disk_safety(min_free_mb=100):
    total, used, free = shutil.disk_usage(REPO_ROOT)
    free_mb = free / (1024 * 1024)
    if free_mb < min_free_mb:
        print(f"[ERROR] Insufficient disk space: {free_mb:.1f}MB available, minimum {min_free_mb}MB required.")
        return False
    return True

def load_manifest():
    manifest_path = REPO_ROOT / "config" / "skills_manifest.yml"
    if not manifest_path.exists():
        manifest_path = REPO_ROOT / "scratch_priority_import" / "manifest.yml"
    with open(manifest_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def get_verified_repos(manifest, source="all"):
    prov = manifest.get("provenance", {})
    repos = []
    
    if source in ("all", "ovos", "verified_ovos"):
        for url in prov.get("verified_openvoiceos_repos", {}).get("repos", []):
            repos.append({"url": url, "org": "OpenVoiceOS", "status": "verified_active"})
            
    if source in ("all", "neon", "verified_neon"):
        for url in prov.get("verified_neongecko_repos", {}).get("repos", []):
            repos.append({"url": url, "org": "NeonGeckoCom", "status": "verified_active"})
            
    if source in ("all", "mycroft", "archived_mycroft"):
        for url in prov.get("archived_mycroft_reference_repos", {}).get("repos", []):
            repos.append({"url": url, "org": "MycroftAI", "status": "archived_reference"})
            
    if source in ("all", "osm"):
        cat_url = prov.get("official_catalog", {}).get("catalog_url")
        mgr_url = prov.get("official_catalog", {}).get("manager_url")
        if cat_url:
            repos.append({"url": cat_url, "org": "OpenVoiceOS", "status": "official_catalog"})
        if mgr_url:
            repos.append({"url": mgr_url, "org": "OpenVoiceOS", "status": "official_manager"})
            
    return repos

def main():
    parser = argparse.ArgumentParser(description="Clone or sync all skill repositories")
    parser.add_argument("--dry-run", action="store_true", help="Print actions without cloning")
    parser.add_argument("--source", type=str, default="all", choices=["all", "ovos", "neon", "mycroft", "osm", "manifest"], help="Filter by upstream source")
    parser.add_argument("--verified-only", action="store_true", help="Clone only verified active OVOS and Neon repos")
    parser.add_argument("--category", type=str, default="all", help="Target specific category")
    parser.add_argument("--depth", type=int, default=1, help="Git clone depth")
    parser.add_argument("--dest-dir", type=str, default=None, help="Custom destination directory (e.g. upstream/)")
    args = parser.parse_args()

    manifest = load_manifest()
    
    print(f"[All-Skills] Repository Sync Engine initialized.")
    print(f"  Source filter: {args.source} | Verified-only: {args.verified_only} | Category: {args.category}")
    
    if not args.dry_run and not check_disk_safety(min_free_mb=100):
        print("[ABORT] Exiting clone run to protect host filesystem.")
        sys.exit(1)

    if args.verified_only or args.source in ("ovos", "neon", "mycroft", "osm"):
        src = "ovos" if args.source == "ovos" else ("neon" if args.source == "neon" else ("mycroft" if args.source == "mycroft" else ("osm" if args.source == "osm" else "all")))
        if args.verified_only and src == "all":
            # only ovos and neon
            repos = get_verified_repos(manifest, "ovos") + get_verified_repos(manifest, "neon")
        else:
            repos = get_verified_repos(manifest, src)
            
        print(f"\n--- Processing {len(repos)} Verified Upstream Repositories ---")
        base_dest = Path(args.dest_dir) if args.dest_dir else (REPO_ROOT / "upstream")
        
        for r in repos:
            url = r["url"]
            repo_name = url.rstrip("/").split("/")[-1]
            org = r["org"]
            dest = base_dest / org / repo_name
            
            if dest.exists():
                print(f"  [EXISTS] {org}/{repo_name} at {dest.relative_to(REPO_ROOT) if dest.is_relative_to(REPO_ROOT) else dest}")
            elif args.dry_run:
                print(f"  [DRY-RUN] Would clone ({r['status']}) {url} -> {dest.relative_to(REPO_ROOT) if dest.is_relative_to(REPO_ROOT) else dest}")
            else:
                print(f"  [CLONE] ({r['status']}) {url} -> {dest}...")
                dest.parent.mkdir(parents=True, exist_ok=True)
                try:
                    subprocess.run(["git", "clone", "--depth", str(args.depth), "--single-branch", url, str(dest)], check=True)
                except Exception as e:
                    print(f"  [WARN] Failed to clone {url}: {e}")
        return

    # Category-based manifest sync
    categories = manifest.get("categories", {})
    total_skills = 0

    for cat_name, cat_data in categories.items():
        if args.category != "all" and args.category.lower() != cat_name.lower():
            continue
        skills = cat_data.get("skills", [])
        print(f"\n--- Category: {cat_name.upper()} ({len(skills)} skills) ---")
        for s in skills:
            total_skills += 1
            skill_id = s.get("id") or s.get("name")
            repo = s.get("repo")
            dest = REPO_ROOT / "skills" / cat_name / skill_id
            if dest.exists():
                print(f"  [EXISTS] {skill_id} at {dest.relative_to(REPO_ROOT)}")
            elif args.dry_run:
                print(f"  [DRY-RUN] Would clone {repo} -> {dest.relative_to(REPO_ROOT)}")
            else:
                print(f"  [CLONE] Cloning {repo} -> {dest.relative_to(REPO_ROOT)}...")
                dest.parent.mkdir(parents=True, exist_ok=True)
                try:
                    subprocess.run(["git", "clone", "--depth", str(args.depth), "--single-branch", repo, str(dest)], check=True)
                except Exception as e:
                    print(f"  [WARN] Failed to clone {repo}: {e}")

    print(f"\n[COMPLETE] Processed skills across categories. Manifest sync complete with zero deletions.")

if __name__ == "__main__":
    main()
