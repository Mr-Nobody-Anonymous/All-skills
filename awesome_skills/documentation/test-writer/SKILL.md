---
name: test-writer
description: |
  Generate unit tests, integration tests, and test plans.
  TRIGGERS - Use when user wants tests, test cases, testing strategy, or test coverage.
source: "https://github.com/Winbda/claude-skills-collection"
source_repository: "Winbda/claude-skills-collection"
source_path: "skills/test-writer/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Test Writer

## Approach
1. Analyze the code to understand functionality
2. Identify test scenarios (happy path, edge cases, errors)
3. Write tests using appropriate framework
4. Include assertions for expected behavior
5. Add edge case coverage

## Output includes:
- Test file with complete test suite
- Test descriptions explaining what each test validates
- Setup/teardown helpers
- Mocking strategy for dependencies
- Coverage recommendations
