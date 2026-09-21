#!/usr/bin/env python3
"""
Download pre-trained models defined in models/model_registry.yaml.
Usage: python scripts/download_models.py [--model MODEL_ID] [--all] [--dry-run]
"""
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

def load_registry():
    try:
        import yaml
        reg_path = ROOT / "models/model_registry.yaml"
        with open(reg_path) as f:
            return yaml.safe_load(f).get("models", {})
    except Exception as e:
        print(f"Failed to load registry: {e}")
        return {}

def download_model(model_id: str, model_info: dict, dry_run: bool = False):
    cache = ROOT / model_info.get("cache_path", f"models/cache/{model_id}")
    if cache.exists():
        print(f"  [EXISTS] {model_id} already cached at {cache}")
        return
    print(f"  [DOWNLOAD] {model_id} ({model_info.get('size_mb', '?')} MB)")
    print(f"    URL: {model_info.get('url', 'N/A')}")
    print(f"    Cache: {cache}")
    if not dry_run:
        cache.mkdir(parents=True, exist_ok=True)
        print(f"    To download, install the provider package and run the model's download command.")
    else:
        print(f"  [DRY-RUN] Would download to {cache}")

def main():
    parser = argparse.ArgumentParser(description="Download All-Skills models")
    parser.add_argument("--model", help="Specific model ID")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    registry = load_registry()
    if not registry:
        print("No models in registry.")
        return

    if args.all:
        for mid, minfo in registry.items():
            download_model(mid, minfo, args.dry_run)
    elif args.model:
        minfo = registry.get(args.model)
        if minfo:
            download_model(args.model, minfo, args.dry_run)
        else:
            print(f"Unknown model: {args.model}")
            print(f"Available: {list(registry.keys())}")
    else:
        print("Available models:")
        for mid, minfo in registry.items():
            print(f"  {mid:40s} ({minfo.get('size_mb', '?')} MB)  {minfo.get('type', '')}")

if __name__ == "__main__":
    main()
