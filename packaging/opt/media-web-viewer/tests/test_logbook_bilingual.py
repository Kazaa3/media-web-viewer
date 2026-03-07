# Kategorie: Logbuch Bilingual Test
# Eingabewerte: Markdown-Dateien mit Sprach-Kommentaren
# Ausgabewerte: Korrekte Extraktion von title_de, title_en, summary_de, summary_en
# Testdateien: Temporäre .md Dateien in /logbuch
# Kommentar: Verifiziert, dass die Metadaten-Extraktion für DE und EN korrekt funktioniert.

import sys, os
from pathlib import Path
import shutil

# Pfad zum Projekt-Root hinzufügen
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import list_logbook_entries

def test_bilingual_metadata_extraction():
    log_dir = Path(__file__).parent.parent / "logbuch"
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
