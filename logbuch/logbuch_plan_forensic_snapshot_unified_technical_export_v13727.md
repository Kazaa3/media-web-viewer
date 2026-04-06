# [PLAN] Forensic Snapshot: Unified Technical Export (v1.37.27)

## Objective
Implement a professional-grade Workstation Snapshot tool to capture the status of all 7 forensic diagnostic layers into a single, unified technical report.

---

## User Review Required
**IMPORTANT:**
- **Technical Document Integrity:** This snapshot aggregates data from DBI (Stats), HYD (Parity), VID (Workers), and REC (Action Log). It provides a complete "Frozen Image" of your workstation's state, perfect for forensic documentation and system health comparisons.

---

## Proposed Changes

### Sidebar UI (`diagnostics_sidebar.html`)
- **[MODIFY]** Add a high-density [SNAPSHOT] button to the sidebar's master header.
- Provide a technical tooltip: "Generate Unified Forensic Report".
- Stylize with a professional chromatic marker (Workstation White/Cyan).

### Controller (`sidebar_controller.js`)
- **[MODIFY]** 
  - Implement `window.__mwv_forensic_rec_actions` session array.
  - Update `addForensicRecAction()` to persist events to this array.
  - Implement `generateForensicSnapshot()`:
    - Aggregates `get_library_forensics` results.
    - Aggregates `get_hydration_stats` results.
    - Captures active worker PIDs.
    - Includes the session's REC Action History.
    - Optionally includes Metadata Samples (first 5 items from the database).
    - Format the results into a professional technical document (JSON or Formatted Text).
    - Trigger a browser-based download of the report (e.g., `mwv_forensic_snapshot_YYYYMMDD.txt`).

---

## Open Questions
- Should the snapshot include the full Sentinel trace? (Recommendation: Keep it separate; the Snapshot is a state summary, while the Trace is a timeline. You already have a dedicated EXPORT for the trace).
- Should we include Metadata Samples (first 5 items from the database) in the snapshot? (Recommendation: Add a "DB Sample" block for technical verification).

---

## Verification Plan

### Automated Tests
- Verify that `generateForensicSnapshot` correctly gathers asynchronous data from all backend bridges before initiating the download.
- Confirm total item counts in the snapshot match the master hydration parity reports.
- Confirm `generateForensicSnapshot` correctly waits for all asynchronous backend responses.
- Verify the generated JSON/Text object contains all 4 mandatory blocks (DBI, HYD, VID, REC).

### Manual Verification
- Navigate to the Diagnostics Sidebar → Click [SNAPSHOT].
- Verify that a technical document is generated and downloaded instantly.
- Open the snapshot → Verify it contains current DBI counts, active worker PIDs, and your REC action history.
- Open the resulting file → Verify it contains:
  - Library Statistics (Category counts)
  - Four-Stage Parity counts
  - Active process PIDs (if any)
  - Your session's recovery history
- Inspect the SENTINEL trace for the snapshot generation event.

---

## Implementation Checklist
- [ ] Add [SNAPSHOT] button to diagnostics_sidebar.html
- [ ] Implement window.__mwv_forensic_rec_actions session array in sidebar_controller.js
- [ ] Update addForensicRecAction() to persist to session array
- [ ] Implement generateForensicSnapshot() in sidebar_controller.js
- [ ] Aggregate DBI, HYD, VID, REC data and format report
- [ ] Trigger browser-based download of technical report
- [ ] Integrate SENTINEL trace logging for snapshot generation

---

"Nur ergänzen und nichts entfernen" — Rebuilding the technical heartbeat now. (Continue / "weiter")
