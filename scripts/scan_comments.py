import argparse
import os
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

def is_line_comment(line, ext):
    s = line.strip()
    if not s:
        return False
    if ext in {'.kt', '.java', '.c', '.cpp', '.h', '.cs', '.swift', '.go', '.js', '.ts', '.jsx', '.tsx', '.php'}:
        if s.startswith('//') or s.startswith('/*') or '*/' in s:
            return True
        if '//' in line and not any(proto in line for proto in ['http://', 'https://', 'file://']):
            parts = line.split('//')
            prefix = parts[0]
            if prefix.count('"') % 2 == 0 and prefix.count("'") % 2 == 0:
                return True
    elif ext in {'.py', '.rb', '.sh', '.ps1', '.yaml', '.yml', '.properties'}:
        if s.startswith('#'):
            return True
        if '#' in line:
            parts = line.split('#')
            prefix = parts[0]
            if prefix.count('"') % 2 == 0 and prefix.count("'") % 2 == 0 and prefix.strip():
                return True
    elif ext in {'.xml', '.html', '.svg'}:
        if '<!--' in s:
            return True
    elif ext in {'.bat', '.cmd'}:
        if s.startswith('::') or s.startswith('REM ') or s == 'REM':
            return True
    return False

def scan_directory(target_dir):
    violations = []
    for root, dirs, files in os.walk(target_dir):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext not in EXTENSIONS:
                continue
            path = os.path.join(root, f)
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as fp:
                    for idx, line in enumerate(fp, 1):
                        if is_line_comment(line, ext):
                            violations.append((path, idx, line.strip()))
            except Exception as e:
                pass
    return violations

def main():
    parser = argparse.ArgumentParser(description='Scan repository for comments.')
    parser.add_argument('--dir', default='.', help='Target directory to scan')
    args = parser.parse_args()

    violations = scan_directory(args.dir)
    if violations:
        print(f'VIOLATIONS: Found {len(violations)} comment(s):')
        for path, line_no, content in violations:
            print(f'  {path}:{line_no}: {content[:80]}')
        sys.exit(1)
    else:
        print('CLEAN: Zero comments found across codebase.')
        sys.exit(0)

if __name__ == '__main__':
    main()
