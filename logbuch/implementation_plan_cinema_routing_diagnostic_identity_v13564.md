# Implementation Plan — Cinema Routing & Diagnostic Identity (v1.35.64)

## Objective
Finalize robust routing and diagnostic labeling for all video assets, ensuring specialized formats are recognized and all queues are synchronized.

---

## Key Goals
- **Diagnostic Format Detection [FIXED]:**
  - Discovery: `isVideoItem` did not recognize `.mp4_pass` and `.mp4_transcoded` as video formats.
  - Fix: Update the global extension registry in `common_helpers.js` to include these specialized diagnostic suffixes.
- **Cinema Queue Synchronization [FIXED]:**
  - Update the Video Player's queue to display `[S12–S15]` stage labels, matching the Audio Player.
  - Fix the "Cinema Queue 0" bug by ensuring the item count updates correctly in the Video tab.
- **Cross-Module Selection [FIXED]:**
  - Fix the click handler in the Video Queue to use the universal `playVideo()` controller instead of a non-existent `play()` function.
  - Update "Play Next/Prev" logic in `audioplayer.js` to use the global router, enabling seamless tab switching between Audio and Video tracks.
- **Version Increment:**
  - Bump to v1.35.64, targeting 29/29 titles perfectly routed and labeled.

---

## Components to Modify
- `web/js/common_helpers.js`: Update `isVideoItem` extension registry.
- `web/js/video.js`: Fix `renderVideoQueue` click handler and stage labeling.
- `web/js/audioplayer.js`: Update `playNext/Prev` to use the global router.
- `web/js/version.js`: Increment to v1.35.64.

---

## Expected Outcome
- Clicking any `[S12–S15]` item in any queue triggers the "Cinema Jump" and starts video playback.
- The Video Queue displays correct stage labels and item counts.
- Sequential navigation (Next/Prev) switches tabs as needed.

---

## Verification
1. Click any `[S12–S15]` item: Cinema tab loads and playback starts.
2. Video Queue shows correct stage labels and item count.
3. Play Next/Prev switches between Audio and Video tabs as needed.

---

*Ready to proceed with routing and labeling finalization as described above.*
