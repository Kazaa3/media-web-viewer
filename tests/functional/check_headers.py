#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: Development Tool
# Eingabewerte: tests/ Verzeichnis oder spezifische Datei
# Ausgabewerte: Compliance-Report, Exit-Code (0=OK, 1=Fehler)
# Testdateien: Keine
# ERWEITERUNGEN (TODO): [ ] Integration als Pre-Commit Hook, [ ] Unterstützung für verschiedene Datei-Typen (.sh)
# KOMMENTAR: Validiert die Einhaltung des Test-Header-Standards.
# VERWENDUNG: python3 scripts/check_test_headers.py [pfad]

"""
KATEGORIE: Development Tool
ZWECK: Validiert die Einhaltung des Test-Header-Standards in allen Testdateien.
EINGABEWERTE: tests/ Verzeichnis oder spezifische Datei
AUSGABEWERTE: Compliance-Report, Exit-Code (0=OK, 1=Fehler)
TESTDATEIEN: Keine
ERWEITERUNGEN (TODO): [ ] Integration als Pre-Commit Hook, [ ] Unterstützung für verschiedene Datei-Typen (.sh)
KOMMENTAR: Validiert die Einhaltung des Test-Header-Standards.
VERWENDUNG: python3 scripts/check_test_headers.py [pfad]
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
    
    # Check if a specific path was provided as an argument
    if len(sys.argv) > 1:
        search_path = Path(sys.argv[1])
        if not search_path.is_absolute():
            search_path = (Path(os.getcwd()) / search_path).resolve()
    else:
        search_path = (project_root / "tests").resolve()
    
    if not search_path.exists():
        print(f"❌ Verzeichnis oder Datei nicht gefunden: {search_path}")
        sys.exit(1)
        
    print(f"🔍 Validiere Test-Header in {search_path}...")
    print("=" * 60)
    
    files_checked = 0
    files_failed = 0
    failures = []
    
    # Decide whether to check a single file or a directory
    if search_path.is_file():
        files_to_check = [search_path]
    else:
        files_to_check = list(search_path.rglob("*.py"))
    
    for file_path in files_to_check:
        if "__pycache__" in str(file_path):
            continue
        
        files_checked += 1
        success, msg = check_file(file_path)
        if not success:
            files_failed += 1
            try:
                rel_path = file_path.relative_to(project_root)
            except ValueError:
                rel_path = file_path
            print(f"❌ {rel_path}: {msg}")
            failures.append(file_path)
        elif search_path.is_file():
            print(f"✅ {file_path.name}: OK")
            
    print("=" * 60)
    print(f"📊 Abschlussbericht:")
    print(f"   Dateien geprüft: {files_checked}")
    print(f"   Dateien korrekt: {files_checked - files_failed}")
    print(f"   Dateien fehlerhaft: {files_failed}")

    if files_failed > 0:
        print("\n⚠️  Bitte korrigiere die Header in den oben genannten Dateien.")
        print("   Standard-Template siehe docs/STYLE_GUIDE.md")
        sys.exit(1)
    else:
        print("\n✨ Alle geprüften Dateien entsprechen dem Standard.")
        sys.exit(0)

if __name__ == "__main__":
    main()
