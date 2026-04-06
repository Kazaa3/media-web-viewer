# Logbuch v1.37.48 – Category Cleanup & Diagnostic Bridge Restoration

**Datum:** 2026-04-06

## Ziel
Restaurierung der Bibliothekshydration und Bereinigung der Kategorie-Mappings (Entfernung von "multimedia").

## Maßnahmen & Änderungen

### 1. Category Mapping Cleanup (SSOT)
- **models.py**
  - Interner Schlüssel: "multimedia" wird zu "video" in `MASTER_CAT_MAP` umbenannt.
  - Alias-Tabelle: `category_alias_table` mappt jetzt "multimedia", "video", "film" usw. auf das kanonische "video".
  - App-Mode: "multimedia" wird als Modus-Flag behandelt, nicht als Dateikategorie.

### 2. Backend Bridge & Diagnostic Restoration
- **main.py**
  - Diagnostics: Fehlende Funktion `get_library_forensics()` wiederhergestellt, um den "Audit Bridge Fault" im UI zu beheben.
  - API-Mismatch: Interne Aufrufe von `db.get_library()` auf das korrekte `db.get_all_media()` umgestellt.
  - Hydration: `get_library` gibt bei Bedarf rohe SQL-Daten zurück (bypasst Filter für Diagnostik).
- **db.py**
  - Legacy-Kompatibilität: `get_library = get_all_media` hinzugefügt.
  - Migration: Automatische Umbenennung aller "multimedia"-Kategorien in der DB zu "video".

### 3. Frontend Alignment
- **common_helpers.js**
  - `isVideoItem` prüft jetzt auf "video" statt auf das alte "multimedia"-Label.

## Offene Frage
- Sollen "multimedia"-Kategorien als Legacy-Alias bestehen bleiben oder sofort hart zu "video" umbenannt werden? (**Vorschlag:** Harte Umbenennung zu "video".)

## Verifikation
- **Automatisiert:**
  - Test: `get_allowed_internal_cats(['multimedia'])` gibt jetzt "video" zurück.
- **Manuell:**
  - Diagnostics Overlay öffnen, prüfen, ob "Audit Bridge Fault" behoben ist.
  - "Alle Medien"-Filter toggeln, Songs wie "Anfangsstadium RMX" erscheinen in der Standardansicht.

---
**Status:** Plan zur Wiederherstellung der Bibliothekshydration und Kategorie-Bereinigung dokumentiert (v1.37.48)
