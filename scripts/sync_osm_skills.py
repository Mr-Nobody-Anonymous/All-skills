"""
OpenVoiceOS Skill Manager (OSM) Catalog Synchronization Utility.
Provides tools to query, inspect, search, and synchronize skills from
the official OpenVoiceOS Skills Manager curated manifest.
"""

import sys
import os
import json
import urllib.request
import argparse
from pathlib import Path
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
CACHE_FILE = REPO_ROOT / "data" / "databases" / "osm_catalog_cache.json"
MANIFEST_FILE = REPO_ROOT / "config" / "skills_manifest.yml"

OSM_CATALOG_RAW_URLS = [
    "https://raw.githubusercontent.com/OpenVoiceOS/ovos-skills-manager/skills-manifest/skills.json",
    "https://raw.githubusercontent.com/OpenVoiceOS/ovos-skills-manager/master/ovos_skills_manager/res/skills.json"
]

def load_manifest():
    if MANIFEST_FILE.exists():
        with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    return {}

def fetch_osm_catalog(force_refresh=False):
    """Fetch the OSM catalog from cache or remote."""
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not force_refresh and CACHE_FILE.exists():
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass

    print("[OSM] Fetching official OSM skills catalog from upstream...")
    catalog = None
    for url in OSM_CATALOG_RAW_URLS:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "All-Skills-OSM-Sync/2.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                if resp.status == 200:
                    catalog = json.loads(resp.read().decode("utf-8"))
                    print(f"[OSM] Successfully fetched catalog from: {url}")
                    break
        except Exception as e:
            print(f"[OSM] Attempt failed for {url}: {e}")

    if catalog is None:
        print("[OSM] Remote fetch failed or offline; using bundled provenance manifest as fallback.")
        manifest = load_manifest()
        prov = manifest.get("provenance", {})
        catalog = {
            "version": "fallback_prov",
            "skills": {}
        }
        for category, section in [
            ("ovos", prov.get("verified_openvoiceos_repos", {}).get("repos", [])),
            ("neon", prov.get("verified_neongecko_repos", {}).get("repos", [])),
            ("mycroft", prov.get("archived_mycroft_reference_repos", {}).get("repos", []))
        ]:
            for r in section:
                name = r.rstrip("/").split("/")[-1]
                catalog["skills"][name] = {
                    "url": r,
                    "name": name,
                    "origin": category,
                    "status": "verified" if category != "mycroft" else "archived"
                }

    try:
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(catalog, f, indent=2)
    except Exception as e:
        print(f"[WARN] Failed to write cache file: {e}")

    return catalog

def search_catalog(catalog, query):
    skills = catalog.get("skills", {})
    if isinstance(skills, list):
        items = [(s.get("name", ""), s) for s in skills]
    else:
        items = skills.items()

    results = []
    q = query.lower()
    for name, data in items:
        url = data.get("url", "")
        desc = data.get("description", "")
        if q in name.lower() or q in url.lower() or q in desc.lower():
            results.append((name, data))
    return results

def print_stats(catalog):
    skills = catalog.get("skills", {})
    count = len(skills)
    print(f"\n==========================================")
    print(f"OpenVoiceOS Skills Manager (OSM) Statistics")
    print(f"==========================================")
    print(f"Catalog Version  : {catalog.get('version', 'unknown')}")
    print(f"Indexed Skills   : {count}")
    print(f"Cache Location   : {CACHE_FILE.relative_to(REPO_ROOT) if CACHE_FILE.is_relative_to(REPO_ROOT) else CACHE_FILE}")
    print(f"==========================================\n")

def main():
    parser = argparse.ArgumentParser(description="Synchronize and query OpenVoiceOS Skills Manager (OSM) catalog")
    parser.add_argument("--refresh", action="store_true", help="Force refresh catalog from remote")
    parser.add_argument("--stats", action="store_true", help="Display catalog stats")
    parser.add_argument("--search", type=str, default=None, help="Search skills by keyword")
    parser.add_argument("--list", action="store_true", help="List all indexed skills")
    args = parser.parse_args()

    catalog = fetch_osm_catalog(force_refresh=args.refresh)

    if args.stats:
        print_stats(catalog)
        return

    if args.search:
        results = search_catalog(catalog, args.search)
        print(f"\n[OSM] Search results for '{args.search}' ({len(results)} matches):")
        for name, data in results:
            url = data.get("url", "N/A")
            desc = data.get("description", "No description available")
            print(f"  - {name}: {url}")
            if desc:
                print(f"      {desc[:100]}...")
        return

    if args.list:
        skills = catalog.get("skills", {})
        items = skills if isinstance(skills, list) else skills.values()
        print(f"\n[OSM] Listing all indexed skills ({len(items)} items):")
        for s in items:
            name = s.get("name", "unknown")
            url = s.get("url", "")
            print(f"  - {name:<35} {url}")
        return

    print_stats(catalog)
    print("Tip: Use --search <keyword> or --list to inspect skills.")

if __name__ == "__main__":
    main()
