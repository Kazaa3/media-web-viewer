# UI Refinement & Connection Debugging – März 2026

## Ziel
- "voffline"-Status beheben
- Chromium-Sandbox-Fehler vermeiden
- Player-Footer/Statusbar ans untere Ende verschieben
- Tab-Struktur (Player, Bibliothek, Item) auf DIV-Balance prüfen und korrigieren

## Backend (src/core/main.py)
- NEU: wait_for_port(port, host='localhost', timeout=10) implementiert, damit der Server vor Browser-Launch bereit ist
- open_session_url:
  - Ruft wait_for_port auf
  - Startet Browser mit --disable-setuid-sandbox und --no-sandbox
  - Loggt explizit Erfolg/Misserfolg des Browser-Starts

## Frontend (web/app.html)
- Player-Controls/Statusbar ans untere Ende des Viewports/Containers verschoben
- DIV-Balance-Check für die ersten 3 Tabs (Player, Bibliothek, Item) durchgeführt
- Gefundene DIV-Ungleichgewichte in diesen Bereichen behoben

## Verifikationsplan
- App-Start: python3 src/core/main.py --debug
- Prüfen, dass Browser auf http://localhost:8345/app.html öffnet (kein Whitescreen)
- Footer/Playerbar ist immer ganz unten
- Mit browser_subagent durch die ersten 3 Tabs klicken und Layout prüfen

## Lessons Learned
- Warten auf offenen Port verhindert Race-Conditions beim Browser-Start
- Sandbox-Flags sind für Chromium in CI/Container-Umgebungen essenziell
- Footer/Playerbar muss explizit positioniert werden, um UI-Leaks zu vermeiden
- Regelmäßige DIV-Balance-Checks verhindern schleichende Layout-Fehler
