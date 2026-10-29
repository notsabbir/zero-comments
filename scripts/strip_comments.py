import argparse
import os
import re
import sys

IGNORE_DIRS = {
    '.git', '.gradle', 'build', '.idea', 'brain', '.system_generated',
    'node_modules', '__pycache__', '.pytest_cache', 'dist', 'out'
}

EXTENSIONS = {
    '.kt', '.java', '.c', '.cpp', '.h', '.cs', '.swift', '.go',
    '.js', '.ts', '.jsx', '.tsx', '.php',
    '.py', '.rb', '.sh', '.ps1', '.yaml', '.yml', '.properties',
    '.xml', '.html', '.svg',
    '.bat', '.cmd'
}

def clean_file_content(content, ext):
    lines = content.splitlines(keepends=True)
    new_lines = []
    in_block = False

    for line in lines:
        s = line.strip()
        if not s:
            new_lines.append(line)
            continue

        if ext in {'.kt', '.java', '.c', '.cpp', '.h', '.cs', '.swift', '.go', '.js', '.ts', '.jsx', '.tsx', '.php'}:
            if in_block:
                if '*/' in line:
                    in_block = False
                    after = line.split('*/', 1)[1]
                    if after.strip():
                        new_lines.append(after)
                continue
            if s.startswith('/*') and '*/' in s:
                before = line.split('/*', 1)[0]
                after = line.split('*/', 1)[1]
                combined = before + after
                if combined.strip():
                    new_lines.append(combined if combined.endswith('\n') else combined + '\n')
                continue
            if s.startswith('/*'):
                in_block = True
                continue
            if s.startswith('//'):
                continue
            if '//' in line and not any(proto in line for proto in ['http://', 'https://', 'file://']):
                parts = line.split('//', 1)
                prefix = parts[0]
                if prefix.count('"') % 2 == 0 and prefix.count("'") % 2 == 0:
                    new_lines.append(prefix.rstrip() + '\n')
                    continue
        elif ext in {'.py', '.rb', '.sh', '.ps1', '.yaml', '.yml', '.properties'}:
            if s.startswith('#'):
                continue
            if '#' in line:
                parts = line.split('#', 1)
                prefix = parts[0]
                if prefix.count('"') % 2 == 0 and prefix.count("'") % 2 == 0 and prefix.strip():
                    new_lines.append(prefix.rstrip() + '\n')
                    continue
        elif ext in {'.xml', '.html', '.svg'}:
            if in_block:
                if '-->' in line:
                    in_block = False
                    after = line.split('-->', 1)[1]
                    if after.strip():
                        new_lines.append(after)
                continue
            if '<!--' in line and '-->' in line:
                cleaned = re.sub(r'<!--.*?-->', '', line)
                if cleaned.strip():
                    new_lines.append(cleaned)
                continue
            if '<!--' in line:
                in_block = True
                before = line.split('<!--', 1)[0]
                if before.strip():
                    new_lines.append(before + '\n')
                continue
        elif ext in {'.bat', '.cmd'}:
            if s.startswith('::') or s.startswith('REM ') or s == 'REM':
                continue

        new_lines.append(line)

    return ''.join(new_lines)

def process_directory(target_dir):
    modified = 0
    for root, dirs, files in os.walk(target_dir):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext not in EXTENSIONS:
                continue
            path = os.path.join(root, f)
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as fp:
                    content = fp.read()
                cleaned = clean_file_content(content, ext)
                if cleaned != content:
                    with open(path, 'w', encoding='utf-8') as fp:
                        fp.write(cleaned)
                    modified += 1
                    print(f'Stripped comments from: {path}')
            except Exception as e:
                print(f'Error processing {path}: {e}', file=sys.stderr)
    return modified

def main():
    parser = argparse.ArgumentParser(description='Strip all comments from codebase.')
    parser.add_argument('--dir', default='.', help='Target directory')
    args = parser.parse_args()

    count = process_directory(args.dir)
    print(f'Complete: Cleaned {count} file(s).')

if __name__ == '__main__':
    main()
