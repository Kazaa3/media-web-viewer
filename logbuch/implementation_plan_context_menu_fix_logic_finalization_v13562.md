# Implementation Plan — Context Menu Fix & Logic Finalization (v1.35.62)

## Objective
Restore full context menu functionality and ensure the diagnostic queue displays all 29 items as intended.

---

## Key Goals
- **Context Menu Restoration [FRONTEND]:**
  - Move from `oncontextmenu` assignment to `addEventListener('contextmenu')` for robust, fragment-safe menu activation.
  - Set `#context-menu` z-index to 20000+ to guarantee visibility above all UI layers.
- **Diagnostic Queue Integrity [LOGIC]:**
  - Fix the "15 Items" bug: Update `syncQueueWithLibrary` in `audioplayer.js` to allow all categories in the Queue when Diagnostic Mode is active, not just "Audio".
  - This will restore the full 29-item baseline in the Queue.
- **Mock Filtering Visibility [HUD]:**
  - Update HUD styles so the "Toggle Mock Filtration" button clearly indicates ON (Blue) or OFF (Grey/Red) state.
- **Version Increment:**
  - Bump to v1.35.62, targeting 29/29 titles visible and right-clickable.

---

## Components to Modify
- `web/js/audioplayer.js`: Relax category checks in `syncQueueWithLibrary`, harden context menu listeners.
- `web/js/common_helpers.js`: Add diagnostic logging to context menu logic.
- `web/js/version.js`: Increment to v1.35.62.

---

## Expected Outcome
- Upon reload, the Queue count will show 29 titles (with mocks) or 20 (without mocks).
- Right-clicking any item opens the context menu with the correct "Media Type" label.
- Context menu is always visible above the player deck.
- HUD clearly shows mock filtration state.

---

## Verification
1. Reload the app: Queue shows 29/29 items.
2. Right-click any item: Menu appears with correct label and is never hidden.
3. Toggle mock filtration: HUD button color updates instantly.

---

*Ready to proceed with the menu fix and full queue restoration as described above.*
