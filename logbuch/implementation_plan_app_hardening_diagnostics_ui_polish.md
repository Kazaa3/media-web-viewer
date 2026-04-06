# Implementation Plan – App Hardening, Diagnostics, and UI Polish

## Ziel
Die App wird für die Zukunft gehärtet, Diagnosen werden transparent im UI gemacht und die Testsequenz wird robust gestaltet.

---

## Proposed Changes

### 1. Robust Testing & Log Analysis
- **Ziel:** Sicherstellen, dass Items definitiv im DOM erscheinen.
- **Aktion:**
  - Testzyklus mit `mock_data_enabled = True` starten, um den Datenfluss Python → DOM zu isolieren.
  - Nach erfolgreicher Validierung (LOGS-Overlay) zurück zu Real Media Rendering schalten.

### 2. Startup Time Visibility
- **Ziel:** Bootzeit der App direkt im UI anzeigen.
- **Aktion:**
  - **main.py:** `eel.get_startup_time()` bereitstellen.
  - **app_core.js:** Bei `DOMContentLoaded` Startup-Zeit abfragen und im Footer anzeigen (z.B. neben v1.34).

### 3. Multi-Instance Check & Kill/Restart
- **Ziel:** Stale-Instanzen erkennen und Neustart ermöglichen.
- **Aktion:**
  - **main.py:** `eel.check_and_restart()` mit psutil implementieren (Waisenprozesse killen, sauberen Restart ausführen).
  - **tools_panel.html & options_helpers.js:** "Prüfen & Neustarten"-Button in "System & Diagnose" einbauen.

### 4. SYNC Button Adjustments
- **Ziel:** SYNC im Footer macht nur ein schnelles GUI-Refresh, kein Deep-Scan.
- **Aktion:**
  - **app.html:** SYNC-Button ruft `refreshLibrary()` (schnelle DB-Abfrage) statt Backend-Scan.
  - **bibliothek.js:** `refreshLibrary()` zeigt Toast und rendert UI neu, ohne zu blockieren.

---

## Open Questions
- Wo soll die Startup-Zeit angezeigt werden? Vorschlag: Neben dem v1.34-Badge unten links im Footer.

---

## Verification Plan
- **Mock Test:** Mock Data erzwingen, App öffnen, "X items appended to DOM!" im LOGS-Overlay prüfen, Mock-Playback testen.
- **Real Test:** Echte Daten wiederherstellen, LOGS und Mediengalerie prüfen.
- **UI Check:** Startup-Zeit sichtbar, SYNC macht schnellen Refresh, "Kill & Restart"-Button in Optionen funktioniert.
