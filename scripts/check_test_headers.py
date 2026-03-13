#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
KATEGORIE: Development Tool
ZWECK: Validiert die Einhaltung des Test-Header-Standards in allen Testdateien.
EINGABEWERTE: tests/ Verzeichnis
AUSGABEWERTE: Compliance-Report, Exit-Code (0=OK, 1=Fehler)
TESTDATEIEN: Keine
ERWEITERUNGEN (TODO):
- [ ] Integration als Pre-Commit Hook
- [ ] Unterstützung für verschiedene Datei-Typen (.sh)
VERWENDUNG: python3 scripts/check_test_headers.py
"""

import os
import sys
import re
from pathlib import Path

# Required fields in the header comments (#)
REQUIRED_COMMENT_FIELDS = [
    "# Kategorie:",
    "# Eingabewerte:",
    "# Ausgabewerte:",
    "# Testdateien:",
    "# ERWEITERUNGEN (TODO):",
    "# KOMMENTAR:",
    "# VERWENDUNG:"
]

# Required fields in the header docstring (""")
REQUIRED_DOCSTRING_FIELDS = [
    "KATEGORIE:",
    "ZWECK:",
    "EINGABEWERTE:",
    "AUSGABEWERTE:",
    "TESTDATEIEN:",
    "ERWEITERUNGEN (TODO):",
    "VERWENDUNG:"
]

def check_file(file_path):
    """Checks a single file for the required dual-header."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 1. Check for # comments (System Parsable)
        missing_comments = []
        for field in REQUIRED_COMMENT_FIELDS:
            if field not in content:
                missing_comments.append(field)
        
        # 2. Check for the first docstring (Human Readable)
        match = re.search(r'"""(.*?)"""', content, re.DOTALL)
        if not match:
            match = re.search(r"'''(.*?)'''", content, re.DOTALL)
            
        if not match:
            return False, "Fehlender Docstring-Header"
        
        header_text = match.group(1).upper()
        missing_doc = []
        for field in REQUIRED_DOCSTRING_FIELDS:
            # Check for field name
            clean_field = field.replace(':', '').upper()
            if clean_field not in header_text:
                missing_doc.append(field)
            # Check for underline (at least 3 dashes) - optional but encouraged
            # if "---" not in header_text:
            #     missing_doc.append(f"{field} (Underline missing)")

        if missing_comments or missing_doc:
            msg = ""
            if missing_comments:
                msg += f"Fehlende # Felder: {', '.join(missing_comments)}. "
            if missing_doc:
                msg += f"Fehlende Docstring-Felder: {', '.join(missing_doc)}"
            return False, msg.strip()
        
        return True, "OK"
    except Exception as e:
        return False, f"Fehler beim Lesen: {e}"

def main():
    project_root = Path(__file__).parent.parent
    tests_dir = project_root / "tests"
    
    if not tests_dir.exists():
        print(f"❌ Verzeichnis nicht gefunden: {tests_dir}")
        sys.exit(1)
        
    print(f"🔍 Validiere Test-Header in {tests_dir}...")
    print("=" * 60)
    
    files_checked = 0
    files_failed = 0
    failures = []
    
    for root, _, files in os.walk(tests_dir):
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                file_path = Path(root) / file
                rel_path = file_path.relative_to(project_root)
                files_checked += 1
                
                is_ok, message = check_file(file_path)
                if not is_ok:
                    files_failed += 1
                    failures.append((rel_path, message))
                    print(f"❌ {rel_path}: {message}")
                else:
                    # Optional: verbose output
                    # print(f"✅ {rel_path}")
                    pass
                    
    print("=" * 60)
    print(f"📊 Abschlussbericht:")
    print(f"   Dateien geprüft: {files_checked}")
    print(f"   Dateien korrekt: {files_checked - files_failed}")
    print(f"   Dateien fehlerhaft: {files_failed}")
    
    if files_failed > 0:
        print("\n⚠️  Bitte korrigiere die Header in den oben genannten Dateien.")
        print(f"   Standard-Template siehe docs/STYLE_GUIDE.md#6-test-script-header-standard")
        sys.exit(1)
    else:
        print("\n✅ Alle Test-Header entsprechen dem Standard.")
        sys.exit(0)

if __name__ == "__main__":
    main()
