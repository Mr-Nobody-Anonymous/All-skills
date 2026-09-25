"""CLI commands must do what they say and exit non-zero when they fail."""

from __future__ import annotations

import contextlib
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from scripts import allskills, manage_awesome_skills  # noqa: E402


def run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, *args], cwd=_ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=300)


class TestProfileInstall(unittest.TestCase):
    """Acceptance 6: installing a profile makes its skills actually appear."""

    def test_install_copies_every_profile_skill_and_records_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "skills"
            proc = run("scripts/allskills.py", "profile", "install", "software-engineer", "--dest", str(dest))
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            expected = allskills.load_profiles()["software-engineer"]["skills"]
            self.assertGreater(len(expected), 3)
            for skill_id in expected:
                self.assertTrue((dest / skill_id / "SKILL.md").is_file(), f"{skill_id} not installed")
            state = json.loads((dest / ".all-skills-profile.json").read_text(encoding="utf-8"))
            self.assertEqual(state["profile"], "software-engineer")
            self.assertEqual(state["skills"], expected)

    def test_missing_skill_fails_before_copying_anything(self):
        real_resolve = allskills.resolve_skill

        def resolve(skill_id):
            return (None, "missing") if skill_id == "tdd" else real_resolve(skill_id)

        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(allskills, "resolve_skill", resolve), \
                contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            dest = Path(tmp) / "skills"
            self.assertEqual(allskills.cmd_profile("install", "software-engineer", dest=str(dest)), 1)
            self.assertFalse(dest.exists(), "nothing may be copied when a skill is missing")

    def test_unknown_profile_and_bad_subcommand_fail(self):
        self.assertEqual(run("scripts/allskills.py", "profile", "install", "no-such-profile").returncode, 1)
        self.assertNotEqual(run("scripts/allskills.py", "frobnicate").returncode, 0)

    def test_list_and_show_report_real_contents(self):
        listing = run("scripts/allskills.py", "profile", "list")
        self.assertEqual(listing.returncode, 0)
        self.assertIn("software-engineer", listing.stdout)
        show = run("scripts/allskills.py", "profile", "show", "universal")
        self.assertEqual(show.returncode, 0)
        self.assertIn("ai-writing-assistant", show.stdout)
        self.assertIn("Planned but not in the library: note-taking, calculator", show.stdout)


class TestVerificationExitCodes(unittest.TestCase):
    """verify / lock / doctor return meaningful exit codes."""

    def test_verify_and_lock_pass_on_a_consistent_checkout(self):
        for args in (("verify",), ("lock", "--verify")):
            proc = run("scripts/allskills.py", *args)
            self.assertEqual(proc.returncode, 0, f"allskills {' '.join(args)} failed:\n{proc.stdout[-3000:]}\n{proc.stderr[-3000:]}")

    def test_harness_verification_fails_when_required_targets_are_missing(self):
        proc = run("scripts/setup_tools.py", "--verify", "--strict")
        if "not linked" in run("scripts/setup_tools.py", "--verify").stdout:
            self.assertEqual(proc.returncode, 1, "missing required harness targets must fail")

    def test_verify_fails_when_a_check_fails(self):
        failing = subprocess.CompletedProcess(args=[], returncode=1, stdout="boom\n", stderr="")
        with mock.patch.object(allskills.subprocess, "run", return_value=failing), \
                contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(allskills.cmd_verify(), 1)


class TestSearch(unittest.TestCase):
    """Search is ranked, paginated, filterable and machine-readable."""

    def test_json_output_is_ranked_and_paginated(self):
        proc = run("scripts/allskills.py", "search", "terraform", "--json", "--limit", "3")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        data = json.loads(proc.stdout)
        self.assertGreater(data["total"], 3)
        self.assertEqual(len(data["results"]), 3)
        catalog = [r["score"] for r in data["results"] if r["source"] == "catalog"]
        self.assertEqual(catalog, sorted(catalog, reverse=True))
        page2 = json.loads(run("scripts/allskills.py", "search", "terraform", "--json",
                               "--limit", "3", "--offset", "3").stdout)
        self.assertNotEqual(page2["results"][0]["id"], data["results"][0]["id"])

    def test_category_filter_and_no_match(self):
        data = json.loads(run("scripts/allskills.py", "search", "terraform", "--json",
                              "--category", "devops").stdout)
        self.assertTrue(data["results"])
        self.assertTrue(all(r["category"] == "devops" for r in data["results"]))
        self.assertEqual(run("scripts/allskills.py", "search", "zzqqxx-nothing").returncode, 1)


class TestCatalogInstallIsNonDestructive(unittest.TestCase):
    """manage_awesome_skills install / install-bundle never silently destroy an existing install.

    Regression: both commands used to ``shutil.rmtree`` any existing destination
    (by default the curated, lock-pinned ``.agents/skills``), exit 0 when bundle
    skills were missing, and crash on ``--path`` outside the repository.
    """

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.dest = self.tmp / "skills"
        self._patch = mock.patch.object(manage_awesome_skills, "INSTALL_BACKUP_DIR", self.tmp / "backups")
        self._patch.start()
        index = json.loads((_ROOT / "awesome_skills" / "skills_index.json").read_text(encoding="utf-8"))
        self.skill_id = next(item["id"] for item in index if manage_awesome_skills.find_skill_on_disk(item["id"])[0])

    def tearDown(self):
        self._patch.stop()
        self._tmp.cleanup()

    def cli(self, *argv: str) -> int:
        with mock.patch.object(sys, "argv", ["manage_awesome_skills.py", *argv]), \
                contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            try:
                manage_awesome_skills.main()
            except SystemExit as exc:
                return int(exc.code or 0)
        return 0

    def test_reinstall_keeps_local_changes_unless_forced_and_backs_them_up(self):
        skill_md = self.dest / self.skill_id / "SKILL.md"
        self.assertEqual(self.cli("install", self.skill_id, "--path", str(self.dest)), 0)
        self.assertTrue(skill_md.is_file())
        edited = skill_md.read_text(encoding="utf-8") + "\nLOCAL EDIT\n"
        skill_md.write_text(edited, encoding="utf-8")

        self.assertEqual(self.cli("install", self.skill_id, "--path", str(self.dest)), 0)
        self.assertEqual(skill_md.read_text(encoding="utf-8"), edited, "an existing install was overwritten")

        self.assertEqual(self.cli("install", self.skill_id, "--path", str(self.dest), "--force"), 0)
        self.assertNotIn("LOCAL EDIT", skill_md.read_text(encoding="utf-8"))
        backups = list((self.tmp / "backups").glob(f"*/*/{self.skill_id}/SKILL.md"))
        self.assertEqual(len(backups), 1, "--force must back up the copy it replaces")
        self.assertEqual(backups[0].read_text(encoding="utf-8"), edited)

    def test_invalid_or_unknown_targets_fail(self):
        self.assertEqual(self.cli("install", "../..", "--path", str(self.dest)), 1)
        self.assertEqual(self.cli("install", "no-such-skill-xyz", "--path", str(self.dest)), 1)
        self.assertEqual(self.cli("info", "no-such-skill-xyz"), 1)
        self.assertFalse(self.dest.exists(), "nothing may be written for an invalid target")

    def test_bundle_with_missing_skill_fails_after_installing_the_rest(self):
        bundles = {"test-bundle": [self.skill_id, "no-such-skill-xyz"]}
        with mock.patch.object(manage_awesome_skills, "BUNDLES", bundles):
            self.assertEqual(self.cli("install-bundle", "test-bundle", "--path", str(self.dest)), 1)
        self.assertTrue((self.dest / self.skill_id / "SKILL.md").is_file())

    def test_destinations_resolving_to_the_same_directory_are_installed_once(self):
        self.dest.mkdir()
        self.assertEqual(manage_awesome_skills._unique_dirs([self.dest, self.dest / ".", self.tmp / "other"]),
                         [self.dest, self.tmp / "other"])


if __name__ == "__main__":
    unittest.main()
