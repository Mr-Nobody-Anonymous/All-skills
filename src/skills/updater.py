"""Non-destructive checks for changes in imported upstream repositories."""
from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass(frozen=True)
class UpdateStatus:
    repository: str
    pinned_commit: str
    upstream_commit: str | None
    changed: bool
    error: str | None = None


def check_updates(workspace_root: Path, timeout: int = 20) -> List[UpdateStatus]:
    manifest = json.loads((workspace_root / "skills" / "SOURCES.json").read_text(encoding="utf-8"))
    repositories = {}
    for source in manifest.get("skills", []):
        repo, commit = source.get("repository"), source.get("commit")
        if repo and commit:
            repositories.setdefault(repo, commit)
    results: List[UpdateStatus] = []
    for repo, pinned in sorted(repositories.items()):
        url = repo if repo.startswith("http") else f"https://github.com/{repo}.git"
        try:
            proc = subprocess.run(
                ["git", "ls-remote", url, "HEAD"], capture_output=True,
                text=True, timeout=timeout, check=False,
            )
            if proc.returncode != 0 or not proc.stdout.strip():
                raise RuntimeError(proc.stderr.strip() or "no HEAD returned")
            upstream = proc.stdout.split()[0]
            results.append(UpdateStatus(repo, pinned, upstream, upstream != pinned))
        except Exception as exc:
            results.append(UpdateStatus(repo, pinned, None, False, str(exc)))
    return results
