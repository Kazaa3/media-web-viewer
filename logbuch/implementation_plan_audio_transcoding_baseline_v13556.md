# Implementation Plan — Audio Transcoding Baseline (v1.35.56)

We are now stress-testing the On-The-Fly Transcoding engine using real ALAC and WMA samples from your library.

## 🛠️ Key Goals
- **Stage 11: Real Audio Transcoding:**
  - Add 2 actual transcoding tasks to the Queue, forcing the backend to spawn FFmpeg and stream converted audio to the browser.
- **Transcode Targets:**
  - **ALAC ➔ FLAC:** 11 - All This and More.alac.flac_transcoded
  - **WMA ➔ OPUS:** 2-09 - Good Old Days.wma.opus_transcoded
- **Queue Growth (24 Titel total):**
  - Expands the diagnostic baseline to 24 Titel, ensuring even "unsupported" formats are playable via the transcoding layer.
- **Backend Verification:**
  - Atomic logging in the backend will show the exact conversion path (e.g., ALAC -> FLAC) in the terminal during playback.

## 📂 Components to Modify
- [NEW] `web/js/diagnostics/stages/stage_transcode_real.js`: 2 real transcoding items.
- [MODIFY] `web/js/version.js`: Increment to v1.35.56.

## 🧪 Expected Outcome
- Clicking the ALAC track will trigger transcoding, with the HUD active and music playing after a brief "TRANSCODING STARTED" pulse in the terminal.
- The WMA track will be converted to Opus in real-time.

---

*This plan ensures robust, transparent transcoding for all major formats, completing the diagnostic baseline for v1.35.56.*
