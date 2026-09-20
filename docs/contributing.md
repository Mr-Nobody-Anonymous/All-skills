# Contributing Guidelines

Thank you for contributing to the **All-Skills Universal Platform**.

---

## 1. Operating Rules & Guardrails

1. **Zero Deletions**: Never delete existing skills, catalogs, or platform files. Deletions will fail automated CI checks.
2. **Strict Schema Compliance**: Every skill package must include valid metadata (`manifest.yml` and `SKILL.md` frontmatter).
3. **Green Test Suite**: All tests must pass before opening a PR:
   ```bash
   python scripts/skills/skills.py test
   python scripts/validate_schema.py
   ```
4. **No Plain Secrets**: Never commit real API keys, credentials, or `.env` files. Use `config/api_keys.yml.template`.

---

## 2. Adding a New Skill

1. Generate the skill boilerplate:
   ```bash
   python tools/skill_creator/template_generator.py --name "new-skill" --category "<category>"
   ```
2. Implement your logic in `skill.py`.
3. Add intent and dialog files under `locale/en-us/`.
4. Add unit tests under `tests/test_skills/`.
5. Run the validator:
   ```bash
   python scripts/skill_validator.py --skill skills/<category>/new-skill
   ```

---

## 3. Pull Request Process

1. Create a feature branch: `git checkout -b feat/add-my-skill`.
2. Commit your changes with conventional commit messages: `feat(skills): add my-skill`.
3. Run `allskills.bat doctor` to ensure all 11 platform harnesses are synchronized.
4. Submit the Pull Request for review.
