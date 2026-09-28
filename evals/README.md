# `evals/` — evaluation suites

Data-driven evaluation cases for routing quality and safety.

| Suite | Files | Measures |
| :--- | :--- | :--- |
| `routing/` | `routing_cases.json`, `trigger_cases.json`, `ood_cases.json` | Correct skill selection, trigger phrases, out-of-distribution rejection |
| `behavioral/` | `*_eval.json` | Expected behaviour of individual skills |
| `adversarial/` | `prompt_injection_cases.json` | Resistance to prompt-injection attempts |
| `security/` | `security_cases.json` | Security scanner detections |

## How to run

```bash
python scripts/run_evals.py          # all suites (runs in CI)
python scripts/run_benchmarks.py     # routing benchmark & latency percentiles
```

Add a case by appending to the relevant JSON file, then run `run_evals.py`.
