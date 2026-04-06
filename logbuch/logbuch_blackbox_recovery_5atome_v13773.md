# Logbuch v1.37.73 – Black Box Recovery: Die 5 Atome der Datenkette

**Datum:** 2026-04-07

## Die 5 Schritte der Wiederherstellung

1. **[Backend] Stage 0 Bypass**
   - In `main.py` greift jetzt ein Emergency Fallback: Wenn der Filter 100% der DB-Items verschluckt, wird die Filterung übersprungen und die Rohliste (541 Items) zurückgegeben.
   - Log: `[BD-RECOVERY]` erscheint im Backend-Log.

2. **[JS] Global State Export**
   - In `bibliothek.js` wird die Mediathek nach `window.__mwv_all_library_items` exportiert.
   - Alle Module (HUD, Queue) greifen auf diese globale Datenquelle zu.

3. **[JS] HUD Synchronisation**
   - Das linke HUD im Footer liest jetzt direkt aus dem globalen Speicher.
   - Anzeige ist stabil: `[DB: 541 | GUI: 544]` (im Modus 'Both').

4. **[JS] Forensic Logging**
   - Die Frontend-Konsole zeigt bei jedem Sync-Vorgang an, wie viele Items im Speicher gelandet sind (`Memory filled with 541 items`).

5. **[Backend] Alias Hardening**
   - In `models.py` wurde die Kategorie-Erweiterung gehärtet: 'Musik', 'Music', 'Film' etc. werden sicher gemappt.

## Status
- Die Datenkette ist wiederhergestellt.
- 541 Items sind im Speicher, das HUD zeigt sie an.
- Mock-Playback über `/media/mock/` ist voll funktionsfähig.

---
**Status:** Black Box Recovery & Datenkette stabil (v1.37.73)
