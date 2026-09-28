"""One workspace model for every entry point (--workspace, env var, discovery)."""

from __future__ import annotations

import contextlib
import io
import json
import os
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

from skills import cli  # noqa: E402
from skills.workspace import ENV_VAR, WorkspaceNotFound, catalog_provisioned, resolve_workspace  # noqa: E402


def make_workspace(root: Path) -> Path:
    (root / "skills" / "utilities" / "demo").mkdir(parents=True)
    (root / "skills" / "utilities" / "demo" / "SKILL.md").write_text(
        "---\nname: demo\ndescription: Demo skill for workspace tests.\n---\n# Demo\n", encoding="utf-8")
    (root / "skills" / "registry.json").write_text(json.dumps({"version": 1, "skills": [
        {"id": "utilities.demo", "name": "demo", "category": "utilities",
         "description": "Demo skill for workspace tests.", "path": "utilities/demo"}]}), encoding="utf-8")
    return root


class TestResolveWorkspace(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name).resolve()
        self.env = mock.patch.dict(os.environ, {}, clear=False)
        self.env.start()
        os.environ.pop(ENV_VAR, None)

    def tearDown(self):
        self.env.stop()
        self._tmp.cleanup()

    def test_resolution_order(self):
        explicit = make_workspace(self.tmp / "explicit")
        from_env = make_workspace(self.tmp / "env")
        discovered = make_workspace(self.tmp / "cwd")
        nested = discovered / "skills" / "utilities"
        self.assertEqual(resolve_workspace(cwd=nested), discovered)
        os.environ[ENV_VAR] = str(from_env)
        self.assertEqual(resolve_workspace(cwd=nested), from_env)
        self.assertEqual(resolve_workspace(explicit, cwd=nested), explicit)

    def test_invalid_overrides_are_rejected(self):
        with self.assertRaises(WorkspaceNotFound):
            resolve_workspace(self.tmp)
        os.environ[ENV_VAR] = str(self.tmp)
        with self.assertRaises(WorkspaceNotFound):
            resolve_workspace()

    def test_falls_back_to_the_source_checkout(self):
        self.assertEqual(resolve_workspace(cwd=self.tmp), _ROOT)

    def test_catalog_provisioning_is_explicit(self):
        ws = make_workspace(self.tmp / "ws")
        self.assertFalse(catalog_provisioned(ws))
        self.assertTrue(catalog_provisioned(_ROOT))


class TestCliUsesTheWorkspace(unittest.TestCase):
    def test_extract_workspace_flag_anywhere(self):
        self.assertEqual(cli._extract_workspace(["list", "--workspace", "/x", "--json"]), ("/x", ["list", "--json"]))
        self.assertEqual(cli._extract_workspace(["--workspace=/y", "route", "q"]), ("/y", ["route", "q"]))

    def test_native_cli_reads_the_given_workspace(self):
        with tempfile.TemporaryDirectory() as tmp:
            ws = make_workspace(Path(tmp))
            out = io.StringIO()
            with contextlib.redirect_stdout(out), self.assertRaises(SystemExit) as ctx:
                cli._run_native_cli(ws, ["list"])
            self.assertEqual(ctx.exception.code, 0)
            self.assertIn("utilities.demo", out.getvalue())
            self.assertIn("Loaded 1 skills", out.getvalue())

    def test_native_cli_without_workspace_fails_clearly(self):
        err = io.StringIO()
        with contextlib.redirect_stderr(err), self.assertRaises(SystemExit) as ctx:
            cli._run_native_cli(None, ["list"], "No All-Skills workspace found.")
        self.assertEqual(ctx.exception.code, 2)
        self.assertIn("No All-Skills workspace found", err.getvalue())

    def test_repository_cli_honours_workspace_flag(self):
        with tempfile.TemporaryDirectory() as tmp:
            ws = make_workspace(Path(tmp))
            proc = subprocess.run([sys.executable, "scripts/skills/skills.py", "--workspace", str(ws), "list"],
                                  cwd=_ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertIn("utilities.demo", proc.stdout)
            bad = subprocess.run([sys.executable, "scripts/skills/skills.py", "--workspace", tmp + "/nope", "list"],
                                 cwd=_ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120)
            self.assertEqual(bad.returncode, 2)


if __name__ == "__main__":
    unittest.main()
