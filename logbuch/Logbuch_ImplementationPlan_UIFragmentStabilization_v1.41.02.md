# Implementation Plan – v1.41.02 UI Fragment Stabilization

This plan addresses the persistent "Black Screen" and "Missing Sub-Nav" issues by identifying and removing hidden inline styles nested within individual UI fragments.

---

## User Review Required
**CAUTION**
- **Bulk Fragment Cleanup:** I will perform a search-and-replace across ALL files in the `web/fragments/` directory to remove hardcoded `display: none` styles. This ensures that when the master container is shown, the content is actually visible.

**IMPORTANT**
- **Real-time Diagnostics:** I will update the DOM HUD to show the current height variables (`--active-header-height` etc.). This will allow us to see if the orchestrator is even alive on your end.

---

## Proposed Changes

### Global Branding & Core Logic
- **[MODIFY] config_master.py**
  - Update VERSION to v1.35.68 to fix the footer branding.
- **[MODIFY] dom_hud.js**
  - Add geometry tracking (H/S/F offsets) to the HUD display.

### Fragment Stabilization (The "Un-Hide" Pass)
- **[BULK MODIFY] web/fragments/*.html**
  - Remove all instances of `style="display: none;"` and `style="display:none;"`.
  - Move any necessary initial-hide logic to the central orchestrator (`ui_core.js`) or CSS classes.

### Sub-Nav Layout Integrity
- **[MODIFY] app.html**
  - Ensure `#sub-nav-container` has a sane min-height or visible fallback if variables are missing.

---

## Open Questions
None. These are stabilization fixes for existing regressions.

---

## Verification Plan

### Manual Verification
- **Footer:** Verify version shows v1.35.68.
- **HUD:** Verify the HUD shows non-zero values for H (38) and S (30) when the Player is active.
- **Fragments:** Verify that selecting "Bibliothek" or "Edit" shows their actual content instead of a black screen.
