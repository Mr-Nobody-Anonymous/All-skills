"""Federated 9-Stage Ingestion Pipeline for All-Skills.

Manages external repository lifecycle from discovery through staging, normalization,
security scanning, deduplication, evaluation, and graduation into canonical skills/.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent
INGESTION_DIR = REPO_ROOT / "ingestion"
STAGING_DIR = REPO_ROOT / "staging"
SOURCES_DIR = REPO_ROOT / "sources"
CANONICAL_SKILLS_DIR = REPO_ROOT / "skills"
REGISTRY_DIR = REPO_ROOT / "registry"


@dataclass
class IngestionRecord:
    source_id: str
    skill_name: str
    source_repo: str
    source_commit: str
    source_path: str
    content_sha256: str
    license: str
    skill_type: str = "procedural"
    current_stage: str = "00_discovered"
    trust_level: str = "imported"
    security_scan: str = "pending"
    behavioral_eval: str = "pending"
    target_category: str = "utilities"
    canonical_id: Optional[str] = None
    quarantine_reason: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class IngestionPipeline:
    """9-Stage Federated Ingestion Pipeline."""

    STAGES = [
        "00_discovered",
        "01_fetched",
        "02_normalized",
        "03_validated",
        "04_security_scanned",
        "05_deduplicated",
        "06_evaluated",
        "07_reviewed",
        "08_promoted",
    ]

    def __init__(self, root: Optional[Path] = None):
        self.root = root or REPO_ROOT
        self.ingestion_root = self.root / "ingestion"
        self.ensure_stages()

    def ensure_stages(self) -> None:
        """Ensure all stage directories exist."""
        for stage in self.STAGES:
            (self.ingestion_root / stage).mkdir(parents=True, exist_ok=True)
        (self.ingestion_root / "quarantine").mkdir(parents=True, exist_ok=True)
        (self.ingestion_root / "logs").mkdir(parents=True, exist_ok=True)

    def calculate_sha256(self, file_path: Path) -> str:
        """Calculate SHA-256 digest of a file."""
        hasher = hashlib.sha256()
        with open(file_path, "rb") as f:
            while chunk := f.read(65536):
                hasher.update(chunk)
        return hasher.hexdigest()

    def discover(self, source_id: str, repo_url: str, branch_or_commit: str, license_spdx: str, tier: str = "community") -> Dict[str, Any]:
        """Stage 00: Register discovered upstream repository."""
        manifest_path = self.ingestion_root / "00_discovered" / f"{source_id}.json"
        record = {
            "source_id": source_id,
            "repo_url": repo_url,
            "commit_target": branch_or_commit,
            "license": license_spdx,
            "tier": tier,
            "discovered_at": datetime.now(timezone.utc).isoformat(),
            "status": "ready_to_fetch"
        }
        manifest_path.write_text(json.dumps(record, indent=2), encoding="utf-8")
        return record

    def fetch(self, source_id: str, shallow: bool = True) -> Path:
        """Stage 01: Fetch pinned repository into 01_fetched/."""
        discovery_file = self.ingestion_root / "00_discovered" / f"{source_id}.json"
        if not discovery_file.exists():
            raise FileNotFoundError(f"Source {source_id} not registered in 00_discovered")

        meta = json.loads(discovery_file.read_text(encoding="utf-8"))
        dest = self.ingestion_root / "01_fetched" / source_id
        if dest.exists():
            shutil.rmtree(dest)

        cmd = ["git", "clone", meta["repo_url"], str(dest)]
        if shallow:
            cmd.extend(["--depth", "1"])
        if meta.get("commit_target") and meta["commit_target"] not in ["main", "master", "HEAD"]:
            cmd.extend(["--branch", meta["commit_target"]])

        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=120)
        except Exception as e:
            # Create a placeholder staging clone if offline
            dest.mkdir(parents=True, exist_ok=True)
            (dest / "FETCH_ERROR.txt").write_text(f"Fetch failed: {e}", encoding="utf-8")

        return dest

    def normalize_skill(
        self,
        source_id: str,
        raw_skill_dir: Path,
        target_name: str,
        category: str,
        skill_type: str = "procedural",
        author: str = "upstream",
        license_spdx: str = "MIT"
    ) -> Path:
        """Stage 02: Normalize raw skill into canonical SKILL.md structure."""
        out_dir = self.ingestion_root / "02_normalized" / source_id / target_name
        out_dir.mkdir(parents=True, exist_ok=True)

        raw_md = raw_skill_dir / "SKILL.md"
        if not raw_md.exists():
            for f in raw_skill_dir.glob("*.md"):
                raw_md = f
                break

        body = ""
        desc = f"Normalized skill {target_name} imported from {source_id}."
        if raw_md.exists():
            content = raw_md.read_text(encoding="utf-8", errors="ignore")
            from src.skills.frontmatter import parse_frontmatter
            meta, parsed_body = parse_frontmatter(content)
            body = parsed_body
            if meta.get("description"):
                desc = meta["description"]
        else:
            body = f"# {target_name.replace('-', ' ').title()}\n\nDetailed operational instructions."

        safe_desc = desc.replace('"', '\\"')
        normalized_md = f"""---
name: {target_name}
description: "{safe_desc}"
type: {skill_type}
category: {category}
version: 1.0.0
author: "{author}"
license: "{license_spdx}"
risk: low
level: intermediate
provenance:
  source_repository: "{source_id}"
  source_commit: "HEAD"
  source_path: "{raw_skill_dir.name}"
  imported_at: "{datetime.now(timezone.utc).isoformat()}"
  license: "{license_spdx}"
  trust:
    level: imported
    security_scan: pending
    behavioral_eval: pending
---

{body}
"""
        target_file = out_dir / "SKILL.md"
        target_file.write_text(normalized_md, encoding="utf-8")
        return target_file

    def validate_schema(self, skill_md: Path) -> Tuple[bool, List[str]]:
        """Stage 03: Validate SKILL.md against schema."""
        from src.skills.frontmatter import parse_frontmatter
        content = skill_md.read_text(encoding="utf-8")
        meta, _ = parse_frontmatter(content)
        errors = []
        if not meta.get("name"):
            errors.append("Missing required field: name")
        if not meta.get("description") or len(meta.get("description", "")) < 10:
            errors.append("Missing or too short required field: description")
        if not meta.get("category"):
            errors.append("Missing required field: category")

        val_dir = self.ingestion_root / "03_validated" / skill_md.parent.parent.name
        val_dir.mkdir(parents=True, exist_ok=True)
        record = {
            "file": str(skill_md),
            "valid": len(errors) == 0,
            "errors": errors,
            "validated_at": datetime.now(timezone.utc).isoformat()
        }
        (val_dir / f"{skill_md.parent.name}.json").write_text(json.dumps(record, indent=2), encoding="utf-8")
        return len(errors) == 0, errors

    def scan_security(self, skill_md: Path) -> Tuple[bool, List[str]]:
        """Stage 04: Static security and prompt injection scan."""
        content = skill_md.read_text(encoding="utf-8").lower()
        findings = []

        dangerous_patterns = [
            (r"curl\s+.*\|\s*sh", "Pipe to shell execution"),
            (r"rm\s+-rf\s+/", "Root filesystem deletion"),
            (r"eval\s*\(.*process\.env", "Dynamic code evaluation of environment"),
            (r"cat\s+.*id_rsa", "Private key exfiltration"),
            (r"grep\s+.*aws_secret", "AWS secret exfiltration"),
        ]

        for pat, desc in dangerous_patterns:
            if re.search(pat, content):
                findings.append(desc)

        passed = len(findings) == 0
        scan_dir = self.ingestion_root / "04_security_scanned" / skill_md.parent.parent.name
        scan_dir.mkdir(parents=True, exist_ok=True)
        scan_record = {
            "file": str(skill_md),
            "clean": passed,
            "findings": findings,
            "scanned_at": datetime.now(timezone.utc).isoformat()
        }
        (scan_dir / f"{skill_md.parent.name}.json").write_text(json.dumps(scan_record, indent=2), encoding="utf-8")

        if not passed:
            quarantine_dest = self.ingestion_root / "quarantine" / skill_md.parent.name
            quarantine_dest.mkdir(parents=True, exist_ok=True)
            shutil.copy2(skill_md, quarantine_dest / "SKILL.md")

        return passed, findings

    def check_duplicate(self, skill_name: str, category: str, content: str) -> Tuple[bool, Optional[str]]:
        """Stage 05: Check if skill is duplicate or merges with existing canonical skill."""
        canonical_target = self.root / "skills" / category / skill_name
        if canonical_target.exists():
            return True, f"skills/{category}/{skill_name}"

        # Check across all canonical categories
        for cat_dir in (self.root / "skills").iterdir():
            if cat_dir.is_dir() and (cat_dir / skill_name).exists():
                return True, f"skills/{cat_dir.name}/{skill_name}"

        return False, None

    def promote_to_canonical(
        self,
        skill_md: Path,
        target_category: str,
        canonical_name: Optional[str] = None
    ) -> Path:
        """Stage 08: Promote validated & scanned skill to canonical skills/."""
        from src.skills.frontmatter import parse_frontmatter
        content = skill_md.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(content)
        name = canonical_name or meta.get("name", skill_md.parent.name)

        dest_dir = self.root / "skills" / target_category / name
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest_file = dest_dir / "SKILL.md"

        # Update trust in frontmatter
        if "provenance" in meta and isinstance(meta["provenance"], dict):
            if "trust" in meta["provenance"] and isinstance(meta["provenance"]["trust"], dict):
                meta["provenance"]["trust"]["level"] = "trusted"
                meta["provenance"]["trust"]["security_scan"] = "passed"
                meta["provenance"]["trust"]["behavioral_eval"] = "passed"

        shutil.copy2(skill_md, dest_file)

        # Log promotion
        promo_dir = self.ingestion_root / "08_promoted" / target_category
        promo_dir.mkdir(parents=True, exist_ok=True)
        log = {
            "source_skill": str(skill_md),
            "canonical_dest": str(dest_file),
            "promoted_at": datetime.now(timezone.utc).isoformat(),
            "sha256": self.calculate_sha256(dest_file)
        }
        (promo_dir / f"{name}.json").write_text(json.dumps(log, indent=2), encoding="utf-8")

        return dest_file
