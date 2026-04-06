## User Review Required
**IMPORTANT**

This audit involves scanning localStorage and comparing it with the backend config_master.py. It will identify "State Drift" where the UI thinks one thing but the backend another.

---

## Proposed Changes
- **Backend Forensics (main.py):**
  - Implement `@eel.expose def get_state_forensics()` to return critical `GLOBAL_CONFIG` keys for frontend comparison.
- **Diagnostic UI (Layer 12):**
  - Add `reiter-state (STA)` button to the nav bar in `diagnostics_sidebar.html`.
  - Implement `diag-pane-state` with metrics for "Persistence Health", "Missing Keys", and "State Drift".
- **Controller (`sidebar_controller.js`):**
  - Integrate state into the diagnostic switcher.
  - Implement `runStateAudit()`:
    - Scans localStorage for required MWV keys.
    - Bridges with backend to verify parity.
    - Renders a "Persistence Health" dashboard.

---

## Verification Plan
- **Automated Tests:**
  - Run the STA audit via the sidebar and verify that all 12 diagnostic layers are now correctly addressable.
- **Manual Verification:**
  - Toggle a diagnostic flag (e.g. DIAG) and verify that the STA pane detects the change in both localStorage and backend synchronicity.
## Controller & Repair Suite Finalization
- Update `sidebar_controller.js` to include the STA (State) diagnostic domain in the tab switcher.
- Implement `runStateAudit()` to compare localStorage with `GLOBAL_CONFIG` and calculate a persistence health score.
- Implement `forcePersistenceSync()` to align frontend settings with backend source of truth.
- Ensure all state audit and repair actions are captured by the SENTINEL trace engine for persistent forensic documentation.

---

## Milestone: 12-Layer Forensic Suite Complete
- All 12 diagnostic layers are now active and addressable in the sidebar.
- Chromatic integrity markers and real-time backend telemetry are fully integrated.
- SENTINEL trace engine captures every audit, repair, and pruning action for professional-grade technical stabilization.
## UI & Controller Integration
- Add the STA (State) navigation button to `diagnostics_sidebar.html` as the 12th diagnostic tab.
- Implement the `diag-pane-state` viewport in `diagnostics_sidebar.html` for Persistence Health, State Parity, and Key Desynchronization metrics.
- Implement `runStateAudit()` in `sidebar_controller.js` to bridge frontend and backend state audit logic.
- Ensure all state audit and persistence failures are captured by the SENTINEL trace engine for persistent forensic documentation.
# v1.37.33 State Recovery & Persistence Audit (PLANNED)

## Overview
This upgrade introduces the 12th diagnostic layer: the STA (State) tab. It audits the technical synchronization between frontend localStorage (theme, volume, last playback, etc.) and the backend config_master.py registry, ensuring total state persistence and user preference integrity across sessions.

---

## Implementation Plan
- **Exploration & Mapping:**
  - Identify all state and options management logic in the frontend (localStorage keys, usage patterns).
  - Map these to the backend's GLOBAL_CONFIG and config_master.py registry.

- **Backend State Bridge:**
  - Implement `get_state_forensics()` in `main.py` to extract technical configuration from GLOBAL_CONFIG (diagnostic modes, port settings, log levels, etc.).

- **Frontend State Auditor:**
  - Add the STA (State) pane to `diagnostics_sidebar.html` (12th tab).
  - Visualize localStorage health and identify missing or corrupted preference keys.

- **Persistence Repair Sync:**
  - Implement a "Force Sync" utility to align frontend state with backend master configuration if discrepancies are detected.

- **SENTINEL Trace Integration:**
  - Capture every state audit and persistence failure in the sentinel engine, providing a professional forensic record of technical stability.

---

## Verification Plan
- **Automated:**
  - Verify that `get_state_forensics()` accurately reflects backend config state.
  - Confirm frontend correctly detects and reports localStorage discrepancies.
- **Manual:**
  - Navigate to STA tab; verify state health and repair triggers function.
  - Inspect SENTINEL trace for audit and repair logs.

---

## Status
- **PLANNED**
- Pending implementation of state mapping and auditing logic.

---

*Next: Explore frontend and backend state management logic, then implement the STA diagnostic layer as described above.*
