# Logbuch v1.37.57 – Walkthrough: Hybrid Hydration & Diagnostic Control Center

**Datum:** 2026-04-06

## Problemstellung
Medien wurden im GUI nur im "Bypass"-Modus angezeigt. Ursache: Pfadauflösung (# im Projektpfad) und Kategorie-Mapping für "unknown"/"unbekannt".

## Maßnahmen & Fixes

### 1. Robuste Pfadauflösung (Pathlib)
- `resolve_media_path` in main.py nutzt jetzt pathlib.Path für alle Existenzprüfungen.
- Spezialzeichen wie # im Pfad oder ' in Dateinamen werden korrekt behandelt.

### 2. Kategorie-Mapping (Unknown / Unbekannt)
- `category_alias_table` in models.py explizit um "unknown" und "unbekannt" erweitert.
- `_apply_library_filters` in main.py nutzt die erweiterten Mappings.

### 3. Diagnostisches Logging
- [BD-AUDIT]-Logs zeigen jetzt die vollständige Liste erlaubter Kategorien beim Droppen von Items.

### 4. Hybrid Hydration & Diagnostic Control Center
- **Hybrid-System:**
  - Backend liefert auf Wunsch echte Items + 3 Mocks (Stage 3, is_mock: true).
  - Frontend kann zwischen Mock (M), Real (R) und Both (B) umschalten.
- **Technischer Footer:**
  - Hydration-Toggle [M | R | B] für Hot-Swap zwischen Modi.
  - [↻]-Button für Full-GUI-Reload (F5).
  - Hover über HYDR zeigt Stage-1-4-Legende.
- **Auto-Sync:**
  - Umschalten des Toggles triggert sofort syncQueueWithLibrary().
  - Modus wird in localStorage persistiert.

## Verifikation
- **Kategorie-Mapping:**
  - CLI-Test: `get_allowed_internal_cats(['audio', 'unbekannt'])` enthält jetzt "unknown".
- **Pfadauflösung:**
  - Kodierte URLs wie `/media/Artist's%20Song.mp3` werden korrekt behandelt.
- **Hybrid/Control Center:**
  - Umschalten zwischen M, R, B funktioniert ohne Neustart.
  - [↻]-Button lädt App komplett neu.
  - Tooltip zeigt Stage-Legende.

---
**Status:** Hybrid-Hydration & Diagnostic Control Center erfolgreich implementiert (v1.37.57)
