# Guide: Adding New Skills

This guide explains how to add new skills to the **All-Skills** repository while following the 7 Architectural Principles.

---

## 1. Skill Interface Contract

Every skill module must be placed in `skills/<category>/<module_name>/` and implement the standard interface:

```python
from typing import Dict, Any, List, Optional

class MyCustomSkill:
    def __init__(self, event_bus: Optional[Any] = None):
        self.event_bus = event_bus
        self.priority = 35
        self.supported_intent = "my_custom.action"
        self.dependencies = []
        self._model = None

    def get_priority(self) -> int:
        return self.priority

    def can_handle(self, intent: str) -> bool:
        return self.supported_intent in intent.lower()

    def declare_dependencies(self) -> List[str]:
        return list(self.dependencies)

    def handle(self, intent_data: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return {
            "status": "success",
            "skill": "MyCustomSkill",
            "result": "Completed successfully"
        }
```

---

## 2. Registering in the Priority Manifest

Add your skill to [`scratch_priority_import/skill_manifest.yaml`](file:///scratch_priority_import/skill_manifest.yaml):

```yaml
my_custom_skill:
  priority: 35
  category: "productivity"
  dependencies: ["intent_engine"]
  load_strategy: "eager"
  resource_requirements:
    cpu: "standard"
    gpu: false
    memory_mb: 50
  status: "enabled"
  supported_platforms: ["all"]
```

---

## 3. Testing Your Skill

Add a unit test in `tests/test_skills/`:

```bash
python -m unittest tests/test_skills/test_my_custom_skill.py
python scripts/skills/skills.py test
```
