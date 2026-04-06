# v1.37.40 Software Stack & Dependency Audit (ENV) (PLANNED)

## Overview
This upgrade introduces the 19th diagnostic layer: the ENV (Environment) tab. It provides real-time observability of your application's software stack, mapping every technical dependency to its current versioning and synchronizing the Global Health (HLT) command layer to a 19-layer model.

---

## Proposed Changes
- **Backend Forensics (main.py):**
  - Implement `@eel.expose def get_environment_forensics()` bridge.
  - Provides versioning data for Python, Eel, psutil, and FFmpeg.
  - Update `get_global_health_audit()` for 19-layer awareness.
- **Diagnostic UI (Layer 19):**
  - Add **ENV** tab button to the nav bar in `diagnostics_sidebar.html`.
  - Implement `diag-pane-env` with stack documentation and real-time versioning metrics.
- **Controller (sidebar_controller.js):**
  - Register `env` domain in the diagnostic switcher.
  - Implement `runEnvAudit()` to visualize the software stack versions and platform identifiers.

---

## Verification Plan
- **Automated Tests:**
  - Trigger the ENV audit and verify that the system correctly identifies all mission-critical dependency versions.
  - Verify that the HLT audit reflects the expanded 19-layer readiness model.
- **Manual Verification:**
  - Verify that clicking ENV provides a high-density summary of the software stack without requiring manual CLI inspection.
  - Confirm that the HLT pane aggregates environment health in the readiness score.

---

## Status
- **PLANNED**
- Implementation plan and task list established; ready for backend and UI implementation.

---

*Next: Implement backend environment forensics and integrate ENV diagnostics in UI and controller as described above.*
