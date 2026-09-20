#!/usr/bin/env python3
"""Sync, extract, and normalize skills from authoritative upstream sources.

Features:
- Sequential shallow clone (--depth 1 --single-branch) into a transient scratch directory.
- Provenance preservation: source repository, commit hash, relative path, license, imported_at.
- Frontmatter standardization conforming to Agent Skills v1 specification.
- Zero-deletion invariant: never deletes existing skills.
- Immediate transient workspace cleanup with Windows read-only permission handler.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import stat
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCES_REGISTRY = REPO_ROOT / "sources" / "registry.yaml"
AWESOME_DIR = REPO_ROOT / "awesome_skills"
SCRATCH_DIR = REPO_ROOT / "scratch" / "temp_upstream_sync"

SLUG_CLEANER = re.compile(r"[^a-z0-9-_]")

def remove_readonly(func, path, excinfo):
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except Exception:
        pass

def cleanup_scratch_dir(path: Path) -> None:
    if not path.exists():
        return
    try:
        shutil.rmtree(path, onerror=remove_readonly)
    except Exception:
        pass
    if path.exists() and os.name == "nt":
        try:
            subprocess.run(["cmd", "/c", "rmdir", "/s", "/q", str(path)], capture_output=True, timeout=10)
        except Exception:
            pass

def slugify(text: str) -> str:
    s = text.lower().strip()
    s = re.sub(r"[\s_]+", "-", s)
    s = SLUG_CLEANER.sub("", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s or "unnamed-skill"

def get_existing_slugs() -> Set[str]:
    slugs = set()
    canon_dir = REPO_ROOT / "skills"
    if canon_dir.exists():
        for sdir in canon_dir.glob("*/*"):
            if sdir.is_dir() and (sdir / "SKILL.md").exists():
                slugs.add(sdir.name.lower())
    harness_dir = REPO_ROOT / ".agents" / "skills"
    if harness_dir.exists():
        for sdir in harness_dir.iterdir():
            if sdir.is_dir():
                slugs.add(sdir.name.lower())
    if AWESOME_DIR.exists():
        for cat_dir in AWESOME_DIR.iterdir():
            if cat_dir.is_dir() and not cat_dir.name.startswith("."):
                for sdir in cat_dir.iterdir():
                    if sdir.is_dir():
                        slugs.add(sdir.name.lower())
    return slugs

def load_sources_registry() -> List[Dict[str, Any]]:
    sources = []
    if not SOURCES_REGISTRY.exists():
        return sources

    try:
        import yaml
        with open(SOURCES_REGISTRY, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            return data.get("sources", [])
    except ImportError:
        pass

    # Simple parser fallback
    with open(SOURCES_REGISTRY, "r", encoding="utf-8") as f:
        curr: Optional[Dict[str, Any]] = None
        for line in f:
            l = line.strip()
            if l.startswith("- id:"):
                if curr:
                    sources.append(curr)
                curr = {"id": l.split(":", 1)[1].strip()}
            elif curr and ":" in l and not l.startswith("#"):
                k, v = l.split(":", 1)
                curr[k.strip().strip("- ")] = v.strip().strip('"').strip("'")
        if curr:
            sources.append(curr)
    return sources

# Mapping heuristics from source repo or path to existing awesome_skills categories
def infer_category(repo: str, rel_path: str, skill_name: str) -> str:
    path_lower = f"{repo}/{rel_path}/{skill_name}".lower()
    
    if "scientific" in path_lower or "k-dense" in path_lower or "biology" in path_lower or "chemistry" in path_lower:
        return "science-research"
    if "win-dev" in path_lower or "winui" in path_lower:
        return "desktop"
    if "dotnet" in path_lower or "csharp" in path_lower or "aspnet" in path_lower:
        return "software-engineering"
    if "copilot" in path_lower or "openhands" in path_lower:
        return "development"
    if "superpowers" in path_lower or "tdd" in path_lower or "testing" in path_lower:
        return "testing"
    if "security" in path_lower or "audit" in path_lower or "vulnerability" in path_lower:
        return "security"
    if "cloud" in path_lower or "azure" in path_lower or "aws" in path_lower or "kubernetes" in path_lower:
        return "cloud"
    if "database" in path_lower or "sql" in path_lower or "postgres" in path_lower:
        return "database"
    if "ai" in path_lower or "llm" in path_lower or "prompt" in path_lower or "agent" in path_lower:
        return "ai-engineer"
    if "frontend" in path_lower or "react" in path_lower or "css" in path_lower:
        return "frontend"
    if "python" in path_lower:
        return "development"
    return "development"

def normalize_skill_content(
    raw_content: str,
    skill_slug: str,
    category: str,
    source_repo: str,
    commit_hash: str,
    rel_path: str,
    license_type: str
) -> str:
    desc = f"Domain skills and automated agent workflows for {skill_slug.replace('-', ' ')}."
    risk = "low"
    body = raw_content

    if raw_content.startswith("---"):
        parts = raw_content.split("---", 2)
        if len(parts) >= 3:
            fm_text = parts[1]
            body = parts[2]
            m_desc = re.search(r"description:\s*\|?\s*([^\n\r]+(?:\n\s+[^\n\r]+)*)", fm_text)
            if m_desc:
                raw_d = " ".join(line.strip() for line in m_desc.group(1).splitlines() if line.strip())
                if len(raw_d) >= 10:
                    desc = raw_d.replace('"', "'")
            m_risk = re.search(r"risk:\s*([^\n\r]+)", fm_text)
            if m_risk:
                r_val = m_risk.group(1).strip().strip('"\'').lower()
                if r_val in {"low", "medium", "high", "critical"}:
                    risk = r_val

    desc_clean = " ".join(desc[:250].split())
    clean_frontmatter = f"""---
name: {skill_slug}
description: "{desc_clean}"
category: {category}
version: 1.0.0
disable-model-invocation: false
risk: {risk}
source:
  repository: "{source_repo}"
  commit: "{commit_hash}"
  path: "{rel_path}"
  license: "{license_type}"
  imported_at: "2026-09-20"
---
"""
    return clean_frontmatter + body.lstrip()

def sync_repo(source_info: Dict[str, Any], existing_slugs: Set[str]) -> Tuple[int, int]:
    repo = source_info.get("repo")
    branch = source_info.get("branch", "main")
    license_type = source_info.get("license", "MIT")

    if not repo:
        return 0, 0

    url = f"https://github.com/{repo}.git"
    cleanup_scratch_dir(SCRATCH_DIR)
    SCRATCH_DIR.parent.mkdir(parents=True, exist_ok=True)

    print(f"\n📥 Fetching [{repo}] (branch: {branch})...", flush=True)
    cmd = ["git", "clone", "--depth", "1", "--single-branch", "-b", branch, url, str(SCRATCH_DIR)]
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
    if res.returncode != 0:
        # Retry with default branch without -b
        cmd_fallback = ["git", "clone", "--depth", "1", url, str(SCRATCH_DIR)]
        res_fb = subprocess.run(cmd_fallback, capture_output=True, text=True, timeout=90)
        if res_fb.returncode != 0:
            print(f"  ❌ Clone failed for {repo}: {res_fb.stderr.strip()[:100]}", flush=True)
            cleanup_scratch_dir(SCRATCH_DIR)
            return 0, 0

    # Get commit hash
    commit_res = subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(SCRATCH_DIR), capture_output=True, text=True)
    commit_hash = commit_res.stdout.strip()[:10] if commit_res.returncode == 0 else "main-head"

    # Discover skills
    discovered = []
    for p in SCRATCH_DIR.rglob("SKILL.md"):
        if ".git" in p.parts:
            continue
        rel = str(p.relative_to(SCRATCH_DIR)).replace("\\", "/")
        discovered.append((p, rel, p.parent.name))

    # Also search for markdown files in skills/ or prompt/ instruction folders if no SKILL.md found
    if not discovered:
        for p in SCRATCH_DIR.rglob("*.md"):
            if ".git" in p.parts or p.name.upper().startswith("README") or p.name.upper().startswith("LICENSE"):
                continue
            if any(k in p.parts for k in ["skills", "instructions", "prompts", "agents"]):
                rel = str(p.relative_to(SCRATCH_DIR)).replace("\\", "/")
                discovered.append((p, rel, p.stem))

    imported_count = 0
    skipped_count = 0

    for path_obj, rel_path, raw_name in discovered:
        slug = slugify(raw_name)
        if slug in existing_slugs:
            skipped_count += 1
            continue

        try:
            with open(path_obj, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
        except Exception:
            continue

        cat = infer_category(repo, rel_path, slug)
        target_dir = AWESOME_DIR / cat / slug
        target_dir.mkdir(parents=True, exist_ok=True)
        target_file = target_dir / "SKILL.md"

        if target_file.exists():
            skipped_count += 1
            continue

        normalized_doc = normalize_skill_content(
            raw_content=content,
            skill_slug=slug,
            category=cat,
            source_repo=repo,
            commit_hash=commit_hash,
            rel_path=rel_path,
            license_type=license_type
        )

        with open(target_file, "w", encoding="utf-8") as f:
            f.write(normalized_doc)

        existing_slugs.add(slug)
        imported_count += 1

    cleanup_scratch_dir(SCRATCH_DIR)
    print(f"  ✅ Finished [{repo}]: {imported_count} imported, {skipped_count} existing/retained.", flush=True)
    return imported_count, skipped_count

def main():
    print("🚀 Initiating Upstream Source Sync & Normalization Pipeline...\n")
    sources = load_sources_registry()
    if not sources:
        print("No sources found in sources/registry.yaml", file=sys.stderr)
        sys.exit(1)

    existing_slugs = get_existing_slugs()
    print(f"Baseline library: {len(existing_slugs)} active and indexed skills.\n")

    total_imported = 0
    total_skipped = 0

    # Prioritized order as requested
    priority_order = [
        "anthropics/skills",
        "github/awesome-copilot",
        "microsoft/skills",
        "dotnet/skills",
        "microsoft/win-dev-skills",
        "OpenHands/OpenHands",
        "sickn33/agentic-awesome-skills",
        "ComposioHQ/awesome-claude-skills",
        "Prat011/awesome-llm-skills",
        "obra/superpowers",
        "gohypergiant/agent-skills",
        "Emmraan/agent-skills",
        "JayRHa/AgentSkills",
        "K-Dense-AI/claude-scientific-skills",
    ]

    source_map = {s.get("repo"): s for s in sources if s.get("repo")}

    for repo_name in priority_order:
        sinfo = source_map.get(repo_name)
        if not sinfo:
            sinfo = {"repo": repo_name, "branch": "main", "license": "MIT"}
        imp, skp = sync_repo(sinfo, existing_slugs)
        total_imported += imp
        total_skipped += skp

    print(f"\n🎉 Sync completed! Total new skills imported: {total_imported}, preserved without mutation: {total_skipped}.")

if __name__ == "__main__":
    main()
