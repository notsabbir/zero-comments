# Zero Comments Coding Standard

## Core Invariant
- **Strictly Zero Comments Across the Entire Project**:
  - No single-line comments (`//`, `#`), multi-line comments (`/* ... */`), XML comments (`<!-- ... -->`), or batch comments (`::`, `REM`) are permitted anywhere in production, test, script, or configuration code.
  - Self-documenting code: Code must explain itself through descriptive naming, clear types, and idiomatic structure rather than explanatory comments.
  - String literals containing URL protocols (`http://`, `https://`) or formatting syntax are preserved and are not treated as comments.
  - Do not add comments during code generation, debugging, refactoring, or testing.
  - If existing comments are encountered in files touched during a task, remove them cleanly.
