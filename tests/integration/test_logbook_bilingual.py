# Kategorie: Logbuch Bilingual Test
# Eingabewerte: Markdown-Dateien mit Sprach-Kommentaren
# Ausgabewerte: Korrekte Extraktion von title_de, title_en, summary_de, summary_en
# Testdateien: Temporäre .md Dateien in /logbuch
# Kommentar: Verifiziert, dass die Metadaten-Extraktion für DE und EN korrekt funktioniert.

import sys
import os
from pathlib import Path

# Pfad zum Projekt-Root hinzufügen

from src.core.main import list_logbook_entries

def test_bilingual_metadata_extraction():
    log_dir = Path(__file__).parents[3] / "logbuch"
    test_file = log_dir / "test_pytest_bilingual.md"

    # Test-Datei erstellen
    content = """<!-- Title_DE: Deutsch Titel -->
<!-- Title_EN: English Title -->
<!-- Summary_DE: Deutsch Zusammenfassung -->
<!-- Summary_EN: English Summary -->
<!-- Category: Tests -->
<!-- Status: ACTIVE -->

# Standard Title
Inhalt hier.
"""

    try:
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(content)

        entries = list_logbook_entries()

        # Den spezifischen Eintrag suchen
        entry = next((e for e in entries if e['name'] == "test_pytest_bilingual"), None)

        assert entry is not None, "Test entry should be found"
        assert entry['title_de'] == "Deutsch Titel"
        assert entry['title_en'] == "English Title"
        assert entry['summary_de'] == "Deutsch Zusammenfassung"
        assert entry['summary_en'] == "English Summary"
        assert entry['title'] == "Standard Title"
        assert entry['status'] == "ACTIVE"
        assert entry['category'] == "Tests"

        print("✅ Bilingual metadata extraction test passed!")

    finally:
        # Aufräumen
        if test_file.exists():
            test_file.unlink()

if __name__ == "__main__":
    test_bilingual_metadata_extraction()
