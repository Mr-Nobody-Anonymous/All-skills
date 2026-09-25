# `hooks/` — lifecycle hooks

Scripts that run before, after, or on failure of a skill execution. Hooks are
declared in [`hooks.json`](hooks.json); a hook marked `"required": true` **fails
closed** — if it is missing or exits non-zero, execution stops.

| Stage | Scripts |
| :--- | :--- |
| `pre/` | `check_environment.py`, `check_git_clean.py`, `check_permissions.py` |
| `post/` | `verify_syntax.py`, `verify_tests.py` |
| `on_failure/` | `handle_recovery.py` |

## How to run

```bash
python scripts/run_hook.py list                        # show configured hooks
python scripts/run_hook.py pre  <skill_id>
python scripts/run_hook.py post <skill_id>
python scripts/run_hook.py failure <skill_id> --error "details"
```

Fail-closed behaviour is covered by `tests/test_security_gates.py`.
