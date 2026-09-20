# Context Window Budgeting & Pruning Rule

## Context Health Directive
- Monitor conversation length and token utilization.
- When conversation exceeds 70% of the active context window or ~40 turns, initiate state distillation.
- Offload verbose terminal outputs, build logs, and large data dumps to persistent files under `scratch/` instead of dumping them directly into conversational context.
- Read files using line slices (`StartLine`/`EndLine`) or pattern search rather than dumping entire files.
- Summarize findings in concise, structured bullet points.
