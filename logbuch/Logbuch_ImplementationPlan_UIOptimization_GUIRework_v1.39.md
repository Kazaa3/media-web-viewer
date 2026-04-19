# Implementation Plan – UI Optimization & GUI Rework (v1.39)

This plan addresses the user's request to accelerate application startup, ensure the sidebar is hidden by default, restore missing sub-menus, and perform a GUI rework for a more premium, professional look.

---

## User Review Required
**IMPORTANT**
- **Performance vs. Stability:** Disabling `kill_on_startup` might lead to port conflicts if the application was not closed correctly. I will implement a faster check to mitigate this.

**NOTE**
- **Sidebar Behavior:** The sidebar will now start in a collapsed state for all categories, but can still be toggled manually via the header button or Alt key.

---

## Proposed Changes

### Backend Optimization & Configuration
- **[MODIFY] config_master.py**
  - Set `kill_on_startup` to `False` by default to accelerate boot.
  - Update `ui_visibility_matrix` for the media category: set `contextual_pill_nav` to `True` (restores sub-menu).
  - Update `ui_visibility_matrix` for all categories: set `sidebar_visible` to `False` (hides sidebar by default).
  - Ensure `fast_startup` is prioritized.
- **[MODIFY] main.py**
  - Optimize the `start_app` sequence to bypass heavy port cleaning if not strictly necessary.
  - Reduce blocking calls in the bootstrap phase.

### GUI Rework & Frontend Fixes
- **[MODIFY] main.css**
  - Implement "Forensic Elite" theme enhancements:
    - Higher contrast for dark mode.
    - Glassmorphism effects for the header and footers.
    - Improved typography and spacing for a "workstation" feel.
    - Subtle micro-animations for tab transitions.
    - Ensure the `.collapsed` sidebar state is perfectly clean.
- **[MODIFY] app.html**
  - Clean up the header layout for a more symmetrical and professional appearance.
  - Ensure the `sub-nav-container` (contextual pills) has proper styling and visibility.
  - Polish the "STATUS" and "DIAGNOSTICS" button designs.
- **[MODIFY] ui_nav_helpers.js**
  - Ensure any hardcoded overrides in `refreshUIVisibility` respect the new configuration.
  - Fix any race conditions that might prevent the sub-menu from appearing at startup.

---

## Open Questions
- Should I implement a "Splash Screen" or a more detailed "Loading" progress bar during the accelerated startup to provide better feedback?
- Do you prefer the "iPad OS" (Light/Rounded) or "Forensic Elite" (Dark/Monospaced/Technical) look as the primary default? (Screenshot shows a mix, I'll lean towards the darker 'Forensic' style as requested).

---

## Verification Plan

### Automated Tests
- Run `scripts/check_backend_data.py` to ensure the config is valid.
- Use `scripts/headless_dom_audit.sh` to verify visible elements after startup.

### Manual Verification
- Restart the app and measure the time to "UI READY".
- Verify the sidebar is collapsed on boot.
- Verify the "Queue / Playlist / Lyrics" sub-menu is visible when the Player tab is active.
- Inspect the new UI elements for premium aesthetics.
