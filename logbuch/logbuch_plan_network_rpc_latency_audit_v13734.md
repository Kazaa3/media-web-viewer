## User Review Required
**IMPORTANT**

This audit measures the "Round Trip Time" (RTT) of your Eel-RPC calls. It is critical for identifying why the UI might feel "sluggish" during deep database scans or transcoding.

---

## Proposed Changes
- **Diagnostic UI (Layer 13):**
  - Add `reiter-net (NET)` button to the nav bar in `diagnostics_sidebar.html`.
  - Implement `diag-pane-network` with metrics for "Avg. Latency", "Last Call Time", and "RPC Health".
- **Controller (`sidebar_controller.js`):**
  - Integrate network into the diagnostic switcher.
  - Implement `runNetworkAudit()`:
    - Performs 3-5 sub-millisecond "ping" calls to the backend via Eel.
    - Calculates jitter and average response frequency.
    - Visualizes the technical responsive-state of the bridge.

---

## Verification Plan
- **Automated Tests:**
  - Trigger the NET audit and verify that latency metrics are rendered with chromatic markers (Green < 15ms, Yellow < 50ms, Red > 50ms).
- **Manual Verification:**
  - Perform a deep library scan while the NET tab is active and verify that the latency audit reflects backend load in real-time.
## Controller & Telemetry Finalization
- Update `sidebar_controller.js` to include the NET (Network) diagnostic domain in the tab switcher.
- Implement `runNetworkAudit()` to perform sub-millisecond pings, calculate average latency, jitter, and response quality.
- Implement real-time throughput and chromatic latency marker visualization in the NET pane.
- Ensure all latency audits and bridge failures are captured by the SENTINEL trace engine for persistent forensic documentation.

---

## Milestone: 13-Layer Forensic Suite Complete
- All 13 diagnostic layers are now active and addressable in the sidebar.
- Real-time backend telemetry and chromatic health markers are fully integrated.
- SENTINEL trace engine captures every audit and bridge synchronization for professional-grade technical stabilization.
# v1.37.34 Network & RPC Latency Audit (PLANNED)

## Overview
This upgrade introduces the 13th diagnostic layer: the NET (Network) tab. It provides real-time observability of Eel-RPC bridge latency, measuring round-trip times and identifying backend bottlenecks to ensure technical responsiveness.

---

## Proposed Changes
- **Backend (main.py):**
  - Implement `@eel.expose def get_net_ping()` bridge for sub-millisecond RTT tracking.
- **Diagnostic UI (Layer 13):**
  - Add **NET** tab button to the nav bar in `diagnostics_sidebar.html`.
  - Implement `diag-pane-network` with metrics for Avg. Bridge Latency, Throughput, and RPC Health Score.
- **Controller (sidebar_controller.js):**
  - Register `network` domain in the diagnostic switcher.
  - Implement `runNetworkAudit()` to perform multiple backend pings, calculate latency/jitter, and render chromatic health markers (Green < 15ms, Yellow < 50ms, Red > 50ms).

---

## Verification Plan
- **Automated Tests:**
  - Run the NET audit via the sidebar and verify that all 13 diagnostic layers are now correctly addressable.
- **Manual Verification:**
  - Observe the NET pane for real-time latency and health score updates.
  - Simulate backend load or network delay and verify chromatic markers and SENTINEL trace logging.

---

## Status
- **PLANNED**
- Pending implementation of backend ping bridge and frontend telemetry logic.

---

*Next: Implement backend ping bridge and integrate NET diagnostics in UI and controller as described above.*
