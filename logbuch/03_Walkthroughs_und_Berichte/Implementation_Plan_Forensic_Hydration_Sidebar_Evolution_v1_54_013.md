# Implementation Plan – Forensic Hydration & Sidebar Evolution (v1.54.013)

## Objective
Enhance workstation visibility into hydration states and modernize the discovery interface with deeper forensic filtering and layer management.

---

## User Review Required

### IMPORTANT
- **New Filter Modes:** Introduce Object and Release modes to the discovery engine. Assumes backend provides `is_object` and `is_release` flags (or similar) in the library payload.

### WARNING
- **DOM Auditor Expansion:** Add a new check (H-9) to the DOM Auditor to detect hydration stalls like "Lade Player..." for identifying silent boot failures.

---

## Proposed Changes

### [Diagnostics] dom_auditor.js
- [MODIFY] Add H-9: Hydration State check to `runDomAudit`.
- [MODIFY] Implement `checkHydrationStall()` to scan the DOM for "Lade Player..." text or empty `.loading-fragment` containers.

### [Diagnostics] fragment_loader.js
- [MODIFY] Integrate `traceUiNav` during the `_executeLoad` lifecycle to provide real-time forensic logs for fragment transitions.

### [UI] ui_nav_helpers.js
- [MODIFY] Update `renderLibrarySidebar` to include a new "Forensic Discovery" section.
- [NEW] Add buttons for ITEM, RELEASE, OBJECT, ROUTE, CATEGORY, and CONTEXT.
- [NEW] Add a "Mock Layer" toggle that cycles hydration modes (REAL → MOCK → BOTH).

### [Core] app_core.js
- [MODIFY] Expand `toggleLibraryFilterMode` to support the new 6-mode cycle.
- [NEW] Implement `cycleHydrationMode()` helper for the sidebar toggle.

### [Library] bibliothek.js
- [MODIFY] Update `renderLibrary` filtering chain to handle item, release, and object modes based on item metadata.

---

## Verification Plan

### Automated Tests
- Run `/home/xc/#Coding/gui_media_web_viewer/.venv/bin/python3 src/core/startup_auditor.py` to verify backend integrity.

### Manual Verification
- **Hydration Logs:** Confirm the "Lade Player..." state is logged and detectable via the DOM Auditor (Tab 'Tests').
- **Sidebar Filters:** Verify that clicking "OBJECT" or "RELEASE" in the sidebar correctly updates the library view and reflects in the HUD.
- **Mock Toggle:** Verify the "Mock Layer" toggle correctly filters the library between real assets and forensic mocks.
