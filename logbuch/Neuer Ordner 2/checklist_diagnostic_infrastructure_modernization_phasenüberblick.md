# Checklist: Modernizing Media Diagnostic Infrastructure (Phases 6–10)
#
# UI Theme & AI Infrastructure Overview
#
# Die Anwendung nutzt ein Premium-Theme im "Carbon/Glass"-Stil mit fortgeschrittenen strukturellen Ankerpunkten für KI-Orchestrierung.
#
# **1. Wording & Style [Theme]**
# - Glassmorphism und Glassmorphic Panels als zentrales Designprinzip
# - Primärfarben: Cyan (#00f2fe), Dunkelgrau (#151515)
# - Visuelle Effekte:
#   - backdrop-filter: blur(14px) für Panel-Transparenz
#   - -webkit-box-reflect für 3D-Coverflow-Effekte
#   - Lineare Farbverläufe mit #00f2fe und #4facfe
# - Wording: Premium-Terminologie wie "Sequential Buffer" (Playlist), "Telemetry Inspector" (Debug), "Chain Config" (Parser)
#
# **2. KI-Anker [AI Readiness]**
# - Explizite strukturelle Marker für KI-basierte Analyse und Orchestrierung
# - Meta-Tag: <meta name="ai-readiness" content="verified" data-ai-id="root-manifest">
# - Data-Attribute: Jedes Tab-Panel und zentrale UI-Element ist mit data-ai-id oder beschreibenden IDs versehen (z.B. für automatisiertes Testing und Discovery)
# - Strukturelle Metadaten: Kommentare mit [AI-READINESS] geben Hinweise auf Komponenten-Hierarchien
#
# **3. Structural Anchors**
# - Kritische IDs in app.html:
#   - main-sidebar: Root-Navigationsanker
#   - main-content-area: Haupt-Rendering-Ziel
#   - multiplexed-media-player-orchestrator-panel: Zentrale Player-Instanz
#
# Key Achievements (2026-03-28)
#
# - Structural Balance: 100% Brace-Balance in app.html (2040/2040), inkl. Fix für offenen if-Block und überzählige Klammer.
# - Diagnostic Suite: UI Integrity Suite (Level 1–12) vollständig aktualisiert und bestanden, inkl. Debug & DB View und Mock Data System.
# - UI Scrolling: Scrolling-Probleme in Reporting/Parser-Tabs durch Flexbox-Layout und CSS-Bereinigung gelöst.
# - Mock Data System: is_mock-Property im Backend/Frontend integriert, Toggle in Optionen, Live-Statistik im Debug-View.
#
# Details und Nachweise siehe walkthrough.md.

## Status: Ongoing

---

### Phase 6: Optimization & AI-Readiness
- [x] 210+ Legacy-Diagnostic-Stages in Master Runner (run_all.py) konsolidiert
- [x] DiagnosticEngine-Basisklasse für type-sichere Methodenerkennung implementiert
- [x] I18nSuiteEngine integriert (JSON-Integrität, Key-Parität, Deep Scan)
- [x] MediaIntegritySuiteEngine integriert (Codec-Registry, Kategorisierungslogik)
- [x] ParserSuiteEngine integriert (Keyword Detection, Metadaten-Extraktion)
- [x] CodeQualitySuiteEngine integriert (Subprocess-Sicherheit, Linting-Readiness)
- [x] EnvSuiteEngine integriert (Artifact-Audit, Versionsprüfung)
- [x] Regression: Fehlende i18n-Keys synchronisiert
- [x] Regression: Variable Scoping (large_builds) in EnvSuiteEngine behoben
- [x] OptimizationSuiteEngine für Master Runner erstellt
- [x] Unicode-Icons durch SVGs ersetzt (JS/HTML optimiert)
- [ ] 100% HTML I18n-Abdeckung (Reduziert auf ~372 Nodes)
- [x] Strukturelle AI-Komplexitätskommentare (app.html, JS Entry Points) ergänzt
- [x] ComplexitySuiteEngine (File/Func metrics) erstellt
- [x] StylesSuiteEngine (Visual/AI Anchor audit) erstellt
- [x] Unicode-to-SVG Migration Template dokumentiert
- [x] Finaler Architektur-Audit (Level 7 Mastery)
- [x] 230+ Stage System Health Verification durchgeführt

---

### Phase 7: Advanced Subtitle Infrastructure
- [x] SubtitleProcessor (Extraktion & Timing) implementiert
- [x] SubtitleSuiteEngine für Master Runner erstellt
- [x] Subtitle APIs in main.py integriert
- [x] Frontend Subtitle Management UI implementiert
- [x] 100% Subtitle Extraction Coverage Audit

---

### Phase 8: Expanded Toolchain & Advanced Diagnostics
- [x] FFPLAY Diagnostic Engine integriert
- [x] FFPROBE Diagnostic Engine erweitert
- [x] SWYH-RS CLI Integration (Audio Streaming)
- [x] MKVToolNix Core Integration (Mux/Extract/Info/Edit)
- [ ] HandBrake CLI Batch Encoding Engine (GPU Support)
- [ ] Media Routing Test Suite (Reporting Tab Integration)
- [ ] Dependency Audit (pymediainfo, enzyme, pymkv, ffmpeg-python)

---

### Phase 9: Advanced Playback & Toolchain Integration
- [x] SWYH-RS CLI Bridge in main.py implementiert
- [x] MKVcleaver-Style Batch Extraction mit mkvextract integriert
- [x] mode_router.py um 10+ Modi erweitert (DASH, MPV, VLC Native, etc.)
- [x] MPV (WASM/Native) in die Playback-UI integriert
- [x] UI Controls für SWYH-RS und Batch Extract hinzugefügt
- [ ] Verifikation via tests/engines/suite_advanced_player.py

---

### Phase 10: Bugfix & Static GUI Integrity
- [x] 21 JS-Syntaxfehler in app.html behoben (verschachtelte Quotes, Literal-Fehler)
- [x] Malformed SVG-Icon-IDs korrigiert (Spaces in hrefs entfernt)
- [x] Fehlende triggerBatchExtract JS-Funktion implementiert
- [x] window.onerror-Bridge für Echtzeit-Backend-Error-Reporting ergänzt
- [x] Static GUI Integrity Suite im Master Diagnostic Runner erstellt/erweitert
- [x] 100% statischer Diagnostic-Pass (Frontend Integrity, non-Selenium)

### Phase 11: Switch Tab & Mock Item Verification
- [x] 'flags' Tab-Mapping in app.html korrigiert
- [x] Fehlende get_db_info Backend-Bridge implementiert
- [x] Level 9 Verification zur UIIntegritySuiteEngine hinzugefügt
- [x] Harte Mock-Items im GUI geprüft und entfernt
- [x] Finaler UI-Integritätslauf (L1–L9)

### Phase 12
- [x] Database Migration Log Loop (init_db spam) behoben
- [x] Scrolling im Parser-Tab (Sidebar & Main Pane) korrigiert
- [x] Scrolling im Media Routing Sub-Tab korrigiert
- [x] is_mock Property in MediaItem und Datenbank implementiert
- [x] Mock Data Configuration Switch integriert
- [x] Debug & Database Integrity Checks (Level 10) in die Diagnostic Suite integriert
---

### Taskblock: Mock-Stages & Level 10+ Integrity

**Database & Models**
- [x] is_mock zur media-Tabelle hinzugefügt (Migration)
- [x] is_mock zur MediaItem-Klasse hinzugefügt
- [x] mock_stage zur media-Tabelle hinzugefügt (Migration)
- [x] mock_stage zur MediaItem-Klasse hinzugefügt
- [x] insert_media für is_mock und mock_stage angepasst
- [x] get_all_media gibt is_mock und mock_stage zurück

**UI & Logic**
- [x] Mock Data Toggle in Optionen > Allgemein implementiert
- [x] Mock Data Filter in Bibliotheksansicht implementiert
- [x] is_mock-Property und mock_stage in MediaItems (UI-Logik)
- [x] Mock Data Toggle im Options-Tab und Backend-Logik
- [x] Datenbank-Initialisierung: Log-Spam und IndentationError behoben
- [x] Vertikales Scrolling in Management-Tabs (Parser, Reporting, Media Routing) gefixt

**Verification & Testing**
- [x] UI Integrity Suite (Level 10–12) erweitert
- [x] Level 10: Debug & Datenbank-Komponenten integriert
- [x] Level 11: Management-Stabilität (Reporting/Parser) integriert
- [x] Level 12: Mock-System-Konfiguration integriert
- [x] Level 1 Structural Balance (fehlende Klammer) behoben
- [x] Hängende Test-Suite gefixt
- [x] Mock-Stages-Funktionalität weiterentwickelt
- [x] main.py auf Import/Linting-Fehler geprüft
- [x] Level 11/12 Integrity Levels verifiziert
- [x] UI Integrity Suite ausgeführt und Erfolg bestätigt

---
###Phase 13
playwright in die etst suite integrieren. als aletrnaative für selenium. beide da lassen aber playwright als default



*Diese Checkliste dokumentiert den laufenden Fortschritt der Modernisierung und Erweiterung der Media Diagnostic Infrastructure (Phasen 6–10).*
