# logbuch_restore_app_functionality_session_logging.md

## Implementation Plan – Restoring App Functionality & Session Logging

**Datum:** 29. März 2026

---

### Backend: logger.py
- `setup_logging(debug_mode=False, level=None, session_id=None)` akzeptiert jetzt optional ein `session_id`.
- Bei Angabe von `session_id` wird ein eindeutiges Logfile `logs/session_{session_id}.log` erzeugt.
- Jede App-Session erhält so eine eigene Diagnosedatei.

---

### Backend: main.py
- `get_library`, `get_library_filtered` und `get_library_folders` werden mit `@eel.expose` für das Frontend verfügbar gemacht.
- Startup-Sequenz aktualisiert: `logger.setup_logging` wird erst nach Generierung von `SESSION_ID` aufgerufen, damit das session-spezifische Logfile korrekt erstellt wird.

---

### Frontend: app.html
- "Video"-Tab-Button in der Navigation wiederhergestellt.
- `multiplexed-media-player-orchestrator-panel` (Video-Player-Container) geprüft und strukturell repariert.
- Alle fehlerhaften Closing-Tags oder Strukturprobleme behoben, damit Items korrekt gerendert werden.

---

### Frontend: ui_nav_helpers.js
- Sicherstellung, dass der "Video"-Tab korrekt in der Media-Subnavigation enthalten ist.
- `switchTab`-Logik für das Video-Panel geprüft und ggf. korrigiert.

---

### Verifikationsplan
- **Automatisiert:**
  - `python main.py --debug` starten und prüfen, ob `logs/session_*.log` erzeugt wird.
  - Über Logs verifizieren, dass `get_library` aufgerufen wird und Daten liefert.
- **Manuell:**
  - App starten und prüfen, dass der "Video"-Tab unter "Media" erscheint.
  - Bibliothek-Items (Audio/Video) erscheinen in "Bibliothek" und "Player".
  - Klick auf Audio-Item startet Playback (Audio-Priorität).
  - Klick auf Video-Item wechselt zum Video-Tab und startet den Player.
  - Im logs/-Verzeichnis erscheinen individuelle Session-Logfiles.

---

*Letzte Änderung: 29.03.2026*
