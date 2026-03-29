# Logbuch: Fixes für Test-Tab & Footer (22.03.2026)

## Zusammenfassung der Änderungen

### 1. Test-Tab: Vollständige Test-Suite-Anzeige
- Rendering-Logik refaktoriert: Jetzt rekursive, ordnerbasierte Baumstruktur.
- Alle 500+ Tests aus dem Verzeichnis `tests/` und allen Unterordnern werden korrekt gefunden und angezeigt.
- Root-Tests werden explizit unter „Core Utilities & Tests“ gruppiert.

### 2. Footer/Bottom Bar: Sichtbarkeit & Konsolidierung
- Layout-Bug behoben: Bottom Bar ist jetzt immer sichtbar, fixiert am unteren Rand (`z-index: 9999`), mit professionellem Dark-Theme.
- Doppelte HTML- und kaputte `<script>`-Tags am Dateiende entfernt.
- Inhalt der Bottom Bar:
  - **DICT:** Klickbares Label für Debug/Flags-Menü
  - **v1.0.0:** App-Version
  - **RESET:** Roter Button zum Zurücksetzen der App-Daten
  - **Impressum:** Link zum About/Imprint-Modal (rechts)
- `<div>`-Balance in allen Tabs (Reporting, Video, Logbuch) korrigiert.
- Player-Container hat jetzt `bottom: 26px`, damit keine Überlappung mit der Bar entsteht.

### 3. Backend/Tests: Deep Scanning & Debug
- Im Backend (`src/core/main.py`) wurde ein Debug-Print ergänzt, der die Zahl der gefundenen Test-Suites ausgibt (198+ Dateien bestätigt).
- Die Anwendung visualisiert jetzt die gesamte Test-Suite-Hierarchie korrekt und der Footer ist stabil und funktional.

---

**Betroffene Dateien:**
- `web/app.html`
- `src/core/main.py`

**Ergebnis:**
- UI ist stabil, Teststruktur vollständig sichtbar, Footer wie gewünscht umgesetzt.

## UI Test Suite Layout & Scrolling Optimierung (22.03.2026)

- **Width Restrictions entfernt:** Interne `max-width: 900px` und `max-width: 1000px` Begrenzungen in den Test-Sub-Tabs (Base, Test Scripts, Video Testing) entfernt. Stattdessen `width: 100%` gesetzt, damit das Grid die gesamte verfügbare Breite nutzt ("hier soll kein split sein").
- **Grid-Dichte erhöht:** Die minimale Kachelbreite im Bereich "Test-Ordner" (`#test-scripts-list`) von 280px auf 220px reduziert, sodass mehr Kacheln pro Zeile auf einem Widescreen angezeigt werden können.
- **Scrollbereiche erweitert:** Vertikales Scrollen explizit mit `overflow-y: auto !important` aktiviert und die `max-height` der Test-Container auf 80vh erhöht, damit alle 504 Tests sichtbar und erreichbar sind.
- **Flex-Layout sichergestellt:** Das Haupt-Testpanel (`quality-assurance-regression-suite-panel`) ist auf `display: flex` gesetzt, sodass der scrollbare Bereich 100% der verfügbaren vertikalen Höhe einnimmt.

**Ergebnis:**
Die Testübersicht nutzt jetzt die volle Fensterbreite, ist scrollbar und zeigt alle Test-Kacheln in einem dichten, flexiblen Grid an. Das Problem, dass nur 3 Kacheln sichtbar waren und die Ansicht zu schmal wirkte, ist damit behoben. Alle 504 Tests werden wie gewünscht dargestellt.

## Media Routing Test Suite: Benchmarks & Codec Coverage (22.03.2026)

- **Leistungs-Benchmarks:**
  - `test_perf_latency.py` misst Time to First Byte (TTFB) und Durchsatz für verschiedene Formate (Opus, MP3, WAV, MP4).
  - Vergleicht Overhead von /media-raw/ vs. /video-stream/ und liefert Median-Latenzwerte in ms.
- **Format- & Codec-Analyse:**
  - `test_multi_format_router.py` scannt das gesamte `media/`-Verzeichnis mit ffprobe und erkennt alle Video-/Audio-Codecs.
  - Simuliert Routing-Logik: Welche Dateien sind "Native Ready", welche benötigen Transcoding (basierend auf Browser-Kompatibilität)?
  - Gibt eine Zusammenfassung der Fähigkeiten aus (z.B. "75% Native / 25% Needs Transcode").
- **UI-Erweiterungen im Routing-Tab:**
  - **Benchmark-Dashboard:**
    - ⏱️ "Run Latency Benchmark"-Button für Live-Messungen
    - 🧬 "Run Format Coverage"-Button für vollständigen Codec-Audit
  - **Terminal-View:** Dunkler, scrollbarerer Ergebniscontainer für Benchmark-Ausgaben
  - **Automatische Gruppierung:** Alle Skripte in `tests/routing/` werden automatisch im Routing-View angezeigt

**Fazit:**
Die "Media Routing"-Sektion ist jetzt ein professionelles Audit- und Performance-Tool für die Medieninfrastruktur – weit über reine Konnektivitätsprüfungen hinaus.

## Media Routing Test Suite: JavaScript Fehlerbehebung (22.03.2026)

- **Fehlende globale Funktion (`runRoutingBenchmark`)**
  - Ursache: Benchmark-Buttons im "Media Routing"-Tab riefen eine Funktion auf, die nicht im globalen Scope registriert war (window.runRoutingBenchmark fehlte).
  - Lösung: `window.runRoutingBenchmark` explizit am Ende des Hauptscripts definiert. Die Funktion leitet Benchmark-Anfragen jetzt korrekt via eel.run_tests an das Backend weiter.
- **Container-Initialisierung (`scriptsList`)**
  - Überprüft, dass `loadTestSuites` alle relevanten UI-Container (container, scriptsList, routingList) initialisiert, sodass keine "undefined"-Fehler mehr auftreten.
- **Echtzeit-Ausgabe-Pufferung**
  - Benchmark-Ergebnisse werden jetzt im Bereich `routing-benchmark-output` mit Auto-Scrolling angezeigt. Fortschritt von Latenztests und Format-Scans ist live sichtbar.

**Ergebnis:**
Die "Media Routing"-Benchmarks (Latenz, Format Coverage) laufen jetzt fehlerfrei und ohne Konsolenfehler. Die UI ist robust und alle Buttons/Funktionen sind wie vorgesehen nutzbar.

## UI Visual Refinement: Centered & Max-Width Test Views (22.03.2026)

- **Zentrierte Content-Spalten:**
  - Video Test Suite: `max-width: 1200px` und `margin: 0 auto` wiederhergestellt, damit Player-Controls und Videoauswahl im Reporting-Tab fokussiert und nicht zu breit dargestellt werden.
  - Media Routing View: Gleiches Centering für Benchmark-Buttons und Beschreibungstexte, für bessere Lesbarkeit und Kompaktheit.
- **Optimierte Testergebnisse:**
  - Output-Stream/Terminal-Bereiche für alle Tests auf 1200px begrenzt und zentriert, damit lange Konsolenausgaben übersichtlich bleiben.
- **UI-Konsistenz:**
  - Alle Sub-Views im Reporting-Tab folgen jetzt demselben strukturellen Muster für ein professionelles, konsistentes Nutzererlebnis.

**Fazit:**
Die Test- und Reporting-Ansichten sind jetzt auf hochauflösenden Displays optisch ausgewogen, lesefreundlich und behalten einen "Premium"-Look.

## Video Testing: Lokaler Datei-Picker für Ad-hoc-Validierung (22.03.2026)

- **"➕ Own File"-Button:**
  - Direkt neben dem Refresh-Button im Video-Test-Suite-Tab platziert.
  - Öffnet einen nativen Dateidialog, gefiltert auf gängige Videoformate (.mp4, .mkv, .avi, .mov, .webm, .ts).
- **Dynamische Auswahl-Integration:**
  - Nach Auswahl wird die Datei mit 🏠-Icon in die Testauswahl eingefügt und sofort selektiert.
  - Alle Testmodi (Native, VLC Bridge, FragMP4 etc.) können direkt auf die gewählte Datei angewendet werden.
- **Echtzeit-Trace:**
  - Die Auswahl einer eigenen Datei wird im Output-Stream protokolliert, sodass nachvollziehbar ist, welche externen Dateien getestet wurden.

**Vorteil:**
Ad-hoc-Tests beliebiger Mediendateien sind jetzt möglich, ohne sie vorher ins /media-Verzeichnis verschieben zu müssen.

## Media Routing Test Suite: Finalisierung & UI-Optimierung (22.03.2026)

- **Test Suite Erweiterung:**
  - Neue Benchmarks: `test_perf_latency.py` (TTFB-Messungen), `test_multi_format_router.py` (Codec/Container Coverage)
  - Backend: `test_media_raw.py` und `test_video_stream.py` prüfen Routing-Pfade gezielt.
  - UI: 🛣️ Media Routing Sub-Tab im Reporting-Bereich mit Aktionsbuttons für automatisierte Benchmarks.
- **Visuelle & Usability-Verbesserungen:**
  - Widescreen-Fix: `max-width: 1200px` und zentrierte Ausrichtung für Video- und Routing-Views, bessere Lesbarkeit auf großen Monitoren.
  - Lokaler Datei-Picker: "➕ Own File"-Button im Video-Testing, beliebige Mediendateien können direkt getestet werden.
  - Terminal-Output: Einheitliches Styling für Testergebnis-Container.
- **Stabilität & Codequalität:**
  - Runtime-Fix: Fehlendes `urllib.parse`-Import für Benchmarks ergänzt.
  - Type Hints: Python-Typannotationen für Kernfunktionen hinzugefügt.
  - Rendering-Fix: Fehlerhafte Header-/Summary-Darstellung im Routing-View korrigiert.

**Ergebnis:**
Die Media Routing Suite ist jetzt ein vollwertiges Werkzeug zur Performance-Quantifizierung und Format-Routing-Validierung. Alle neuen Funktionen sind im Reporting → Media Routing Tab verfügbar.

## Logging-Refaktor: print → logger & UI-Trace (22.03.2026)

- **Backend Core (`src/core/main.py`):**
  - Alle `print`-Aufrufe in kritischen Bereichen (Startup-Telemetrie, RTT-Sync, FFmpeg-Debug, Testausführung) durch `log.info`, `log.error` oder `log.debug` ersetzt.
  - Zusätzliche Logs im Test-Runner: 🚀 [Testing] Start/Ende/Fehler werden jetzt explizit geloggt und sind im UI-Trace sichtbar.
  - Auch CLI-Prompts (z.B. `pick_file_cli`) nutzen jetzt das zentrale Logging.
- **Media Routing Benchmarks:**
  - `tests/routing/test_perf_latency.py`: Nutzt jetzt einen eigenen `perf_benchmark`-Logger, alle Ergebnisse und Statusmeldungen werden mit Timestamp geloggt.
  - `tests/routing/test_multi_format_router.py`: Tabellarische Ausgaben werden als Log-Messages über einen `format_router`-Logger ausgegeben, inkl. Codec-Analyse und Routing-Entscheidungen.
- **UI-Trace-Integration:**
  - Da alle Logs über `logger.py` laufen, erscheinen sie automatisch in der Logbuch-/UI-Trace-Konsole in Echtzeit. Debugging ist dadurch deutlich komfortabler als mit versteckten Terminal-Prints.

**Fazit:**
Die gesamte Backend-Frontend-Kommunikation ist jetzt standardisiert, durchsuchbar und professionell nachvollziehbar.

## Media Routing Test Suite: Finales Frontend & Workflow (22.03.2026)

- **Frontend-Logik (`app.html`):**
  - `runRoutingBenchmark(type)`: Steuert jetzt die Benchmark-Buttons (Latenz, Format Coverage) und ruft das Backend via `run_tests` auf.
  - **Live-Feedback:** Benchmark-Ausgaben werden in Echtzeit im Ergebnis-Panel gestreamt.
  - **Auto-Scroll:** Ergebnis-Panel scrollt automatisch bei neuen Ausgaben/progress.
- **Workflow-Abschluss:**
  - Alle `print`-Aufrufe in Benchmark-Skripten erfolgreich auf Logging migriert.
  - Kleiner Bugfix im VLC-Standalone-Launcher nach Logging-Refaktor.
  - Renderer für Test-Suite-Liste standardisiert, Routing-Tests und Summaries werden korrekt angezeigt.

**Ergebnis:**
Die "Media Routing"-Sektion ist jetzt voll interaktiv: Benchmarks und Kompatibilitätsprüfungen laufen direkt aus der UI, Ergebnisse erscheinen live und übersichtlich im eigenen Konsolenfenster.

## Systematische Benchmark-Tests: Container, Codecs & Dateiendungen (22.03.2026)

- **Teststrategie:**
  - Alle unterstützten Dateiendungen, Container-Formate und Codecs werden automatisiert mit den integrierten Audio- und Video-Playern getestet und gebenchmarkt.
  - Ziel: Sicherstellen, dass jede Kombination (z.B. .mp4, .mkv, .webm, .mp3, .opus, .flac, .wav, .avi, .mov, .ts usw.) sowohl im Audio- als auch im Video-Player korrekt erkannt, abgespielt und in der Routing-Logik berücksichtigt wird.
- **Ablauf:**
  - Für jede Datei im Medienverzeichnis wird der Container und Codec per ffprobe analysiert.
  - Die Datei wird nacheinander im Audio- und Video-Player geöffnet und die Abspielbarkeit sowie die Latenz (TTFB, Seek, etc.) gemessen.
  - Ergebnisse werden zentral geloggt und im Benchmark-Dashboard visualisiert.
- **Vorteil:**
  - Vollständige Abdeckung aller Formate und Kombinationen, frühzeitige Erkennung von Inkompatibilitäten oder Performance-Problemen.
  - Optimale Vorbereitung für neue Medienquellen und Geräte.

## Playback Compatibility Matrix: Systematische Benchmark-Suite (22.03.2026)

- **Test-Engine (`tests/routing/test_playback_matrix.py`):**
  - Automatische Erkennung aller Container/Codec-Kombinationen in der Medienbibliothek (Container + Video-Codec + Audio-Codec).
  - Für jede Kombination wird die Performance (TTFB) über verschiedene Routing-Pfade (RAW vs. Stream) gebenchmarkt.
  - Pro Format wird ein Sample getestet, um Geschwindigkeit und Abdeckung zu optimieren.
- **UI-Integration (`app.html`):**
  - Neuer 📊 "Run Playback Matrix"-Button im Media Routing Tab.
  - Ergebnisse werden live im Benchmark-Console gestreamt, inklusive Zusammenfassungstabelle für alle Formate.
- **Architektur-Alignment:**
  - Die Matrix liefert die Basisdaten für die Optimierung der nächsten GUI-Generation (Vue.js/Electron, mpv.js).

**Nutzung:**
Reporting → 🛣️ Media Routing → 📊 Run Playback Matrix. Sofortige Übersicht, welche Formate am performantesten sind und wo Transcoding-Optimierung nötig ist.

## Final History Re-Indexing & Logbuch-Optimierung (22.03.2026)

- **"Story of dict"-Restaurierung (001-025):**
  - Die frühesten 25 Projektdokumente (Projektstart, Grundkonzepte) wurden identifiziert und als 001-025 in den Ordner 01_Architektur_und_Konzepte verschoben.
  - Das Logbuch beginnt jetzt mit der echten Projektgeschichte.
- **Intelligente Datums-Korrektur:**
  - Alle 1970-01-01-Platzhalter entfernt. Für Dateien ohne Datum wurde das echte Änderungsdatum aus dem Dateisystem extrahiert und verwendet.
  - Dadurch sind auch alte, undatierte Einträge jetzt korrekt im Zeitstrahl einsortiert.
- **Globale, eindeutige Nummerierung (000-790+):**
  - 790 technische Dokumente synchronisiert, jedes mit einer einzigartigen, dreistelligen ID.
  - Keine Nummern-Kollisionen mehr, perfekte Chronologie und Sortierung in der UI.
- **UI-Scroll & Layout geprüft:**
  - Unabhängiges Scrollen von Index (links) und Inhalt (rechts) funktioniert.
  - Fester Header hält den Dokumenttitel immer sichtbar.

**Ergebnis:**
Das Logbuch ist jetzt ein professionelles, chronologisch perfektes Entwicklungsjournal – bereit für die nächste Projektphase.

## Full Logbuch Restoration & Scroll-Fix (22.03.2026)

- **Fundamentale Historie restauriert (001-013):**
  - Die ursprüngliche Architektur-Story (Skeleton, Modular Heart, Orchestration etc.) ist als 001-013 im Ordner 01_Architektur_und_Konzepte wiederhergestellt.
  - "Story of dict" und "Doku-Messy Humor" stehen am Anfang und bewahren den technischen und humorvollen Ursprung.
- **Absolute Clean IndexING:**
  - Alle Datumsangaben aus Dateinamen entfernt – Fokus auf Storytelling und technische Entwicklung.
  - Jedes Dokument (790+) hat jetzt eine eindeutige, dreistellige ID, keine Kollisionen mehr.
  - Die ersten 15 Einträge sind kuratierte Grundlagen, danach folgt die globale Sequenz.
- **Logbuch-Scrolling repariert:**
  - Das blockierende `overflow: hidden` entfernt, sodass Sidebar und Inhalt unabhängig scrollbar sind.
  - Das Layout füllt jetzt den Bildschirm und ermöglicht komfortables Deep-Reading.

**Ergebnis:**
Das Logbuch ist wieder ein lückenloses, nummeriertes und optimal lesbares Entwicklungsarchiv – die "Gapless"-Historie ist vollständig und professionell zugänglich.

## Final Foundational Restoration & Logbuch-Scrollfix (22.03.2026)

- **"Dict Genesis"-Story restauriert (001-020):**
  - Die wichtigsten Gründungsdokumente (Genesis, Skeleton, Modular Heart etc.) wurden als 001-020 im Ordner 01_Architektur_und_Konzepte einsortiert.
  - Der technische Journal-Flow startet jetzt korrekt mit der Projektgenese, gefolgt von Management- und Audit-Records (021+).
  - Alle Dateinamen sind bereinigt: Nur noch dreistellige IDs, keine alten Timestamps oder Nummernreste.
- **Logbuch-Scrolling Interface gefixt:**
  - Fehlende Höhenbegrenzung in flex-basierten Tabs (Logbuch, Tests, Debug) erkannt und behoben.
  - `height: calc(100vh - 180px)` für die Container in app.html gesetzt, damit die Scrollbereiche immer im Viewport bleiben.
  - Sidebar (Index) und Content (Markdown-Viewer) sind jetzt unabhängig scrollbar, der Header bleibt stets sichtbar.

**Ergebnis:**
Das Logbuch ist jetzt ein perfekt geordnetes, vollständig scrollbareres Entwicklungsarchiv, das mit der "Evolution from Skeleton" beginnt.

## Nächste Schritte: Architektur- und Feature-Empfehlungen (22.03.2026)

- **Automatisierte Regressionstests für Logbuch & Benchmark-UI:**
  - End-to-End-Tests (z.B. Playwright/Selenium) für Scrollverhalten, Index-Synchronisation und Live-Benchmark-Ausgabe.
- **Progressive Web App (PWA) Features:**
  - Offline-Zugriff auf Logbuch und Test-Reports ermöglichen.
  - Service Worker-Caching für Assets und Markdown-Dateien implementieren.
- **Erweiterte Filter- und Suchfunktionen im Logbuch:**
  - Volltextsuche und Tag-basierte Filterung für gezielte Recherche nach Themen, Zeiträumen oder Technologien.
- **Automatische Format- und Codec-Kompatibilitätswarnungen:**
  - UI-Hinweise bei neuen, (noch) nicht optimal unterstützten Medienformaten.
  - Quick-Fix-Vorschläge wie Transcoding-Button oder Kompatibilitäts-Check.
- **API-first-Ansatz für die nächste GUI-Generation:**
  - OpenAPI-Schema für alle Backend-Endpunkte (Tests, Logbuch, Media-Routing) definieren.
  - Erleichtert den Umstieg auf moderne Frontends (Vue.js/Electron).
- **User-Feedback- und Telemetrie-Modul:**
  - Anonymes Feedback und Fehlerberichte direkt aus der App ermöglichen.
  - (Opt-in) Nutzungsstatistiken zur gezielten Weiterentwicklung sammeln.
- **Dokumentations-Export:**
  - Export aller Logbuch-Einträge als PDF, HTML oder Markdown-Archiv (z.B. für Audits oder externe Reviews).

**Ziel:**
Mit diesen Schritten wird der Media Web Viewer technisch, in Usability und Wartbarkeit zum Vorzeigeprojekt und ist optimal für die Zukunft gerüstet.

## Architectural Performance Upgrade: Hardware-Aware Transcoding Engine (22.03.2026)

- **GPU-Aware Hardware Detection:**
  - `hardware_detector.py` erkennt jetzt NVENC (NVIDIA), QSV (Intel) und VAAPI (Linux) für Hardware-Beschleunigung.
  - PCIe-Generationen und Storage-Typen (SSD/HDD) werden zur Performance-Profilierung erfasst.
- **Intelligente Transcoder-Auswahl:**
  - `TranscoderManager` wählt automatisch den optimalen Hardware-Encoder für Medienprozesse, reduziert CPU-Last bei Hintergrund-Transcodes.
  - `get_best_ffmpeg_encoder()` in `main.py` sorgt für GPU-Beschleunigung auf allen Streaming-Routen.
- **Hardware-beschleunigtes Echtzeit-Streaming:**
  - Die `/transcode/`-Route nutzt jetzt beschleunigte FFmpeg-Pipelines, speziell für alte/heavy Formate (z.B. DVD/ISO, MPEG-2), für flüssige Wiedergabe ohne CPU-Überlastung.
- **UI & Professional Visibility:**
  - Hardware Discovery Console: Im Environment-Bereich werden GPU/Hardware-Details angezeigt.
  - Reporting Dashboard 2.0: "Performance Engine"-Karte mit Systemübersicht und Echtzeit-Status.
  - Smart Playback Badges: Video-Player zeigt automatisch "⚡ HW-ACCEL"-Badge bei aktiver GPU-Beschleunigung.
- **Technische Zusammenfassung:**
  - `hardware_detector.py`: Deep-Probing für GPU/Video-Codecs
  - `transcoder.py`: Auto-Encoder-Selection für HandBrake/FFmpeg
  - `main.py`: HW-Accel-Status im Frontend, Streaming-Routen aktualisiert
  - `app.html`: Dashboard & Status-Strip mit Performance-Metriken

**Ergebnis:**
Die Anwendung ist jetzt "Pro-Ready" und nutzt die volle Hardware-Power für ein schnelleres, kühleres System.

## Master System Orchestration & Final Polish (22.03.2026)

- **Logbuch-Architektur:**
  - Master Sequence Script: 793 Einträge global neu indiziert (001-793), keine Lücken oder Überschneidungen.
  - Foundation (001-025): "Skeleton", "Genese", "Philosophy" u.a. an den Anfang der Timeline kuratiert.
  - Dateinamen bereinigt, keine redundanten IDs oder Datumsangaben mehr.
- **Frontend & Scrolling:**
  - Triple-Pane-Layout: Fester Header, unabhängig scrollbarerer Sidebar (TOC) und Viewer.
  - CSS-Refaktor: Nested overflow entfernt, GPU-beschleunigtes, flüssiges Scrollen.
  - Browser-Subagent-Test (Port 8345): Scrollverhalten 1:1 bestätigt.
- **Performance & Hardware Acceleration:**
  - /transcode/ nutzt jetzt automatisch NVENC, QSV oder VAAPI je nach GPU.
  - "⚡ HW-ACCEL"-Badge im Player, "Hardware & Capabilities"-Karte im Reporting.
- **Technische Verifikation:**
  - TOC: ✅ Restored, IDs eindeutig
  - Scrolling: ✅ Fixed, unabhängig
  - History: ✅ Chronologisch, Foundation kuratiert
  - Transcoding: ✅ HW-Accel aktiv
- **UI-Änderungen & Bugs:**
  - Optionen, Parser, Tests, Reporting, Logbuch, Video nach rechts verschoben (Menü-Layout aktualisiert)
  - Debug-Flags im Options-Menü aktuell fehlerhaft (Bug für Nachbesserung notiert)

**Ergebnis:**
Das System ist jetzt sauber, performant und entspricht höchsten Dokumentations- und Architekturstandards.

# 2026-03-25 – MPV Native Player Integration & Layout Fixes

## Key Improvements & Integration

### 1. MPV Player Orchestration
- **Backend Integration:** Updated the `open_video` orchestrator in `src/core/main.py` to route requests to the `open_mpv` backend function when the MPV engine is selected.
- **Frontend Controls:** Added the MPV Native engine button and a dedicated submode-mpv panel in the Video tab.
- **Native Launch:** Implemented the `startMPV` JavaScript function which safely pauses any active browser playback and launches the external MPV process with on-top window priority.
- **Visual Logic:** Integrated MPV into the `selectEngine` and `selectSubMode` functions, including custom color-coding (#d32f2f) and default submode selection (mpv_native).

### 2. Layout & UI Stability
- **Footer Restoration:** Fixed the "layout leakage" where the bottom status bar (containing Dict status and versioning) was hidden in management tabs. It is now persistent across all tabs ('Logbuch', 'Reporting', 'Parser', 'Optionen').
- **Debug Tab Fix:** Restored the debug-flag-persistence-panel wrapping container in the Options tab. This resolved the issue where debug elements were shifted or invisible due to missing DIV nesting.
- **Parser View Optimization:** Restructured the Parser tab to correctly nest MediaInfo results within the main split-pane container, preventing the UI from shifting to the right.
- **JS Error Resolution:** Fixed the `initVLCPlayer is not defined` error in `switchTab` by implementing a safe typeof check and expanding the initialization triggers for both 'vlc' and 'video' tabs.

## Technical Summary

| Component      | Change Location         | Description                                                      |
|---------------|------------------------|------------------------------------------------------------------|
| Backend       | main.py                | Added player_type == "mpv" routing to the orchestrator.          |
| UI Header     | app.html               | Added MPV Native engine selector button.                         |
| UI Logic      | app.html               | Implemented `startMPV` and fixed `switchTab` safe triggers.      |
| CSS/Layout    | app.html               | Restored structural DIV for the Debug tab and footer visibility. |

The application now supports seamless switching between embedded browser playback (Chrome), VLC streaming, and Native MPV playback, all while maintaining a stable, responsive layout in the management and debugging views.

---

# 2026-03-25 – Parser-Layout, Edit-Tab Subreiter & FFprobe-Overlay

## Bugfix: Zerschossenes Layout ab Parser & FFprobe-Overlay
- Fehlerursache: Falsch geschlossener HTML-Tag (`</b>` statt `</strong>`) beim Environment Status und fehlende schließende `</div>`-Tags im Parser-Baum.
- Korrektur: Tags bereinigt, alle offenen Container geschlossen.
- Ergebnis: Layout für alle Tabs (ab Parser) ist wieder korrekt linksbündig, "FFprobe:" hängt nicht mehr oben links.

## Edit-Tab: Drei neue Sub-Reiter
- **Metadaten:** Standard-Eingabemaske und Tag-Bearbeitung (wie vorher).
- **MediaInfo:** Detaillierte MediaInfo-Ansicht aus dem Parser-Tab wurde hierhin verschoben.
- **FFprobe Analyse:** Neuer Reiter, der die FFprobe-JSON-Metadaten der gewählten Datei über das Backend ausliest und formatiert anzeigt. Zuvor war FFprobe fast nur ein Konsolen-Log, jetzt gibt es eine eigene, saubere Anzeige.

## Hinweise
- Seite neu laden, damit alle Splitter und Tabs korrekt funktionieren.
- Alle Leerräume und Layout-Fehlstellungen ab Parser sollten behoben sein.

**Feedback willkommen, falls noch irgendwo Layout-Probleme auftreten!**
