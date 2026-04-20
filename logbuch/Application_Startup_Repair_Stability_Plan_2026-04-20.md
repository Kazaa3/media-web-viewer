# Application Startup Repair & Stability Plan

**Date:** 2026-04-20

The application is currently failing to start due to several ImportErrors and missing core functions in the backend infrastructure. This plan outlines the steps to restore stability and ensure a clean boot sequence.

---

## User Review Required
**IMPORTANT**

A new configuration file `config_master.json` will be created in the project root to persist `GLOBAL_CONFIG` changes.

---

## Proposed Changes
### Core Infrastructure

**[MODIFY] config_master.py**
- Implement `save_config()` function to persist `GLOBAL_CONFIG` to `config_master.json`.
- Implement basic `load_config_from_file()` to ensure persistent settings are respected across restarts.

**[MODIFY] startup_auditor.py**
- Add `run_preflight_audit()` as a standardized entry point for `main.py`.
- Ensure it wraps the existing `run_audit()` logic with enhanced reporting.

**[MODIFY] main.py**
- Cleanup redundant and conflicting import blocks.
- Synchronize `from src.core import ...` with the actual file structure.
- Fix broken calls to `run_preflight_audit`.

---

## Verification Plan

### Automated Tests
- Run the application via `python src/core/main.py` and verify it reaches the "Success: UI SYNCHRONIZED" state.
- Inspect `logs/app.log` for any hidden ImportError or NameError cascades.

### Manual Verification
- Verify that the GUI loads beyond the "Player Loading" screen.
- Change a setting in the UI (e.g., App Mode) and verify that `config_master.json` is updated.
