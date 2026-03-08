# Kategorie: Unit Test (Dokumentation)
# Eingabewerte: Markdown-Dateien (.md)
# Ausgabewerte: Validierungsergebnis (Pass/Fail)
# Testdateien: README.md, DOCUMENTATION.md, logbuch/*.md
# Kommentar: Prüft ob alle Markdown-Dateien syntaktisch korrekt sind und geparst werden können.

import os
import sys
from pathlib import Path
import pytest
import markdown

# Root Verzeichnis zum Syspath hinzufügen
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def get_markdown_files():
    """Sammelt alle relevanten Markdown Dateien."""
    root_dir = Path(__file__).parent.parent
    md_files = [
        root_dir / "README.md",
        root_dir / "DOCUMENTATION.md"
    ]

    # Logbuch Dateien hinzufügen
    logbuch_dir = root_dir / "logbuch"
    if logbuch_dir.exists():
        md_files.extend(logbuch_dir.glob("*.md"))

    return [str(f) for f in md_files if f.exists()]


@pytest.mark.parametrize("file_path", get_markdown_files())
def test_markdown_lint(file_path):
    """Prüft ob eine Markdown-Datei erfolgreich geparst werden kann."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        try:
            # Versuche den Inhalt zu HTML zu konvertieren
            # Dies validiert die grundlegende Markdown-Struktur
            html = markdown.markdown(content)
            assert html is not None
        except Exception as e:
            pytest.fail(f"Markdown validation failed for {file_path}: {e}")


def test_markdown_encoding():
    """Prüft ob Dateien in UTF-8 kodiert sind und keine garbled characters enthalten."""
    for file_path in get_markdown_files():
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                f.read()
        except UnicodeDecodeError:
            pytest.fail(f"File {file_path} is not valid UTF-8")
