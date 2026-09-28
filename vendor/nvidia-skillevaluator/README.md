# NVIDIA SkillEvaluator Integration

This directory hosts the adapted **NVIDIA SkillEvaluator** 3-tier validation and behavioral evaluation framework for the All-Skills federated platform.

## 3-Tier Architecture
1. **Tier 1: Validation & Quality Gate**
   - YAML frontmatter schema conformance (`schemas/skill-frontmatter.schema.json`).
   - AST security scanning (destructive commands, credentials, shell injections).
   - Composite quality score computation.
2. **Tier 2: Deduplication & Overlap Gate**
   - Jaccard and cosine token overlap against existing canonical and catalog skills.
   - Prevents duplicate canonical suites.
3. **Tier 3: Behavioral & Execution Gate**
   - Verification of structural directives, execution workflows, and test criteria.

## Usage
```python
from vendor.nvidia_skillevaluator.evaluator import SkillEvaluator
from pathlib import Path

evaluator = SkillEvaluator()
report = evaluator.evaluate_full(Path("skills/mobile/android-compose/SKILL.md"))
print(report.overall_verdict)  # "PASSED"
```
