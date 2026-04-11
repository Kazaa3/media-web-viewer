## Milestone: 14-Layer Forensic Suite Complete
- All 14 diagnostic layers are now active and addressable in the sidebar.
- Process Control & Zombie Audit (PRC) provides real-time mapping and surgical termination of background workers (FFmpeg, ffprobe, scanning subprocesses).
- The PRC pane features individual "Kill" hooks and an atomic PURGE ZOMBIE WORKERS repair utility.
- Recursive PID mapping ensures no stalled worker escapes technical oversight.
- SENTINEL trace engine captures every process audit and zombie purge for professional-grade technical stabilization.
- System stable at v1.37.35. Walkthrough and documentation updated to reflect the ultimate cockpit capacity.
## UI & Controller Integration Finalization
- Add the PRC (Process) navigation button and `diag-pane-process` telemetry viewport to `diagnostics_sidebar.html` as the 14th diagnostic layer.
- Implement real-time metrics for Active Sub-processes, Zombie Count, and per-process Worker Health Score in the PRC pane.
- Implement `runProcessAudit()` in `sidebar_controller.js` to visualize the process hierarchy and provide "Kill" hooks for stalled workers.
- Implement a "Repair" utility to surgically terminate stalled workers without impacting the main application thread.
- Ensure all process audits and zombie purges are captured by the SENTINEL trace engine for persistent forensic documentation.
# v1.37.35 Process Control & Zombie Audit (PLANNED)

## Overview
This upgrade introduces the 14th diagnostic layer: the PRC (Process) tab. It provides real-time observability of your application's process hierarchy, mapping parent-child relationships and enabling the detection and termination of zombie/background worker processes.

---

## Proposed Changes
- **Backend (main.py):**
  - Implement `get_process_forensics()` bridge using psutil to map all child/background processes (FFmpeg, ffprobe, scanning workers, etc.).
  - Implement `terminate_worker_process(pid)` bridge to allow targeted termination of stalled/zombie workers.
- **Diagnostic UI (Layer 14):**
  - Add **PRC** tab button to the nav bar in `diagnostics_sidebar.html`.
  - Implement `diag-pane-process` with real-time process hierarchy, resource impact, and "Kill" hooks for individual workers.
- **Controller (sidebar_controller.js):**
  - Register `process` domain in the diagnostic switcher.
  - Implement `runProcessAudit()` to visualize the process tree and provide kill actions for stalled workers.

---

## Verification Plan
- **Automated Tests:**
  - Run the PRC audit via the sidebar and verify that all 14 diagnostic layers are now correctly addressable.
  - Simulate a zombie process and verify that it is detected and can be terminated from the UI.
- **Manual Verification:**
  - Observe the PRC pane for real-time process hierarchy and resource impact updates.
  - Use the "Kill" button to terminate a background worker and verify SENTINEL trace logging.

---

## Status
- **PLANNED**
- psutil confirmed available; ready for backend and UI implementation.

---

*Next: Implement backend process forensics and integrate PRC diagnostics in UI and controller as described above.*
