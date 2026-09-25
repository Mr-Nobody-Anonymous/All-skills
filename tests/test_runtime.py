"""Tests for Universal Skill Execution Runtime (src/skills/runtime.py)."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
_SRC = _ROOT / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from skills.runtime import ExecutionResult, ExecutionRuntime


class TestExecutionRuntime(unittest.TestCase):
    """Test suite for universal skill execution, policy gates, and audit logs."""

    def setUp(self):
        self.workspace_root = Path(__file__).resolve().parents[1]
        self.temp_dir = tempfile.TemporaryDirectory()
        self.audit_log_path = Path(self.temp_dir.name) / "test_audit_log.jsonl"
        self.runtime = ExecutionRuntime(
            workspace_root=self.workspace_root,
            audit_log_path=self.audit_log_path,
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_runtime_execute_valid_skill(self):
        """Without an executor, a skill is *prepared* (instructions for the agent), never reported as done.

        This test previously asserted a fabricated ``completed`` status, synthesised
        outputs, ``verified: True`` and tools marked "acquired" although nothing ran.
        """
        result = self.runtime.execute(
            skill="development.debugging",
            input={"code_snippet": "def foo(): return 1 / 0", "issue": "ZeroDivisionError"},
            tools=["file_read", "file_edit"],
        )
        self.assertEqual(result.status, "prepared")
        self.assertFalse(result.executed)
        self.assertEqual(result.skill, "development.debugging")
        self.assertGreater(result.duration_ms, 0)
        self.assertTrue(len(result.audit_id) > 0)
        self.assertIn("# Debugging", result.outputs["instructions"])
        self.assertEqual(result.outputs["inputs"]["issue"], "ZeroDivisionError")
        self.assertFalse(result.verification["verified"])
        self.assertEqual(result.verification["postconditions"], "not_evaluated")
        self.assertIn("security_policy", result.verification["gates_passed"])
        self.assertTrue(result.cost["tokens_are_estimate"])
        self.assertGreater(result.cost["estimated_tokens"], 50)
        self.assertEqual(result.tool_calls, [])
        authorized = result.verification["tools_authorized"]
        self.assertEqual([t["tool"] for t in authorized], ["file_read", "file_edit"])
        self.assertEqual(authorized[1]["capabilities"], ["filesystem.write"])

    def test_runtime_blocks_revoked_killswitch_skill(self):
        """Executing any skill in revocations.json must be blocked immediately."""
        # Test against malicious-eval or a temporary revocations file
        temp_revocations = Path(self.temp_dir.name) / "revocations.json"
        temp_revocations.write_text(
            json.dumps({
                "schema_version": "1.0.0",
                "revoked_skills": {
                    "malicious.exfiltrate": {
                        "revoked_at": "2026-09-21T00:00:00Z",
                        "reason": "Active data exfiltration detected",
                        "severity": "CRITICAL"
                    }
                }
            }),
            encoding="utf-8"
        )
        runtime = ExecutionRuntime(
            workspace_root=self.workspace_root,
            audit_log_path=self.audit_log_path,
        )
        runtime._revocations_path = temp_revocations

        result = runtime.execute("malicious.exfiltrate")
        self.assertEqual(result.status, "blocked")
        self.assertIn("kill-switch", result.error)
        self.assertIn("Active data exfiltration detected", result.error)

    def test_runtime_denies_explicitly_blocked_permission(self):
        """If caller policy explicitly denies a required capability, runtime blocks execution."""
        result = self.runtime.execute(
            skill="development.debugging",
            permissions={"filesystem.read": "deny"},
            tools=["file_read"],
        )
        self.assertEqual(result.status, "blocked")
        self.assertIn("denied", result.error.lower())
        self.assertIn("filesystem.read", result.error)

    def test_runtime_audit_log_records_execution(self):
        """Every execution invocation must append a structured record to audit_log.jsonl."""
        result = self.runtime.execute(
            skill="development.debugging",
            input={"test": True},
            session_id="test-session-123",
        )
        self.assertTrue(self.audit_log_path.exists())
        lines = self.audit_log_path.read_text(encoding="utf-8").strip().splitlines()
        self.assertGreaterEqual(len(lines), 1)
        last_entry = json.loads(lines[-1])
        self.assertEqual(last_entry["audit_id"], result.audit_id)
        self.assertEqual(last_entry["skill"], "development.debugging")
        self.assertEqual(last_entry["status"], "prepared")
        self.assertEqual(last_entry["session_id"], "test-session-123")
        self.assertGreater(last_entry["duration_ms"], 0)

    def test_runtime_fails_on_nonexistent_skill(self):
        """Executing a skill not present in the registry fails cleanly with audit."""
        result = self.runtime.execute("nonexistent.skill.id")
        self.assertEqual(result.status, "failed")
        self.assertIn("not found in registry", result.error)

    def test_runtime_blocks_ssrf_inputs(self):
        """Input URLs pointing to internal loopback, private IPs, or cloud metadata must be blocked."""
        result = self.runtime.execute(
            skill="development.debugging",
            input={"webhook_url": "http://169.254.169.254/latest/meta-data/"},
        )
        self.assertEqual(result.status, "blocked")
        self.assertIn("SSRF", result.error)

    def test_runtime_simulate_mode(self):
        """Simulation returns execution plan and required capabilities without execution."""
        sim = self.runtime.simulate("development.debugging")
        self.assertEqual(sim["skill"], "development.debugging")
        self.assertEqual(sim["simulation_status"], "would_succeed")
        self.assertEqual(sim["verdict"], "ALLOW")
        self.assertIn("capabilities_required", sim)

    def test_runtime_audit_redaction(self):
        """Audit logging must redact embedded private keys, bearer tokens, and cloud keys."""
        # Intentionally log an error with sensitive token
        audit_id = "test-redact-1"
        self.runtime._log_audit(
            audit_id=audit_id,
            skill="test.skill",
            status="failed",
            duration_ms=10.0,
            session_id="s1",
            policy_verdict="DENY",
            tool_calls=[],
            error="Failed with token: Bearer secret_token_xyz and AKIA1234567890ABCDEF",
        )
        with open(self.audit_log_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        last_entry = json.loads(lines[-1])
        self.assertNotIn("secret_token_xyz", last_entry["error"])
        self.assertNotIn("AKIA1234567890ABCDEF", last_entry["error"])
        self.assertIn("[REDACTED_AWS_KEY]", last_entry["error"])
        self.assertIn("[REDACTED_TOKEN]", last_entry["error"])

    def test_runtime_result_to_dict(self):
        """ExecutionResult.to_dict() returns all required fields for structured API consumers."""
        result = ExecutionResult(
            status="completed",
            skill="test.skill",
            outputs={"out": 1},
            duration_ms=42.5,
            audit_id="abc-123",
        )
        d = result.to_dict()
        self.assertEqual(d["status"], "completed")
        self.assertEqual(d["skill"], "test.skill")
        self.assertEqual(d["duration_ms"], 42.5)
        self.assertEqual(d["audit_id"], "abc-123")
        self.assertEqual(d["outputs"]["out"], 1)


if __name__ == "__main__":
    unittest.main()
