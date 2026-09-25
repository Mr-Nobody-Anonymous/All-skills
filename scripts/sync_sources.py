#!/usr/bin/env python3
"""Import and update skills from upstream sources — lossless, pinned and reviewable.

Guarantees
- Whole skill packages are copied (``scripts/``, ``references/``, ``assets/``...),
  so relative references inside ``SKILL.md`` keep working.
- Upstream frontmatter is preserved as-is (``version``, ``disable-model-invocation``
  and every other field); the importer only adds ``category`` when missing and a
  ``source`` provenance record: repository, path, full commit SHA, license,
  real import timestamp and the package's content SHA-256.
- Licenses are never assumed: package LICENSE file, then repository LICENSE,
  then the license explicitly declared for the source in ``sources/registry.yaml``,
  otherwise ``NOASSERTION``.
- Identities are namespaced by (repository, path). A different upstream skill
  whose name collides with an existing one is imported as ``<slug>--<owner>``
  instead of being skipped or merged into the wrong skill.
- Existing imports are never overwritten silently. ``--update`` shows what
  changed (file list and a diff of SKILL.md); ``--update --apply`` backs the
  current package up under ``scratch/import_backups/<id>/`` before replacing it,
  and ``--rollback <id>`` restores it.
- Every import is recorded in ``sources/imports.lock.json``. A source may pin a
  revision with ``commit:`` in ``sources/registry.yaml``.

Usage
    python scripts/sync_sources.py                   # import new skills from every source
    python scripts/sync_sources.py --source superpowers
    python scripts/sync_sources.py --update          # review available updates (no writes)
    python scripts/sync_sources.py --update --apply  # apply updates (with backup)
    python scripts/sync_sources.py --rollback 20260925T101500Z
Third-party code is never executed during import.
"""
from __future__ import annotations

import argparse
import difflib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))
from skills.lock import compute_skill_tree_hash  # noqa: E402

SOURCES_REGISTRY = REPO_ROOT / "sources" / "registry.yaml"
IMPORTS_LOCK = REPO_ROOT / "sources" / "imports.lock.json"
AWESOME_DIR = REPO_ROOT / "awesome_skills"
SCRATCH_DIR = REPO_ROOT / "scratch" / "temp_upstream_sync"
BACKUP_DIR = REPO_ROOT / "scratch" / "import_backups"
SLUG_CLEANER = re.compile(r"[^a-z0-9-_]")
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", re.DOTALL)
IGNORED_PARTS = {".git", "__pycache__", "node_modules", ".DS_Store"}


# ─── helpers ────────────────────────────────────────────────────────────────

def remove_readonly(func, path, excinfo):  # pragma: no cover - Windows only
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except Exception:
        pass


def cleanup_scratch_dir(path: Path) -> None:
    if path.exists():
        if sys.version_info >= (3, 12):
            shutil.rmtree(path, onexc=remove_readonly)
        else:
            shutil.rmtree(path, onerror=remove_readonly)


def slugify(text: str) -> str:
    s = text.lower().strip()
    s = re.sub(r"[\s_]+", "-", s)
    s = SLUG_CLEANER.sub("", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s or "unnamed-skill"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def load_sources_registry(path: Optional[Path] = None) -> List[Dict[str, Any]]:
    path = path or SOURCES_REGISTRY
    if not path.exists():
        return []
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return list(data.get("sources", []))


def infer_category(repo: str, rel_path: str, skill_name: str) -> str:
    path_lower = f"{repo}/{rel_path}/{skill_name}".lower()
    rules = [
        (("scientific", "k-dense", "biology", "chemistry"), "science-research"),
        (("win-dev", "winui"), "desktop"),
        (("dotnet", "csharp", "aspnet"), "software-engineering"),
        (("copilot", "openhands"), "development"),
        (("superpowers", "tdd", "testing"), "testing"),
        (("security", "audit", "vulnerability"), "security"),
        (("cloud", "azure", "aws", "kubernetes"), "cloud"),
        (("database", "sql", "postgres"), "database"),
        (("llm", "prompt", "agent"), "ai-engineer"),
        (("frontend", "react", "css"), "frontend"),
    ]
    for needles, category in rules:
        if any(n in path_lower for n in needles):
            return category
    return "development"


# ─── license detection ──────────────────────────────────────────────────────

_LICENSE_PATTERNS = [
    (re.compile(r"Apache License,?\s+Version 2\.0", re.I), "Apache-2.0"),
    (re.compile(r"\bMIT License\b|Permission is hereby granted, free of charge", re.I), "MIT"),
    (re.compile(r"GNU GENERAL PUBLIC LICENSE\s+Version 3", re.I), "GPL-3.0"),
    (re.compile(r"GNU GENERAL PUBLIC LICENSE\s+Version 2", re.I), "GPL-2.0"),
    (re.compile(r"Mozilla Public License,?\s+(Version|v\.?)\s*2\.0", re.I), "MPL-2.0"),
    (re.compile(r"BSD 3-Clause|Redistributions of source code must retain.*Neither the name", re.I | re.S), "BSD-3-Clause"),
    (re.compile(r"BSD 2-Clause", re.I), "BSD-2-Clause"),
    (re.compile(r"Creative Commons Attribution 4\.0|CC BY 4\.0", re.I), "CC-BY-4.0"),
]


def _license_from_file(folder: Path) -> Optional[str]:
    for name in ("LICENSE", "LICENSE.md", "LICENSE.txt", "LICENCE", "COPYING"):
        f = folder / name
        if f.is_file():
            text = f.read_text(encoding="utf-8", errors="ignore")[:4000]
            for pattern, spdx in _LICENSE_PATTERNS:
                if pattern.search(text):
                    return spdx
            return "LicenseRef-see-LICENSE"
    return None


def detect_license(package_dir: Path, checkout: Path, declared: Optional[str]) -> Tuple[str, str]:
    """Return (license, how it was determined). Never assumes a license."""
    found = _license_from_file(package_dir)
    if found:
        return found, "package LICENSE file"
    found = _license_from_file(checkout)
    if found:
        return found, "repository LICENSE file"
    if declared:
        return str(declared), "declared in sources/registry.yaml"
    return "NOASSERTION", "no license information found"


# ─── fetching ───────────────────────────────────────────────────────────────

def fetch_source(source: Dict[str, Any], dest: Path) -> str:
    """Clone a source into ``dest`` and return the full commit SHA checked out."""
    repo = str(source.get("url") or source.get("repo") or "")
    local = Path(repo)
    url = str(local) if local.exists() else (repo if "://" in repo or repo.startswith("git@") else f"https://github.com/{repo}.git")
    cleanup_scratch_dir(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    pinned = source.get("commit")
    if pinned:
        subprocess.run(["git", "init", "-q", str(dest)], check=True)
        subprocess.run(["git", "-C", str(dest), "fetch", "-q", "--depth", "1", url, str(pinned)], check=True, timeout=180)
        subprocess.run(["git", "-C", str(dest), "checkout", "-q", "FETCH_HEAD"], check=True)
    else:
        cmd = ["git", "clone", "-q", "--depth", "1"]
        if source.get("branch"):
            cmd += ["--branch", str(source["branch"])]
        subprocess.run(cmd + [url, str(dest)], check=True, timeout=180)
    sha = subprocess.run(["git", "-C", str(dest), "rev-parse", "HEAD"], check=True, capture_output=True, text=True)
    return sha.stdout.strip()


def discover_packages(checkout: Path, skill_paths: Optional[List[str]]) -> List[Tuple[Path, str]]:
    """(package_dir, path relative to the repository) for every SKILL.md under ``skill_paths``."""
    roots = [checkout / p for p in skill_paths] if skill_paths else [checkout]
    found: Dict[str, Path] = {}
    for root in roots:
        if not root.exists():
            continue
        for skill_md in sorted(root.rglob("SKILL.md")):
            if IGNORED_PARTS & set(skill_md.relative_to(checkout).parts):
                continue
            rel = skill_md.parent.relative_to(checkout).as_posix()
            found[rel] = skill_md.parent
    return [(found[rel], rel) for rel in sorted(found)]


# ─── packaging ──────────────────────────────────────────────────────────────

def _ignore(_dir: str, names: List[str]) -> List[str]:
    return [n for n in names if n in IGNORED_PARTS]


def merge_frontmatter(skill_md_text: str, slug: str, category: str, provenance: Dict[str, Any]) -> str:
    """Keep the upstream frontmatter and body; add category (if absent) and provenance."""
    match = FRONTMATTER_RE.match(skill_md_text)
    meta: Dict[str, Any] = {}
    body = skill_md_text
    if match:
        loaded = yaml.safe_load(match.group(1))
        if isinstance(loaded, dict):
            meta = loaded
        body = match.group(2)
    if not meta.get("name"):
        meta["name"] = slug
    if not meta.get("description"):
        first = next((ln.strip("# ").strip() for ln in body.splitlines() if ln.strip() and not ln.startswith("---")), "")
        if first:
            meta["description"] = first[:250]
    meta.setdefault("category", category)
    upstream_source = meta.get("source")
    record = dict(provenance)
    if upstream_source and upstream_source != provenance:
        record["upstream_source"] = upstream_source
    meta["source"] = record
    dumped = yaml.safe_dump(meta, sort_keys=False, allow_unicode=True, width=1000)
    return f"---\n{dumped}---\n{body if body.startswith(chr(10)) else chr(10) + body}"


def install_package(package_dir: Path, dest: Path, slug: str, category: str, provenance: Dict[str, Any]) -> None:
    """Copy the full package, then rewrite only SKILL.md's frontmatter."""
    shutil.copytree(package_dir, dest, ignore=_ignore)
    skill_md = dest / "SKILL.md"
    skill_md.write_text(merge_frontmatter(skill_md.read_text(encoding="utf-8", errors="replace"),
                                          slug, category, provenance), encoding="utf-8")


# ─── plan ───────────────────────────────────────────────────────────────────

@dataclass
class PlanItem:
    action: str  # new | changed | unchanged | legacy
    repository: str
    path: str
    package_dir: Path
    dest: Path
    content_sha256: str
    details: List[str] = field(default_factory=list)


def load_lock(path: Optional[Path] = None) -> Dict[str, Any]:
    path = path or IMPORTS_LOCK
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {"version": 1, "imports": {}}


def save_lock(lock: Dict[str, Any], path: Optional[Path] = None) -> None:
    path = path or IMPORTS_LOCK
    lock["imports"] = dict(sorted(lock["imports"].items()))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(lock, indent=2) + "\n", encoding="utf-8")


def legacy_index(awesome_dir: Path) -> Dict[Tuple[str, str], Path]:
    """Catalog skills imported before the lock existed, keyed by (repository, path)."""
    index: Dict[Tuple[str, str], Path] = {}
    for skill_md in awesome_dir.glob("*/*/SKILL.md"):
        match = FRONTMATTER_RE.match(skill_md.read_text(encoding="utf-8", errors="replace"))
        if not match:
            continue
        try:
            meta = yaml.safe_load(match.group(1))
        except yaml.YAMLError:
            continue
        if not isinstance(meta, dict):
            continue
        src = meta.get("source")
        repo = src.get("repository") if isinstance(src, dict) else meta.get("source_repository")
        path = src.get("path") if isinstance(src, dict) else meta.get("source_path")
        if repo and path:
            key = (str(repo).strip(), re.sub(r"/SKILL\.md$", "", str(path).strip().strip("/")))
            index[key] = skill_md.parent
    return index


def plan_source(repository: str, checkout: Path, skill_paths: Optional[List[str]], lock: Dict[str, Any],
                awesome_dir: Path, legacy: Dict[Tuple[str, str], Path],
                category: Optional[str] = None) -> List[PlanItem]:
    """Classify every package of a source as new / changed / unchanged / legacy.

    ``category`` (optional, from the source definition) overrides the keyword
    inference used to place *new* packages; existing imports never move.
    """
    by_identity = {(v["repository"], v["path"]): awesome_dir.parent / k for k, v in lock["imports"].items()}
    local = Path(repository)
    owner = slugify(local.name if local.exists() else repository.split("/")[0])
    items: List[PlanItem] = []
    claimed: set[Path] = set()
    for package_dir, rel in discover_packages(checkout, skill_paths):
        digest, _ = compute_skill_tree_hash(package_dir)
        identity = (repository, rel)
        if identity in by_identity:
            dest = by_identity[identity]
            locked = lock["imports"][dest.relative_to(awesome_dir.parent).as_posix()]
            action = "unchanged" if locked.get("content_sha256") == digest else "changed"
            items.append(PlanItem(action, repository, rel, package_dir, dest, digest))
            continue
        if identity in legacy:
            items.append(PlanItem("legacy", repository, rel, package_dir, legacy[identity], digest,
                                  ["imported before sources/imports.lock.json existed; unpinned"]))
            continue
        slug = slugify(package_dir.name)
        target_category = slugify(category) if category else infer_category(repository, rel, slug)
        dest = awesome_dir / target_category / slug
        if dest.exists() or dest in claimed:
            dest = awesome_dir / target_category / f"{slug}--{owner}"
        claimed.add(dest)
        items.append(PlanItem("new", repository, rel, package_dir, dest, digest))
    return items


def describe_changes(item: PlanItem, limit: int = 40) -> List[str]:
    """File-level changes and a SKILL.md diff between the local package and upstream."""
    def files(root: Path) -> Dict[str, bytes]:
        return {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob("*")
                if p.is_file() and not IGNORED_PARTS & set(p.relative_to(root).parts)}
    local, upstream = files(item.dest), files(item.package_dir)
    lines = [f"  + {f}" for f in sorted(set(upstream) - set(local))]
    lines += [f"  - {f}" for f in sorted(set(local) - set(upstream))]
    lines += [f"  ~ {f}" for f in sorted(set(local) & set(upstream)) if f != "SKILL.md" and local[f] != upstream[f]]
    if "SKILL.md" in local and "SKILL.md" in upstream:
        strip = lambda b: FRONTMATTER_RE.sub(r"\2", b.decode("utf-8", "replace"))  # noqa: E731
        diff = list(difflib.unified_diff(strip(local["SKILL.md"]).splitlines(), strip(upstream["SKILL.md"]).splitlines(),
                                         "local SKILL.md", "upstream SKILL.md", n=1, lineterm=""))
        lines += ["    " + d for d in diff[:limit]]
        if len(diff) > limit:
            lines.append(f"    ... {len(diff) - limit} more diff lines")
    return lines


# ─── apply / rollback ───────────────────────────────────────────────────────

def provenance_for(item: PlanItem, commit: str, checkout: Path, declared_license: Optional[str]) -> Dict[str, Any]:
    license_id, how = detect_license(item.package_dir, checkout, declared_license)
    return {
        "repository": item.repository,
        "path": item.path,
        "commit": commit,
        "license": license_id,
        "license_source": how,
        "imported_at": now_utc(),
        "content_sha256": item.content_sha256,
    }


def apply_items(items: List[PlanItem], commit: str, checkout: Path, declared_license: Optional[str],
                lock: Dict[str, Any], apply_updates: bool, backup_id: str, backup_root: Optional[Path] = None) -> Dict[str, int]:
    backup_root = backup_root or BACKUP_DIR
    counts = {"imported": 0, "updated": 0}
    for item in items:
        if item.action == "new" or (item.action in ("changed", "legacy") and apply_updates):
            if item.dest.exists():
                backup = backup_root / backup_id / item.dest.relative_to(AWESOME_DIR.parent)
                backup.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(item.dest), str(backup))
            prov = provenance_for(item, commit, checkout, declared_license)
            install_package(item.package_dir, item.dest, slugify(item.dest.name), item.dest.parent.name, prov)
            lock["imports"][item.dest.relative_to(AWESOME_DIR.parent).as_posix()] = prov
            counts["imported" if item.action == "new" else "updated"] += 1
    if counts["updated"]:
        snapshot = backup_root / backup_id / "imports.lock.before.json"
        snapshot.parent.mkdir(parents=True, exist_ok=True)
        if IMPORTS_LOCK.exists() and not snapshot.exists():
            shutil.copy2(IMPORTS_LOCK, snapshot)
    return counts


def rollback(backup_id: str, backup_root: Optional[Path] = None) -> int:
    root = (backup_root or BACKUP_DIR) / backup_id
    if not root.is_dir():
        print(f"No backup named {backup_id!r} in {backup_root or BACKUP_DIR}", file=sys.stderr)
        return 1
    restored = 0
    for skill_md in sorted(root.rglob("SKILL.md")):
        package = skill_md.parent
        target = AWESOME_DIR.parent / package.relative_to(root)
        if target.exists():
            shutil.rmtree(target)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(package, target)
        restored += 1
    snapshot = root / "imports.lock.before.json"
    if snapshot.exists():
        shutil.copy2(snapshot, IMPORTS_LOCK)
    print(f"Restored {restored} package(s) from backup {backup_id}.")
    return 0


# ─── CLI ────────────────────────────────────────────────────────────────────

def run(sources: List[Dict[str, Any]], update: bool, apply_updates: bool) -> int:
    lock = load_lock()
    legacy = legacy_index(AWESOME_DIR)
    backup_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    totals = {"new": 0, "changed": 0, "unchanged": 0, "legacy": 0, "imported": 0, "updated": 0}
    for source in sources:
        repository = str(source.get("repo") or source.get("url") or "")
        if not repository:
            continue
        print(f"\n📥 {source.get('id', repository)} ({repository})")
        try:
            commit = fetch_source(source, SCRATCH_DIR)
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
            print(f"  ❌ fetch failed: {exc}")
            continue
        try:
            items = plan_source(repository, SCRATCH_DIR, source.get("skill_paths"), lock, AWESOME_DIR, legacy,
                                source.get("category"))
            for item in items:
                totals[item.action] += 1
            reviewable = [i for i in items if i.action in ("changed", "legacy")]
            if update:
                for item in reviewable:
                    print(f"  {item.action.upper():9} {item.path} -> {item.dest.relative_to(REPO_ROOT)}")
                    for line in describe_changes(item):
                        print(line)
            counts = apply_items([i for i in items if i.action == "new" or (update and apply_updates)],
                                 commit, SCRATCH_DIR, source.get("license"), lock, update and apply_updates, backup_id)
            totals["imported"] += counts["imported"]
            totals["updated"] += counts["updated"]
            print(f"  commit {commit[:12]}: {counts['imported']} imported, {counts['updated']} updated, "
                  f"{sum(1 for i in items if i.action == 'unchanged')} unchanged, {len(reviewable)} with updates to review")
        finally:
            cleanup_scratch_dir(SCRATCH_DIR)
    save_lock(lock)
    print(f"\nSummary: {totals['imported']} new skill(s) imported, {totals['updated']} updated, "
          f"{totals['changed'] + totals['legacy'] - totals['updated']} update(s) awaiting review "
          f"(run with --update, then --update --apply).")
    if totals["updated"]:
        print(f"Backup of replaced packages: scratch/import_backups/{backup_id} (--rollback {backup_id})")
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Import and update skills from upstream sources")
    parser.add_argument("--source", action="append", help="Only this source id (repeatable)")
    parser.add_argument("--update", action="store_true", help="Review updates to existing imports (no writes)")
    parser.add_argument("--apply", action="store_true", help="With --update: apply the reviewed updates (with backup)")
    parser.add_argument("--rollback", metavar="BACKUP_ID", help="Restore packages replaced by an --apply run")
    args = parser.parse_args(argv)
    if args.rollback:
        return rollback(args.rollback)
    sources = load_sources_registry()
    if args.source:
        sources = [s for s in sources if s.get("id") in set(args.source)]
    if not sources:
        print("No matching sources in sources/registry.yaml", file=sys.stderr)
        return 1
    return run(sources, args.update, args.apply)


if __name__ == "__main__":
    sys.exit(main())
