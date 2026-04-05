# Implementation Plan — Universal Interaction Polish (v1.35.60)

## Objective
Polish the user interaction layer for universal media handling. Ensure right-click menus and playback routing are robust, context-aware, and visually clear for all media types (audio, video, ISO).

---

## Key Goals
- **Right-Click Menu Restoration [FRONTEND]:**
  - Fix `showContextMenu` in `common_helpers.js`.
  - Add high-visibility diagnostic badges to menu (audio, audio transcoded, video native, video transcoded hd).
- **Action Logic:**
  - Ensure "Abspielen" triggers the correct `playMediaObject` router.
- **Universal Click-to-Switch [AUDIOPLAYER]:**
  - Fix bug where clicking a video in the Queue tries to play as audio (0:00 error).
  - Update Queue click handler to use the Central Orchestrator: clicking a Video/ISO slides in the Video Cinema tab.
- **ISO Metadata Handling:**
  - Ensure ISO images are categorized as `video transcoded hd` and routed to the Video Player, not audio hardware.
- **Version Increment:**
  - Bump to v1.35.60. Baseline remains 29–30 items, now with full interactive support.

---

## Components to Modify
- `web/js/common_helpers.js`: Fix `showContextMenu`, add media type badge logic.
- `web/js/audioplayer.js`: Update `renderPlaylist` click handler for cross-module switching.
- `web/js/app_core.js`: Enhance `playMediaObject` to handle queue-resident items without duplicates.
- `web/js/version.js`: Increment to v1.35.60.

---

## Expected Outcome
- Right-clicking an ISO shows menu: `MEDIA TYPE: VIDEO TRANSCODED HD`.
- Left-clicking a Video/ISO in the Queue slides in the Video Player and starts streaming as MP4.
- Audio Player is hidden for video/ISO; no more 0:00 errors.
- All menu and routing logic is robust and context-aware.

---

## Verification
1. Right-click any ISO: menu shows correct badge and type.
2. Left-click a Video/ISO: Video Player appears, playback starts, Audio Player hides.
3. Confirm no duplicate playback or routing errors.

---

*Ready to proceed with the Universal Interaction Polish as described above.*
