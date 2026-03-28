# Checklist: Modernizing Media Diagnostic Infrastructure (Phases 6–10)

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
- [ ] 100% statischer Diagnostic-Pass (Frontend Integrity, non-Selenium)

### Phase 11: Switch Tab & Mock Item Verification
- 'flags' Tab-Mapping in app.html korrigieren
- Fehlende get_db_info Backend-Bridge implementieren
- Level 9 Verification zur UIIntegritySuiteEngine hinzufügen
- Harte Mock-Items im GUI prüfen und entfernen
- Finaler UI-Integritätslauf (L1–L9)

### Phase 12
- [ ] Database Migration Log Loop (init_db spam) beheben
- [ ] Scrolling im Parser-Tab (Sidebar & Main Pane) korrigieren
- [ ] Scrolling im Media Routing Sub-Tab korrigieren
- [ ] is_mock Property in MediaItem und Datenbank implementieren
- [ ] Mock Data Configuration Switch integrieren
- [ ] Debug & Database Integrity Checks (Level 10) in die Diagnostic Suite integrieren
---

### Taskblock: Mock-Stages & Level 10+ Integrity

**Database & Models**
- [ ] is_mock zur media-Tabelle hinzufügen (Migration)
- [ ] is_mock zur MediaItem-Klasse hinzufügen
- [ ] mock_stage zur media-Tabelle hinzufügen (Migration)
- [ ] mock_stage zur MediaItem-Klasse hinzufügen
- [ ] insert_media für is_mock und mock_stage anpassen
- [ ] get_all_media gibt is_mock und mock_stage zurück

**UI & Logic**
- [ ] Mock Data Toggle in Optionen > Allgemein implementieren
- [ ] Mock Data Filter in Bibliotheksansicht implementieren
- [ ] is_mock-Property und mock_stage in MediaItems (UI-Logik)
- [ ] Mock Data Toggle im Options-Tab und Backend-Logik
- [ ] Datenbank-Initialisierung: Log-Spam und IndentationError beheben
- [ ] Vertikales Scrolling in Management-Tabs (Parser, Reporting, Media Routing) fixen

**Verification & Testing**
- [ ] UI Integrity Suite (Level 10–12) erweitern
- [ ] Level 10: Debug & Datenbank-Komponenten integrieren
- [ ] Level 11: Management-Stabilität (Reporting/Parser) integrieren
- [ ] Level 12: Mock-System-Konfiguration integrieren
- [ ] Level 1 Structural Balance (fehlende Klammer) beheben
- [ ] Hängende Test-Suite fixen
- [ ] Mock-Stages-Funktionalität weiterentwickeln
- [ ] main.py auf Import/Linting-Fehler prüfen
- [ ] Level 11/12 Integrity Levels verifizieren
- [ ] UI Integrity Suite ausführen und Erfolg bestätigen

---
###Phase 13
playwright in die etst suite integrieren. als aletrnaative für selenium. beide da lassen aber playwright als default



*Diese Checkliste dokumentiert den laufenden Fortschritt der Modernisierung und Erweiterung der Media Diagnostic Infrastructure (Phasen 6–10).*
