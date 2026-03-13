#dict - Desktop Media Player and Library Manager v1.34
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: Git / Quality Assurance
# Eingabewerte: Staged files, File sizes
# Ausgabewerte: Warnungen/Fehler bei zu großen Dateien
# Testdateien: Keine
# ERWEITERUNGEN (TODO): [ ] Integration als git pre-commit hook
# KOMMENTAR: Verhindert, dass versehentlich riesige Binärdateien in Git landen.

"""
KATEGORIE: Git / Quality Assurance
ZWECK: Überprüfung der Dateigrößen vor dem Commit, um das 100MB-GitHub-Limit einzuhalten.
EINGABEWERTE: Liste der für den Commit vorgemerkten Dateien.
AUSGABEWERTE: Bericht über zu große Dateien.
VERWENDUNG: python3 scripts/git_guard.py check
"""

import os
import sys
import subprocess
from pathlib import Path

# --- Configuration ---
MAX_FILE_SIZE_MB = 50.0  # Warn threshold
LIMIT_FILE_SIZE_MB = 100.0 # Error threshold (GitHub Limit)

def get_staged_files():
    """Get list of files staged for commit."""
    try:
        output = subprocess.check_output(["git", "diff", "--cached", "--name-only"], text=True)
        return output.splitlines()
    except Exception as e:
        print(f"❌ Fehler beim Abrufen der Git-Dateien: {e}")
        return []

def check_file_sizes(files):
    """Check sizes of given files and report issues."""
    too_big = []
    warnings = []
    
    for f_path in files:
        p = Path(f_path)
        if not p.exists(): continue
        
        size_mb = p.stat().st_size / (1024 * 1024)
        
        if size_mb >= LIMIT_FILE_SIZE_MB:
            too_big.append((f_path, size_mb))
        elif size_mb >= MAX_FILE_SIZE_MB:
            warnings.append((f_path, size_mb))
            
    return too_big, warnings

def main():
    print("🛡️ Git Guard: Prüfe Dateigrößen...")
    staged = get_staged_files()
    
    if not staged:
        print("✅ Keine Dateien zum Prüfen vorgemerkt.")
        return

    too_big, warnings = check_file_sizes(staged)
    
    if warnings:
        print("\n⚠️  WARNHINWEIS (Große Dateien):")
        for f, s in warnings:
            print(f"  - {f}: {s:.2f} MB")
            
    if too_big:
        print("\n❌ FEHLER: Dateien überschreiten das GitHub-Limit (100MB):")
        for f, s in too_big:
            print(f"  - {f}: {s:.2f} MB")
        print("\n🛑 Commit wird blockiert. Bitte entferne diese Dateien oder nutze Git LFS.")
        sys.exit(1)
    
    if not warnings and not too_big:
        print(f"✅ Alle {len(staged)} Dateien sind innerhalb der Limits.")

if __name__ == "__main__":
    main()
