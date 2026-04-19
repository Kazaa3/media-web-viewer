# Implementation Plan – UI Hydration & Evolution Sync (v1.54.012)

## Objective
Resolve the GUI hydration stall ("LADE PLAYER...") and synchronize the workstation's evolution baseline for full duty-readiness.

---

## User Review Required

### IMPORTANT
- **Evolution Mode Sync:** Shift `ui_evolution_mode` from `stable` to `rebuild` in `config_master.py`. This aligns the backend with the modern UI and ensures the dynamic Fragment Loader is engaged.

### WARNING
- **Version Baseline:** Update the `VERSION` file to `v1.54.012` to eliminate version drift in the footer HUD.

---

## Proposed Changes

### [Core] VERSION
- [MODIFY] Update version string to `v1.54.012`.

### [Core] config_master.py
- [MODIFY] Update `ui_evolution_mode` to `rebuild` (line 824).

### [Web] app_core.js
- [MODIFY] Harden the BOOT-WATCHDOG (line 658) to ensure it forces player fragment hydration even if backend configuration reporting is delayed.

### [Web] ui_nav_helpers.js
- [MODIFY] Ensure `switchMainCategory('media')` correctly triggers initial tab hydration for the player viewport in `rebuild` mode.

---

## Verification Plan

### Automated Tests
- Run `/home/xc/#Coding/gui_media_web_viewer/.venv/bin/python3 src/core/startup_auditor.py` to verify integrity audit passes.
- Run `/home/xc/#Coding/gui_media_web_viewer/.venv/bin/python3 src/core/main.py` to verify the workstation boots and reaches the "Core Ready" state.

### Manual Verification
- Confirm that the GUI successfully hydrates beyond "LADE PLAYER..." and reveals the Mediengalerie.
- Verify the footer reports `v1.54.012-EVO-STABLE`.
