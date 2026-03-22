# Parser Capabilities & Settings Exposure

**Datum:** 12. März 2026

---

## Ziel
Standardisierte Architektur für Metadaten-Parser: Jeder Parser meldet seine Fähigkeiten (unterstützte Tags, Codecs) und stellt seine Konfiguration (CLI-Flags, Funktionsoptionen) im UI bereit.

---

### Architekturänderungen
- **parsers/format_utils.py:**
  - PARSER_CONFIG erweitert um parser_settings für granulare Konfiguration.
- **parsers/media_parser.py:**
  - Neue Funktion `get_parser_info()` aggregiert Fähigkeiten.
  - Parser-Loop übergibt spezifische Einstellungen an jedes Modul.
- **Alle Parser-Module (mutagen_parser.py, mkvmerge_parser.py, ...):**
  - `get_capabilities()`: Gibt unterstützte Tags und Codecs zurück.
  - `get_settings_schema()`: Gibt konfigurierbare Einstellungen (z.B. CLI-Flags) zurück.
  - `parse(..., settings=None)`: Unterstützt dynamische Settings.

---

### Web Interface
- **web/app.html:**
  - "Parser"-Tab erhält einen detaillierten "Parser Settings"-Abschnitt.
  - Interaktiver Capability-Viewer für jeden Parser.
  - Felder für benutzerdefinierte CLI-Flags.

---

### Verifikation
- **Automatisierte Tests:**
  - `pytest tests/test_parser_capabilities.py`: Prüft, ob alle Parser ihre Fähigkeiten korrekt melden.
  - `pytest tests/test_parser_settings.py`: Prüft, ob Settings in PARSER_CONFIG die Extraktion beeinflussen.
- **Manuelle Verifikation:**
  - "Parser"-Tab öffnen, Capability- und Settings-Ansicht prüfen.
  - CLI-Flag für mkvmerge ändern, Effekt im Log prüfen.
  - MP3-Titel im App editieren, "Save to File" klicken, Tags extern prüfen (exiftool/VLC).
  - Wiederholen für FLAC und MKV.

---

*Entry created: 12. März 2026*
