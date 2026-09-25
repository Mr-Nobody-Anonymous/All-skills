"""Acceptance 7 and upstream update safety for scripts/sync_sources.py.

Uses throw-away local Git repositories as upstream sources (no network).
"""

from __future__ import annotations

import contextlib
import io
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest import mock

import yaml

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from scripts import sync_sources  # noqa: E402

GIT = shutil.which("git")

SKILL = """---
name: demo
description: Demonstration skill with supporting files.
version: 2.1.0
disable-model-invocation: true
allowed-tools:
- Read
---

# Demo

Run `scripts/run.py` and read `references/guide.md`.
"""


def git(cwd: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(cwd), *args], check=True, capture_output=True, text=True).stdout.strip()


def make_upstream(root: Path, name: str, skill_text: str = SKILL, license_text: str | None = None) -> Path:
    repo = root / name
    pkg = repo / "skills" / "demo"
    (pkg / "scripts").mkdir(parents=True)
    (pkg / "references").mkdir()
    (pkg / "SKILL.md").write_text(skill_text, encoding="utf-8")
    (pkg / "scripts" / "run.py").write_text("print('hello')\n", encoding="utf-8")
    (pkg / "references" / "guide.md").write_text("# Guide\n", encoding="utf-8")
    if license_text:
        (repo / "LICENSE").write_text(license_text, encoding="utf-8")
    git(root, "init", "-q", str(repo))
    git(repo, "-c", "user.email=t@example.com", "-c", "user.name=t", "add", "-A")
    git(repo, "-c", "user.email=t@example.com", "-c", "user.name=t", "commit", "-q", "-m", "init")
    return repo


def frontmatter(path: Path) -> dict:
    return yaml.safe_load(re.match(r"^---\n(.*?)\n---", path.read_text(encoding="utf-8"), re.S).group(1))


@unittest.skipIf(GIT is None, "git is required")
class TestImporter(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        workspace = self.root / "workspace"
        (workspace / "awesome_skills").mkdir(parents=True)
        self.patches = [
            mock.patch.object(sync_sources, "AWESOME_DIR", workspace / "awesome_skills"),
            mock.patch.object(sync_sources, "IMPORTS_LOCK", workspace / "sources" / "imports.lock.json"),
            mock.patch.object(sync_sources, "SCRATCH_DIR", workspace / "scratch" / "sync"),
            mock.patch.object(sync_sources, "BACKUP_DIR", workspace / "scratch" / "backups"),
            mock.patch.object(sync_sources, "REPO_ROOT", workspace),
        ]
        for p in self.patches:
            p.start()
        self.workspace = workspace

    def tearDown(self):
        for p in self.patches:
            p.stop()
        self._tmp.cleanup()

    def sync(self, repo: Path, update: bool = False, apply: bool = False, license: str | None = None) -> str:
        source = {"id": repo.name, "repo": str(repo), "skill_paths": ["skills"]}
        if license:
            source["license"] = license
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(sync_sources.run([source], update, apply), 0)
        return out.getvalue()

    def installed(self) -> list[Path]:
        return sorted(self.workspace.glob("awesome_skills/*/*/SKILL.md"))

    def test_full_package_and_upstream_metadata_are_preserved(self):
        """Acceptance 7: supporting files keep working and metadata is not rewritten."""
        upstream = make_upstream(self.root, "upstream")
        self.sync(upstream)
        [skill_md] = self.installed()
        pkg = skill_md.parent
        self.assertTrue((pkg / "scripts" / "run.py").is_file())
        self.assertTrue((pkg / "references" / "guide.md").is_file())
        for ref in re.findall(r"`([\w/.-]+\.(?:py|md))`", skill_md.read_text(encoding="utf-8")):
            self.assertTrue((pkg / ref).is_file(), f"reference {ref} is broken")

        meta = frontmatter(skill_md)
        self.assertEqual(meta["version"], "2.1.0")
        self.assertIs(meta["disable-model-invocation"], True)
        self.assertEqual(meta["allowed-tools"], ["Read"])
        src = meta["source"]
        self.assertEqual(src["commit"], git(upstream, "rev-parse", "HEAD"))
        self.assertEqual(len(src["commit"]), 40)
        self.assertEqual(src["license"], "NOASSERTION")
        imported = datetime.fromisoformat(src["imported_at"].replace("Z", "+00:00"))
        self.assertLess((datetime.now(timezone.utc) - imported).total_seconds(), 600)
        self.assertEqual(len(src["content_sha256"]), 64)
        lock = json.loads(sync_sources.IMPORTS_LOCK.read_text(encoding="utf-8"))
        self.assertEqual(list(lock["imports"].values())[0]["commit"], src["commit"])

    def test_license_is_detected_or_declared_never_assumed(self):
        mit = make_upstream(self.root, "mit-repo", license_text="MIT License\n\nPermission is hereby granted, free of charge, ...")
        self.sync(mit)
        self.assertEqual(frontmatter(self.installed()[0])["source"]["license"], "MIT")

    def test_updates_are_reviewed_backed_up_and_reversible(self):
        upstream = make_upstream(self.root, "upstream")
        self.sync(upstream)
        [skill_md] = self.installed()
        original = skill_md.read_text(encoding="utf-8")

        (upstream / "skills" / "demo" / "SKILL.md").write_text(SKILL.replace("# Demo", "# Demo v2"), encoding="utf-8")
        (upstream / "skills" / "demo" / "scripts" / "new.py").write_text("x = 1\n", encoding="utf-8")
        git(upstream, "-c", "user.email=t@example.com", "-c", "user.name=t", "commit", "-qam", "v2")
        git(upstream, "-c", "user.email=t@example.com", "-c", "user.name=t", "add", "-A")
        git(upstream, "-c", "user.email=t@example.com", "-c", "user.name=t", "commit", "-qm", "add script")

        plain = self.sync(upstream)
        self.assertIn("1 with updates to review", plain)
        self.assertEqual(skill_md.read_text(encoding="utf-8"), original, "plain sync must not overwrite")

        review = self.sync(upstream, update=True)
        self.assertIn("+ scripts/new.py", review)
        self.assertIn("+# Demo v2", review)
        self.assertEqual(skill_md.read_text(encoding="utf-8"), original, "--update alone must not write")

        applied = self.sync(upstream, update=True, apply=True)
        self.assertIn("# Demo v2", skill_md.read_text(encoding="utf-8"))
        self.assertTrue((skill_md.parent / "scripts" / "new.py").is_file())
        backup_id = re.search(r"--rollback (\S+)\)", applied).group(1)

        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(sync_sources.rollback(backup_id), 0)
        self.assertEqual(skill_md.read_text(encoding="utf-8"), original)
        self.assertFalse((skill_md.parent / "scripts" / "new.py").exists())

    def test_same_named_skills_from_different_sources_are_not_conflated(self):
        self.sync(make_upstream(self.root, "first"))
        self.sync(make_upstream(self.root, "second"))
        names = sorted(p.parent.name for p in self.installed())
        self.assertEqual(names, ["demo", "demo--second"])
        repos = {frontmatter(p)["source"]["repository"] for p in self.installed()}
        self.assertEqual(len(repos), 2)
        again = self.sync(make_upstream(self.root, "third"))
        self.assertIn("1 imported", again)
        self.assertEqual(len(self.installed()), 3)


if __name__ == "__main__":
    unittest.main()
