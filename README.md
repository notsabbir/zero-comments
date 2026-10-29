# Zero Comments Plugin

An Antigravity plugin and coding standard that strictly enforces zero comments across entire codebases. It provides automatic rule enforcement, multi-language scanning, and safe in-place comment stripping.

## Why Zero Comments?

Code should be self-documenting. Explanatory comments frequently rot, contradict implementation changes, or explain *what* rather than *why*. By prohibiting comments:
- Variable, function, and class names must be clear, precise, and descriptive.
- Logic must remain simple, modular, and readable.
- Codebases remain concise and clutter-free.

## What is Included

1. **Rule (`rules/AGENTS.md`)**: Automatically activates whenever the plugin is enabled, preventing AI pair-programmers and agents from generating comments.
2. **Skill (`skills/zero-comments/SKILL.md`)**: Equips agents with procedures to scan, audit, and strip comments across diverse languages.
3. **Audit CLI (`scripts/scan_comments.py`)**: A portable Python script for local checks or CI/CD pipelines. Exits `0` if clean, `1` if comments are found.
4. **Stripper CLI (`scripts/strip_comments.py`)**: A safe, syntax-aware utility to remove comments in-place while preserving URLs and string literals.

## Supported Formats

- **JVM & C-Style**: Kotlin, Java, C, C++, C#, Swift, Go (`//`, `/* ... */`)
- **Web & Scripting**: JavaScript, TypeScript, PHP, JSX, TSX (`//`, `/* ... */`)
- **Hash-Style**: Python, Ruby, Bash, PowerShell, YAML, Properties (`#`)
- **Markup**: XML, HTML, SVG (`<!-- ... -->`)
- **Windows Batch**: Batch scripts (`::`, `REM`)

## Installation

### Option 1: Install in Antigravity (Local Global Config)

Clone or copy this folder into your local Antigravity plugins directory:

```bash
git clone https://github.com/your-username/zero-comments-plugin.git ~/.gemini/config/plugins/zero-comments
```

Restart Antigravity or enable the plugin in the Plugins settings.

### Option 2: Project-Level Workspace Plugin

Copy the plugin into your project's `.agents` directory:

```text
your-project/
└── .agents/
    └── plugins/
        └── zero-comments/
            ├── plugin.json
            ├── rules/
            └── skills/
```

## CLI Usage

### Scan Repository for Comments
```bash
python scripts/scan_comments.py --dir .
```

### Strip Comments in Place
```bash
python scripts/strip_comments.py --dir .
```

## License

MIT
