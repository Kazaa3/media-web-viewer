# Erweiterung Debug-Tab & Konsole – Parser-Logs, Laufzeit-Info, Log-Level

**Datum:** 14.03.2026

## 1. Detaillierte Parser-Logs (Magic-Checks)
- Der Log-Logbuffer wurde von 1.000 auf 10.000 Zeilen erhöht.
- Dadurch gehen bei großen Scans keine frühen (wichtigen) Logzeilen mehr verloren.
- Parser-Logs wie "Skipping" und "Magic-Checks" sind jetzt zuverlässig im Frontend sichtbar.

## 2. Laufzeit-Informationen & PIDs
- Neuer Bereich "Laufzeit-Info & Log-Level" im Debug-Tab.
- Zeigt live an:
  - **Python PID:** Prozess-ID der laufenden Python-Instanz
  - **Browser PID:** Prozess-ID des gestarteten Chromium/Chrome-Fensters
  - **Log-Level:** Aktueller Logging-Schwellenwert

## 3. Dynamische Log-Level Wahl
- Log-Level kann jetzt direkt im Debug-Tab per Dropdown (DEBUG, INFO, WARNING, ERROR) geändert werden.
- Änderung wird sofort an alle Logger im Backend übernommen.
- Ermöglicht detaillierte Analysen (DEBUG) zur Laufzeit ohne Neustart.

## 4. Branding & UI
- Bereich heißt jetzt einheitlich "Laufzeit-Info & Log-Level" (bzw. "Runtime Info & Log Level" auf Englisch).
- Die Datenbank-Statistik nutzt das korrekte Label `database_item`.

---

### Testanleitung
1. Beenden Sie die aktuelle Sitzung (Ctrl+C im Terminal).
2. Starten Sie die App neu:
   ```bash
   /home/xc/#Coding/gui_media_web_viewer/.venv_run/bin/python /home/xc/#Coding/gui_media_web_viewer/src/core/main.py
   ```
3. Wechseln Sie in das Tab Debug & DB.
4. Oben links erscheinen PIDs und Log-Level. Schalten Sie auf DEBUG, um Parser-Traces in der Konsole zu sehen.

---

**Ergebnis:**
- Parser-Logs sind vollständig sichtbar.
- Laufzeit-Infos und Log-Level sind übersichtlich und live verfügbar.
- Log-Level ist zur Laufzeit flexibel umschaltbar.
- UI und Labels sind konsistent.