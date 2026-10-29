"""Portability guards.

These tests exist because of a real CI failure: a harness link at
``.github/skills`` was committed as a symlink whose target was an absolute
machine-local path (``/home/user/All-skills/.agents/skills``). Git stores a
symlink as a blob containing its target, so the link resolved for exactly one
person and broke ``allskills verify`` on every runner — Ubuntu, macOS and
Windows alike.

The rules encoded here:

* no tracked symlink may carry an absolute target, and
* no tracked symlink may point outside the repository, and
* the documented test count must not depend on which optional packages happen
  to be installed on the machine that measured it.
"""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import compute_stats  # noqa: E402


def tracked_symlinks() -> list[tuple[str, str]]:
    """(path, target) for every symlink git tracks, or [] when git is absent."""
    listed = subprocess.run(
        ["git", "ls-files", "-s"], cwd=ROOT, capture_output=True, text=True, check=False
    )
    if listed.returncode != 0:
        return []
    links = []
    for line in listed.stdout.splitlines():
        meta, _, path = line.partition("\t")
        if meta.split()[0] != "120000":  # git mode for a symlink
            continue
        shown = subprocess.run(
            ["git", "show", f":{path}"], cwd=ROOT, capture_output=True, text=True, check=False
        )
        if shown.returncode == 0:
            links.append((path, shown.stdout.strip()))
    return links


class TestNoMachineLocalSymlinks(unittest.TestCase):
    def test_tracked_symlinks_have_relative_targets(self) -> None:
        if not (ROOT / ".git").exists():
            self.skipTest("not a git checkout")
        offenders = [f"{path} -> {target}" for path, target in tracked_symlinks()
                     if Path(target).is_absolute()]
        self.assertEqual(
            offenders, [],
            "absolute symlink targets resolve only on the machine that created them:\n  "
            + "\n  ".join(offenders),
        )

    def test_tracked_symlinks_stay_inside_the_repository(self) -> None:
        if not (ROOT / ".git").exists():
            self.skipTest("not a git checkout")
        offenders = []
        for path, target in tracked_symlinks():
            resolved = (ROOT / path).parent / target
            try:
                resolved.resolve().relative_to(ROOT.resolve())
            except ValueError:
                offenders.append(f"{path} -> {target}")
        self.assertEqual(offenders, [], f"symlinks escape the repository: {offenders}")

    def test_generated_harness_links_are_not_committed(self) -> None:
        """.github/skills is produced by scripts/setup_tools.py per machine."""
        tracked = {path for path, _ in tracked_symlinks()}
        self.assertNotIn(
            ".github/skills", tracked,
            "harness links are machine-local output; keep them gitignored",
        )


class TestTestCountIsEnvironmentIndependent(unittest.TestCase):
    """The number in stats.json must be the same on any machine."""

    def test_stats_test_count_matches_the_source(self) -> None:
        stats = json.loads((ROOT / "stats.json").read_text(encoding="utf-8"))
        self.assertEqual(stats["tests"], compute_stats.count_test_cases(ROOT))

    def test_count_does_not_import_the_test_modules(self) -> None:
        """Counting must not execute test code (no imports, no side effects)."""
        source = (ROOT / "scripts" / "compute_stats.py").read_text(encoding="utf-8")
        body = source[source.index("def count_test_cases("):source.index("def compute_platform_stats(")]
        self.assertNotIn("import_module", body)
        self.assertNotIn("TestLoader", body)
        self.assertIn("ast.parse", body)

    def test_excluded_ecc_suite_is_documented(self) -> None:
        """tests/ecc needs the optional `llm` package and never runs in CI."""
        body = (ROOT / "scripts" / "compute_stats.py").read_text(encoding="utf-8")
        block = body[body.index("def count_test_cases("):body.index("def compute_platform_stats(")]
        self.assertIn("ecc", block)
        self.assertIn("scratch_priority_import", block)


class TestCIJobsInstallWhatTheyRun(unittest.TestCase):
    """A job that runs a Node gate must install the Node dependencies first.

    The "Documentation counts & skill layout" step shells out to
    ``scripts/ci/validate-skills.js`` (needs js-yaml) and
    ``scripts/ci/validate-install-manifests.js`` (needs ajv). The validate job
    never ran ``npm ci``, so the step could not pass on a clean runner — it went
    unnoticed only because an earlier step failed first and skipped it. This
    test catches the whole class: any job that invokes a Node gate needing a
    third-party module must install it earlier in the same job.
    """

    WORKFLOWS = ROOT / ".github" / "workflows"
    INSTALL_HINTS = ("npm ci", "npm install")

    def jobs(self) -> dict[str, list[str]]:
        import yaml

        jobs: dict[str, list[str]] = {}
        for path in sorted(self.WORKFLOWS.glob("*.yml")):
            data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
            for name, job in (data.get("jobs") or {}).items():
                runs = [
                    str(step.get("run", ""))
                    for step in (job.get("steps") or [])
                    if isinstance(step, dict)
                ]
                jobs[f"{path.name}:{name}"] = runs
        return jobs

    def test_node_gate_steps_are_preceded_by_an_install(self) -> None:
        try:
            import yaml  # noqa: F401
        except ModuleNotFoundError:
            self.skipTest("pyyaml unavailable")

        offenders = []
        for job, runs in self.jobs().items():
            installed = False
            for command in runs:
                if any(hint in command for hint in self.INSTALL_HINTS):
                    installed = True
                uses_node_gate = "scripts/ci/" in command and "node " in command
                if uses_node_gate and not installed:
                    offenders.append(f"{job}: {command.strip().splitlines()[0]}")
        self.assertEqual(
            offenders, [],
            "these jobs run a Node gate without installing its dependencies:\n  "
            + "\n  ".join(offenders),
        )

    def test_every_node_gate_in_ci_exists(self) -> None:
        referenced = set()
        for runs in self.jobs().values():
            for command in runs:
                for token in command.replace("|", " ").split():
                    if token.startswith("scripts/ci/") and token.endswith(".js"):
                        referenced.add(token)
        missing = sorted(path for path in referenced if not (ROOT / path).exists())
        self.assertEqual(missing, [], f"CI references gates that do not exist: {missing}")


if __name__ == "__main__":
    unittest.main()
