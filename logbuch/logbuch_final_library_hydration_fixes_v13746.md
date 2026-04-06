# Logbuch v1.37.46 – Final Library Hydration Fixes

**Datum:** 2026-04-06

## Zusammenfassung der letzten Fixes

### 1. Datenbank-Normalisierung
- Die Migration in `src/core/db.py` wurde aktualisiert: Alle Kategorien "unbekannt", NULL-Werte oder leere Strings werden automatisch in das kanonische Label "unknown" umbenannt.
- Ergebnis: Die Datenbank ist jetzt vollständig synchron mit der neuen SSOT-Filterlogik (Source of Truth).

### 2. Path-Resolution-Härtung
- In `src/core/main.py` wird jetzt überall `pathlib.Path` verwendet.
- Spezialzeichen wie # (im Projektordner) oder ' in Dateinamen werden korrekt behandelt und verursachen keine Fehler mehr bei Existenzprüfungen.

### 3. Kategorie-Mapping-Synchronisierung
- Die Abbildung von "unbekannt" (UI) auf "unknown" (DB) ist aktiv und sorgt dafür, dass alle ehemals "versteckten" Items in der Produktionsansicht erscheinen.
- Die Filterlogik akzeptiert jetzt beide Varianten und zeigt alle relevanten Medien an.

## Fortschrittsübersicht
- Modelle (`models.py`): Kategorie-Mapping & Unknowns gepatcht
- Hauptlogik (`main.py`): Filter-Resilienz & Path-Handling gehärtet
- Datenbank (`db.py`): Kategorie-Normalisierung implementiert
- Verifikation: Die Bibliothek wird mit Produktionsfiltern korrekt angezeigt

## Ergebnis
Die Anwendung zeigt jetzt die gesamte Mediathek korrekt an – ein Umschalten auf "Bypass" (RAW) ist nicht mehr nötig. Alle als "unbekannt" konfigurierten Items werden zuverlässig mit ihren physischen Assets in der Datenbank verknüpft und angezeigt.

---
**Status:** Hydration-Fixes abgeschlossen, Bibliothek vollständig sichtbar (v1.37.46)
