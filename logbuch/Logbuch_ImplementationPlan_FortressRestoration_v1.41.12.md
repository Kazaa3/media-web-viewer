# Implementation Plan – v1.41.12 Fortress Restoration

This plan implements a "Zero-Ghost" startup policy and ensures the sub-menu is redundantly populated to eliminate empty states.

---

## User Review Required
**CAUTION**
- **Ghost Kill Policy:** From now on, the application will automatically and aggressively purge any process occupying its port (8345) before starting. This ensures you are always running the latest code without manual intervention.

**IMPORTANT**
- **Sub-Nav Guardian:** I discovered that the sub-menu population could fail silently if a single script error occurs. I am moving to an "Atomic Render" model where the menu is only cleared IF the new buttons are successfully generated.

---

## Proposed Changes

### Startup Logic (Zero-Ghost)
- **[MODIFY] main.py**
  - **Environment Cleansing:** Call `pc.cleanup_environment()` at the top of `start_app()`.
  - **Port Watchdog:** Implement a small loop that waits for the OS to release port 8345 after killing ghosts, before allowing `eel.start`.

### Navigation Integrity (JS)
- **[MODIFY] ui_nav_helpers.js**
  - **Atomic Rendering:** Only clear the `sub-nav-container` once the new `innerHTML` string is complete and verified.
  - **Health Heartbeat:** Add a recurring check (every 3 seconds) that verifies if the sub-nav is empty while a category is active; if so, trigger `updateGlobalSubNav`.

### Geometry & CSS
- **[MODIFY] main.css**
  - **Visibility Guarantee:** Enforce `display: flex !important` for the pill container and add a `min-width` to ensure pills never collapse into a 0-pixel space.

---

## Open Questions
None.

---

## Verification Plan

### Manual Verification
- **Ghost Test:** Start the app, close it with the "X" (to simulate a ghost), and start it again. Verify it boots correctly on the same port.
- **Sub-Nav Check:** Toggle "STATUS" and "Player" and verify the pills appear within < 500ms.
- **Empty Guard:** Manually delete the sub-nav contents in the console and verify the "Guardian" re-hydrates them within 3 seconds.
