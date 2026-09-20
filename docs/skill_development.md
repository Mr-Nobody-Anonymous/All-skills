# Skill Development Guide

This guide details how to create, test, package, and publish voice and multimodal skills in the All-Skills ecosystem.

---

## 1. Skill Package Structure

Every skill lives under `skills/<category>/<skill-name>/` and adheres to the following layout:

```
skills/<category>/<skill-name>/
├── __init__.py          # Python package entry point
├── skill.py            # Primary Skill implementation class inheriting from BaseVoiceSkill
├── manifest.yml        # Metadata, priority tier, dependencies, and intents
├── requirements.txt    # Python package dependencies
├── README.md           # User-facing documentation and invocation examples
└── locale/
    └── en-us/
        ├── intents/    # Padatious / Adapt intent definitions (*.intent)
        ├── dialog/     # Spoken response templates (*.dialog)
        └── vocab/      # Keyword entity vocabularies (*.voc)
```

---

## 2. Skill Implementation Example

```python
from core.skill_loader import BaseVoiceSkill

class ExampleSkill(BaseVoiceSkill):
    def __init__(self):
        super().__init__("ExampleSkill")

    def initialize(self):
        self.register_intent_file("example.intent", self.handle_example)

    def handle_example(self, message):
        self.speak_dialog("example_response", {"user": message.data.get("user", "User")})
```

---

## 3. Creating Skills with Built-in Tools

Use the `tools/skill_creator/template_generator.py` utility to scaffold new skills automatically:

```bash
python tools/skill_creator/template_generator.py \
    --name "my-custom-skill" \
    --category "productivity" \
    --tier "TIER_2_HIGH"
```

---

## 4. Testing Your Skill

Use the automated testing tool:

```bash
# Test intent parsing and dialog matching
python tools/skill_tester/intent_tester.py --skill skills/productivity/skill-todo-list/

# Run complete platform test suite
python scripts/skills/skills.py test
```
