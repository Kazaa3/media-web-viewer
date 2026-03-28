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

### Phase 10: Bugfix & MPV Refinement
- [ ] JS-Syntaxfehler in app.html beheben (verschachtelte Quotes in showToast)
- [ ] Fehlende triggerBatchExtract JS-Funktion implementieren
- [ ] web/js/mpv-player.js in web/js/mpv_player.js umbenennen
- [ ] "missing )"-Fehler beheben (vermutlich JS-String-Terminierung)
- [ ] Fix-Verifikation mit nicht-Selenium-Methoden (Diagnostic Suite)

---

*Diese Checkliste dokumentiert den laufenden Fortschritt der Modernisierung und Erweiterung der Media Diagnostic Infrastructure (Phasen 6–10).*