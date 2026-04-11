# Logbuch v1.37.68 – Recovery-Maßnahmen & Playback-Transparenz

**Datum:** 2026-04-06

## Durchgeführte Korrekturen

### 1. Mock-Playback-Fix
- Mock-Dateien von `media/mock/` nach `web/media/mock/` verschoben.
- Da `web/` das Root des Eel-Servers ist, sind die Dateien jetzt direkt über `/media/mock/filename.mp3` streambar.
- Backend-Pfade entsprechend aktualisiert.

### 2. Transparenz & Debugging
- **Backend (main.py):**
  - Protokolliert jetzt explizit die ersten 50 Dateikategorien, die vom Filter verworfen werden (`[BD-AUDIT] Dropped...`).
  - Logs zeigen sofort, warum Items nicht in der GUI ankommen.
- **Frontend (bibliothek.js):**
  - `renderLibrary` gibt `[FE-AUDIT] STAGE 0: Initial Count` in der Konsole aus, um den Zustand der Items vor der Filterung zu überwachen.

### 3. Status-HUD
- `updateSyncAnchor`-Logik finalisiert: Footer ([DB: X | GUI: Y]) wird bei jeder Hydration korrekt aktualisiert.

## Nächste Schritte
- Mock-Titel (Megaloh, Benjie, Beginner) anklicken und prüfen, ob der Ton abgespielt wird.
- Browser-Konsole (F12) und Backend-Logs auf `[BD-AUDIT]` und `[FE-AUDIT]` Ausgaben prüfen, um die Filterkette zu überwachen.

---
**Status:** Recovery-Maßnahmen & Playback-Transparenz erfolgreich umgesetzt (v1.37.68)
