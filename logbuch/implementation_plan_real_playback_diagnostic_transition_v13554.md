# Implementation Plan — Real Playback & Diagnostic Transition (v1.35.54)

## Overview
The HUD shows v1.35.53 and only 13 Titel (mock items), causing 0:00 playback. This plan introduces a toggle to hide mock data, fixes registration lag, and enables real library scanning and atomic backend logging.

## 🛠️ Key Goals
- **"Hide Mock Data" Logic:**
  - Add a toggle to the DATA-HUD to hide S1–S8 mock/broken tests, leaving only real items in the Queue.
- **Fix Registration Lag:**
  - Make RecoveryManager auto-refresh the hydration every time a new stage registers, ensuring all 22 Titel appear.
- **Playback Audit [BACKEND]:**
  - Add atomic logging to the backend media route to log the exact path requested, aiding in debugging 0:00 playback.
- **Transition to "Real Scan":**
  - Add a "SCAN REAL LIBRARY" button to the HUD to trigger a non-diagnostic, real database scan of the media/ folder.

## 📂 Components to Modify
- `web/js/diagnostics/recovery_manager.js`: Implement item filtering (is_mock) and reactive hydration.
- `web/js/diagnostics/gui_integrity.js`: Add "Hide Mocks" and "Scan Library" buttons to the HUD.
- `web/app_bottle.py`: Add atomic logging to serve_media.

## 🧪 Expected Outcome
- On reload, clicking "HIDE MOCKS" drops the Queue from 22 to ~8 real items.
- Playing a FLAC or MP3 will move the seeker past 0:00.
- "SCAN REAL LIBRARY" enables a full, non-diagnostic scan.

---

*This plan will enable a seamless transition from diagnostic to real playback and provide robust visibility and control for final verification.*
