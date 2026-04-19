# Implementation Plan – Forensic Sentinel Hardening (v1.54.014)

## Objective
Resolve persistent "Lade Player..." hydration stalls by implementing a background diagnostic pulse that automatically recovers stalled viewports.

---

## User Review Required

### IMPORTANT
- **Forensic Heartbeat:** Introduce a 5-second recurring pulse (Sentinel Evolution Heartbeat) that runs the DOM Auditor in the background. If a "STALLED" state is detected, the UI will automatically attempt a forensic recovery (Force Reload + Category Sync).

### WARNING
- **Nomenclature Alignment:** Synchronize `switchPlayerInternalView` and `switchPlayerView` to eliminate navigation dead-ends.

---

## Proposed Changes

### [Core] app_core.js
- [MODIFY] Harden the BOOT-WATCHDOG to use the new `checkHydrationStall()` for better precision.
- [NEW] Implement `initForensicHeartbeat()`:
  - Cycles every 5000ms.
  - Runs `window.runDomAudit()`.
  - If stall detected (H-9), triggers `eel.log_ui_event('FORENSIC-STALL-DETECTED', ...)` and `refreshLibrary()`.

### [UI] player_queue.html
- [MODIFY] Alias `switchPlayerInternalView` to `window.switchPlayerView` for global orchestrator compatibility.
- [MODIFY] Add a 500ms delay to the initial `switchPlayerView('warteschlange')` call to ensure DOM readiness after fragment injection.

### [UI] ui_nav_helpers.js
- [MODIFY] Enhance `switchPlayerView` to explicitly call `renderAudioQueue()` and `renderPhotoQueue()` to guarantee list hydration.

### [Diagnostics] dom_auditor.js
- [MODIFY] Update `runDomAudit` to return the full audit results object for the Heartbeat sentinel.

---

## Verification Plan

### Automated Tests
- Run `/home/xc/#Coding/gui_media_web_viewer/.venv/bin/python3 src/core/startup_auditor.py` to verify system integrity.

### Manual Verification
- **Heartbeat Logs:** Verify that `[SENTINEL-PULSE]` messages appear in the console every 5s.
- **Stall Recovery:** Manually inject "LADE PLAYER..." text into the viewport via console and verify that the Heartbeat triggers a recovery within 5s.
- **Queue Rendering:** Confirm that navigating to 'media' correctly hydrates the Mediengalerie with the item list.
