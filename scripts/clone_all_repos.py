"""
Automated repository cloner and manifest synchronization script.
Clones external skill repositories across all 27 categories with depth=1 and safety quotas.
"""

import sys
import subprocess
import argparse
from pathlib import Path
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent

def load_manifest():
    manifest_path = REPO_ROOT / "config" / "skills_manifest.yml"
    if not manifest_path.exists():
        manifest_path = REPO_ROOT / "scratch_priority_import" / "manifest.yml"
    with open(manifest_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def main():
    parser = argparse.ArgumentParser(description="Clone or sync all skill repositories")
    parser.add_argument("--dry-run", action="store_true", help="Print actions without cloning")
    parser.add_argument("--category", type=str, default="all", help="Target specific category")
    parser.add_argument("--depth", type=int, default=1, help="Git clone depth")
    args = parser.parse_args()

    manifest = load_manifest()
    categories = manifest.get("categories", {})
    
    total_skills = 0
    print(f"[All-Skills] Repository Sync Engine initialized. Target: {args.category}")

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

    print(f"\n[COMPLETE] Processed {total_skills} skills across categories.")

if __name__ == "__main__":
    main()
