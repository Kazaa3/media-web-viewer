# Logbuch: Python-Statusbars & Fortschrittsanzeigen

## Ziel

Vergleich und Empfehlungen für Statusbar- und Fortschrittsbalken-Bibliotheken in Python, speziell für Media- und Batch-Anwendungen.

---

## 1. Bibliotheken im Vergleich

- **tqdm**
  - Sehr schnell, minimalistisch, stabil
  - Ideal für Schleifen, Dateioperationen, Batch-Jobs
  - Goldstandard für einfache Fortschrittsanzeigen

- **rich**
  - Fortschrittsbalken plus Logging, Tabellen, farbige CLI-Ausgabe
  - Perfekt für Entwickler-CLIs und Dashboards mit mehreren Tasks
  - Modernes, visuelles Paket

- **alive-progress**
  - Animierte, auffällige Fortschrittsbalken
  - Gut für lange Tasks, bei denen visuelles Feedback motiviert

---

## 2. Schnelle Integration

**tqdm – Beispiel:**

```python
from tqdm import tqdm
import time

for i in tqdm(range(100), desc="Scanne Medien"):
    time.sleep(0.02)
```

**rich – Beispiel:**

```python
from rich.progress import track
import time

for item in track(range(100), description="Verarbeite MKVs..."):
    time.sleep(0.02)
```

---

## 3. Empfehlung für Media-Library

- **tqdm** für Backend-Skripte, Batch-Scanner, Datei- und Medienoperationen (z.B. FFmpeg, Scraping, scan_media)
- **rich** für CLI-Dashboards, parallele Tasks, Logging und Status in einem Terminal

---

## 4. Installation

```bash
pip install tqdm rich alive-progress
```

**Offline:**

```bash
pip install --no-index --find-links ./packages tqdm rich alive-progress
```

---

## 5. Fazit

---

## 6. Praxis-Logbuch: Startup-Stabilisierung & StatusBar

---

## 7. DOM-Test-Hook & Watchdog-Integration

**Backend DOM Test Hook:**
- Neue @eel.expose-Funktion report_items_spawned(count, source) in src/core/main.py
- Loggt das erfolgreiche Rendern von UI-Elementen mit log.info(), wie gewünscht

**Frontend DOM Watchdog:**
- Diagnoseskript im <head> von web/app.html eingefügt
- Bestätigt initiale Eel-Connection (report_spawn)
- Pollt auf .playlist-item, #playlist-container und meldet automatisch an Backend, sobald Elemente gefunden werden (ITEM SIND GESPAWNED)

**Logging-Integration:**
- Terminal: STDOUT: [DOM TEST] ITEM SIND GESPAWNED (Count: X, Source: DOM_WATCHDOG)
- Debug-Log: [INFO] [app.main] [DOM TEST] ITEM SIND GESPAWNED ...

**Final Cleanup:**
- Einstiegspunkt konsolidiert, .venv_core als Hauptumgebung erzwungen, doppelte Funktionsdefinitionen und Legacy-Mock-Logik entfernt

**Verifikation:**
- App läuft und meldet Status alle 5s
- Testabschluss: http://localhost:8345 im Browser öffnen und auf STDOUT: [DOM TEST] ITEM SIND GESPAWNED ... achten

Siehe Walkthrough für Details und Screenshots.

**Wesentliche Verbesserungen:**
- Terminal-Progressbar: scripts/status_bar_utils.py integriert, zeigt Fortschritt bei Startup-Phasen (Umgebung, Module, State)
- Anti-Stalling-Watchdog: start_app() meldet alle 5s "ALIVE" und gibt nach 60s einen klaren Fehler, falls das UI nicht verbindet
- Duplicate Exposures: AssertionError durch doppelte @eel.expose-Decorator (z.B. read_file) behoben
- Environment-Stabilität: Erzwingt immer .venv_core und prüft Abhängigkeiten/Pfade

**Aktueller Status:**
Die App läuft und wartet auf die Frontend-Verbindung:

```
STDOUT: [Eel] Launching app.html on port 8345...
STDOUT: [Eel] Server started. Monitoring for frontend synchronization...
STDOUT: [Watchdog] WAITING FOR FRONTEND (ALIVE: 5s)...
```

Nach dem Laden des Frontends im Browser (http://localhost:8345) erscheint:

```
STDOUT: [Success] UI SYNCHRONIZED. MWV READY.
```

Siehe Walkthrough für Details und Screenshots.

- tqdm = Standard für schnelle Fortschrittsanzeigen
- rich = Für schöne, komplexe CLI-Tools
- alive-progress = Für animierte, motivierende Balken bei langen Tasks

---

*Siehe Quellcode und weitere Beispiele in der Projekt-Dokumentation.*
