# Logbuch v1.37.70 – Implementation Plan: Final Chain Restoration (v1.35.68)

**Datum:** 2026-04-06

## Ziel
Wiederherstellung der Sichtbarkeit aller 541 Library-Items durch globalen State-Export und ein robustes "Black Hole"-Recovery im Backend.

## Maßnahmen & Änderungen

### 1. Global State Export (Frontend)
- **bibliothek.js**
  - `let allLibraryItems = [];` wird zu `window.__mwv_all_library_items = [];` geändert.
  - Alle Referenzen werden auf die globale Variable umgestellt, damit audioplayer.js und HUD den [DB: X]-Count korrekt berechnen können.
- **audioplayer.js**
  - HUD-Sync-Logik liest jetzt aus `window.__mwv_all_library_items`.

### 2. Backend Hydration & Recovery (Backend)
- **main.py**
  - Emergency Raw Fallback: In `get_library()` wird geprüft, ob `len(filtered_media) == 0` und `len(all_media) > 0`.
  - Falls ja, wird `all_media` (Raw) zurückgegeben und ein `[BD-CRITICAL]`-Fehler mit Audit-Resultaten geloggt.
  - So sind die 541 Items immer sichtbar, auch bei Filter-Misskonfiguration.

### 3. Data Parity
- **models.py**
  - 'unbekannt' und 'unknown' werden als Aliase für 'audio' in MASTER_CAT_MAP aufgenommen (defensiv).

## Verifikation
- **Manuell:**
  - Footer HUD zeigt [DB: 541 | GUI: 544] im 'Both'-Modus.
  - Moduswechsel (M/R/B): Zahlen aktualisieren sich sofort.
  - Klick auf 'Megaloh': Playback funktioniert.

---
**Status:** Final Chain Restoration Plan dokumentiert (v1.37.70)
