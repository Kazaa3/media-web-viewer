#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: Requirements Completeness Test
# Eingabewerte: src/**/*.py, requirements*.txt
# Ausgabewerte: Dependency Report
# Testdateien: src/**/*.py, requirements*.txt
# Kommentar: Checks if all imports in the source code are covered by requirements files.

import os
import re
import sys
from pathlib import Path

def test_requirements():
    print("\n🧪 Test: Requirements Completeness Scan")
    
    project_root = Path(__file__).parent.parent
    src_dir = project_root / "src"
    req_files = list(project_root.glob("requirements*.txt"))
    
    if not req_files:
        print("⚠️  No requirements.txt found.")
        return False

    all_reqs = set()
    
    def parse_req_file(file_path):
        if not file_path.exists():
            return
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if line.startswith('-r '):
                    sub_rel_path = line[3:].strip()
                    sub_file = file_path.parent / sub_rel_path
                    parse_req_file(sub_file)
                    continue
                # Match package name before any version specifiers (==, >=, <=, >, <)
                match = re.match(r'^([a-zA-Z0-9_\-]+)', line)
                if match:
                    pkg = match.group(1).lower().replace('-', '_')
                    all_reqs.add(pkg)

    for rf in req_files:
        parse_req_file(rf)

    print(f"   ├─ Found {len(all_reqs)} dependencies in {len(req_files)} requirements files.")

    # Standard library modules to ignore
    stdlib = {
        'os', 'sys', 'pathlib', 're', 'json', 'time', 'subprocess', 'shutil', 
        'logging', 'threading', 'socket', 'platform', 'urllib', 'mimetypes', 
        'uuid', 'traceback', 'datetime', 'hashlib', 'base64', 'glob', 'tempfile',
        'argparse', 'typing', 'collections', 'importlib', 'math', 'random', 'itertools',
        'base64', 'inspect', 'signal', 'atexit', '__future__', 'abc', 'copy',
        'multiprocessing', 'queue', 'sqlite3', 'tkinter', 'webbrowser', 'pkg_resources'
    }

    used_imports = set()
    for py_file in src_dir.rglob("*.py"):
        with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            # find 'import x' or 'from x import ...'
            imports = re.findall(r'^\s*import\s+([a-zA-Z0-9_]+)', content, re.MULTILINE)
            from_imports = re.findall(r'^\s*from\s+([a-zA-Z0-9_]+)', content, re.MULTILINE)
            used_imports.update(imports)
            used_imports.update(from_imports)

    # Filter project internal imports
    project_dirs = {d.name for d in src_dir.iterdir() if d.is_dir()}
    project_dirs.add('src')
    # Adding known project submodules that might be imported relatively or as roots
    project_dirs.update({'db', 'logger', 'web', 'env_handler', 'parser', 'parsers', 'models', 'core'})
    
    external_imports = used_imports - stdlib - project_dirs - {''}
    
    missing_reqs = []
    for imp in external_imports:
        if imp.lower() not in all_reqs:
            missing_reqs.append(imp)

    if missing_reqs:
        print(f"      ⚠️  Potential missing dependencies in requirements.txt: {sorted(missing_reqs)}")
    else:
        print("      ✅ All external imports seem to be covered by requirements.txt.")

    print("\n✅ Requirements Completeness Scan complete.")
    return True

if __name__ == "__main__":
    if test_requirements():
        sys.exit(0)
    else:
        sys.exit(1)
