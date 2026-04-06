# Forensic Controller Integration Walkthrough (v1.37.13)

## Overview
Both the Video Health (VID) and Database Index Resilience (DBI) forensic suites are now fully implemented and integrated into the Diagnostics Overlay.

## New Forensic Capabilities
- **Deep FFmpeg Probe (VID):**
  - Traces real-time health of transcoding and remuxing pipelines.
  - Identifies stalls and process latency.
- **Ghost Item Detector (DBI):**
  - Performs library-wide file-system parity scan.
  - Detects database entries pointing to non-existent media.
- **SQLite Resilience (DBI):**
  - Executes high-speed PRAGMA integrity_check audits for index corruption.
- **SENTINEL Synchronization:**
  - Every forensic audit pulse is logged for long-term review.

## Usage
1. Open Diagnostics Overlay and select VID or DBI tab.
2. Run probes to analyze video pipeline or database health.
3. Review results and SENTINEL logs for persistent forensic records.

---

Both forensic suites are now online. Are there any other system components you'd like to harden?
