# Pipeline Recovery: Super-Kill Bridge (v1.37.18) — Implementation Plan

## 🛡️ Building the Pipeline Recovery Bridge

- **Atomic Kill Switch:**
  - Identify and implement backend logic in main.py (leveraging ./scripts/super_kill.py) to safely terminate orphaned or stalled FFmpeg processes.
- **Forensic UI Control:**
  - Add a [RECOVER PIPELINE] button to the VID (Video Health) tab in diagnostics_sidebar.html for immediate tactical recovery.
- **Sentinel Audit:**
  - Capture all pipeline recovery events in the SENTINEL engine for persistent forensic logging.

---

## Proposed Changes
- **Backend (main.py):**
  - Implement `kill_stalled_ffmpeg_streams()` Eel bridge.
  - Integrate with super_kill.py or use targeted psutil/subprocess calls to purge media-related processes.
- **Sidebar UI (diagnostics_sidebar.html):**
  - Add [RECOVER PIPELINE] button and recovery status indicator to the VID pane.
- **Controller (sidebar_controller.js):**
  - Implement `triggerPipelineRecovery()` for frontend-to-backend handshake and SENTINEL event logging.

---

## Open Questions
- Should a "Dry Run" (list-only) mode be implemented, or is a direct "Kill All" more effective for recovery? (Direct Kill recommended for efficiency.)

---

## Verification Plan
- **Automated:** Spawn a mock FFmpeg process and verify the kill_stalled_ffmpeg_streams bridge terminates it.
- **Manual:** Start video playback, open VID Probe, click [RECOVER PIPELINE], verify playback stops and SENTINEL logs the recovery.

---

**Principle:** "Nur ergänzen und nichts entfernen" — All expansions are additive and modular.
