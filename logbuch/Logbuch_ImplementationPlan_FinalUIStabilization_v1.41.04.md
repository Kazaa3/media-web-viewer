# Implementation Plan – v1.41.04 Final UI Stabilization

This plan definitively resolves the "Black Screen" and "Missing Sub-Menu" issues through structural enforcement and backend versioning, while strictly respecting the integrity of historical log files.

---

## User Review Required
**IMPORTANT**
- **Log Protection:** I have confirmed that all .md files in the logbuch/ directory have been reverted to their original state. No further changes will be made to any documentation or log files.

**TIP**
- **Backend Versioning:** I will create a VERSION file in the project root containing v1.41.00. This allows config_master.py to pull the version accurately without needing hardcoded string replacements in the code.

---

## Proposed Changes

### Core Versioning
- **[NEW] VERSION**
  - Create file with content: v1.41.00

### Fragment & Layout Stabilization
- **[MODIFY] main.css**
  - **Sub-Nav Enforcement:** Ensure `#sub-nav-container` has a `min-height: 30px` when visible to prevent vertical collapse.
  - **Content Deck Depth:** Ensure `.tab-content` elements have a guaranteed `z-index` and `display: flex !important` when active.
- **[MODIFY] app.html**
  - Remove any remaining `style="display: none;"` from the sub-nav and main containers to allow CSS to manage visibility.

### Logic Alignment
- **[MODIFY] ui_core.js**
  - Add a safety check to `init()` to ensure that if the backend config is delayed, the UI starts with a visible "Safe Mode" state for the Player view.

---

## Open Questions
None. This is a targeted fix to restore visual integrity.

---

## Verification Plan

### Manual Verification
- **Logbuch:** Check `logbuch/` files to confirm they still show v1.35.68 (historical record).
- **Footer:** Confirm version is reported as v1.41.00 via the new VERSION file.
- **Sub-Nav:** Confirm the sub-navigation pills (Queue/Playlist) are visible and clickable.
- **Visibility:** Verify that the black screen is replaced by actual content (Player Queue or Library Items).
