<!-- Category: Fix -->
<!-- Status: COMPLETED -->
<!-- Title (DE): Environment- und Datenbank-Bereinigung mit DB-Isolation -->
<!-- Title (EN): Environment and Database Cleanup with DB Isolation -->
<!-- Summary (DE): Behebt inkonsistente Bibliothekseinträge durch Bereinigung alter DB-Dateien, saubere Scan-Ordner und klare aktive User-DB -->
<!-- Summary (EN): Fixes inconsistent library entries via legacy DB cleanup, sanitized scan directories, and clear active user DB isolation -->

# Environment- und Datenbank-Bereinigung mit DB-Isolation

**Version:** 1.2.23  
**Datum:** 8. März 2026  
**Status:** ✅ COMPLETED

## Problem (beobachtet)

In der Bibliothek traten inkonsistente Zustände auf:
- Anfangszustand: mehrere Einträge (u. a. Anfangsstadium RMX, Einfach & Leicht, Beethoven, Leaving Earth)
- Nach Neustart: nur noch 4 Einträge
- Später: nur noch 1 Eintrag

Das deutet auf vermischte Datenquellen hin (mehrere lokale DB-Dateien + wechselnde Scan-Konfiguration).

## Root Cause

1. **Mehrere DB-Dateien im System** (historisch/legacy):
   - `/home/xc/media_library.db`
   - `/home/xc/#Coding/gui_media_web_viewer/media_library.db`
   - `/home/xc/#Coding/gui_media_web_viewer/dist/media_library.db`
   - `/home/xc/#Coding/media_library.db`
2. **Aktive App-DB** ist jedoch ausschließlich:
   - `/home/xc/.media-web-viewer/media_library.db`
3. **Fehlerhafte Scan-Konfiguration** enthielt projektinterne Ordner (z. B. `logbuch`) als Scan-Quelle.

## Implementierte Lösung

### 1) Klare aktive DB-Isolation (`db.py`)
- Neue Funktion `get_active_db_path()`
- Legacy-DB-Erkennung via `get_legacy_db_candidates()`
- Legacy-DB-Listing via `list_legacy_databases()`
- Legacy-DB-Cleanup via `cleanup_legacy_databases()`

### 2) Saubere Scan-Konfiguration (`parsers/format_utils.py`)
- Default `scan_dirs` auf `[]` gesetzt (keine Demo-/Alt-Daten automatisch)
- Neue Sanitizer-Funktion `sanitize_scan_dirs()`:
  - entfernt ungültige/verwaiste Pfade
  - entfernt Duplikate
  - blockiert interne Projektordner (`logbuch`, `dist`, `.git`, `.venv`, `packaging`)
- Sanitizer wird bei Load und Save der Parser-Konfiguration angewendet

### 3) Reset erweitert (`main.py`)
- `reset_app_data()` löscht jetzt zusätzlich Legacy-DB-Dateien
- Startup warnt bei gefundenen Legacy-DB-Dateien (werden ignoriert)

## Umgesetzte Bereinigung (lokal ausgeführt)

Bereinigung durchgeführt und validiert:
- Aktive DB nach Reset: **0 Einträge**
- Legacy-DB-Dateien: **gefunden und gelöscht**
- Scan-Ordner in Config auf leer gesetzt (`scan_dirs = []`)

Ergebnis:
- Keine falschen Alt-Einträge mehr in der aktiven Umgebung
- Keine konkurrierenden lokalen DB-Dateien mehr

## Tests

Neue Test-Suite: `tests/test_environment_cleanup.py`
- **7 Tests bestanden**
- Validiert:
  - aktive DB-Pfad-Isolation
  - Legacy-DB-Erkennung (ohne aktive DB)
  - Legacy-DB-Cleanup
  - Sanitizing der Scan-Ordner

Zusätzlich Regressionscheck:
- `tests/test_browser_preference.py` + `tests/test_session_management.py`
- **21 Tests bestanden**

## Ergebnis

Die Umgebung ist jetzt sauber und deterministisch:
- genau eine aktive User-DB
- keine Alt-DB-Leichen
- keine internen Projektordner als Medienquelle
- konsistentes Verhalten nach Neustarts
