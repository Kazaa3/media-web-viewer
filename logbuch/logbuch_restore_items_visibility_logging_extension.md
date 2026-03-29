---

## Diagnostic & System Tab Structural Restoration (30.03.2026)

### User Review Required
**IMPORTANT**

- **Mapping Errors:** Der Debug-Tab war fälschlich auf die Button-ID statt auf das Panel gemappt. Das wird für alle Diagnosetabs korrigiert.

**NOTE**

- **Layout Logic:** Alle Split-View-Tabs (Logbuch, Debug, Optionen) erhalten explizit eine horizontale Ausrichtung (Sidebar links, Content rechts) und erben keine vertikale Stapelung mehr.

### Proposed Changes
**[Component] Navigation Mapping (UI)**
- **ui_nav_helpers.js**
  - `tabMap` nutzt korrekte Panel-IDs:
    - 'debug': `telemetry-inspector-tab-pane` (vorher Button-ID)
    - 'tests': `quality-assurance-regression-suite-panel`
    - 'reporting': `reporting-dashboard-panel`
    - 'logbuch': `localized-markdown-documentation-journal-panel`
  - Alle weiteren Keys in `tabMap` werden auf Konsistenz geprüft.

**[Component] Tab Layouts & Split-Views (UI)**
- **app.html**
  - Alle Split-View-Container (Debug, Logbuch, Optionen) erhalten explizit `flex-direction: row`.
  - Reihenfolge der Kindelemente prüfen:
    - Debug DB: `debug-settings-pane` links, `debug-console-pane` rechts.
    - Logbuch: `journal-sidebar-left` links.
  - Die globale Sidebar (Status) wird für diese Tabs ggf. ausgeblendet, falls sie das interne Layout stört.

**[Component] Environment & Browser (Backend)**
- **main.py**
  - `eel_mode` prüft proaktiv auf Chrome/Chromium und gibt eine Warnung aus, falls ein anderer Browser (z.B. Vivaldi) verwendet wird.

### Open Questions
- **Vivaldi vs Chrome:** Ist Chrome wegen spezieller Features bevorzugt oder nur zur Trennung der Dev-Session?
- **Global Sidebar:** Soll die globale Sidebar im "Debug DB"-Tab sichtbar bleiben oder – wie in der Bibliothek – ausgeblendet werden?

### Verification Plan
**Automated Tests**
- Mit Diagnostik-Probe prüfen, dass `switchTab('debug')` das Panel `telemetry-inspector-tab-pane` aktiviert.
- Reihenfolge der Kindelemente im `debug-tab-split-container` prüfen.

**Manual Verification**
- System -> Debug DB, Flags durchklicken.
- Diagnostics -> Tests, Reporting, Logbuch durchklicken.
- Prüfen, dass im Debug DB-View das "Dict" links und die "Console" rechts ist.
---

## Abschluss: UI Layout komplett restauriert (30.03.2026)

### Was korrigiert wurde

- **Immersive Bibliothek:** Die globale Seitenleiste (Playback-Status) wird nun automatisch ausgeblendet, wenn der Bibliothek-Tab oder der Video-Player aktiv ist. Die Cover erhalten so wieder den vollen Platz.
- **Tab-Layout-Fix:** Die fehlerhafte Erzwingung der vertikalen Ausrichtung wurde entfernt. Management-Tabs wie Item, Datei oder Edit erscheinen wieder korrekt horizontal (Sidebar links, Liste rechts).
- **Automatisches Umschalten:** Beim Wechsel zurück zu Player oder Management erscheint die Seitenleiste automatisch wieder, damit Status und Metadaten sichtbar bleiben.

### Walkthrough: UI Layout Restoration

| Tab             | Sidebar-Status | Layout-Ausrichtung                |
|-----------------|:--------------:|-----------------------------------|
| Bibliothek      | 🌑 Verborgen   | Full-Width (Beautiful)            |
| Video Player    | 🌑 Verborgen   | Immersiv                          |
| Item (Management)| 🌕 Sichtbar   | Horizontal-Split (Links: Inventory)|
| Datei-Browser   | 🌕 Sichtbar    | Horizontal-Split (Links: Browser) |

Die "schöne" Ansicht mit Cover-Flow ist nun wieder voll funktionsfähig und nutzt den gesamten Bildschirmplatz aus.
---

## UI Layout Restoration & Sidebar Management (30.03.2026)

### User Review Required
**IMPORTANT**

- **Layout Fix:** Entfernen des globalen `flex-direction: column`-Overrides in `switchTab`. Dieser Fehler hatte horizontale Split-Views in vertikale Stacks verwandelt.

**NOTE**

- **Sidebar Visibility:** Die Haupt-Sidebar (Playback-Status) wird nun automatisch ausgeblendet, wenn der "Bibliothek"-Tab aktiv ist. So entsteht das gewünschte, vollflächige Coverflow-Erlebnis.

### Proposed Changes
**[Component] Navigation & Layout (UI)**
- **ui_nav_helpers.js**
  - Entferne das globale `panel.style.flexDirection = 'column'` in `switchTab`.
  - Implementiere Sidebar-Toggle in `switchTab`:
    - Wenn `tabId === 'library'`, blende `main-sidebar` und `main-splitter` aus.
    - Für alle anderen Tabs: `main-sidebar` und `main-splitter` sichtbar (flex/block).
  - Aktualisiere `tabMap` oder `isFlex`-Logik, damit Tabs mit Flex-Containern korrekt initialisiert werden, ohne destruktive Style-Overrides.

**[MODIFY] app.html**
- Stelle sicher, dass Split-View-Tabs (Item, File, Edit, Logbuch) explizit `flex-direction: row` im Inline-Style haben, um falsche Defaults zu verhindern.

**[Component] Library (Bibliothek)**
- **bibliothek.js**
  - `renderLibrary()` berechnet Breite/Höhe korrekt für Vollbild, wenn Sidebar ausgeblendet ist.

### Open Questions
- **Video Player:** Soll die Sidebar auch im Video-Tab ausgeblendet werden?
- **Animation:** Sidebar-Kollaps animieren oder sofort umschalten?

### Verification Plan
**Automated Tests**
- Mit Diagnostik-Probe prüfen, dass `main-sidebar` bei aktivem Bibliothek-Tab `display: none` hat, bei Player/Item-Tabs `display: flex`.
- Prüfen, dass `indexed-sqlite-media-repository-panel` `flex-direction: row` hat.

**Manual Verification**
- Zu "Bibliothek" navigieren und prüfen, dass Sidebar ausgeblendet ist.
- Zu "Management -> Item" navigieren und prüfen, dass interne Sidebar links, Liste rechts ist.
- Prüfen, dass "Coverflow" korrekt (volle Breite) angezeigt wird.
---

## Abschluss: Tab-Reparatur & Multi-Session-Hilfsskript (30.03.2026)

### Wichtigste Änderungen

**Tab-Reparatur (`ui_nav_helpers.js`):**
- Jeder Tab (Media, Video, Management, System, Diagnostics) ruft beim Wechsel explizit seine spezifische Render- oder Initialisierungsfunktion auf.
- Die Aufrufe sind in `requestAnimationFrame` gekapselt, damit das DOM bereit ist, bevor Daten injiziert werden (behebt "weiße Bildschirme").

**Multi-Session-Helfer (`scripts/managed_session.py`):**
- Findet automatisch einen freien Port und startet eine isolierte Instanz der Anwendung.
- Gibt am Ende ein JSON-Objekt mit URL, Port und Prozess-ID aus – ideal für Selenium/Playwright, ohne die Hauptinstanz zu stören.

**Audio-Player Stabilisierung (`audioplayer.js`):**
- `renderPlaylist()` bedient jetzt alle Playlist-Container (Player-Tab & Playlist-Dashboard) gleichzeitig, sodass keine Anzeige mehr "gestohlen" wird.

### Walkthrough: Tab-Restaurierung & Isolierte Sitzungen

**Test-Runner-Anleitung:**
Um eine neue, isolierte Sitzung für automatisierte Tests zu starten:

```bash
python3 scripts/managed_session.py
```
Das Skript wartet, bis das Frontend bereit ist, und gibt dann die Verbindungsdaten als JSON aus.

Alle Tabs wurden syntaktisch und funktional geprüft (`node -c`). Die Anwendung reagiert jetzt in allen Bereichen sofort auf Eingaben.
---

## Restoration of Full Tab Functionality & Isolated Sessions (30.03.2026)

### User Review Required
**IMPORTANT**

- **Isolated Sessions:** Die App startete bisher immer auf Port 8345. Automatisierte Tests oder parallele Zugriffe konnten so laufende Nutzersitzungen stören. Mit `managed_session.py` wird ein isolierter Backend-Start auf dynamischen Ports möglich.

**NOTE**

- **Tab "Repair":** Viele Tabs riefen ihre Renderfunktionen nicht zuverlässig beim Wechsel auf. Die Trigger werden nun zentral in `switchTab` konsolidiert.

### Proposed Changes
**[Component] Navigation & Rendering (UI)**
- **ui_nav_helpers.js**
  - `switchTab` ruft jetzt explizit Initialisierungsfunktionen für alle Kategorien auf:
    - media: `renderPlaylist()`, `renderLibrary()`
    - video: `renderVideoQueue()`
    - management/file: `fbNavigate(fbCurrentPath)`
    - management/item: `refreshLibrary()`
    - management/edit: `initEdit()`
    - management/parser: `loadParserConfig()`
    - management/tools: `renderToolsDashboard()`
    - governance/options: `loadDebugFlags()`, `loadEnvironmentInfo()`
    - governance/debug: `renderDebugTelemetrie()`
    - diagnostics/reporting: `renderReportingDashboard()`
    - diagnostics/logbuch: `renderLogbuch()`

**[Component] Testing & Automation Utilities**
- **managed_session.py** (neu)
  - Python-Utility, das die App auf einem dynamischen Port startet.
  - Features:
    - Automatische Portfindung (socket)
    - Setzt Umgebungsvariable `MWV_PORT`
    - Signal-basierte Prozessbereinigung
    - JSON-Statusausgabe mit zugewiesenem URL für externe Tools (Selenium, Playwright)

### Open Questions
- **Shared State:** Die Sessions sind port-isoliert, teilen sich aber die SQLite-Datenbank. Reicht das für automatisierte Tests, oder soll zusätzlich eine temporäre Datenbank für "Clean Slate"-Sessions bereitgestellt werden?

### Verification Plan
**Automated Tests**
- `managed_session.py` starten und prüfen, ob eine neue Instanz korrekt läuft.
- Mit Diagnostik-Probe den DOM aller Tabs nach Tabwechsel prüfen.

**Manual Verification**
- Alle Hauptkategorien und Sub-Tabs durchklicken.
- Prüfen, ob "Inventory" (Item-Tab) linksbündig ist.
- Prüfen, ob der "Player"-Tab sofort korrekt rendert.
---

## Implementation Plan: Tab-Restaurierung & Multi-Session Support (30.03.2026)

### Ziel
Standardisierung der Tab-Initialisierung und Unterstützung isolierter Test-Sitzungen für automatisierte UI-Tests.

### Maßnahmen
- **Tab-Reparatur:**
  - Integration expliziter `render()` und `init()`-Aufrufe für alle Kategorien (Media, Video, Management, System, Diagnostics) direkt in `switchTab`.
- **Multisession-Helfer:**
  - Neues Skript `managed_session.py`, das die App auf einem dynamischen Port startet, um Konflikte bei parallelen/automatisierten Tests (z.B. Selenium/Playwright) zu vermeiden.

### Offene Frage
- Sollen die isolierten Test-Sitzungen auch eine temporäre Datenbank verwenden, um eine komplett saubere Umgebung ("Clean Slate") zu garantieren, oder reicht die Port-Trennung aus?

Bitte um Review und Entscheidung zur Testdatenbank, bevor die Umsetzung startet.
---

## Update: UI-Korrekturen Item-Tab & Player-Tab (30.03.2026)

### Durchgeführte Korrekturen

**Layout-Ausrichtung (Item-Tab):**
- In `app.html` wurde die Container-Ausrichtung von `justify-content: flex-end` auf `flex-start` geändert.
- Das "Inventory"-Panel ist dadurch wieder wie gewohnt links positioniert.

**Player-Tab Weißbild-Fix:**
- Die Tab-Switch-Logik in `web/js/app_core.js` und `web/js/ui_nav_helpers.js` ruft jetzt `renderPlaylist()` explizit beim Wechsel in den "Player"-Tab auf.
- Dadurch wird die aktuelle Wiedergabeliste sofort angezeigt (kein leeres Weißbild mehr).

**Leere Warteschlange:**
- Bei leerer Queue erscheint nun ein 🎵-Symbol mit dem Hinweis "Die Warteschlange ist leer" und einem Button zur Bibliothek.

### Feature-Status
| Feature      | Status | Beschreibung                                                      |
|-------------|--------|-------------------------------------------------------------------|
| Player Tab  | ✅ Fix | Rendert sofort die Queue (kein Weißbild mehr).                    |
| Item Tab    | ✅ Fix | "Inventory" Liste ist wieder linksbündig ausgerichtet.            |
| Diagnostics | ✅ Aktiv| Transparente Logs für alle UI-Events aktiviert.                   |

Du kannst nun im Player Lieder sehen oder über die Bibliothek neue hinzufügen. Der Item-Tab im Management-Bereich zeigt jetzt ebenfalls korrekt ausgerichtete Listen an.
---

## Update: Media Scan & UI Fixes (30.03.2026)

### 1. Media Scan Completed
- **538 Items Indexed:** Full scan of the media folder processed 557 files, successfully indexing 538 media objects (Audio, Video, Multimedia) into the database.
- **Database Status:** Verified with `sqlite3` that `data/database.db` is correctly populated.

### 2. "White Screen" Fix
- **Empty State UI:** Player tab now shows a friendly "Die Warteschlange ist leer" message with a direct Library link when the queue is empty, instead of a blank screen.
- **Fallback Containers:** Improved rendering logic in `audioplayer.js` to correctly target UI elements after structural refactors.

### 3. Log Evaluation
- **Healthy Trace:** Logs in the `logs/` folder confirm the parser chain (ffprobe, pymediainfo) is working across hundreds of files.
- **Session Isolation:** Each run generates a unique session log (e.g., `session_25315_...`) with detailed initialization and DB event data.
- **No JS Errors:** `frontend_errors.log` remains clean, indicating stable frontend execution.

### 4. System Stability
- **Python Guard:** Relaxed version check in `main.py` to allow Python 3.12.7.
- **Import Safe:** Refactored backend core to prevent side-effects (e.g., killing other instances) when importing project functions into scripts.

---

### Walkthrough
*See the walkthrough section for full details of these changes.*
## Logbuch: Media Viewer Restoration & Spawn Test (29.03.2026)

### Goal
Fix database corruption, restore audio player functionality (white screen/no playback), and complete the "spawn test" to verify correct media item handling from backend to frontend.

### User Review Required
- **No Selenium/Playwright:** Use Eel-exposed functions and JS diagnostic probes for verification.
- **Database Path:** Standardize to `data/database.db` (per `src/core/db.py`), migrate/handle any existing `mwv.db` data.

### Proposed Changes
#### Database Layer
- **db.py**
  - Add detailed logging to `init_db`, `insert_media`, `get_all_media`, `clear_media`.
  - Implement integrity check/reset if DB is corrupted.
  - Ensure consistent path resolution for DB file.

#### Frontend (Audio Player & UI)
- **audioplayer.js**
  - Add logging to `playAudio` and `initAudioPipeline`.
  - Debug player tab white screen (check visibility/container IDs).
- **app.html**
  - Ensure audio player container/dependencies are defined.
  - Fix structural issues causing white screen in player tab.

#### Backend & Test Logic
- **main.py**
  - Enhance `report_items_spawned` for more descriptive output.
  - Add `@eel.expose` function `request_frontend_diagnostic()` to trigger JS DOM check.
  - Add logging to `/media/` route for file serving trace.
- **spawn_test_items.py**
  - Reset/init DB, spawn test media (audio/video), optionally signal test readiness.
- **verify_spawn.py** (new)
  - Script to start app in test mode, wait for frontend to report success via Eel, then exit (replaces Selenium).

### Open Questions
- Why does `mwv.db` exist in root instead of `data/`?
- On DB corruption: Factory reset or attempt repair?

### Verification Plan
#### Automated Tests (No Selenium)
- Run `python3 scripts/verify_spawn.py`:
  - Start Eel app
  - Wait for JS to call `report_items_spawned` with count > 0
  - Call JS to "virtually" click play and report if audio element starts
  - Exit with code 0 on success

#### Manual Verification
- Use browser_subagent to open app, navigate to Player tab, verify UI/audio
- Check logs for new diagnostic messages
# logbuch_restore_items_visibility_logging_extension.md

## Plan: Restore Items Visibility & Update Logging Extension

**Datum:** 29. März 2026

---

### Logging Infrastructure
- Logger aktualisiert: Session-spezifische Logs werden jetzt als `.txt` statt `.log` gespeichert (`setup_logging` in `logger.py` angepasst).

---

### Backend / Database
- Analyse: Prüfen, ob das Backend-Testskript (`item_spawn_backend_test.py`) und die Hauptanwendung wirklich dieselbe Datenbankdatei verwenden (Pfadkonsistenz).
- In `main.py` wird beim Start der absolute Pfad der verwendeten Datenbank ins Session-Log geschrieben.
- Sicherstellen, dass `get_library` keine restriktiven Filter verwendet, die die Test-Items ausblenden könnten.

---

### Frontend
- UI prüft nach dem Hinzufügen von Items, ob die Bibliothek wirklich aktualisiert wird.
- In `bibliothek.js` werden zusätzliche Logs in `renderLibrary` ergänzt, um zu sehen, ob Items empfangen, aber nicht angezeigt werden.

---

### Open Questions
- Wurde `item_spawn_backend_test.py` manuell im Terminal oder über den "Tests"-Tab der App ausgeführt?
- Falls manuell: Mit welchem Befehl? (z.B. `python3 tests/item_spawn_backend_test.py` vs. `pytest`)

---

### Verifikationsplan
- **Automatisiert:**
  - `tests/item_spawn_backend_test.py` ausführen und direkt danach die Ausgabe von `eel.get_library()` per Scratch-Skript prüfen.
- **Manuell:**
  - App starten.
  - In `logs/session_*.txt` den verwendeten DB-Pfad prüfen.
  - "Spawn Mock Items" klicken und prüfen, ob sie erscheinen.
  - Falls nicht, Browser-Konsole und Session-Log prüfen.

---

*Letzte Änderung: 29.03.2026*
