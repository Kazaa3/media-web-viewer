# Logbuch: UI Professionalism & HUD Enhancement (v1.46.093)

## Date: 2026-04-19

---

## Implementation Plan

### 1. Sidebar Accessibility
- Modified `.sidebar` and `.sidebar-lane` in `shell_master.css`:
  - Changed overflow settings from `hidden` to `overflow-y: auto`.
  - Set `overflow-x: hidden` to prevent horizontal shifting during scroll.

### 2. Context Menu (Right-Click) Repair
- Updated `showContextMenu(e, item)` in `common_helpers.js`:
  - Cleared menu content (`menu.innerHTML = ''`) before building new entries to prevent cumulative items.
  - Added a z-index check to ensure the menu floats above all other fragments.
  - Optionally included "VLC" and "MPV" options in the dynamic options array for parity with the standalone fragment.

### 3. HUD Hydration Stage Indicator
- Added a new `<span>` with ID `hydr-stage-indicator` next to the R button in the hydration group in `shell_master.html`.
- Updated `refreshForensicLeds()` in `common_helpers.js` to pull the current stage from `window.ForensicHydrationBridge.stage` and update the stage indicator.

### 4. Mock Path Synchronization
- Updated the synthetic mock generation loop (Stage 1) in `forensic_hydration_bridge.js` to use `media/test_files/` as the path prefix for all emergency pulsars.

---

## Verification Plan
- **Automated Tests:**
  - `node -c web/js/*.js`: Syntax check.
  - Path audit: Verify that mock paths in the generated library items contain the `test_files` subfolder.
- **Manual Verification:**
  - Sidebar Scroll: Hover over the sidebar and verify that a scrollbar appears when items exceed the viewport height.
  - Context Menu: Right-click multiple different items and verify the menu resets correctly each time (no double-entries).
  - HUD Stage: Watch the HUD during boot and verify the stage indicator moves from 0 -> 1 -> 2.

---

## Status
- [x] Sidebar accessibility improved
- [x] Context menu logic repaired
- [x] HUD hydration stage indicator added
- [x] Mock path synchronization complete
- [ ] Manual/automated verification pending

---

## Notes
- All synthetic mocks now point to `media/test_files/` as requested. Ensure this directory exists to avoid "File Not Found" errors.
- Awaiting user review and verification.
