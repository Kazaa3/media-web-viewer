# Implementation Plan — Universal Event & Navigation Patch (v1.35.63)

## Objective
Synchronize context menu IDs and harden video player routing to ensure seamless interaction and playback transitions.

---

## Key Goals
- **Context Menu ID Sync [FIXED]:**
  - Discovery: The code referenced `context-menu`, but the fragment was named `custom-context-menu`.
  - Fix: Synchronize both to `context-menu` across `common_helpers.js` and the HTML fragment for reliable menu activation.
- **Hardened Video Routing [FIXED]:**
  - Discovery: `playMediaObject` used a fixed 150ms delay, which was too short for the fragment loader to finish rendering the Cinema player.
  - Fix: Replace the timer with a proper callback. `playVideo` will only fire after `switchTab` transition is 100% complete and the DOM is ready.
- **Z-Index & Visibility Audit:**
  - Ensure the context menu is forced to the front with `pointer-events: all` and `z-index: 100005`.
- **Version Increment:**
  - Bump to v1.35.63, targeting 29/29 titles routable and right-clickable.

---

## Components to Modify
- `web/fragments/context_menu.html`: Rename ID to `context-menu`.
- `web/js/app_core.js`: Update `playMediaObject` to use navigation callbacks instead of timers.
- `web/js/version.js`: Increment to v1.35.63.

---

## Expected Outcome
- Clicking a Video in the Queue instantly switches to the Cinema tab and starts playback, with no white screen or delay.
- Right-clicking any item pops up the diagnostic menu reliably.

---

## Verification
1. Click a Video in the Queue: Cinema tab loads and playback starts without delay.
2. Right-click any item: Context menu appears with correct diagnostic label and full interactivity.

---

*Ready to proceed with synchronized IDs and the transition fix as described above.*
