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

from scripts import import_priority_repos, import_vetted_skills, sync_sources  # noqa: E402

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
    return subprocess.run(["git", "-C", str(cwd), *args], check=True, capture_output=True, text=True, encoding="utf-8", errors="replace").stdout.strip()


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
        # Git marks object files read-only; don't fail teardown on Windows.
        self._tmp = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
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

    def test_repository_license_and_notice_travel_with_the_package(self):
        upstream = make_upstream(self.root, "noticed",
                                 license_text="MIT License\n\nPermission is hereby granted, free of charge, ...\n")
        (upstream / "NOTICE").write_text("Demo project NOTICE\n", encoding="utf-8")
        git(upstream, "-c", "user.email=t@example.com", "-c", "user.name=t", "add", "-A")
        git(upstream, "-c", "user.email=t@example.com", "-c", "user.name=t", "commit", "-q", "-m", "notice")
        self.sync(upstream)

        skill_md = self.installed()[0]
        self.assertIn("MIT License", (skill_md.parent / "LICENSE").read_text(encoding="utf-8"),
                      "a repository-level licence must be redistributed with the package")
        self.assertEqual((skill_md.parent / "NOTICE").read_text(encoding="utf-8"), "Demo project NOTICE\n")
        src = frontmatter(skill_md)["source"]
        self.assertEqual((src["license"], src["license_source"]), ("MIT", "repository LICENSE file"))
        self.assertEqual(src["license_files"], ["LICENSE", "NOTICE"])

        self.assertIn("1 unchanged, 0 with updates", self.sync(upstream, update=True),
                      "copied notices must not look like an upstream change")

        (upstream / "LICENSE").write_text("Apache License, Version 2.0, January 2004\n", encoding="utf-8")
        git(upstream, "-c", "user.email=t@example.com", "-c", "user.name=t", "commit", "-q", "-am", "relicense")
        review = self.sync(upstream, update=True)
        self.assertIn("1 with updates to review", review, "an upstream licence change is an update to review")
        self.assertIn("~ LICENSE", review)

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


def tree_digest(root: Path) -> dict:
    """Relative path -> bytes for every file under ``root`` (used to prove it is untouched)."""
    return {str(f.relative_to(root)): f.read_bytes() for f in sorted(root.rglob("*")) if f.is_file()}


@unittest.skipIf(GIT is None, "git is required")
class TestPriorityImporter(unittest.TestCase):
    """scripts/import_priority_repos.py must use the lossless pipeline and never delete shipped code.

    Regression: it used to rewrite SKILL.md files (dropping metadata, resetting
    versions), stamp a fixed date/licence, and finish with
    ``shutil.rmtree(REPO_ROOT / "scratch_priority_import")`` — a shipped package.
    """

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.root = Path(self._tmp.name)
        workspace = self.root / "workspace"
        (workspace / "awesome_skills").mkdir(parents=True)
        # import_priority_repos loads ``sync_sources`` via sys.path, which can be a
        # different module object from ``scripts.sync_sources``: patch every copy,
        # otherwise the import would run against the real checkout.
        modules = {id(m): m for m in (sync_sources, import_priority_repos.sync_sources)}.values()
        self.patches = [
            mock.patch.object(module, name, value)
            for module in modules
            for name, value in (
                ("AWESOME_DIR", workspace / "awesome_skills"),
                ("IMPORTS_LOCK", workspace / "sources" / "imports.lock.json"),
                ("SCRATCH_DIR", workspace / "scratch" / "sync"),
                ("BACKUP_DIR", workspace / "scratch" / "backups"),
                ("REPO_ROOT", workspace),
            )
        ]
        for patcher in self.patches:
            patcher.start()
        self.workspace = workspace

    def tearDown(self):
        for patcher in self.patches:
            patcher.stop()
        self._tmp.cleanup()

    def test_priority_import_is_lossless_categorised_and_leaves_shipped_code_alone(self):
        self.assertEqual(import_priority_repos.sync_sources.AWESOME_DIR, self.workspace / "awesome_skills",
                         "refusing to run: the importer is not isolated from the real checkout")
        package = _ROOT / "scratch_priority_import"
        before = tree_digest(package)
        self.assertTrue(before, "fixture sanity: scratch_priority_import must exist in the checkout")

        upstream = make_upstream(self.root, "priority-upstream")
        entry = {"repo": str(upstream), "default_cat": "robotics", "domain": "Test", "license": ""}
        with mock.patch.object(import_priority_repos, "PRIORITY_REPOS", [entry]):
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = import_priority_repos.main(["--repo", str(upstream)])
        self.assertEqual(code, 0, out.getvalue())

        installed = sorted(self.workspace.glob("awesome_skills/*/*/SKILL.md"))
        self.assertEqual([p.parent.relative_to(self.workspace / "awesome_skills").as_posix() for p in installed],
                         ["robotics/demo"], "new skills go to the configured category")
        pkg = installed[0].parent
        self.assertTrue((pkg / "scripts" / "run.py").is_file(), "complete package, not just SKILL.md")
        self.assertTrue((pkg / "references" / "guide.md").is_file())
        meta = frontmatter(installed[0])
        self.assertEqual(meta["version"], "2.1.0", "upstream version must not be reset")
        self.assertIs(meta["disable-model-invocation"], True, "upstream invocation policy must be kept")
        self.assertEqual(meta["source"]["license"], "NOASSERTION", "no LICENSE file and no declaration")
        self.assertRegex(meta["source"]["commit"], r"^[0-9a-f]{40}$")
        self.assertNotEqual(str(meta["source"]["imported_at"])[:10], "2026-09-20", "no hard-coded import date")

        self.assertEqual(tree_digest(package), before, "the shipped scratch_priority_import package was modified")
        self.assertFalse((_ROOT / "awesome_skills" / "robotics" / "demo").exists(), "import leaked into the checkout")

    def test_unknown_repository_and_apply_without_update_are_refused(self):
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            self.assertEqual(import_priority_repos.main(["--repo", "nobody/nothing"]), 1)
            self.assertEqual(import_priority_repos.main(["--apply"]), 2)
        self.assertIn("Unknown priority repositories", err.getvalue())

    def test_module_no_longer_owns_a_scratch_directory(self):
        source = (_ROOT / "scripts" / "import_priority_repos.py").read_text(encoding="utf-8")
        self.assertNotIn("rmtree", source)
        self.assertFalse(hasattr(import_priority_repos, "SCRATCH_DIR"))


@unittest.skipIf(GIT is None, "git is required")
class TestVettedImporter(unittest.TestCase):
    """scripts/import_vetted_skills.py records provenance only when it is true.

    Regression: it stamped ``imported_at: 2026-09-01`` on every run, recorded the
    pinned commit without checking the checkout, never compared the LICENSE with
    the declared licence, and overwrote wrappers curated after import.
    """

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.root = Path(self._tmp.name)
        self.audit = self.root / "audit"
        self.audit.mkdir()
        checkout = self.audit / "superpowers"
        (checkout / "skills" / "brainstorming").mkdir(parents=True)
        (checkout / "skills" / "brainstorming" / "SKILL.md").write_text(
            "---\nname: brainstorming\ndescription: upstream\n---\n\n# Upstream\n", encoding="utf-8")
        (checkout / "LICENSE").write_text("MIT License\n\nPermission is hereby granted, free of charge, ...\n",
                                          encoding="utf-8")
        git(self.audit, "init", "-q", str(checkout))
        git(checkout, "-c", "user.email=t@example.com", "-c", "user.name=t", "add", "-A")
        git(checkout, "-c", "user.email=t@example.com", "-c", "user.name=t", "commit", "-q", "-m", "init")
        self.commit = git(checkout, "rev-parse", "HEAD")
        self.repo_root = self.root / "repo"
        self.skill_md = self.repo_root / "skills" / "development" / "brainstorming" / "SKILL.md"
        self._root_patch = mock.patch.object(import_vetted_skills, "ROOT", self.repo_root)
        self._root_patch.start()

    def tearDown(self):
        self._root_patch.stop()
        self._tmp.cleanup()

    def spec(self, commit: str | None = None, license_: str = "MIT") -> tuple:
        return ("development", "brainstorming", "obra/superpowers", "brainstorming", commit or self.commit,
                license_, "Jesse Vincent", "Clarify intent before implementation.", ["design-first"],
                ["brainstorm this", "design this"], ["design"], [])

    def run_import(self, spec: tuple, *extra: str) -> int:
        with mock.patch.object(import_vetted_skills, "SPECS", [spec]), \
                contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return import_vetted_skills.main(["--audit-dir", str(self.audit), *extra])

    def test_checkout_not_at_the_pinned_commit_is_refused(self):
        self.assertEqual(self.run_import(self.spec(commit="0" * 40)), 1)
        self.assertFalse(self.repo_root.exists(), "nothing may be written when provenance is wrong")

    def test_license_mismatch_is_refused(self):
        self.assertEqual(self.run_import(self.spec(license_="Apache-2.0")), 1)
        self.assertFalse(self.repo_root.exists())

    def test_verified_import_is_stamped_with_the_real_date_and_curation_is_preserved(self):
        self.assertEqual(self.run_import(self.spec()), 0)
        today = datetime.now(timezone.utc).date().isoformat()
        text = self.skill_md.read_text(encoding="utf-8")
        self.assertIn(f"imported_at: {today}\n", text)
        self.assertIn(f"source_commit: {self.commit}\n", text)
        self.assertTrue((self.skill_md.parent / "references" / "upstream-SKILL.md").is_file())
        self.assertIn("MIT License", (self.skill_md.parent / "LICENSE").read_text(encoding="utf-8"))

        curated = text.replace(f"imported_at: {today}", "imported_at: 2020-01-02") + "\n<!-- curated -->\n"
        self.skill_md.write_text(curated, encoding="utf-8")
        self.assertEqual(self.run_import(self.spec()), 0)
        self.assertEqual(self.skill_md.read_text(encoding="utf-8"), curated, "curated wrapper was overwritten")

        self.assertEqual(self.run_import(self.spec(), "--force"), 0)
        regenerated = self.skill_md.read_text(encoding="utf-8")
        self.assertNotIn("<!-- curated -->", regenerated)
        self.assertIn("imported_at: 2020-01-02\n", regenerated, "--force must keep the first import date")


if __name__ == "__main__":
    unittest.main()
