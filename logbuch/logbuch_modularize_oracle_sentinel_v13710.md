# Modernizing Diagnostics Overlay: Modularization & SENTINEL (v1.37.10)

## Context
To improve maintainability and extensibility, the Diagnostics Overlay will be modularized into a standalone HTML fragment and JavaScript controller, leveraging the FragmentLoader architecture. This enables easier updates, cleaner app.html, and dynamic loading for performance.

---

## Implementation Plan

### 1. HTML Fragment
- **diagnostics_overlay.html**
  - Move the entire `<div id="global-diagnostics-sidebar">` and all tabs into this file.
  - Include a dedicated viewport for the SENTINEL (live-trace) log.

### 2. JavaScript Controller
- **overlay_controller.js**
  - Centralize UI logic: `switchDiagnosticsSidebarTab`, `toggleDiagnosticsSidebar`, and all tab renderers.
  - Implement SENTINEL engine: live-listening logic for system events.

### 3. Application Integration
- **app.html**
  - Remove diagnostics HTML/CSS, add `<div id="diagnostics-overlay-container"></div>`.
  - Update pulse icon click to trigger `FragmentLoader.load()` if diagnostics overlay is not present.

### 4. Logic Refactoring
- **js/diagnostics_helpers.js**
  - Retain only backend-to-frontend bridge functions (e.g., `eel.audit_specific_item`).
  - Remove UI-specific DOM manipulations.

---

## Open Questions
- **Branding:** Use "ORACLE" for the full diagnostics overlay and "SENTINEL" for the live-trace tab? (Default: ORACLE for overlay, SENTINEL for log.)
- **Load Timing:** Load overlay on first click or in background after main player is ready? (Suggested: background load for zero latency.)

---

## Verification Plan
- **Automated:**
  - Diagnostics overlay container is empty at boot, populated after fragment load.
  - "Item Track" and "Hydration" tabs work as before.
- **Manual:**
  - Pulse icon opens sidebar without issues.
  - SENTINEL live log updates in real-time.

---

**Date:** 2026-04-06
**Author:** GitHub Copilot
