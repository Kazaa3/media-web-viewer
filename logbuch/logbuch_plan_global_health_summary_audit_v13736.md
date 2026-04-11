## User Review Required
**IMPORTANT**

The HLT layer is the "Command Dashboard" of your workstation. It performs a multi-point audit across all existing layers to calculate your Global Technical Readiness Score.

---

## Proposed Changes
- **Backend Forensics (Master Audit, main.py):**
  - Implement `@eel.expose def get_global_health_audit()`.
  - Queries `db_health`, `sys_telemetry`, `volume_heuristics`, and `process_forensics`.
  - Calculates a weighted score based on critical failure points.
  - Determines the "Operational Readiness Level" (BATTLE-READY, STABILIZED, DEGRADED, CRITICAL).
- **Diagnostic UI (Layer 15):**
  - Add `reiter-hlt (HLT)` button to the nav bar as the "Master Tab" in `diagnostics_sidebar.html`.
  - Implement `diag-pane-health` with a high-fidelity "Readiness Display".
- **Controller (`sidebar_controller.js`):**
  - Integrate health domain into the diagnostic switcher.
  - Implement `runGlobalHealthAudit()`:
    - Aggregates data from multiple domains.
    - Renders a chromatic health radar for all 15 layers.

---

## Verification Plan
- **Automated Tests:**
  - Trigger the HLT audit and verify that it correctly identifies a simulated "Database Stall" or "System Load" from the aggregated telemetry.
- **Manual Verification:**
  - Verify that clicking HLT provides a comprehensive summary of all technical aspects without requiring manual inspection of individual tabs.
## Milestone: 15-Layer Forensic Suite Complete
- All 15 diagnostic layers are now active and addressable in the sidebar.
- Global Health & Command Dashboard (HLT) aggregates all telemetry into a single Operational Readiness Score.
- Weighted readiness heuristics categorize the technical state (BATTLE-READY, STABILIZED, DEGRADED, CRITICAL) based on real-time forensics.
- The HLT dashboard features 15 chromatic tiles visualizing the health of every diagnostic layer in a single high-fidelity viewport.
- All layers are modular, synchronized, and integrated with the SENTINEL engine.
- System stable at v1.37.36. Walkthrough and documentation updated to reflect the ultimate cockpit capacity.
# v1.37.36 Global Health & Mission-Critical Summary (HLT) (PLANNED)

## Overview
This upgrade introduces the 15th and final "Command Layer": the HLT (Health) tab. It aggregates telemetry from all 14 diagnostic layers, providing a single Global Technical Score and an operational "Readiness Level" for your workstation.

---

## Proposed Changes
- **Backend (main.py):**
  - Implement `@eel.expose def get_global_health_audit()` bridge to aggregate and weight-check all diagnostic domains (DB, SYS, VOL, PLY, PRC, etc.).
- **Diagnostic UI (Layer 15):**
  - Add **HLT** tab button to the nav bar in `diagnostics_sidebar.html`.
  - Implement `diag-pane-health` with a large Technical Readiness Score, Status Radar for all sub-layers, and a mission-critical RECOVERY LOG.
- **Controller (sidebar_controller.js):**
  - Register `health` domain in the diagnostic switcher.
  - Implement `runGlobalHealthAudit()` to visualize the workstation's total technical state with chromatic health markers and readiness levels (BATTLE-READY, STABILIZED, DEGRADED, CRITICAL).

---

## Verification Plan
- **Automated Tests:**
  - Run the HLT audit via the sidebar and verify that all 15 diagnostic layers are now correctly addressable.
  - Simulate a sub-layer failure and verify that the readiness level and health score update accordingly.
- **Manual Verification:**
  - Observe the HLT pane for real-time readiness and health score updates.
  - Review the RECOVERY LOG for all recent operational events and failures.

---

## Status
- **PLANNED**
- Implementation plan and task list established; ready for backend and UI implementation.

---

*Next: Implement backend health aggregator and integrate HLT diagnostics in UI and controller as described above.*
