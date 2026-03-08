# Kategorie: Integration Test (Dokumentation)
# Eingabewerte: Doxyfile, Source Code (.py)
# Ausgabewerte: Doxygen-Exit-Code (0), Warnungen/Fehler
# Testdateien: Doxyfile, main.py, db.py, parsers/*.py
# Kommentar: Prüft ob die Doxygen-Dokumentation ohne kritische Fehler generiert werden kann.

import os
import subprocess
import shutil
from pathlib import Path
import pytest

def test_doxygen_installed():
    """Prüft ob Doxygen auf dem System installiert ist."""
    try:
        subprocess.run(["doxygen", "-v"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        pytest.fail("Doxygen ist nicht installiert oder nicht im PATH erreichbar.")

def test_doxygen_generation():
    """Prüft ob Doxygen die Dokumentation erfolgreich generieren kann."""
    root_dir = Path(__file__).parent.parent
    doxyfile = root_dir / "Doxyfile"
    
    if not doxyfile.exists():
        pytest.fail("Doxyfile wurde im Root-Verzeichnis nicht gefunden.")
    
    # Doxygen ausführen
    result = subprocess.run(
        ["doxygen", str(doxyfile)],
        cwd=str(root_dir),
        capture_output=True,
        text=True
    )
    
    # Exit-Code prüfen (0 ist Erfolg)
    assert result.returncode == 0, f"Doxygen fehlgeschlagen mit Exit-Code {result.returncode}. Output: {result.stderr}"
    
    # Prüfen ob Warnings vorhanden sind (optional, aber gut für Qualität)
    # warnings = [line for line in result.stderr.split('\n') if 'warning:' in line.lower()]
    # assert not warnings, f"Doxygen hat Warnungen generiert: {warnings}"

def test_doxygen_output_exists():
    """Prüft ob das docs/ Verzeichnis nach der Generierung existiert."""
    root_dir = Path(__file__).parent.parent
    docs_dir = root_dir / "docs"
    
    assert docs_dir.exists(), "Doxygen hat kein 'docs/' Verzeichnis erstellt."
    assert (docs_dir / "html").exists(), "Doxygen hat kein 'html/' Unterverzeichnis erstellt."
    assert (docs_dir / "html" / "index.html").exists(), "Doxygen hat kein 'index.html' generiert."
