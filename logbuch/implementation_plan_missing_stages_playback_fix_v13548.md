# Implementation Plan — Missing Stages & Playback Fix (v1.35.48)

## Overview
Analysis revealed a 9/13 item discrepancy and a playback failure (0:00 / 0:00). The missing stages (Negative & Positive) were deleted from the stages/ folder, and the "Golden Sample" MP3 is not reaching the HTML5 audio element due to a likely backend path-resolution issue.

## 🛠️ Key Goals
- **Restore the missing 4 Stages (13/13):**
  - Recreate `stage_negative.js` (2 items) and `stage_positive.js` (2 items) in `web/js/diagnostics/stages/`.
  - This will restore the Queue to 13 items.
- **Fix the Audio Pipeline:**
  - Audit and harden the media-serving route in `src/core/main.py`.
  - Add a "Diagnostic-Pass" so the backend will serve diagnostic items not yet in the database.
- **Confirm v1.35.48:**
  - Ensure all headers and footers display v1.35.48 as the stable baseline.

## 📂 Files to Create/Modify
- [NEW] `web/js/diagnostics/stages/stage_negative.js` (Missing file tests)
- [NEW] `web/js/diagnostics/stages/stage_positive.js` (Healthy file tests)
- `src/core/main.py`: Harden media-serving route for non-indexed files.

## 🧪 Expected Outcome
- On reload, the Queue will show 13 items.
- Pressing play on the [REAL-PLAY] item will play audio.
- All version tags will show v1.35.48.

---

*This plan will restore full diagnostic coverage and ensure reliable playback for the Golden Sample and all test tracks.*
