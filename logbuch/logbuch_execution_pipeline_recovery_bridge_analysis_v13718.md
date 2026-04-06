# Pipeline Recovery: Super-Kill Bridge (v1.37.18) — Analysis & Integration

## 🛡️ Building the Pipeline Recovery Bridge

- **Targeted Media Purge:**
  - Implemented `kill_media_processes(target="ffmpeg")` in main.py for verified, path-aware termination of media processes (ffmpeg, mkvmerge) to resolve pipeline stalls.
- **Forensic UI Integration:**
  - Identified the VID (Video Health) pane in diagnostics_sidebar.html for the [RECOVER] button and recovery status indicator.
- **SENTINEL Trace Integration:**
  - Every recovery event is captured by the SENTINEL engine, providing a persistent forensic record of system maintenance and process termination.

---

## Implementation Plan
- **Backend (main.py):**
  - Implement `kill_stalled_ffmpeg_streams()` Eel bridge, integrating with super_kill.py logic.
- **Sidebar UI (diagnostics_sidebar.html):**
  - Add [RECOVER] button and recovery status indicator to the VID pane.
- **Controller (sidebar_controller.js):**
  - Implement `triggerPipelineRecovery()` for frontend-backend handshake and SENTINEL event logging.

---

## Open Questions
- Should the recovery action also trigger an automatic SENTINEL Alert on the frontend? (White "Tactical Recovery Executed" notification recommended.)

---

## Verification Plan
- **Automated:** Spawn a mock FFmpeg process and verify the kill_stalled_ffmpeg_streams bridge terminates it.
- **Manual:** Start video playback, open VID Probe, click [RECOVER], verify playback stops and SENTINEL logs the recovery.

---

**Principle:** "Nur ergänzen und nichts entfernen" — All expansions are additive and modular.
