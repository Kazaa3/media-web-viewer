# Modernizing Media Diagnostic Infrastructure Checklist

This checklist tracks the comprehensive modernization of the media-web-viewer’s diagnostic infrastructure, consolidating legacy stages, introducing robust diagnostic engines, and ensuring advanced toolchain and UI integration. Each phase is mapped to concrete actions and verification steps.

---

## Phase 1–5: Foundation & Consolidation
- [ ] Consolidate 210+ legacy diagnostic stages into unified master runner (`run_all.py`)
- [ ] Implement `DiagnosticEngine` base class for type-safe method discovery
- [ ] Integrate `I18nSuiteEngine` (JSON integrity, key parity, deep scan)
- [ ] Integrate `MediaIntegritySuiteEngine` (Codec registry, categorization logic)
- [ ] Integrate `ParserSuiteEngine` (Keyword detection, metadata extraction)
- [ ] Integrate `CodeQualitySuiteEngine` (Subprocess safety, linting readiness)
- [ ] Integrate `EnvSuiteEngine` (Artifact audit, version verification)
- [ ] Fix regression: Sync missing i18n keys identified by diagnostic suite
- [ ] Fix regression: Variable scoping (`large_builds`) in `EnvSuiteEngine`

---

## Phase 6: Optimization & AI-Readiness
- [ ] Create `OptimizationSuiteEngine` for master runner
- [ ] Replace Unicode icons with SVGs (JS/HTML optimized)
- [ ] Ensure 100% HTML I18n coverage (reduced to ~372 nodes)
- [ ] Add structural AI complexity comments (app.html, JS entry points)
- [ ] Create `ComplexitySuiteEngine` (File/Func metrics)
- [ ] Create `StylesSuiteEngine` (Visual/AI Anchor audit)
- [ ] Document Unicode-to-SVG migration template
- [ ] Final architectural audit (Level 7 Mastery)
- [ ] Conclusive 230+ stage system health verification

---

## Phase 7: Advanced Subtitle Infrastructure
- [ ] Implement `SubtitleProcessor` (Extraction & Timing)
- [ ] Create `SubtitleSuiteEngine` for master runner
- [ ] Integrate Subtitle APIs into `main.py`
- [ ] Implement frontend subtitle management UI
- [ ] 100% subtitle extraction coverage audit

---

## Phase 8: Expanded Toolchain & Advanced Diagnostics
- [ ] FFPLAY & FFPROBE Diagnostic Engines
- [ ] SWYH-RS CLI Integration (Audio Streaming)
- [ ] MKVToolNix Core Integration (Mux/Extract/Info/Edit)
- [ ] HandBrake CLI Batch Encoding Engine (GPU Support)
- [ ] Media Routing Test Suite (Reporting Tab Integration)
- [ ] Dependency audit (pymediainfo, enzyme, pymkv, ffmpeg-python)

---

## Phase 9: Advanced Playback & Toolchain Integration
- [ ] Implement SWYH-RS CLI bridge in `main.py`
- [ ] Add MKVcleaver-style batch extraction logic using mkvextract
- [ ] Expand `mode_router.py` with 10+ modes (DASH, MPV, VLC Native)
- [ ] Integrate MPV (WASM/Native) into frontend playback
- [ ] Add UI controls for SWYH-RS and Batch Extract
- [ ] Verify via `tests/engines/suite_advanced_player.py`

---

## Phase 10: Bugfix & Static GUI Integrity
- [ ] Fix 21 JS syntax errors in `app.html` (nested quotes & literal breakage)
- [ ] Correct malformed SVG icon IDs (removed spaces in hrefs)
- [ ] Implement missing `triggerBatchExtract` JS function
- [ ] Implement `window.onerror` bridge for real-time backend error reporting
- [ ] Create/enhance Static GUI Integrity Suite in master diagnostic runner
- [ ] Verify fix using non-Selenium methods (100% static diagnostic pass)

---

## Phase 11: Switch Tab & Mock Item Verification
- [ ] Correct 'flags' tab mapping in `app.html`
- [ ] Implement missing `get_db_info` backend bridge
- [ ] Add Level 9 verification to `UIIntegritySuiteEngine`
- [ ] Audit and remove hardcoded mock items in GUI
- [ ] Final UI integrity run (L1–L9)

---

## Phase 12: Layout Refinement & Mock Data Integration
- [ ] Resolve database migration log loop (init_db spam)
- [ ] Fix scrolling in parser tab (sidebar & main pane)
- [ ] Fix scrolling in media routing sub-tab
- [ ] Implement `is_mock` property in `MediaItem` and database
- [ ] Add mock data configuration switch
- [ ] Integrate debug & database integrity checks (Level 10)

---

## Verification
- [ ] Automated and manual tests for each phase
- [ ] All diagnostic engines and UI features verified as passing
- [ ] Documentation and checklists updated after each milestone

---

**Status:** In Progress / To Be Updated Per Milestone
