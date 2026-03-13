# Media Web Viewer - Style Guide & Standards

This document establishes the technical standards and best practices for the Media Web Viewer project. Adherence to these rules is mandatory to ensure code consistency, prevent regressions, and maintain a high-quality test suite.

## 1. Python Syntax & Coding Standards

### Avoid Syntax Bloat & Regression
- First line: `#dict - Desktop Media Player and Library Manager`
- Use descriptive error messages in all `assert` statements.
- Group multiple related assertions into logical blocks with comments.

## 2. Test Classification & Reporting
#dict - Desktop Media Player and Library Manager v1.34
#dict - Web Media Player and Library Manager v.{VERSION}
Tests MUST be grouped according to their focus and complexity:

- `tests/tech/`: Technology-specific tests (FFmpeg, VLC, Mutagen, Scapy).
- `tests/basic/`: Core functionality, smoke tests, and fast validation.
- `tests/advanced/`: Integration, E2E, and performance scenarios.
- `tests/category/`: Organized by media type (Audio, Video, Playlist, UI).
- `tests/iso/`: Long-running tests for disk images (DVD/Blu-ray).

### Test Artifacts
- All logs, screenshots, and temporary fragments must be stored in `tests/artifacts/`.
- Never use hardcoded absolute paths to personal directories (e.g., `/home/username/`). Use `Path(__file__)` or established project constants.


### User Data & Environment
- **Anonymization**: Never hardcode personal linux usernames (`xc`), file paths, or IP addresses in tests.

### Media Assets
- **Copyright**: Do not include copyrighted media (covers, albums, videos) in the repository.

## 4. Repository Hygiene (.gitignore)
- `*.log`: Application and test logs.
- `*.json` (fragments): Temporary result files (e.g., `m4b_all_tools_results.json`).
- `screenshots/` & `*.png`: UI capture fragments.

- **i18n**: All UI strings must be localized via `web/i18n.json`.
- **Kebab-Case**: Use kebab-case for HTML IDs (`my-button-id`).


## 6. Test Script Header Standard

Every test script MUST start with a standardized dual-header:
- VERWENDUNG field with explicit start command (e.g., pytest tests/test_transcoding_fixed.py -v)

### Approved Template

```python
# dict - Web Media Player and Library Manager
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: [Kategorie Name]
# Eingabewerte: [Werte]
# Ausgabewerte: [Ergebnisse]
# Testdateien: [Dateien oder 'Keine']
# ERWEITERUNGEN (TODO): [Checkliste]
# KOMMENTAR: [Kurzer Kommentar oder Zweck]
# VERWENDUNG: pytest tests/[pfad]/[file].py -v

"""
KATEGORIE:
----------
[Kategorie Name]

ZWECK:
------
[Kurze Beschreibung des Testzwecks]

EINGABEWERTE:
-------------
- [Wert 1]

AUSGABEWERTE:
-------------
- [Ergebnis 1]

TESTDATEIEN:
------------
- [Pfad oder 'Keine']

ERWEITERUNGEN (TODO):
---------------------
- [ ] [Zukünftiges Feature]

VERWENDUNG:
-----------
    pytest tests/[pfad]/[file].py -v
"""
```

### Key Rules
## E2E Test Header Convention

E2E tests must follow the same header standard, but add:
- Kategorie: E2E Test
- Eingabewerte: UI, Selenium, browser, etc.
- Ausgabewerte: Screenshots, Log-Ausgaben, Fehler
- Testdateien: E2E test scripts, reference screenshots
- Startbefehl: pytest tests/e2e/test_[name].py -v

## Audit Script Header Convention

Audit scripts must include:
- Purpose and scope (DE/EN bilingual docstring)
- Test directory (e.g., tests/)
- Explicit list of included test file names (use 'File:' or 'Datei:' prefix for clarity)
- Usage instructions (start command)

Example header:
```python
# dict - Web Media Player and Library Manager v.{VERSION}
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: Audit Script
# Eingabewerte: [Dateien, Daten]
# Ausgabewerte: [Ergebnisse, Log-Ausgaben]
# Testdateien: [Dateien oder 'Keine']
# ERWEITERUNGEN (TODO): [Checkliste]
# KOMMENTAR: [Kurzer Kommentar oder Zweck]
# VERWENDUNG: python tests/[pfad]/[file].py

"""
KATEGORIE:
----------
Audit Script

ZWECK:
------
[Kurze Beschreibung des Audit-Zwecks]

EINGABEWERTE:
-------------
- [Dateien, Daten]

AUSGABEWERTE:
-------------
- [Ergebnisse, Log-Ausgaben]

TESTDATEIEN:
------------
- [Dateien oder 'Keine']

ERWEITERUNGEN (TODO):
---------------------
- [ ] [Zukünftiges Feature]

VERWENDUNG:
-----------
    python tests/[pfad]/[file].py
"""
```



## .md Documentation Naming Convention

All .md documentation files must include 'dict - Desktop Media Player and Library Manager' as the first line for naming consistency and project identification.

## Codebuch Entry Convention

All codebook entries must include:
- Required header line: `#dict - Desktop Media Player and Library Manager`
- Shebang and UTF-8 encoding
- Structured metadata fields (Kategorie, Eingabewerte, Ausgabewerte, Testdateien, ERWEITERUNGEN (TODO), KOMMENTAR, VERWENDUNG)
- Bilingual docstring (DE/EN) describing purpose, scope, and usage
- Reference: See logbuch/ItemType_Category_Map.md for detailed codebook entry requirements and examples

Example header:
```python
#dict - Desktop Media Player and Library Manager
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: Codebuch Entry
# Eingabewerte: [Werte]
# Ausgabewerte: [Ergebnisse]
# Testdateien: [Dateien oder 'Keine']
# ERWEITERUNGEN (TODO): [Checkliste]
# KOMMENTAR: [Kurzer Kommentar oder Zweck]
# VERWENDUNG: python codebuch/[pfad]/[file].py

"""
KATEGORIE:
----------
Codebuch Entry

ZWECK:
------
[Kurze Beschreibung des Codebuch-Eintrags]

EINGABEWERTE:
-------------
- [Wert 1]

AUSGABEWERTE:
-------------
- [Ergebnis 1]

TESTDATEIEN:
------------
- [Pfad oder 'Keine']

ERWEITERUNGEN (TODO):
---------------------
- [ ] [Zukünftiges Feature]

VERWENDUNG:
-----------
    python codebuch/[pfad]/[file].py
"""
```

## Zusätzliche Docstrings für Prosa-Erklärungen

Neben dem Header und den Funktions-Dokumentationen kann ein zusätzlicher Docstring am Anfang des Skripts stehen, der prosaartige Erklärungen, Hintergrund, Motivation oder Teststrategie enthält.

Dieser Docstring kann in Deutsch und Englisch verfasst werden und soll den Kontext, die Zielsetzung und Besonderheiten des Tests erläutern.

Beispiel:

    """
    FFmpeg Transcoding Fix Test Suite (DE/EN)
    =========================================
    
    DE:
    Testet die Behebung des Transcoding-Bugs und die Optimierung der Parameter für FFmpeg und ALAC-Erkennung.
    
    EN:
    Tests the fix for the transcoding bug and optimization of parameters for FFmpeg and ALAC detection.
    
    Motivation:
        Dieser Test prüft, ob die Fehlerursache im Transcoding-Workflow behoben wurde und ob die neuen Parameter zu einer besseren Performance führen.
    """

## Funktions-Dokumentation: Google-Style, bilingual

Jede Funktion im Testskript soll einen Google-Style Docstring enthalten, der sowohl Deutsch als auch Englisch umfasst.

Der Docstring beschreibt Zweck, Parameter, Rückgabewerte und Fehlerfälle.

Beispiel:

    def test_ffmpeg_transcoding():
        """
        DE:
        Testet die Transcodierung mit FFmpeg und prüft, ob die Parameter korrekt gesetzt sind.

        EN:
        Tests transcoding with FFmpeg and checks if parameters are set correctly.

        Args:
            Keine.
        Returns:
            Keine.
        Raises:
            AssertionError: Wenn die Transcodierung fehlschlägt.
        """
        # ...existing code...

Die Funktions-Docstrings sind von den prosaartigen Modul-Docstrings und dem Header getrennt und müssen für jede Testfunktion vorhanden sein.

## Build-Artefakte und CI/CD

- Build-Artefakte (z.B. .deb, .exe, .whl) sollen immer in build/ oder dist/ abgelegt werden.
- Der Projekt-Root darf keine Build-Artefakte enthalten.
- Die Verzeichnisse build/ und dist/ sowie alle Artefakte (*.deb, *.exe, *.whl) müssen in .gitignore eingetragen werden.
- Nur Quellcode und Dokumentation werden im Git-Repository versioniert.
- Artefakte werden über CI/CD (z.B. GitHub Releases) bereitgestellt, nicht im Git-Repo.

Beispiel für .gitignore:

    build/
    dist/
    *.deb
    *.exe
    *.whl

## Test Header Style (Audit Scripts)

All test audit scripts should include a standardized header with:
- Purpose and scope (DE/EN bilingual docstring)
- Test directory (e.g., tests/)
- Explicit list of included test file names (use 'File:' or 'Datei:' prefix for clarity)
- Usage instructions

Example header:
"""
Test Header/Docstring Audit

Checks for missing standardized headers and Google-style bilingual docstrings in test files listed in the GUI overview.

Test Directory: tests/
File / Datei:
- test_abase.py
- test_bplayer.py
- test_debug_and_db.py
- test_library.py
- test_modals.py
- test_options.py
- test_playlist.py
- test_teststab.py
- test_videoplayer.py
# Add more as needed...

Usage:
    python tests/check_missing_test_headers.py
"""

Update all audit scripts to follow this header pattern for easier test discovery and maintainability.
