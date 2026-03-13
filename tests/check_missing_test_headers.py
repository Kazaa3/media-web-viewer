# Test Header/Docstring Audit

This script checks for missing standardized headers and Google-style bilingual docstrings in test files listed in the GUI overview.

## Usage
Run this script from the project root:

```bash
python tests/check_missing_test_headers.py
```

## What it does
- Scans the listed test files for header/docstring patterns.
- Prints a list of files missing documentation.

---

import os
import re

# List of test files from GUI overview (add full paths as needed)
test_files = [
    "tests/test_abase.py",
    "tests/test_bplayer.py",
    "tests/test_debug_and_db.py",
    "tests/test_library.py",
    "tests/test_modals.py",
    "tests/test_options.py",
    "tests/test_playlist.py",
    "tests/test_teststab.py",
    "tests/test_videoplayer.py",
    # Add more as needed...
]

HEADER_PATTERN = re.compile(r"# Kategorie:|\"\"\".*DE:.*EN:", re.DOTALL)

def check_header(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read(2048)  # Only read the first 2KB
            return bool(HEADER_PATTERN.search(content))
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return False

def main():
    missing = []
    for file in test_files:
        if not check_header(file):
            missing.append(file)
    if missing:
        print("Tests missing standardized header/docstring:")
        for file in missing:
            print(f" - {file}")
    else:
        print("All listed tests have standardized headers.")

if __name__ == "__main__":
    main()
