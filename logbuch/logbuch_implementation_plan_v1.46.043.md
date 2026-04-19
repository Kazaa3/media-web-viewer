# Implementation Plan: Orchestrator Unification & MPV WASM Support (v1.46.043)

## Context
This plan resolves the architectural overlap between the "Native Orchestrator" and the smart_route engine. It integrates MPV WASM (vsm) into the primary playback pipeline and ensures a unified forensic audit trail.

---

## User Review Required

### Logic Unification
- Refactor `VideoHandler.process()` to delegate its mode-decision to `smart_route`.
- Ensures specialized modes like `mpv_wasm` (Interactive/WebM) are available in the main UI, not just in test suites.

### MIME & Route Sync
- Switching to `smart_route` changes some internal mode names (e.g., `direct` → `direct_play`).
- Ensure the frontend `video.js` is synchronized with these new identifiers.

---

## Proposed Changes

### [Backend]
#### [MODIFY] `video_handler.py`
- Refactor `process()`:
    - Call `src.core.mode_router.smart_route()` for the initial mode decision.
    - Map the `smart_route` results back to the URL/Path structure required by `main.py`.

#### [MODIFY] `mode_router.py`
- Inject `[PLAY-PULSE]` auditing into `smart_route`.
- Refine the `mpv_wasm` detection logic to ensure it triggers correctly for specialized containers.

### [Frontend]
#### [MODIFY] `video.js`
- Update code to handle new mode names from the backend (`direct_play`, `mse`, `mpv_wasm`).
- Add a specific handler/switch for `mpv_wasm` playback.

---

## Open Questions
- Should `direct_play` still use the `/stream/via/direct/` route or the simpler `/direct/` route? (Proposed: Keep `/stream/via/direct/` for consistency with the recent MP3 fix).

---

## Verification Plan

### Automated Tests
- Run `eel.smart_route(file_path)` and verify it returns `mpv_wasm` for WebM or interactive files.

### Manual Verification
- Play a WebM file and verify it triggers the MPV WASM mode in the logs.
- Play an MP4 file and verify it still uses `direct_play`.

---

(See <attachments> above for file contents. You may not need to search or read the file again.)
