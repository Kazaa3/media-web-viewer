# Implementation Plan – Comprehensive Forensic Decoupling & Modernization (v1.54.022)

## Objective
Systematically extract all functional subsystems from the 7000+ line `main.py` into specialized API modules, transforming it into a lean bootstrap entry point while maintaining functional parity via the Eel registration bridge.

---

## User Review Required

### IMPORTANT
- High-impact structural refactoring: Over 100 exposed functions will be migrated to new modules. Code organization will change significantly, but functional parity will be maintained.

### WARNING
- 8+ new API modules will be created. Migration will proceed in logical batches to ensure stability.

---

## Proposed Changes

### 1. New API Modules [NEW]
Create the following modules in `src/core/`:
- `api_config.py`: App settings & localization.
- `api_environment.py`: System overview, venv management, pip installer.
- `api_ui.py`: UI state, tracing, and integrity/QA checks.
- `api_transcoding.py`: Integration with HandBrake and MKVToolNix.
- `api_playback.py`: Basic playback controls and path resolution.
- `api_orchestrator.py`: Smart video routing and orchestration.
- `api_streaming.py`: MediaMTX, VLC HLS, and VLC Pipe engines.
- `api_testing.py`: Test discovery and benchmarking.
- `api_subtitles.py`: Subtitle extraction and timing logic.

### 2. Specialized Migrations
- **api_library.py**: Migrate Round 5.5 Media Scanner logic from `main.py`. Consolidate database CRUD operations (`delete_media`, `rename_media`, `update_tags`).
- **api_reporting.py**: Take over all diagnostic reporting (`get_db_info`, `get_multimedia_analysis`, `get_model_analysis`).
- **api_core_app.py**: Take over workstation governance endpoints and versioning logic.

### 3. Entry Point Slimming
- **main.py**: [Surgical Cleanup]
  - Remove all functional logic blocks.
  - Preserve only the import grid (bridge) and the Eel startup/application loop.
  - Ensure all `@eel.expose` functions are registered correctly from their new locations.

---

## Open Questions
- Do you prefer a single massive cleanup or migration in 2-3 batches? (e.g. Batch 1: Config/Env/UI, Batch 2: Playback/Streaming, Batch 3: Library/Scanner)

---

## Verification Plan

### Automated Verification
- Run `startup_auditor.py` to verify all endpoints are reachable.
- Verify `main.py` starts without syntax errors using `python3 -m py_compile`.

### Manual Verification
- Visual check of the BOOT terminal for registration logs.
- Test "Smart Play" for a video and an audio file to ensure routing bridge is intact.
- Verify system dashboard (`get_sys_overview`) still populates correctly.
