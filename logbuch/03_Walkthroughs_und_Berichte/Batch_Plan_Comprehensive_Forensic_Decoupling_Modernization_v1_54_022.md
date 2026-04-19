# Batch Plan – Comprehensive Forensic Decoupling & Modernization (v1.54.022)

## Overview
Systematic extraction of all functional subsystems from the 7000+ line `main.py` into specialized API modules, with a legacy archive for full logic preservation. Migration will proceed in logical batches to ensure stability and maintain functional parity.

---

## Batch 1: Foundation & Infrastructure
- Create `src/core/api_config.py` and migrate config endpoints
- Create `src/core/api_environment.py` and migrate environment endpoints
- Create `src/core/api_ui.py` and migrate UI/QA endpoints
- Register and verify Batch 1 modules

## Batch 2: Media Scanner & Database CRUD
- Extract scanner logic from `main.py`
- Implement migrated logic in `api_library.py`
- Consolidate database CRUD operations (`delete_media`, `rename_media`, `update_tags`)
- Register and verify Batch 2

## Batch 3: Playback & Orchestration
- Create `src/core/api_playback.py`
- Create `src/core/api_orchestrator.py`
- Create `src/core/api_streaming.py` (MediaMTX/VLC-Pipes)
- Register Batch 3 and verify playback/streaming

## Batch 4: Specialized Forensic Tools
- Create `src/core/api_transcoding.py`
- Create `src/core/api_testing.py`
- Create `src/core/api_subtitles.py`
- Create `src/core/api_media_tools.py` (specialized media transformation/analysis)
- Register Batch 4 and verify toolchain

## Batch 5: Preservation & Legacy Hub
- Create `src/core/api_legacy_archive.py`
- Restore and expose all legacy/diagnostic functions (e.g., `rtt_stress_ping`, `rtt_item_test`, `confirm_receipt`)
- Document all unused/redundant logic for forensic reference

## Batch 6: Final Core Slimming
- Remove all functional logic from `main.py`, preserving only the import grid and Eel startup loop
- Ensure all `@eel.expose` functions are registered from their new locations
- Establish new entry point standards (v1.54.023)

---

## Verification Plan
- Run `startup_auditor.py` to verify all endpoints are reachable after each batch
- Verify `main.py` starts without syntax errors using `python3 -m py_compile`
- Visual check of BOOT terminal for registration logs
- Test "Smart Play" for video/audio to ensure routing bridge is intact
- Verify system dashboard (`get_sys_overview`) still populates correctly

---

## Open Questions
- Do you prefer a single massive cleanup or migration in 2-3 batches?
- Should the legacy archive include all previously omitted diagnostics for full forensic traceability?
