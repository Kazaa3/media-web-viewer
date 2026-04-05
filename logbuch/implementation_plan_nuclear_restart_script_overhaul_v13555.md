# Implementation Plan — Nuclear Restart & Script Overhaul (v1.35.55)

## Overview
A native "Kill & Restart" system will be implemented, allowing a complete backend reboot from the DATA-HUD. Cleanup scripts will be hardened to prevent zombie FFmpeg/FFplay processes, and a UI toggle will allow hiding mock data for focused real-asset testing.

## 🛠️ Key Goals
- **"Nuclear Restart" Button [UI]:**
  - Add a high-priority "HARD REBOOT BACKEND" button to the HUD, displaying the current PID for verification.
- **Hard Reboot Bridge [BACKEND]:**
  - Add a `nuclear_restart()` function to `main.py` that spawns a detached shell running `reboot_mwv.sh` and exits the current process.
- **Script Overhaul [SCRIPTS]:**
  - `cleanup_mwv.sh`: Add `pkill` logic for ffmpeg and ffplay to ensure no background transcoders remain.
  - `reboot_mwv.sh`: New script to clean up and start the MWV backend in one step.
- **Hide Mock Data:**
  - Add a "HIDE MOCK DATA" toggle to the HUD to filter out S1–S8 tests, showing only real format samples.

## 📂 Components to Modify
- [NEW] `scripts/reboot_mwv.sh`: Clean-and-Start orchestration.
- [MODIFY] `scripts/cleanup_mwv.sh`: Enhanced zombie-process termination.
- [MODIFY] `src/core/main.py`: Implement hard_restart Eel bridge.
- [MODIFY] `web/js/diagnostics/gui_integrity.js`: Add "NUCLEAR RESTART" button.

## 🧪 Expected Outcome
- If playback stalls at 0:00, clicking "HARD REBOOT" will restart the backend, with a new PID shown in the HUD.
- Mock items can be hidden, showing only real MP3/FLAC/WAV assets for focused testing.

---

*This plan ensures robust backend recovery, process hygiene, and focused diagnostic visibility for v1.35.55.*
