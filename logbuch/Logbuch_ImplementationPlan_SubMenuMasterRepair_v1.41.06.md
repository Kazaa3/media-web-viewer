# Implementation Plan – v1.41.06 Sub-Menu Master Repair

This plan restores the "Mega-Nav" sub-menu (pill bar) and ensures it is centrally controllable through the unified configuration layer.

---

## User Review Required
**IMPORTANT**
- **Central Control:** I will add a `force_sub_nav_visible` flag to the `ui_settings` in `config_master.py`. This will allow you to globally enable or disable the sub-menu across all categories from a single location.

**TIP**
- **Category Restoration:** The reason the sub-menu was empty for the "STATUS" view is a missing mapping in the navigation registry. I will add a dedicated sub-menu cluster for the Status/Diagnostics view.

---

## Proposed Changes

### Central Configuration
- **[MODIFY] config_master.py**
  - **New Master Toggle:** Add `"force_sub_nav_visible": True` to the `ui_settings` dictionary.
  - **Matrix Audit:** Ensure all categories (including status) are present in the `ui_visibility_matrix`.

### UI Orchestration
- **[MODIFY] ui_core.js**
  - **Override Logic:** Update the `apply()` function to check for the master `force_sub_nav_visible` flag. If true, it will override the per-category matrix setting and show the bar.
- **[MODIFY] ui_nav_helpers.js**
  - **Status Mapping:** Add the status category to the `subNavMap` with relevant diagnostic tabs (Logs, Health, Metrics).
  - **Validation:** Ensure `updateGlobalSubNav` correctly falls back to a sensible default if the category is unknown.

### Geometry Cleanup
- **[MODIFY] main.css**
  - **Visual Depth:** Add a subtle gradient background to `#sub-nav-container` to ensure it is distinguishable from the black player background.

---

## Open Questions
None. This is a targeted restoration of a core UI component.

---

## Verification Plan

### Manual Verification
- **Config Toggle:** Set `force_sub_nav_visible` to `False` in `config_master.py` and verify the bar disappears globally.
- **Category Switch:** Click "Player" and verify "Queue / Playlist" appear.
- **Status View:** Click "STATUS" and verify the new diagnostic pills (Logs/Health) appear in the sub-menu.
