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
