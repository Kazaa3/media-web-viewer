# v1.37.39 Internal API Registry & Documentation Audit (API) (PLANNED)

## Overview
This upgrade introduces the 18th diagnostic layer: the API (Internal API Registry) tab. It provides real-time transparency into all backend bridges (Eel-exposed functions), ensuring technical clarity and live documentation for development and troubleshooting.

---

## Proposed Changes
- **Backend Forensics (main.py):**
  - Implement `@eel.expose def get_api_forensics()` bridge.
  - Lists all exposed Eel functions within the main.py scope.
  - Captures the function name and its docstring for live documentation.
  - Update `get_global_health_audit()` to an 18-layer weighted model.
- **Diagnostic UI (Layer 18):**
  - Add **API** tab button to the nav bar in `diagnostics_sidebar.html`.
  - Implement `diag-pane-api` with a high-density "Live Bridge Registry".
- **Controller (sidebar_controller.js):**
  - Register `api` domain in the diagnostic switcher.
  - Implement `runApiAudit()` to visualize the detected API mapping and provide a searchable list of backend endpoints.

---

## Verification Plan
- **Automated Tests:**
  - Trigger the API audit and verify that it correctly identifies itself (`get_api_forensics`) in the registry.
- **Manual Verification:**
  - Verify that the HLT score correctly reflects the addition of the 18th diagnostic layer.

---

## Status
- **PLANNED**
- Implementation plan and task list established; ready for backend and UI implementation.

---

*Next: Implement backend API forensics and integrate API diagnostics in UI and controller as described above.*
