# `adapters/` — agent harness & I/O adapters

| Path | Contents |
| :--- | :--- |
| `*.yaml` | One configuration per supported agent harness (Claude Code, Cursor, Codex, Copilot, Gemini, Goose, Cline, Roo, OpenCode, VS Code, Windsurf) plus `agents.yaml` |
| `input/`, `input_adapters/` | Text, voice, image and multimodal input adapters |
| `output/`, `output_adapters/` | Text, voice, visual and action output adapters |

## How to run

```bash
python scripts/setup_tools.py --status        # which harnesses are linked
python scripts/setup_tools.py                 # create harness links from these configs
python -m pytest tests/test_adapters_conformance.py -v   # adapter conformance tests
```

When adding a harness, add its YAML file here and a case to
`tests/test_adapters_conformance.py`.
