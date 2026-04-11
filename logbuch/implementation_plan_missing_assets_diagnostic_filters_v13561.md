# Implementation Plan — Missing Assets & Diagnostic Filters (v1.35.61)

## Objective
Restore the full 29-item diagnostic baseline and implement a Media Type Dropdown for high-fidelity queue filtering.

---

## Key Goals
- **Unified Stage Registration [APP.HTML]:**
  - Register all missing diagnostic scripts (e.g., `stage_format_real.js`, `stage_video_universal.js`) to ensure the library is fully hydrated.
- **Type Selection Dropdown [UI]:**
  - Add a `<select>` dropdown to the top-right of the Queue Pane (next to "Liste leeren").
  - Options: Alle Medien, Nur Audio, Nur Video, Nur ISO, Nur Transcoded.
  - Use premium glassmorphic styling for visual clarity.
- **High-Fidelity Filtering [LOGIC]:**
  - Update `audioplayer.js` to support real-time filtering of the diagnostic queue without reloading the app.
  - Implement `filterQueueByType()` and update `renderPlaylist` to respect the active filter.
  - Filter logic will detect `.iso` files and `_transcoded` suffixes for precise diagnostic views.
- **Version Increment:**
  - Bump to v1.35.61, targeting 29/29 titles hydrated and filterable.

---

## Components to Modify
- `web/js/app.html`: Add the missing 4 diagnostic stage scripts.
- `web/fragments/player_queue.html`: Inject the `<select>` dropdown with premium glassmorphic styling.
- `web/js/audioplayer.js`: Implement `filterQueueByType()` and update `renderPlaylist` for filtering.
- `web/js/version.js`: Increment to v1.35.61.

---

## Expected Outcome
- On reload, the Queue displays all 29 titles.
- The new dropdown allows filtering by media type (All, Audio, Video, ISO, Transcoded) in real time.

---

## Verification
1. Reload the app: 29 items appear in the Queue.
2. Use the dropdown to filter: only matching items are shown, with no reload required.

---

*Ready to proceed with restoring missing files and implementing the type selection as described above.*
