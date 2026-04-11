# Logbuch v1.37.66 – Hydration-Synchronisierung & Black-Hole-Fix abgeschlossen

**Datum:** 2026-04-06

## Durchgeführte Änderungen

### 1. Globaler Sync-Anchor
- `updateSyncAnchor` in `common_helpers.js` verschoben und global verfügbar gemacht.
- Das Feld [DB: 541 | GUI: 544] im Footer wird bei jeder Synchronisation mit Echtzeitdaten befüllt.

### 2. Funktionale Hydration-Toggles
- Buttons M (Mock), R (Real), B (Both) lösen sofortige Re-Hydration der Bibliothek und Queue aus.
- Aktiver Button wird optisch durch grünen Indikator hervorgehoben.

### 3. Library Black-Hole Fix
- `renderLibrary` in `bibliothek.js` respektiert jetzt `window.__mwv_hydration_mode`.
- 541 reale Items aus der DB werden korrekt angezeigt, sobald "Real" oder "Both" aktiv ist.

### 4. Backend-Mock-Injektion
- Mock-Assets werden in Both- und Mock-Modi zuverlässig injiziert, unabhängig vom Audit-Status.

## Verifizierung
- **Status-HUD:** Zeigt korrekt [DB: 541 | GUI: 544] (Both) bzw. [DB: 541 | GUI: 541] (Real).
- **Toggles:** Klick auf "R" filtert Mocks heraus, zeigt nur reale Dateien.
- **Queue-Parity:** Playlist wird synchron zur Library aktualisiert.

---
**Status:** Hydration-Synchronisierung & Black-Hole-Fix abgeschlossen, System bereit für Testbetrieb (v1.37.66)
