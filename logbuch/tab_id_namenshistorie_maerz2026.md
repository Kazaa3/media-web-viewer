# Namenshistorie & Rückkehrmöglichkeit: Tab- und Panel-IDs – März 2026

## Hintergrund
Im Zuge von Refactoring und UI-Modernisierung wurden die IDs der wichtigsten Tabs, Panels und UI-Elemente mehrfach angepasst. Für automatisierte Tests, UI-Selektoren und die langfristige Wartbarkeit ist eine konsistente Benennung entscheidend.

## Aktuelle required_ids
- active-queue-tab-trigger (Player)
- coverflow-library-tab-trigger (Bibliothek)
- filesystem-crawler-tab-trigger (Datei)
- system-registry-tab-trigger (Optionen)
- app-footer
- sync-indicator
- main-split-container
- qa-validation-tab-trigger (Tests)
- documentation-journal-tab-trigger (Logbuch)
- media-orchestrator-tab-trigger (VLC/Video)

## Historische/weitere IDs im Code
- indexed-sqlite-repository-tab-trigger (Item)
- crud-metadata-tab-trigger (Edit)
- chain-config-tab-trigger (Parser)
- telemetry-inspector-tab-trigger (Debug)
- reporting-dashboard-tab-trigger (Reporting)
- sequential-buffer-tab-trigger (Playlist)
- footer-artwork-raster-buffer (Footer-Artwork)

## Erkenntnisse & Empfehlung
- Die aktuelle required_ids-Liste ist ein Subset der alten IDs – ein Rollback auf die alten Namen ist jederzeit möglich.
- Für Regressionstests und Legacy-Kompatibilität empfiehlt es sich, die alten IDs im Code zu belassen oder als Alias vorzuhalten.
- Ein konsistentes ID-Schema erleichtert Migration, Testautomatisierung und UI-Refactoring.

## Lessons Learned
- Namensänderungen sollten immer dokumentiert und versioniert werden.
- UI-Tests und Selektoren müssen bei ID-Änderungen mitgepflegt werden.
- Rückkehr zu bewährten ID-Schemata ist jederzeit möglich, solange die Historie nachvollziehbar bleibt.

---

## Fix Footer, Tabs, and Startup Speed (März 2026)

### Ziel
UI- und Performance-Probleme im gui_media_web_viewer nachhaltig beheben:
- Audio-Player-Footer und Statusbar als einheitlicher, fixierter Bereich am unteren Rand
- Parser, Debug, Tests als unabhängige Tabs (keine Verschachtelung)
- Startup-Optimierung: UI-Start priorisieren, Blockaden vermeiden

### Umsetzung
#### UI Fixes (web/app.html)
- **Audio Player Footer & Statusbar:**
  - `.player-container` auf `position: fixed; bottom: 0; left: 0; right: 0;` gesetzt
  - `body { padding-bottom: ... }` ergänzt
  - Statusbar (#app-footer) mit Player-Controls in einen gemeinsamen Footer-Bereich zusammengeführt
- **DIV-Balance & Tabstruktur:**
  - Systematische Korrektur aller DIV-Imbalancen (analyze_divs_verbose.py, Ziel: Level 0 am Body-Ende)
  - Parser, Debug, Tests als unabhängige Sibling-Tabs, nicht in Options verschachtelt

#### Startup-Optimierung (src/core/main.py)
- **UI-Start priorisieren:**
  - `ensure_singleton()` und andere schwere Checks nach eel.start() oder in Hintergrund-Thread verschoben
  - Blockierendes `time.sleep(2.0)` entfernt oder asynchronisiert
  - env_handler.validate_safe_startup in Hintergrundphase ausgelagert
- **Profiling:**
  - _ensure_project_venv_active und eel.start auf Verzögerungen geprüft (10-30s Delay identifiziert)

### Verifikationsplan
- **Automatisierte Tests:**
  - analyze_divs_verbose.py: Level 0 am Body-Ende
  - Manuelle Tab-Checks: Options/Architektur → Parser → Debug → Tests (keine Verschachtelung)
  - Startup-Profiling: UI erscheint schnell, Hintergrundtasks laufen weiter
- **Manuelle Checks:**
  - Footer bleibt beim Scrollen immer sichtbar, Statusbar und Player-Controls sind vereint
  - Tabs funktionieren unabhängig

### Lessons Learned
- Konsolidierter Footer verbessert UX und Übersichtlichkeit
- DIV-Balance-Analyse ist Pflicht für große HTML-Dateien
- Früher UI-Start und Hintergrundinitialisierung erhöhen die Responsivität
- Tabstruktur muss regelmäßig auf Verschachtelungsfehler geprüft werden

---

## Logbuch: Startup- und Parser-Trace, Fehleranalyse (März 2026)

### Startup-Log & Beobachtungen
- Python 3.12.7, venv (.venv_run), Chromium wird im App-Mode gestartet
- Startup-Optimierung: UI erscheint früh, Hintergrundtasks (Scan, DB, Parser) laufen asynchron weiter
- Warnings zu charset_normalizer und urllib3/chardet – keine unmittelbare Auswirkung, aber für spätere Kompatibilität prüfen

### Parser- und Scan-Trace
- Media-Scan erkennt und indiziert Ordner und Filme korrekt
- Artwork-Extraktion für Ordner/Filme läuft, aber oft kein passendes Cover gefunden (Final success: False)
- Audio-Parsing: Fehler bei music_tag-Parser (duration), einige Skips bei anderen Parsers, aber keine Blockade
- Einzelne Dateien (z.B. FLAC, WAV) werden mit mehreren Parsern durchlaufen, Fehler werden geloggt, aber System bleibt stabil

### Fehler & Hinweise
- AttributeError: 'NoneType' object has no attribute 'receive' (bottle_websocket/eel) – tritt auf, wenn kein WebSocket-Client verbunden ist; kann ignoriert werden, solange keine UI-Funktionalität fehlt
- HTTP 500 für fehlende Icons (SVGs) – statische Assets prüfen
- Keine Blockade oder Crash, Backend bleibt responsiv

### Lessons Learned
- Startup-Optimierung funktioniert: UI ist schnell sichtbar, Backend arbeitet im Hintergrund
- Parser-Fehler werden robust abgefangen, Logs sind ausreichend detailliert
- Warnings zu Dependencies und fehlende Cover sollten mittelfristig adressiert werden
- WebSocket-Fehler sind harmlos, solange keine UI-Funktionalität betroffen ist
