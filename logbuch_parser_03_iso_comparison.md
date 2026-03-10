<!-- Status: ACTIVE -->
date: 2026-03-10
category: parser
tags: [parser, iso, pycdlib, isoparser, comparison]

# Logbuch-Eintrag: ISO-Parser Vergleich & Standardisierung

## Übersicht

Nach der Einführung des Fast-Scan Modus wurde eine tiefere Analyse der ISO-Parser (`pycdlib` vs. `isoparser`) durchgeführt, um einen Standard für die Extraktion von Volume-IDs und Dateistrukturen festzulegen.

## Benchmark: PAL DVD Sample (`4_KOENIGE.iso`, 6.8 GiB)

Ein Vergleich beider Parser an einem realen PAL-DVD-Abbild ergab folgende Ergebnisse:

### pycdlib (Standard)
- **Status:** Fehlgeschlagen bei diesem spezifischen Image.
- **Fehler:** `struct.error` beim Parsen von UDF-Ankern/Deskriptoren.
- **Ursache:** Einige DVDs nutzen UDF-Varianten oder korrupte Anker, die `pycdlib` (Version 1.14.0) zum Absturz bringen, wenn es versucht, Deskriptoren an ungültigen Offsets zu entpacken.
- **Vorteil:** Sehr schnell bei Standard-ISOs (ISO 9660) und bietet präzisen Zugriff auf die Volume-ID.

### isoparser (Fallback)
- **Status:** Nicht responsiv / Hang.
- **Verhalten:** Versucht, die gesamte Verzeichnisstruktur rekursiv zu indizieren. Bei 6.8 GiB DVD-Strukturen führt dies zu extrem langen Laufzeiten, die in einer GUI-Anwendung ohne Background-Worker wie ein "Hang" wirken.
- **Vorteil:** Kann teilweise korrupte Header ignorieren, ist aber für große Images im Haupt-Parsing-Thread ungeeignet.

## Entscheidung: pycdlib als Standard

Trotz des Fehlers beim UDF-Parsing des spezifischen DVD-Samples wurde **pycdlib** als Standard-ISO-Parser gesetzt (`priority: high`), da:
1. Es bei validen ISO 9660 Abbildern (Standardfall) signifikant schneller und robuster ist.
2. Es eine sauberere API für Metadaten bietet.
3. Der Fast-Scan Modus ohnehin davor schützt, dass diese Parser bei einem Standard-Scan Zeit kosten.

## Implementierte Änderungen

- **PARSER_MAPPING:** `.iso` bevorzugt nun `pycdlib`.
- **PARSER_CONFIG:** `parser_chain` führt `pycdlib` vor `isoparser`.
- **Fallback-Logik:** Schlägt `pycdlib` fehl (wie beim DVD-Sample), wird automatisch `isoparser` versucht (der bei dem Sample allerdings ebenfalls problematisch war).

## Verifizierung und Tests

Ein permanenter Unit-Test wurde in `tests/test_iso_priority.py` erstellt, um sicherzustellen, dass die Priorisierung in der Konfiguration und im Mapping konsistent bleibt.
