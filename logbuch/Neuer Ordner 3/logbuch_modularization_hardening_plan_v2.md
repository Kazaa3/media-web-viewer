# Implementation Plan – Hardening & Modularization (v2)

This plan outlines the steps to harden the application environment (Python 3.14.2), modularize key JavaScript components from app.html into dedicated helper files, and prepare for offline builds.

## User Review Required
**IMPORTANT**

- **Python Version Requirement:** Strict Python 3.14.2 enforcement. `main.py` will check this and only run within the `.venv_run` virtual environment.
- **Modularization:** Large blocks of JavaScript will be moved from `app.html` to `web/js/`. This improves maintainability but requires careful verification of all imports.
- **Offline Assets:** The Python 3.14.2 source installer will be saved in `packages/python/` for offline reproducibility.

## Proposed Changes

### 1. Hardening System & Environment
- **[MODIFY] main.py**
  - Update the strict version check to require Python 3.14.2.
  - Enhance the `.venv_run` guard to ensure the application only runs within the designated virtual environment.
  - Refactor `log_js_error` to ensure structured logging into `logs/frontend_errors.log`.
- **[MODIFY] .python-version**
  - Explicitly set to 3.14.2.
- **[NEW] [packages/python/Python-3.14.2.tar.xz]**
  - Download and save the Python 3.14.2 source/installer for offline build processes.

### 2. Modularize Reporting Component
- **[MODIFY] reporting_helpers.js**
  - Move `switchReportingView` from `ui_nav_helpers.js` to this file.
  - Extract analytics logic (Plotly charts, dashboard population) from `app.html` (around line 9473).
  - Implement `updateAnalyticsDashboard`.

### 3. Modularize Video Player Component
- **[NEW] video.js**
  - Create `video.js` as requested.
  - Extract `selectEngine` and core Video.js orchestration logic from `app.html` (around line 7218).
  - House the Video.js player initialization and standard configuration here.
- **[MODIFY] video_helpers.js**
  - Consolidate engine switching and player state management logic here.

### 4. Implement DOM 7 Debugging Suite
- **[MODIFY] debug_helpers.js**
  - Extract UI trace hooks and "Div balance" checks from `app.html` (line 10053).
  - Implement the "7 stages of UI integrity" logic (Stage 1: DOM Load, Stage 2: Eel Sync, Stage 3: Asset Integrity, Stage 4: Div Balance, Stage 5: Event Listeners, Stage 6: Layout Stability, Stage 7: Performance Check).

### 5. Clean up app.html
- **[MODIFY] app.html**
  - Remove extracted `<script>` blocks (Analytics at 9473, selectEngine at 7218, Integrity at 10053).
  - Add new script imports:
    ```html
    <script src="js/video.js"></script>
    <script src="js/video_helpers.js"></script>
    <script src="js/reporting_helpers.js"></script>
    <script src="js/debug_helpers.js"></script>
    ```

## Open Questions
- **Python Installer Source:** Which specific distribution (Source, Gzipped source, or a specific Linux binary) should be saved for the offline build?
- **Video.js Dependencies:** Should `video.js` also include the Video.js library itself (via local file) for offline use, or stick to the CDN for now?

## Verification Plan

### Automated Tests
- Run `python3 src/core/main.py --debug` to verify environment guards.
- Check `logs/frontend_errors.log` after triggering a test error.

### Manual Verification
- **Reporting:** Open the "Reporting" tab and verify charts populate correctly.
- **Video Player:** Switch between "Chrome Native", "VLC", and "MTX" engines; verify playback starts.
- **Debug:** Run the "UI Integrity Check" from the Debug tab and verify all 7 stages pass.
