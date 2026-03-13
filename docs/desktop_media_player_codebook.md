#dict - Web Media Player and Library Manager

> .md logbook files should list all valid header names used in the project, including both desktop and web variants. Use '#dict - Web Media Player and Library Manager' for browser-based scripts/docs, and '#dict - Desktop Media Player and Library Manager' for desktop app scripts/docs. Both follow the same header and metadata conventions.

# Desktop Media Player Codebook

This codebook documents the conventions, metadata fields, and header requirements for all scripts, tests, and documentation in the Media Web Viewer project.

## Header Standard

All scripts, tests, and .md files must start with:
- `dict - Desktop Media Player and Library Manager`
- Shebang (`#!/usr/bin/env python3`) and UTF-8 encoding (`# -*- coding: utf-8 -*-`) for Python files
- Structured metadata fields: Kategorie, Eingabewerte, Ausgabewerte, Testdateien, ERWEITERUNGEN (TODO), KOMMENTAR, VERWENDUNG
- Bilingual docstring (DE/EN) for purpose, scope, and usage
- Explicit start command in VERWENDUNG (e.g., pytest tests/test_transcoding_fixed.py -v)

## Example Header (Python)

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# App: dict - Desktop Media Player and Library Manager
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

## Example Header (.md)

```
dict - Desktop Media Player and Library Manager

# [Title]

[Description, metadata fields, and conventions as above]
```

## Reference
See logbuch/ItemType_Category_Map.md for detailed codebook entry requirements and examples.

## Purpose
This codebook ensures consistent naming, metadata, and documentation across all project files for maintainability, discoverability, and CI integration.
