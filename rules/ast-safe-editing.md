# AST Safe Editing Rule

## Structural Code Modification Directive
- Avoid brittle regex find-and-replace across multi-line blocks that span nested control structures.
- Include 3 to 5 lines of surrounding syntactic context when editing code with line-replacement tools to guarantee match uniqueness.
- For structural transforms or renames, prefer AST-aware tools (`ast-grep`, `tree-sitter`, Python `ast` / `libcst`, `jscodeshift`).
- **Mandatory AST Verification**: Never complete a turn modifying source code without running an AST parse / dry-run syntax check (`python -m py_compile`, `node --check`, `json.tool`) to ensure zero syntax errors.
