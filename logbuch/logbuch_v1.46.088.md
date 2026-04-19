# Logbuch: Click Interactivity Restoration (v1.46.088)

## Date: 2026-04-19

---

## Implementation Plan

### Core Logic & Interaction
- **app_core.js**
  - Refactored `playMediaObject` to check the current active tab via `document.body.getAttribute('data-mwv-tab')`.
  - If already on the target tab ('player' or 'video'), the play callback is executed immediately without calling `switchTab`.
  - This eliminates the destructive fragment reload that was disrupting the click event and playback handshake.

- **audioplayer.js**
  - Removed `pointer-events: none` from the inner item content div.
  - Ensured that clicks on any part of the track item correctly bubble to the `legacy-track-item` container.

- **main.css**
  - Updated `.legacy-track-item` style to use `cursor: pointer` for better visual feedback.

---

## Verification Plan
- **Click Responsiveness:** Verify that clicking an item in the queue starts playback instantly without the tab "flashing" or re-loading.
- **Cross-Tab Playback:** Verify that clicking an item from the Library (different tab) still correctly switches to the Player and starts playback.
- **Visual Feedback:** Confirm the mouse cursor changes to a pointer when hovering over items.

---

## Status
- [x] Force reload removed from active tab clicks
- [x] Pointer events and bubbling fixed
- [x] Visual feedback improved
- [ ] Manual/automated verification pending

---

## Notes
- This change restores fast, non-disruptive playback interactivity and improves user experience.
- Awaiting user review and verification.
