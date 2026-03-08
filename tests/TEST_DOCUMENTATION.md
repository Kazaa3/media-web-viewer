# Test Suite Documentation - Media Web Viewer

**Datum:** 8. März 2026  
**Version:** 1.3.1  
**Gesamt-Tests:** 53 Test-Dateien  
**Status:** ✅ Kern-Tests bestanden (27/27)

---

## 📊 Test-Übersicht

### Nach Größe

| Kategorie | Anzahl | Beschreibung |
|-----------|--------|--------------|
| **SMALL** (< 30 Zeilen) | 7 | Minimale Quick-Tests, sollten erweitert werden |
| **MEDIUM** (30-99 Zeilen) | 27 | Solide Unit-Tests mit Assertions |
| **LARGE** (100+ Zeilen) | 19 | Umfassende Test-Suites mit mehreren Testfällen |

### Nach Status

| Status | Anzahl | Tests |
|--------|--------|-------|
| ✅ **PASSED** | 27 | Kern-Funktionalität validiert |
| ⚠️ **MINIMAL** | 7 | Benötigen Erweiterung |
| 📝 **TODO** | 19 | Sollten regelmäßig ausgeführt werden |

---

## 🎯 Kern-Test-Suites (KRITISCH)

### 1. test_i18n_completeness.py ✅
**Größe:** 476 Zeilen  
**Status:** 9/9 Tests bestanden  
**Zweck:** Validiert vollständige Internationalisierung

**Tests:**
- ✅ JSON-Struktur & Syntax
- ✅ Key-Parität (314 DE/EN Keys)
- ✅ Required Keys vorhanden
- ✅ Keine hardcoded Strings
- ✅ Keine veralteten i18n() Aufrufe
- ✅ @eel.expose Dekoratoren
- ✅ data-i18n Attribute (137 validiert)
- ✅ t() Funktionsaufrufe (113 validiert)
- ✅ Alle loading/error Keys verwendet

**Dokumentation:**
```python
# Eingabewerte: web/i18n.json, web/app.html
# Ausgabewerte: Pass/Fail Status für jeden Test
# Testdateien: web/i18n.json, web/app.html
# Kommentar: Kern-Test für i18n-Integrität
```

---

### 2. test_i18n_deep_scan.py ✅
**Größe:** 834 Zeilen  
**Status:** 8/8 Tests bestanden  
**Zweck:** Deep Scan für nicht-internationalisierte Texte

**Tests:**
- ✅ HTML Static Text Elements
- ✅ alert()/confirm() Texte
- ✅ innerHTML/innerText Assignments
- ✅ JavaScript String Literals
- ✅ Button/Label Hardcoded Text
- ✅ placeholder/title Attribute
- ✅ Type Cardinality (102/102)
- ✅ console.log Messages

**Dokumentation:**
```python
# Eingabewerte: web/app.html (vollständiger Scan)
# Ausgabewerte: Cardinality-Matrix, gefundene Hardcoded Strings
# Testdateien: web/app.html
# Kommentar: Findet ALLE nicht-internationalisierten Texte
```

---

### 3. test_ui_events.py ✅
**Größe:** 934 Zeilen  
**Status:** 10/10 Tests bestanden  
**Zweck:** Validiert UI-Interaktivität

**Tests:**
- ✅ Button Click-Handler (45 validiert)
- ✅ Input Change-Handler (11 validiert)
- ✅ Event Handler Statistics
- ✅ Critical Buttons vorhanden
- ✅ Link Click-Handler
- ✅ Select Dropdowns
- ✅ Keyboard Shortcuts
- ✅ Eel Backend Functions (53 Aufrufe)
- ✅ Modal Open/Close Handler
- ✅ Form Validation

**Dokumentation:**
```python
# Eingabewerte: web/app.html (Event-Handler-Analyse)
# Ausgabewerte: Liste aller Event-Handler, fehlende Handler
# Testdateien: web/app.html
# Kommentar: Stellt sicher, dass ALLE UI-Elemente funktional sind
```

---

## 📁 Vollständige Test-Liste

### A. Internationalisierung (3 Tests)

#### test_i18n_completeness.py ✅
- **Kategorie:** i18n Basis-Validierung
- **Zeilen:** 476
- **Status:** 9/9 PASSED
- **Eingaben:** web/i18n.json, web/app.html
- **Ausgaben:** Key-Parität, Attribute-Validierung
- **Beschreibung:** Validiert i18n-Infrastruktur: JSON-Struktur, Key-Parität (314 DE/EN), data-i18n Attribute

#### test_i18n_deep_scan.py ✅
- **Kategorie:** i18n Deep Scan
- **Zeilen:** 834
- **Status:** 8/8 PASSED
- **Eingaben:** web/app.html (vollständiger Code-Scan)
- **Ausgaben:** Cardinality 102/102, keine Hardcoded Strings
- **Beschreibung:** Findet ALLE nicht-internationalisierten Texte mit Regex-Analyse

#### test_ui_events.py ✅
- **Kategorie:** UI Events & Interaktionen
- **Zeilen:** 934
- **Status:** 10/10 PASSED
- **Eingaben:** web/app.html (Event-Handler)
- **Ausgaben:** 45 Buttons, 53 Backend-Calls validiert
- **Beschreibung:** Validiert vollständige UI-Interaktivität

---

### B. Umgebungs-Management (7 Tests)

#### test_environment_dependencies.py 📝
- **Kategorie:** Dependency Check
- **Zeilen:** 375
- **Eingaben:** requirements.txt, sys.modules
- **Ausgaben:** Installierte vs. benötigte Pakete
- **Beschreibung:** Prüft ob alle Dependencies installiert sind (eel, mutagen, pymediainfo, etc.)

#### test_environment_info.py 📝
- **Kategorie:** Environment Information
- **Zeilen:** 426
- **Eingaben:** sys.executable, conda list, pip list
- **Ausgaben:** Python-Version, Umgebungstyp, installierte Pakete
- **Beschreibung:** Sammelt umfassende Umgebungsinformationen

#### test_environment_isolation.py ⚠️
- **Kategorie:** Environment Isolation Test
- **Zeilen:** 66
- **Eingaben:** sys.path, os.environ
- **Ausgaben:** Konflikte zwischen Umgebungen
- **Beschreibung:** Stellt sicher, dass Conda/venv korrekt isoliert sind

#### test_environment_cleanup.py 📝
- **Kategorie:** Database Cleanup
- **Zeilen:** 128
- **Eingaben:** environment.db
- **Ausgaben:** Aufräum-Status
- **Beschreibung:** Testet Cleanup-Logik für environment.db

#### test_python_environments.py 📝
- **Kategorie:** Python Environment Detection
- **Zeilen:** 559
- **Eingaben:** Conda-Installation, System Python
- **Ausgaben:** Liste aller Python-Umgebungen
- **Beschreibung:** Erkennt alle verfügbaren Python-Umgebungen

#### test_python_version.py ⚠️
- **Kategorie:** Python Version Check
- **Zeilen:** 116
- **Eingaben:** sys.version_info
- **Ausgaben:** Python 3.8+ erforderlich
- **Beschreibung:** Validiert Python-Version >= 3.8

#### test_conda_integration.py 📝
- **Kategorie:** Conda Integration Test
- **Zeilen:** (TODO)
- **Status:** Noch nicht implementiert
- **Beschreibung:** Testet Conda-spezifische Funktionalität

---

### C. Parser & Media-Verarbeitung (10 Tests)

#### test_parse.py ⚠️
- **Kategorie:** Parser Integration
- **Zeilen:** 89
- **Eingaben:** media/*.m4b, media/*.opus
- **Ausgaben:** Parsing-Ergebnisse (Titel, Artist, Duration)
- **Beschreibung:** Testet Haupt-Parser-Funktionen

#### test_parse2.py ⚠️
- **Kategorie:** Extended Parser Test
- **Zeilen:** 24 (SMALL)
- **Eingaben:** Verschiedene Audio-Formate
- **Ausgaben:** Format-spezifische Metadaten
- **Beschreibung:** Minimaler Parser-Test, sollte erweitert werden

#### test_parser_logic.py ⚠️
- **Kategorie:** Parser Logic Unit Test
- **Zeilen:** 29 (SMALL)
- **Eingaben:** Mock-Daten
- **Ausgaben:** Parser-Logik-Validierung
- **Beschreibung:** Unit-Tests für Parser-Helfer-Funktionen

#### test_parser_modes.py ⚠️
- **Kategorie:** Parser Mode Selection
- **Zeilen:** 42
- **Eingaben:** Verschiedene Dateitypen
- **Ausgaben:** Korrekter Parser für jeden Typ
- **Beschreibung:** Testet automatische Parser-Auswahl

#### test_mkv.py ⚠️
- **Kategorie:** Format Test (MKV)
- **Zeilen:** 24 (SMALL)
- **Eingaben:** FFmpeg Output
- **Ausgaben:** Bitrate-Extraktion
- **Beschreibung:** Testet MKV-Container-Parsing (Quick-Test, sollte erweitert werden)

#### test_mp3_tags.py ⚠️
- **Kategorie:** Metadata Extraction (Mutagen)
- **Zeilen:** 20 (SMALL)
- **Eingaben:** media/sample.mp3
- **Ausgaben:** ID3v2 Tags (TPE1, TDRC)
- **Beschreibung:** Mutagen-Library-Test (minimal, sollte erweitert werden)

#### test_pcm.py ⚠️
- **Kategorie:** Audio Bit-Depth Test
- **Zeilen:** 22 (SMALL)
- **Eingaben:** media/*.wav (16-bit, 24-bit)
- **Ausgaben:** Korrekte Bit-Depth Metadaten
- **Beschreibung:** FFmpeg PCM-Audio-Test (minimal)

#### test_bitdepth.py ⚠️
- **Kategorie:** Bit-Depth Detection
- **Zeilen:** 28 (SMALL)
- **Eingaben:** WAV/FLAC-Dateien
- **Ausgaben:** Bit-Depth (16/24/32 Bit)
- **Beschreibung:** Prüft Bit-Tiefe-Erkennung (schneller Test)

#### test_stream.py ⚠️
- **Kategorie:** FFprobe Duration Extraction
- **Zeilen:** 18 (SMALL)
- **Eingaben:** media/sample.alac
- **Ausgaben:** Dauer in Sekunden
- **Beschreibung:** FFprobe-Funktionstest (minimal, sollte robuster sein)

#### test_chapters_logic.py ⚠️
- **Kategorie:** Chapter Parsing
- **Zeilen:** 48
- **Eingaben:** M4B-Dateien mit Kapiteln
- **Ausgaben:** Chapter-Liste
- **Beschreibung:** Testet Chapter-Extraktion aus Audiobooks

---

### D. Datenbank & Logik (5 Tests)

#### test_db_logic.py ⚠️
- **Kategorie:** Database Logic
- **Zeilen:** 72
- **Eingaben:** SQLite DB-Operationen
- **Ausgaben:** CRUD-Test-Resultate
- **Beschreibung:** Testet Datenbank-CRUD-Operationen

#### test_media_item_logic.py ⚠️
- **Kategorie:** MediaItem Class Logic
- **Zeilen:** 53
- **Eingaben:** Mock MediaItem-Objekte
- **Ausgaben:** Property-Validierung
- **Beschreibung:** Unit-Tests für MediaItem-Klasse

#### test_types_logic.py ⚠️
- **Kategorie:** UI / Types Test
- **Zeilen:** 76
- **Eingaben:** Dateinamen, Pfade
- **Ausgaben:** Kategorien (Hörbuch, Film, etc.)
- **Beschreibung:** Testet automatische Typ-Erkennung

#### test_media_type_consistency.py ⚠️
- **Kategorie:** Type Consistency Check
- **Zeilen:** 63
- **Eingaben:** Media-Library
- **Ausgaben:** Type-Mapping-Validierung
- **Beschreibung:** Stellt sicher, dass Typ-Zuordnung konsistent ist

#### test_separated_fields.py ⚠️
- **Kategorie:** Field Separation Logic
- **Zeilen:** 83
- **Eingaben:** Kombinierte Felder (Artist/Album)
- **Ausgaben:** Getrennte Felder
- **Beschreibung:** Testet Feld-Parsing-Logik

---

### E. UI & Integration (6 Tests)

#### test_ui_integrity.py ✅
- **Kategorie:** UI Structure Validation
- **Zeilen:** 95
- **Status:** 6/6 PASSED
- **Eingaben:** web/app.html
- **Ausgaben:** Tag-Balance, Tab-IDs, tabMap
- **Beschreibung:** Validiert HTML-Struktur und JS-Konfiguration

#### test_backend_connection.py ⚠️
- **Kategorie:** Backend Ping Test
- **Zeilen:** 33
- **Eingaben:** Mock Eel-Backend
- **Ausgaben:** Ping-Response
- **Beschreibung:** Testet Backend-Erreichbarkeit

#### test_network.py ⚠️
- **Kategorie:** Network & Server Test
- **Zeilen:** 91
- **Eingaben:** HTTP Server auf localhost
- **Ausgaben:** Server läuft, Ports verfügbar
- **Beschreibung:** Testet Bottle-Server-Funktionalität

#### test_route.py ⚠️
- **Kategorie:** Route Testing
- **Zeilen:** 44
- **Eingaben:** Flask/Bottle-Routes
- **Ausgaben:** Route-Responses
- **Beschreibung:** Testet HTTP-Routen

#### test_route_debug.py ⚠️
- **Kategorie:** Route Debugging
- **Zeilen:** 43
- **Eingaben:** Debug-Routes
- **Ausgaben:** Debug-Informationen
- **Beschreibung:** Erweiterte Route-Debugging-Tests

#### test_route_debug2.py ⚠️
- **Kategorie:** Additional Route Debug
- **Zeilen:** 44
- **Eingaben:** Weitere Debug-Routes
- **Ausgaben:** Erweiterte Debug-Infos
- **Beschreibung:** Zusätzliche Debugging-Validierung

---

### F. Logbuch & Dokumentation (3 Tests)

#### test_logbook_bilingual.py ✅
- **Kategorie:** Logbuch Bilingual Test
- **Zeilen:** 60
- **Status:** PASSED
- **Eingaben:** logbuch/*.md mit Metadaten
- **Ausgaben:** title_de, title_en, summary_de, summary_en
- **Beschreibung:** Testet bilinguale Metadaten-Extraktion

#### test_logbook_parsing.py 📝
- **Kategorie:** Logbook Markdown Parsing
- **Zeilen:** 114
- **Eingaben:** logbuch/*.md
- **Ausgaben:** Parsed Markdown-Struktur
- **Beschreibung:** Validiert Logbuch-Parser-Funktionen

#### test_markdown_validation.py ⚠️
- **Kategorie:** Markdown Validity Check
- **Zeilen:** 34
- **Eingaben:** *.md (Projekt-weit)
- **Ausgaben:** Markdown-Syntax-Fehler
- **Beschreibung:** Prüft Markdown-Dateien auf Syntax-Fehler

---

### G. Browser & Launcher (4 Tests)

#### test_browser_launch.py 📝
- **Kategorie:** Browser Launch Test
- **Zeilen:** 227
- **Eingaben:** Chromium/Firefox-Pfade
- **Ausgaben:** Browser-Start-Status
- **Beschreibung:** Testet automatisches Browser-Launching

#### test_browser_preference.py 📝
- **Kategorie:** Browser Preference Logic
- **Zeilen:** 373
- **Eingaben:** Browser-Konfiguration
- **Ausgaben:** Bevorzugter Browser
- **Beschreibung:** Testet Browser-Auswahl-Logik

#### test_launcher.py 📝
- **Kategorie:** Application Launcher
- **Zeilen:** 454
- **Eingaben:** Kommandozeilen-Args
- **Ausgaben:** Launch-Status
- **Beschreibung:** Testet App-Launch-Logik

#### test_startup_variants.py 📝
- **Kategorie:** Startup Configuration Tests
- **Zeilen:** 307
- **Eingaben:** Verschiedene Startup-Modi
- **Ausgaben:** Startup-Validierung
- **Beschreibung:** Testet verschiedene Startup-Szenarien

---

### H. Build & Deployment (5 Tests)

#### test_build_integrity.py ⚠️
- **Kategorie:** Build Integrity Check
- **Zeilen:** 60
- **Eingaben:** build/-Verzeichnis
- **Ausgaben:** Build-Vollständigkeit
- **Beschreibung:** Validiert Build-Artefakte

#### test_reinstall_deb.py 📝
- **Kategorie:** DEB Package Reinstallation
- **Zeilen:** 330
- **Eingaben:** .deb-Paket
- **Ausgaben:** Installation-Status
- **Beschreibung:** Testet automatische DEB-Neuinstallation

#### test_pipeline.py 📝
- **Kategorie:** CI/CD Pipeline Test
- **Zeilen:** 204
- **Eingaben:** Pipeline-Konfiguration
- **Ausgaben:** Pipeline-Status
- **Beschreibung:** Testet Build-Pipeline

#### test_version_sync.py 📝
- **Kategorie:** Version Synchronization
- **Zeilen:** (zu erstellen)
- **Eingaben:** VERSION, VERSION_SYNC.json
- **Ausgaben:** Alle Versionen synchron
- **Beschreibung:** Stellt sicher, dass Versionsnummern konsistent sind

#### test_doxygen.py ⚠️
- **Kategorie:** Doxygen Documentation
- **Zeilen:** 52
- **Eingaben:** Doxyfile, Quellcode
- **Ausgaben:** Doxygen-Build-Status
- **Beschreibung:** Testet Doxygen-Dokumentationsgenerierung

---

### I. Session & State (3 Tests)

#### test_session_management.py 📝
- **Kategorie:** Session Management
- **Zeilen:** 436
- **Eingaben:** Session-State
- **Ausgaben:** Session-Persistenz
- **Beschreibung:** Testet Session-Handling

#### test_sessionless_mode.py 📝
- **Kategorie:** Sessionless Operation
- **Zeilen:** 128
- **Eingaben:** CLI ohne Session
- **Ausgaben:** Funktioniert ohne Session-DB
- **Beschreibung:** Testet App-Betrieb ohne Session-State

#### test_cli_args.py ⚠️
- **Kategorie:** CLI Argument Parsing
- **Zeilen:** 41
- **Eingaben:** sys.argv
- **Ausgaben:** Parsed CLI-Args
- **Beschreibung:** Testet Kommandozeilen-Argument-Parsing

---

### J. Debugging & Development (5 Tests)

#### test_debug_flags.py ⚠️
- **Kategorie:** Debug Flag Tests
- **Zeilen:** 36
- **Eingaben:** --debug, --verbose Flags
- **Ausgaben:** Debug-Output
- **Beschreibung:** Testet Debug-Modi

#### test_all_debug_flags.py ⚠️
- **Kategorie:** All Debug Flags
- **Zeilen:** 73
- **Eingaben:** Alle Debug-Flags
- **Ausgaben:** Umfassender Debug-Output
- **Beschreibung:** Testet alle Debug-Kombinationen

#### test_logging.py ⚠️
- **Kategorie:** Logging System Test
- **Zeilen:** 80
- **Eingaben:** logger.py
- **Ausgaben:** Log-Messages
- **Beschreibung:** Validiert Logging-Funktionalität

#### test_linting.py ⚠️
- **Kategorie:** Code Linting
- **Zeilen:** 63
- **Eingaben:** Python-Quellcode
- **Ausgaben:** Linting-Fehler
- **Beschreibung:** Führt pylint/flake8 über Code aus

#### test_pyautogui_integration.py ⚠️
- **Kategorie:** PyAutoGUI Integration
- **Zeilen:** 50
- **Eingaben:** UI-Automation-Skripte
- **Ausgaben:** Automation-Status
- **Beschreibung:** Testet automatisierte UI-Tests

---

### K. Sortierung & Spezial-Features (2 Tests)

#### test_sorting_advanced.py ⚠️
- **Kategorie:** Natural Sorting
- **Zeilen:** 43
- **Eingaben:** Dateinamen mit Nummern
- **Ausgaben:** Korrekt sortierte Liste
- **Beschreibung:** Testet Natural Sorting-Algorithmus

#### test_vlc_integration.py 📝
- **Kategorie:** VLC Integration
- **Zeilen:** (zu prüfen)
- **Eingaben:** VLC-Playlisten (m3u8)
- **Ausgaben:** Import/Export-Status
- **Beschreibung:** Testet VLC-Playlist-Integration

---

## 💡 Empfehlungen

### 🔴 Priorität 1: Kleine Tests erweitern

Diese 7 Tests sind zu minimal und sollten zu vollständigen Unit-Tests erweitert werden:

1. **test_stream.py** (18 Zeilen)
   - Füge pytest-Struktur hinzu
   - Teste verschiedene Audio-Formate
   - Teste Fehlerbehandlung (missing files)
   - Füge Assertions hinzu

2. **test_mp3_tags.py** (20 Zeilen)
   - Teste alle ID3-Tag-Typen
   - Teste fehlende Tags
   - Teste beschädigte Dateien
   - Verwende pytest fixtures

3. **test_pcm.py** (22 Zeilen)
   - Teste mehr Bit-Depths (8/16/24/32)
   - Teste verschiedene Sample-Rates
   - Teste Mono/Stereo
   - Füge Edge-Cases hinzu

4. **test_mkv.py** (24 Zeilen)
   - Teste verschiedene MKV-Codecs
   - Teste Multi-Audio-Tracks
   - Teste Untertitel
   - Füge Container-Validierung hinzu

5. **test_parse2.py** (24 Zeilen)
   - Erweitere zu umfassender Parser-Suite
   - Teste alle unterstützten Formate
   - Füge Benchmark-Tests hinzu
   - Dokumentiere Expected vs Actual

6. **test_bitdepth.py** (28 Zeilen)
   - Teste alle Audio-Formate
   - Teste signierte/unsignierte PCM
   - Teste Float-Formate
   - Füge Validierungs-Logic hinzu

7. **test_parser_logic.py** (29 Zeilen)
   - Teste alle Parser-Helper-Funktionen
   - Teste Parser-Selection-Logic
   - Teste Fallback-Mechanismen
   - Füge Mock-Tests hinzu

### 🟡 Priorität 2: Regelmäßige Test-Ausführung

Erstelle einen CI/CD-Job, der diese Tests regelmäßig ausführt:

- test_i18n_completeness.py ✅
- test_i18n_deep_scan.py ✅
- test_ui_events.py ✅
- test_ui_integrity.py ✅
- test_logbook_bilingual.py ✅
- test_environment_dependencies.py
- test_build_integrity.py

### 🟢 Priorität 3: Neue Tests hinzufügen

Erstelle Tests für fehlende Bereiche:

- **test_video_player.py** (NEU)
  - Teste HTML5 Video Element
  - Teste Format-Unterstützung (MP4/WebM/MKV)
  - Teste Player-Controls
  - Teste Fullscreen-Mode

- **test_feature_modal.py** (NEU)
  - Teste list_feature_modal_items()
  - Teste Logbook-Integration
  - Teste Root-Docs-Integration
  - Teste Status-Filterung

- **test_version_consistency.py** (NEU)
  - Teste VERSION-Datei
  - Teste VERSION_SYNC.json
  - Teste alle Versionsnummern synchron
  - Teste PyInstaller .spec File

---

## 🚀 Verwendung

### Alle Tests ausführen
```bash
bash tests/run_all_tests.sh
```

### Einzelne Test-Suite ausführen
```bash
python tests/test_i18n_completeness.py
python tests/test_i18n_deep_scan.py
python tests/test_ui_events.py
```

### Tests mit pytest
```bash
pytest tests/ -v
pytest tests/test_i18n_completeness.py::test_i18n_json_structure
```

### Test-Coverage anzeigen
```bash
pytest --cov=. --cov-report=html tests/
```

---

## 📈 Metriken

- **Gesamt Tests:** 53 Test-Dateien
- **Kern-Tests:** 27/27 bestanden (100%)
- **Code-Coverage:** ~75% (geschätzt)
- **i18n Keys:** 314/314 validiert
- **UI Elements:** 102/102 internationalisiert
- **Event Handler:** 45 Buttons validiert
- **Backend Calls:** 53 Funktionen getestet

---

**Zuletzt aktualisiert:** 8. März 2026  
**Verantwortlich:** Test-Suite-Maintainer  
**Nächste Review:** Nach jedem Major-Release
