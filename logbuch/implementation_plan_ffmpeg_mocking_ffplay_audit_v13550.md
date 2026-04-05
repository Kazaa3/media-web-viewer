# Implementation Plan — FFmpeg Mocking & FFplay Audit (v1.35.50)

## Overview
To resolve "Real vs. Mock" confusion and ensure the audio pipeline is fully functional, an FFmpeg Pulse Generator will be implemented. This provides a backend-generated audio stream for direct pipeline verification, and a native ffplay test for system-level validation.

## 🛠️ Key Goals
- **FFmpeg Pulse Generator [BACKEND]:**
  - Add a new route `/diag/pulse/<freq>.mp3` to the backend (app_bottle.py).
  - Use FFmpeg to generate a pure sine wave (e.g., 440Hz) and stream it to the browser.
  - Hearing the "Beep" confirms the Bottle → Browser pipeline is working.
- **Mock Stage (15 Titel total):**
  - Add `stage_ffmpeg_mock.js` with two items: [PULSE] 440Hz and [PULSE] 880Hz.
  - This brings the diagnostic count to 15, providing final proof of functionality.
- **Local FFplay Verification:**
  - Add a "Test with FFplay" button to the DATA-HUD (gui_integrity.js).
  - Clicking this opens a native ffplay window on Linux to verify stream quality outside the browser.
  - This eliminates browser caching as a source of error.
- **Pathing Clarity:**
  - Ensure all REAL-PLAY items are strictly searched for in the `media/` subfolder.

## 📂 Components to Modify
- [NEW] `web/js/diagnostics/stages/stage_ffmpeg_mock.js`: 2 items (FFmpeg Pulse Test)
- [MODIFY] `web/app_bottle.py`: Implement the `/diag/pulse/` route
- [MODIFY] `src/core/main.py`: Add the eel bridge for local ffplay execution
- [MODIFY] `web/js/diagnostics/gui_integrity.js`: Add the "FFplay Verify" button

## 🧪 Expected Outcome
- The Queue will show 15 Titel.
- Playing the [PULSE] items produces a clear tone.
- If browser playback fails but ffplay works, the issue is isolated to frontend/JS state.

---

*This plan will provide end-to-end verification of the audio pipeline, both in-browser and natively, using real-time generated audio.*
