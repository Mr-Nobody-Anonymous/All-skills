#!/usr/bin/env python3
"""Ecosystem and agent adapter conformance test suite."""

import sys
import unittest
from pathlib import Path
import yaml

_ROOT = Path(__file__).resolve().parents[1]
_SRC = _ROOT / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from adapters import (
    TextInputAdapter,
    TextOutputAdapter,
    ActionOutputAdapter,
)


class TestAdaptersConformance(unittest.TestCase):
    """Verifies that all 11 agent adapter definitions conform to the harness specification."""

    def setUp(self):
        self.adapters_dir = _ROOT / "adapters"

    def test_all_11_agent_configs_valid_yaml(self):
        """All 11 agent configurations must exist and parse as valid YAML with required keys."""
        agents = [
            "claude", "cline", "codex", "copilot", "cursor",
            "gemini", "goose", "opencode", "roo", "vscode", "windsurf"
        ]
        for agent in agents:
            config_file = self.adapters_dir / f"{agent}.yaml"
            self.assertTrue(config_file.exists(), f"Missing configuration file for agent: {agent}")
            with open(config_file, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            self.assertIsInstance(data, dict, f"Invalid YAML structure for {agent}")
            self.assertIn("agent_id", data, f"Missing 'agent_id' in {agent}.yaml")
            self.assertIn("discovery_paths", data, f"Missing 'discovery_paths' in {agent}.yaml")

    def test_agents_registry_manifest_contains_platform_harnesses(self):
        """agents.yaml must define registered platform harnesses."""
        agents_yaml = self.adapters_dir / "agents.yaml"
        self.assertTrue(agents_yaml.exists())
        with open(agents_yaml, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        self.assertIn("agents", data)
        registered_agents = set(data["agents"].keys())
        self.assertIn("claude-code", registered_agents)
        self.assertIn("cursor", registered_agents)
        self.assertIn("gemini-cli", registered_agents)
        self.assertIn("codex-cli", registered_agents)

    def test_input_and_output_adapter_instantiation(self):
        """Core input/output adapters instantiate cleanly and implement base transform methods."""
        in_adapter = TextInputAdapter()
        res = in_adapter.adapt("test prompt")
        self.assertIsNotNone(res)
        self.assertEqual(res["type"], "text")
        self.assertEqual(res["content"], "test prompt")

        out_adapter = TextOutputAdapter()
        rendered = out_adapter.format({"text": "success"}, format_type="markdown")
        self.assertIn("success", rendered)

        act_adapter = ActionOutputAdapter()
        self.assertIsNotNone(act_adapter)


if __name__ == "__main__":
    unittest.main()
