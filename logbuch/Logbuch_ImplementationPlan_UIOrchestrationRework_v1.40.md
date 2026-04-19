# Implementation Plan – UI Orchestration Rework (v1.40)

This plan addresses the "broken" GUI state caused by scattered logic and conflicting state sources (JS vs. CSS vs. LocalStorage). We will transition to a Strict Configuration-First architecture.

---

## User Review Required
**IMPORTANT**
- **LocalStorage Policy:** I will disable the automatic "restoration" of the sidebar and header state from localStorage on startup. The application will strictly follow the `config_master.py` defaults to ensure a predictable "Workstation" experience. User toggles will remain functional at runtime but will not survive a restart unless configured in the backend.

**CAUTION**
- **Structural CSS Change:** I am moving visibility control from JS `.style.display` to CSS classes on the `<body>`. If you have custom scripts that manually hide elements, they may be overridden by this new system.

---

## Proposed Changes

### Core UI Engine
- **[NEW] ui_core.js**
  - Implement `window.MWV_UI` singleton.
  - Centralize UI_CONSTANTS (Header: 38px, SubNav: 30px, Footer: 48px).
  - Handle the application of categories via `MWV_UI.apply(category)`.
  - Enforce geometry updates globally via a single `requestAnimationFrame` hook.

### Styling & Layout Integrity
- **[MODIFY] main.css**
  - Implement state-based visibility classes:
    - `.mwv-hide-header`
    - `.mwv-hide-subnav`
    - `.mwv-hide-footer`
    - `.mwv-sidebar-collapsed`
  - Ensure absolute alignment with the 38px/30px/48px geometry.

- **[MODIFY] app.html**
  - Add the new `ui_core.js` script tag.
  - Remove redundant inline styles in the high-level containers that conflict with the matrix.

### Logic Decoupling
- **[MODIFY] ui_nav_helpers.js**
  - Deprecate `refreshUIVisibility`, `refreshViewportLayout`, and `updateLayoutOffsets`.
  - Point all visibility-related calls to `MWV_UI`.
  - Clean up `DOMContentLoaded` to remove conflicting localStorage lookups.

- **[MODIFY] app_core.js**
  - Update `mwv_finalize_boot` to use the new `MWV_UI` orchestrator for the initial category setup.
  - Eliminate race conditions in fragment loading that cause "black holes".

---

## Open Questions
- Should we allow any localStorage overrides at all for the structural elements, or should it be 100% config-driven? (I recommend 100% config-driven for "Forensic Workstation" consistency).
- Are there specific tabs where you always want the sidebar visible, regardless of the global state?

---

## Verification Plan

### Automated Checks
- Run `tests/verify_v139.py` (updated for v1.40 logic) to check backend parity.
- Use grep to ensure no JS file still contains direct `.style.display = 'none'` for master components.

### Manual Verification
- Boot app: Check if it follows `config_master.py` perfectly.
- Toggle Sidebar: Verify it works and shifts the layout correctly.
- Switch Tabs: Verify that transitions are atomic and no elements "flicker" in or out incorrectly.
