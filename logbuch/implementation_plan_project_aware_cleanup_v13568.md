# Implementation Plan: Project-Aware Cleanup & Stabilization (v1.35.68)

## Overview
This plan details the deployment of a path-aware process reaper, the integration of a centralized diagnostic hub, and the restoration of real media hydration for the Media Viewer application.

## Key Highlights
- **Path-Aware Reaper:** Ensures no phantom processes hold port 8345 by scanning for any process whose command line contains the project path (`gui_media_web_viewer`).
- **Diagnostic Hub:** Adds toggles for log verbosity and DOM health auditing directly in the Options panel for real-time control.
- **Atomic Hydration:** Implements a fail-safe mechanism to ensure the player queue is never empty, auto-filling it if needed.

## Implementation Steps
1. **Deploy /tmp/super_kill.py:**
   - Uses `psutil` to identify and SIGKILL all processes related to the project path, ensuring a clean environment before restart.
2. **Centralized Diagnostic Hub:**
   - Integrate a new section in Options > Debug for log level selection (INFO, DEBUG, ERROR) and DOM Health Auditor toggle.
   - Real-time log ingestion and control over backend log stream intensity.
3. **Atomic Hydration:**
   - Add logic to auto-fill the player queue if it remains empty for more than 5 seconds, using real media files from the workspace.
4. **Unified Versioning:**
   - Synchronize `main.py` and `version.js` to v1.35.68 to resolve any version drift or "Old Ghost" reporting.
5. **Real DB Hydration:**
   - After environment cleanup, re-run the Direct Scan to populate the library from `./media`.

## Open Questions
- Should the "Direct Scan" be triggered automatically after backend restart, or manually via the new "Sync" button?
- Should the DOM Health Auditor's lime borders be enabled by default for this version?

## Verification
- All zombie processes are purged; only one backend instance remains.
- UI and backend both report v1.35.68.
- Library is hydrated with real media files.
- Logging and diagnostic controls are available in the Options panel.
- Player queue is never empty due to atomic hydration.

## Outcome
- **Restored:** Clean, stable environment, correct versioning, centralized diagnostics, and reliable real audio playback.
- **Status:** Awaiting user review and preference for scan/auditor defaults before execution.
