# `tests/` — test suite

Unit, integration and regression tests for the platform. Tests are written with
`unittest` and also run under `pytest`.

## How to run

```bash
python -m pip install -e ".[test]"                           # from the repository root
python scripts/skills/skills.py test                         # canonical runner used by CI (No-Regression Gate 2)
pytest tests scratch_priority_import/tests --cov             # everything, with coverage for src/skills
pytest tests/test_regressions.py -v                          # a single module
python -m unittest tests.skill_tests.test_router -v          # a single module with unittest
```

## Layout

| Path | Covers |
| :--- | :--- |
| `skill_tests/` | Registry, router, validator, chains, conflicts, lifecycle, quality, live routing |
| `test_runtime.py` | Execution runtime, policy gates and audit logging |
| `test_security_gates.py` | Hook fail-closed behaviour, scanners, quarantine, revocations |
| `test_adapters_conformance.py` | Harness adapter configurations |
| `test_regressions.py` | Permanent regression tests for previously shipped bugs |
| `test_core/`, `test_integration/`, `test_interfaces/`, `test_memory/`, `test_plugins/`, … | Voice/multimodal OS subsystems |

## Rules

- Every bug fix ships with a regression test — see
  [`docs/NO_REGRESSION_POLICY.md`](../docs/NO_REGRESSION_POLICY.md) §3.
- The discovered test count is recorded in `stats.json`; after adding tests run
  `python scripts/compute_stats.py && python scripts/generate_readme_stats.py && python scripts/generate_baselines.py`.
