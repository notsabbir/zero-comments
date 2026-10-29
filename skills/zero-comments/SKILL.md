---
name: zero-comments
description: How to audit, detect, and cleanly strip all comments across multi-language codebases without breaking string literals, regexes, or build scripts.
---

# Zero Comments Skill

## Purpose
Enforce a clean, comment-free codebase by scanning, auditing, and stripping single-line, multi-line, XML, and script comments across all file formats while preserving string literals, URLs, and documentation markdown files.

## Supported Languages & Formats
- **C-Style & JVM**: Kotlin, Java, C, C++, C#, Swift, Go (`//`, `/* ... */`)
- **Web & Scripting**: JavaScript, TypeScript, PHP (`//`, `/* ... */`)
- **Hash-Style**: Python, Ruby, Bash, PowerShell, YAML, Properties (`#`)
- **Markup**: XML, HTML, SVG (`<!-- ... -->`)
- **Batch / Windows**: Batch files (`::`, `REM`)

## Workflow

### 1. Audit / Scan
Run the repository scanner to find any comment lines across the target directory:
```bash
python scripts/scan_comments.py --dir .
```
The scanner inspects source files, parses string literal bounds, and reports any comments with exact file paths and line numbers. It exits with code `0` if clean or code `1` if violations are found.

### 2. Clean / Strip
To automatically strip comments across files in-place:
```bash
python scripts/strip_comments.py --dir .
```
The stripper safely removes comments while:
- Preserving strings containing `//` (such as `http://` or `https://` URLs)
- Preserving shebang lines if required (`#!/usr/bin/env ...`)
- Preserving pure Markdown documentation files (`README.md`, docs)
- Leaving code formatting intact

### 3. Verification Gate
After stripping comments:
1. Re-run `python scripts/scan_comments.py --dir .` to confirm zero violations.
2. Run your project's automated test suite (`./gradlew test`, `pytest`, `npm test`) to confirm that all tests pass and no functionality was altered.
