# v1.37.37 Unified Driver & Hardware Audit (DRV) (PLANNED)

## Overview
This upgrade introduces the 16th diagnostic layer: the DRV (Driver) tab. It provides real-time observability of your system's hardware acceleration capabilities, GPU visibility, and transcoder optimization, leveraging the existing hardware_detector module.

---

## Proposed Changes
- **Backend Forensics (main.py):**
  - Implement `@eel.expose def get_hardware_forensics()` bridge.
  - Queries FFmpeg for supported encoders and hardware acceleration paths.
  - Detects GPU availability via `nvidia-smi` or platform-specific probes.
  - Aggregates "Acceleration Health" based on the detected hardware profile.
- **Diagnostic UI (Layer 16):**
  - Add **DRV** tab button to the nav bar in `diagnostics_sidebar.html`.
  - Implement `diag-pane-driver` with metrics for "GPU VISIBILITY", "ACCEL HEALTH", and "CODEC MATRIX".
- **Controller (sidebar_controller.js):**
  - Integrate driver domain into the diagnostic switcher.
  - Implement `runHardwareAudit()` to visualize detected hardware acceleration paths and provide a professional codec-support matrix (H.264, HEVC, AV1).

---

## Verification Plan
- **Automated Tests:**
  - Trigger the DRV audit and verify that the system correctly identifies the backend FFmpeg version and any detected hardware encoders.
- **Manual Verification:**
  - Verify that clicking DRV provides a high-density summary of your platform's transcoding capabilities without requiring manual CLI inspection.

---

## Status
- **PLANNED**
- hardware_detector module confirmed available; ready for backend and UI implementation.

---

*Next: Implement backend hardware forensics and integrate DRV diagnostics in UI and controller as described above.*
