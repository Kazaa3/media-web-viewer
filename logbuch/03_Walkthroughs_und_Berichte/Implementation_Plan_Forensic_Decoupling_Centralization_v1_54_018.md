# Implementation Plan – Forensic Decoupling & Centralization (v1.54.018)

## Objective
Modernize the workstation's architecture by decoupling the monolithic `main.py`, centralizing tool orchestration, and enforcing a single-source-of-truth (SSOT) for tools and versioning.

---

## User Review Required

### IMPORTANT
- Over 20 functions will be moved from `main.py` into specialized modules. Backend imports must be synchronized to avoid Eel bridge errors.

---

## Proposed Changes

### [Component] UI Consistency & SSOT
- **shell_master.css**
  - Icon Contrast: Update `.master-header.elite-inversion .tool-icon-btn` to use black/dark-gray for visibility on white backgrounds.
- **shell_master.html**
  - Dynamic Title: Replace hardcoded version in `<title>` with a placeholder to be hydrated by `ui_nav_helpers.js`.
- **ui_nav_helpers.js**
  - Workstation Identity: Implement `updateWorkstationIdentity()` to fetch the version from `window.CONFIG.version` and update the document title.

### [Component] Backend Orchestration
- **config_master.py**
  - [NEW] `TOOLS_REGISTRY`: Centralize binary discovery and metadata for ffmpeg, vlc, ffplay, etc.
  - SSOT Alignment: Ensure all tool-related logic uses the new registry.
- **api_config.py** (NEW)
  - Orchestration: Move `@eel.expose` functions related to core configuration (get/set) to this module.

### [Component] Main Refactoring
- **main.py**
  - Slimming: Remove logic related to diagnostic reporting, UI events, and media stream routing.
  - Imports: Decentralize imports to the respective `api_*.py` modules to reduce startup latency.

---

## Open Questions
- Should the `TOOLS_REGISTRY` include auto-healing logic (e.g., attempting to re-download missing binaries via `shutil.which` or a package manager)?

---

## Verification Plan

### Automated Tests
- `python3 src/core/main.py --force-boot`: Verify the refactored backend starts correctly without import errors.
- `startup_auditor.py`: Confirm system integrity.

### Manual Verification
- Verify icons are visible in both Dark and Elite (White) modes.
- Confirm the browser title correctly displays "Media Viewer [Version] - MASTER".
- Verify that "Queue All" and other media discovery functions still work after relocation.
