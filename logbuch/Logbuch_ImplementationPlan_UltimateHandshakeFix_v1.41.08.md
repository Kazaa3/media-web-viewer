# Implementation Plan – v1.41.08 Ultimate Handshake Fix

This plan implements a "Simple & Reliable" boot concept to eliminate black screens and missing sub-menus caused by backend handshake stalls.

---

## User Review Required
**IMPORTANT**
- **Safe-Boot Sequence:** I will implement a 2-second timeout for all backend configuration calls. If the backend is slow or stuck, the UI will automatically continue in Safe Mode with default visibility settings instead of staying black.

**TIP**
- **Visibility Lockdown:** I will enforce a "Minimum Visibility" rule in the CSS. All main content areas will be forced to render after a 5-second safety timer, bypassing any stuck JavaScript loading state.

---

## Proposed Changes

### UI Orchestration (Safe-Init)
- **[MODIFY] ui_core.js**
  - **Timeout Logic:** Wrap the `eel.get_ui_settings` call in a `Promise.race` with a 2000ms timeout.
  - **Fail-Safe Apply:** If the timeout triggers, immediately fire `apply('media')` with hardcoded safe-defaults to show the Header and Sub-Nav.
  - **Boot Watchdog:** Add a global timer that removes all loading-fragment overlays and forces `opacity: 1` on containers after 5 seconds of inactivity.

### Navigation Integrity
- **[MODIFY] ui_nav_helpers.js**
  - **Redundant Population:** Ensure `updateGlobalSubNav()` is triggered as a fallback if the DOM observer detects an empty bar during a category switch.
  - **Status Category:** Finalize the status pill-cluster mapping to ensure it appears correctly upon clicking "STATUS".

### Geometry & CSS
- **[MODIFY] main.css**
  - **Structural Guard:** Ensure `body.mwv-hide-subnav #sub-nav-container` only sets `height: 0` and `overflow: hidden` instead of `display: none`, allowing the browser to keep the layout slots ready.

---

## Open Questions
None. This is a stability-first architectural hardening.

---

## Verification Plan

### Manual Verification
- **Normal Boot:** Start the app and verify it loads instantly.
- **Stall Test:** I will temporarily block the backend version call in a test run and verify the UI still renders the "Safe Mode" layout within 2 seconds.
- **Sub-Menu Check:** Click through categories and verify the pills update and stay visible.
