"""Permanent regression tests (docs/NO_REGRESSION_POLICY.md §3 "Bug-to-Regression").

Each test pins a defect that previously shipped on ``main``:

1. ``pip install -e .`` crashed because ``setup.py`` duplicated metadata that the
   PEP 621 ``[project]`` table did not declare (covered by CI's install step).
2. An unanchored ``build/`` rule in ``.gitignore`` silently kept the
   ``awesome_skills/automation/build`` skill out of Git, so catalog statistics
   could never verify on a fresh clone.
3. 158 skill package ``__init__.py`` files contained literal ``\\n`` escapes
   (SyntaxError) and all 142 ``handler.py`` modules subclassed ``BaseSkill``
   before importing it (NameError), so no skill handler could be imported.
4. ``skills.lock`` digests depended on the host OS (CRLF checkouts, path sort
   order, ``__pycache__`` files), so a lockfile generated on Windows reported
   every skill as "tampered" on Linux CI.
5. The packaged CLI's ``doctor`` command called ``Validator`` with the wrong
   signature and crashed with ``TypeError``.
6. ``skills/dependencies.json`` recorded which tools were installed on the
   machine that generated it, so ``refresh_registry.py --check`` failed in CI.
7. Overall quality scores were aggregated with float ``sum()``, whose algorithm
   changed in Python 3.12, so boundary scores differed between interpreters.
8. The frontmatter parser read YAML compact sequences ("tags:\n- a") as empty
   lists, silently dropping triggers, aliases, tools and dependencies of every
   canonical and active skill; block scalars also truncated the frontmatter.
9. On Windows, harness-link detection reported every *missing* target as a
   broken junction (ctypes returned INVALID_FILE_ATTRIBUTES as -1), so
   ``setup_tools.py --verify`` failed on every clean checkout.
10. Documented counts drifted from ``stats.json`` ("94 tests", "243 domains",
    "122 canonical skills"): sync rules only covered README/SKILLS, matched
    hard-coded old values, lower-cased what they rewrote, and ``--verify``
    never looked at the docs at all.
"""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

_ROOT = Path(__file__).resolve().parents[1]
_SRC = _ROOT / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from skills.lock import compute_skill_tree_hash  # noqa: E402

_SKILLS_DIR = _ROOT / "skills"
_CATALOG_INDEX = _ROOT / "awesome_skills" / "skills_index.json"


def _catalog_skill_dirs() -> list[str]:
    records = json.loads(_CATALOG_INDEX.read_text(encoding="utf-8"))
    dirs = []
    for record in records:
        path = record["path"].replace("\\", "/")
        dirs.append(path[: -len("/SKILL.md")] if path.endswith("/SKILL.md") else path)
    return dirs


class TestCatalogIsFullyTracked(unittest.TestCase):
    """Regression #2 — catalog skills must never be hidden by .gitignore."""

    def test_every_catalog_index_entry_exists_on_disk(self):
        # Directory-level check: a few upstream entries are bundles whose SKILL.md
        # files live one level deeper, but every indexed skill directory must exist.
        missing = [d for d in _catalog_skill_dirs() if not (_ROOT / d).is_dir()]
        self.assertEqual(missing, [], f"{len(missing)} catalog skills missing, e.g. {missing[:5]}")

    def test_gitignore_does_not_match_catalog_skills(self):
        if shutil.which("git") is None or not (_ROOT / ".git").exists():
            self.skipTest("git checkout not available")
        stdin = "\n".join(f"{d}/SKILL.md" for d in _catalog_skill_dirs())
        proc = subprocess.run(
            ["git", "check-ignore", "--no-index", "--stdin"],
            cwd=_ROOT, input=stdin, capture_output=True, text=True, encoding="utf-8", errors="replace", check=False,
        )
        ignored = [line for line in proc.stdout.splitlines() if line.strip()]
        self.assertEqual(ignored, [], f".gitignore hides catalog skills: {ignored[:5]}")


class TestSkillHandlersImportable(unittest.TestCase):
    """Regression #3 — every skill package and handler must be importable."""

    def test_skill_packages_compile(self):
        broken = []
        for init in sorted(_SKILLS_DIR.rglob("__init__.py")):
            try:
                compile(init.read_text(encoding="utf-8"), str(init), "exec")
            except SyntaxError as exc:
                broken.append(f"{init.relative_to(_ROOT)}: {exc.msg}")
        self.assertEqual(broken, [], f"{len(broken)} skill packages do not compile: {broken[:5]}")

    def test_skill_handlers_import_and_instantiate(self):
        handlers = sorted(_SKILLS_DIR.rglob("handler.py"))
        self.assertGreater(len(handlers), 0)
        failures = []
        for handler in handlers:
            rel = handler.relative_to(_ROOT)
            name = "_regression_handler_" + "_".join(rel.with_suffix("").parts)
            spec = importlib.util.spec_from_file_location(name, handler)
            assert spec is not None and spec.loader is not None
            module = importlib.util.module_from_spec(spec)
            try:
                with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                    spec.loader.exec_module(module)
                skill_classes = [
                    obj for obj in vars(module).values()
                    if isinstance(obj, type) and obj.__module__ == name and obj.__name__ != "BaseSkill"
                ]
                if not skill_classes:
                    failures.append(f"{rel}: no skill class defined")
                for cls in skill_classes:
                    result = cls().handle("regression-test", {})
                    if not isinstance(result, dict):
                        failures.append(f"{rel}: {cls.__name__}.handle() returned {type(result).__name__}")
            except Exception as exc:  # noqa: BLE001 - report every broken handler at once
                failures.append(f"{rel}: {type(exc).__name__}: {exc}")
            finally:
                sys.modules.pop(name, None)
        self.assertEqual(failures, [], f"{len(failures)} broken handlers, e.g. {failures[:5]}")


class TestLockHashIsPlatformIndependent(unittest.TestCase):
    """Regression #4 — skills.lock digests must be identical on every OS."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.skill = Path(self._tmp.name) / "demo-skill"
        (self.skill / "references").mkdir(parents=True)
        (self.skill / "SKILL.md").write_bytes(b"---\nname: demo-skill\n---\n\n# Demo\nline two\n")
        (self.skill / "references" / "guide.md").write_bytes(b"# Guide\n\n- step\n")
        (self.skill / "Zeta.md").write_bytes(b"upper-case name sorts differently on Windows\n")
        (self.skill / "asset.bin").write_bytes(b"\x00\x01\r\n\x02")  # binary: hashed byte-for-byte

    def tearDown(self):
        self._tmp.cleanup()

    def test_crlf_checkout_produces_same_digest(self):
        lf_digest, lf_files = compute_skill_tree_hash(self.skill)
        for path in self.skill.rglob("*.md"):
            path.write_bytes(path.read_bytes().replace(b"\n", b"\r\n"))
        crlf_digest, crlf_files = compute_skill_tree_hash(self.skill)
        self.assertEqual(lf_digest, crlf_digest)
        self.assertEqual(lf_files, crlf_files)

    def test_binary_content_changes_are_detected(self):
        before, _ = compute_skill_tree_hash(self.skill)
        (self.skill / "asset.bin").write_bytes(b"\x00\x01\n\x02")
        after, _ = compute_skill_tree_hash(self.skill)
        self.assertNotEqual(before, after)

    def test_order_uses_posix_relative_paths(self):
        _, files = compute_skill_tree_hash(self.skill)
        self.assertEqual(files, sorted(files))
        self.assertIn("references/guide.md", files)

    def test_interpreter_caches_and_hidden_files_are_ignored(self):
        before, _ = compute_skill_tree_hash(self.skill)
        (self.skill / "__pycache__").mkdir()
        (self.skill / "__pycache__" / "handler.cpython-311.pyc").write_bytes(b"\x00cache")
        (self.skill / ".cache").mkdir()
        (self.skill / ".cache" / "tmp.txt").write_text("scratch", encoding="utf-8")
        after, files = compute_skill_tree_hash(self.skill)
        self.assertEqual(before, after)
        self.assertFalse(any("__pycache__" in f or f.startswith(".") for f in files))


class TestDependenciesIndexIsEnvironmentIndependent(unittest.TestCase):
    """Regression #6 — skills/dependencies.json must not depend on the local machine.

    It used to record which tools were installed where it was generated, so
    ``refresh_registry.py --check`` failed on every other machine (including CI).
    """

    def test_generated_index_ignores_installed_tools(self):
        from skills import dependencies
        from skills.registry import load_registry

        entries = load_registry(_ROOT).entries

        def generate(tools_available: bool) -> dict:
            dependencies._DEP_CACHE.clear()
            with mock.patch.object(dependencies.shutil, "which",
                                   return_value="/usr/bin/tool" if tools_available else None), \
                    mock.patch.object(dependencies.importlib.util, "find_spec",
                                      return_value=object() if tools_available else None):
                return dependencies.generate_dependencies_json(entries)

        try:
            everything_installed = generate(True)
            nothing_installed = generate(False)
        finally:
            dependencies._DEP_CACHE.clear()
        self.assertEqual(everything_installed, nothing_installed)
        committed = json.loads((_SKILLS_DIR / "dependencies.json").read_text(encoding="utf-8"))
        self.assertEqual(committed, nothing_installed)


class TestQualityScoreIsInterpreterIndependent(unittest.TestCase):
    """Regression #7 — registry quality scores must not depend on the Python version."""

    def test_boundary_score_rounds_half_up(self):
        from skills.quality import QualityReport, _weighted_overall

        # Exact weighted sum is 6.45; float sum() gives 6.4499… on Python < 3.12.
        report = QualityReport(
            skill_id="boundary", documentation=9.0, maintenance=3.0, reliability=9.0,
            security=9.0, compatibility=6.0, usefulness=0.0,
        )
        self.assertEqual(_weighted_overall(report), 6.5)


class TestFrontmatterParserMatchesYaml(unittest.TestCase):
    """Regression #8 — skill frontmatter must parse like YAML."""

    def test_yaml_constructs_used_by_skills(self):
        from skills.frontmatter import parse_frontmatter

        text = (
            "---\n"
            "name: demo\n"
            "tags:\n- a\n- b\n"
            "dependencies:\n- optional:docker\n- url: http://example.com\n"
            "description: 'first line\n  continued'\n"
            "notes: >\n  folded\n  text\n"
            "tools: [file_read, file_write]\n"
            "---\nbody\n"
        )
        meta, body = parse_frontmatter(text)
        self.assertEqual(meta["tags"], ["a", "b"])
        self.assertEqual(meta["dependencies"], ["optional:docker", {"url": "http://example.com"}])
        self.assertEqual(meta["description"], "first line continued")
        self.assertEqual(meta["notes"], "folded text")
        self.assertEqual(meta["tools"], ["file_read", "file_write"])
        self.assertEqual(body, "body\n")

    def test_library_frontmatter_matches_pyyaml(self):
        import re

        import yaml

        from skills.frontmatter import parse_frontmatter

        def norm(value):
            if isinstance(value, dict):
                return {str(k): norm(v) for k, v in value.items()}
            if isinstance(value, list):
                return [norm(v) for v in value]
            if isinstance(value, bool):
                return str(value).lower()
            return "" if value is None else str(value).strip()

        files = sorted(_SKILLS_DIR.glob("*/*/SKILL.md")) + sorted((_ROOT / ".agents" / "skills").glob("*/SKILL.md"))
        self.assertGreater(len(files), 100)
        mismatches = []
        for path in files:
            text = path.read_text(encoding="utf-8")
            block = re.match(r"^---\s*\n(.*?)\n---", text, re.S)
            self.assertIsNotNone(block, f"{path} has no frontmatter")
            reference = yaml.safe_load(block.group(1)) or {}
            parsed, _ = parse_frontmatter(text)
            mismatches += [f"{path.relative_to(_ROOT)}:{k}" for k, v in reference.items() if norm(v) != norm(parsed.get(k))]
        self.assertEqual(mismatches, [], f"{len(mismatches)} fields differ from YAML, e.g. {mismatches[:5]}")


class TestHarnessLinkDetection(unittest.TestCase):
    """Regression #9 — only real symlinks/junctions count as harness links."""

    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("_regression_setup_tools", _ROOT / "scripts" / "setup_tools.py")
        assert spec is not None and spec.loader is not None
        cls.setup_tools = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.setup_tools)

    def test_missing_and_real_paths_are_not_links(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            self.assertFalse(self.setup_tools.is_link_or_junction(base / "missing"))
            (base / "real").mkdir()
            self.assertFalse(self.setup_tools.is_link_or_junction(base / "real"))

    def test_symlinks_are_links(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            (base / "target").mkdir()
            try:
                (base / "link").symlink_to(base / "target", target_is_directory=True)
            except (OSError, NotImplementedError):
                self.skipTest("creating symlinks is not permitted here")
            self.assertTrue(self.setup_tools.is_link_or_junction(base / "link"))


class TestNativeCliDoctor(unittest.TestCase):
    """Regression #5 — the packaged CLI's doctor command must not crash."""

    def test_native_doctor_runs_validation(self):
        from skills import cli

        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout), self.assertRaises(SystemExit) as ctx:
            cli._run_native_cli(_ROOT, ["doctor"])
        self.assertIn(ctx.exception.code, (0, 1))
        self.assertIn("Doctor Diagnostic:", stdout.getvalue())
        self.assertIn("Validation Errors:", stdout.getvalue())


class TestDocumentationCountsMatchStats(unittest.TestCase):
    """Regression #10 — documented counts follow stats.json in every doc."""

    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("compute_stats_under_test",
                                                      _ROOT / "scripts" / "compute_stats.py")
        assert spec and spec.loader
        cls.cs = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.cs)

    def test_stale_claims_are_rewritten_in_place(self):
        stats = json.loads((_ROOT / "stats.json").read_text(encoding="utf-8"))
        stats.update({"tests": 237, "canonical_skills": 124, "active_harness_skills": 72, "categories": 251,
                      "catalog_skills": 14855, "total_unique_skills": 12757})

        def box(*cells: str) -> str:  # a two-column ASCII-art box row (widths 31 and 33)
            return "│" + "│".join(c.ljust(w) for c, w in zip(cells, (31, 33))) + "│"

        text = "\n".join([
            "intro",
            "# Run full health diagnostics and test suite (94 tests)",
            "| 94 unit tests validating loader |",
            "All 122 canonical skills and 70 active harness skills",
            "## Pre-Loaded Active Harness Skills (70 Skills)",
            "organized across 243 functional domains; `14,000` categorized implementations",
            '<img src="https://img.shields.io/badge/catalog-9%2C999%20Catalog%20Entries-0ea5e9" alt="9,999 Catalog Entries" />',
            box("  • 99 CI-Gated Tests", "  • 9,999 Catalog Entries"),
            "Over 9,000 unique skills and 9,999 catalog entries",
        ])
        new, changes = self.cs.apply_doc_counts(text, stats)
        self.assertIn("test suite (237 tests)", new, "case of the surrounding text must be preserved")
        self.assertIn("| 237 unit tests validating loader |", new)
        self.assertIn("All 124 canonical skills and 72 active harness skills", new)
        self.assertIn("Active Harness Skills (72 Skills)", new)
        self.assertIn("across 251 functional domains; `14,855` categorized", new)
        self.assertIn("badge/catalog-14%2C855%20Catalog%20Entries", new, "badge paths use URL-encoded separators")
        self.assertIn('alt="14,855 Catalog Entries"', new)
        self.assertIn(box("  • 237 CI-Gated Tests", "  • 14,855 Catalog Entries"), new, "boxes stay aligned")
        self.assertIn("Over 12,757 unique skills and 14,855 catalog entries", new,
                      "catalog entries and unique skills are different metrics")
        self.assertIn((2, "94", "237"), changes, "drift is reported with its line number")
        self.assertEqual(self.cs.apply_doc_counts(new, stats)[1], [], "syncing must be idempotent")

    def test_documentation_makes_no_static_passing_or_verified_claims(self):
        for pattern, _key, _style in self.cs.DOC_COUNT_RULES:
            self.assertNotRegex(pattern.pattern, r"(?i)passing|verified", "a sync rule would assert a status")
        readme = (_ROOT / "README.md").read_text(encoding="utf-8")
        for claim in (r"\d+/\d+ Passing", r"Tests? Passing", r"%20Passing", r"Verified%20Skills",
                      r"Curated & Tested", r"least-privilege sandboxing", r"sandboxed, composable"):
            self.assertNotRegex(readme, claim, "CI status comes from live badges, trust from recorded evidence")

    def test_repository_documentation_agrees_with_stats_json(self):
        stats = json.loads((_ROOT / "stats.json").read_text(encoding="utf-8"))
        self.assertEqual(self.cs.verify_docs(stats, _ROOT), [],
                         "run: python scripts/compute_stats.py --sync-readme")


if __name__ == "__main__":
    unittest.main()
