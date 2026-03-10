<!-- Status: ACTIVE -->
date: 2026-03-10
category: performance
tags: [parser, fast-scan, optimization, iso, ui]

# Logbuch-Eintrag: Performance-Optimierung – Fast-Scan Modus

## Übersicht

Der Media Web Viewer unterstützt eine Vielzahl von Metadaten-Parsern. Einige dieser Parser (wie `isoparser`, `pycdlib` oder der `ebml`-Parser) sind jedoch ressourcenintensiv und können bei großen Dateien (insbesondere MKV oder ISO) zu Verzögerungen von mehreren Sekunden pro Datei führen.

Um die Benutzererfahrung bei großen Mediensammlungen zu verbessern, wurde ein **Fast-Scan Modus** implementiert.

## Implementierung

### Backend-Logik

In `parsers/media_parser.py` wurde eine globale Prüfung eingeführt, die bekannte "langsame" Parser überspringt, sofern:
1. Der **Fast-Scan Modus** aktiviert ist (Standard).
2. Der Extraktions-Modus nicht auf `full` (ausführlicher Scan) steht.

```python
# parsers/media_parser.py
is_slow = step_name in SLOW_PARSERS
fast_scan = PARSER_CONFIG.get("fast_scan_enabled", True)

if is_slow and mode != 'full' and fast_scan:
    log.debug(f"⏩ [Fast-Scan] Skipping slow parser '{step_name}'")
    continue
```

Diese Logik wird ergänzt durch eine Liste in `parsers/format_utils.py`:
```python
SLOW_PARSERS = {"isoparser", "pycdlib", "ebml", "mkvparse", "enzyme", "pymkv"}
```

### Frontend-Integration

Die Benutzeroberfläche wurde um einen Schalter im "Parser-Tab" erweitert, mit dem der Benutzer den Fast-Scan Modus deaktivieren kann, falls eine detaillierte Analyse der ISO-Files erwünscht ist.

- **Badges:** Bekannte langsame Parser werden in der Liste visuell mit einem "Langsam" / "Slow" Badge markiert.
- **Toggle:** Ein zentraler Toggle aktiviert/deaktiviert die Optimierung global.

## Vorteile

- **Geschwindigkeit:** Reduziert die Scan-Zeit für Dateisammlungen mit vielen ISO-Dateien von Minuten auf Sekunden.
- **Stabilität:** Verhindert Hänger bei korrupten oder extrem großen ISO-Strukturen im Standard-Scan.
- **Transparenz:** Benutzer sehen sofort, welche Parser zeitaufwendig sind.

## Verifizierung

Die Funktionalität wurde mit dem Test-Skript `tests/test_fast_scan.py` verifiziert, welches die korrekte Übersprung-Logik in verschiedenen Modi (Lightweight + Enabled, Lightweight + Disabled, Full) prüft.
