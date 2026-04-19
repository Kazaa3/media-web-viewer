# Implementation Plan – Import Synchronization (v1.54.012)

## Objective
Resolve `NameError: name 'PORT_CLEANUP_CMD' is not defined` by centralizing core configuration imports in `main.py`.

---

## User Review Required

### IMPORTANT
- **Import Centralization:** Move `PORT_CLEANUP_CMD`, `GLOBAL_CONFIG`, and `BITRATE_QUALITY_THRESHOLDS` into the primary import block from `src.core.config_master` in `main.py`.
- This resolves the `NameError` and eliminates redundant local imports throughout the 7000+ line file.

---

## Proposed Changes

### [Core] main.py
- [MODIFY] Update the import block from `src.core.config_master` (line 41) to include:
  - `GLOBAL_CONFIG`
  - `PORT_CLEANUP_CMD`
  - `BITRATE_QUALITY_THRESHOLDS`
  - `DEPENDENCY_REGISTRY`
- [MODIFY] Remove redundant local imports of these constants throughout the file (optional but recommended for cleanliness).

---

## Verification Plan

### Automated Tests
- Run `/home/xc/#Coding/gui_media_web_viewer/.venv/bin/python3 src/core/startup_auditor.py` to verify the workstation integrity audit passes.
- Run `/home/xc/#Coding/gui_media_web_viewer/.venv/bin/python3 src/core/main.py` to verify the application reaches "Application started" and initializes the UI loop without a `NameError`.

### Manual Verification
- Confirm that the workstation starts and reaches the UI successfully.
