# Implementation Plan: Media Orchestration Hardening & Playback Fix (v1.46.042)

## Context
This plan resolves the reported MP3/Audio playback failure and implements a unified forensic audit trail ([PLAY-PULSE]) for the media workstation's playback engines.

---

## User Review Required

### MIME Resolution
- Switching `server_file_direct` from auto to an explicit MIME mapping for common forensic formats (MP3, MP4, MKV).
- Ensures the browser's HTML5 pipeline correctly identifies streamable assets.

### Forensic Audit
- All playback attempts (Audio/Video) will now trigger a [PLAY-PULSE] log in both backend and frontend, including the resolved route and MIME type.

---

## Proposed Changes

### [Backend]
#### [MODIFY] `main.py`
- `server_file_direct`:
    - Add explicit MIME mapping for `.mp3` → `audio/mpeg` and `.wav` → `audio/wav`.
    - Inject [PLAY-PULSE] log with resolved path and headers.
- `get_play_source`:
    - Add [PLAY-PULSE] entry for the video orchestrator routing.

### [Frontend]
#### [MODIFY] `audioplayer.js`
- Enhance `playAudio` with explicit forensic trace calls (`mwv_trace`).
- Ensure `onerror` on the audio pipeline triggers a recovery toast.

#### [MODIFY] `video.js`
- `playVideo`:
    - Add [PLAY-PULSE] trace for the VideoPlayer Orchestrator.
    - Synchronize forensic metadata with the diagnostic HUD.

---

## Open Questions
- Should we implement a "Playback Health Check" that probes the direct stream route before attempting to play? (Proposed: Added to future roadmap, currently focus on logging).

---

## Verification Plan

### Automated Tests
- Run `verify_ultimate.py` (if updated) or a simple curl to `/stream/via/direct/` to verify headers.

### Manual Verification
- Play an MP3 file and check the console/logs for [PLAY-PULSE].
- Verify the `content-type` header in browser DevTools is `audio/mpeg`.
- Play a video and verify the orchestrator logging in the diagnostic sidebar.

---

(See <attachments> above for file contents. You may not need to search or read the file again.)
