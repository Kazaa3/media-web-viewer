# Logbuch v1.37.67 – Recovery & Playback Fix: Mock-Assets & Black-Hole

**Datum:** 2026-04-06

## Ziel
Behebung des "0-Item"-Black-Hole-Bugs in der Hauptbibliothek und Reparatur des Mock-Media-Playbacks durch korrekte Pfadauflösung und Kategorie-Mapping.

## Maßnahmen & Änderungen

### 1. File System & Paths
- **Neues Verzeichnis:** `web/media/mock/`
  - Alle Mock-Assets (megaloh.mp3, benjie.mp3, beginner.mp3) werden hierhin verschoben.
  - Assets sind dann über `/media/mock/...` im Browser erreichbar, was für den Player notwendig ist.
- **main.py**
  - `realistic_mocks`-Pfade auf `/media/mock/filename.mp3` aktualisiert.
  - Debug-Logging in `_apply_library_filters` erweitert, um Drop-Gründe für die 541 Items zu tracen.

### 2. Library Hydration
- **bibliothek.js**
  - Aggressives Logging in `renderLibrary()` hinzugefügt, um den Zustand von `allLibraryItems` zu debuggen.
  - Sicherstellen, dass `hmode` korrekt mit dem Backend synchronisiert wird.
- **common_helpers.js**
  - `updateSyncAnchor` finalisiert, damit das HUD [DB: X | GUI: Y] immer den echten Zustand anzeigt.

## Offene Frage
- Soll das ursprüngliche `media/mock`-Verzeichnis als Backup erhalten bleiben? (**Vorschlag:** Komplett nach `web/media/mock` verschieben.)

## Verifikation
- **Manuell:**
  - Mock-Item (z.B. Megaloh) anklicken, Playback funktioniert.
  - Footer HUD zeigt [DB: 541 | GUI: 544] im 'Both'-Modus.
  - Auf 'Real' umschalten, Library Grid zeigt 541 echte Items.

---
**Status:** Recovery & Playback Fix – Mock-Assets & Black-Hole-Bug adressiert (v1.37.67)
