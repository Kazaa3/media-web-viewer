# [PLAN] Storage Forensic Audit: Volume Discovery (v1.37.30)

## Objective
Implement a professional-grade Storage (STR) tab to provide deep observability into the physical ./media volume, including file distribution, large asset discovery, and path integrity auditing.

---

## User Review Required
**NOTE:**
- **Storage Volume Audit:** This upgrade adds the "Physical Layer" to your workstation. You will be able to see exactly where your large assets reside and audit the integrity of the filesystem paths themselves.

---

## Proposed Changes

### Backend (`main.py`)
- **[MODIFY]** Implement `get_storage_forensics()` Eel bridge.
- **Logic:**
  - Recursive walk of the ./media directory.
  - Statistics: Total File/Folder counts + Disk Usage.
  - Heuristics: Find Top 10 Largest Files (Discovery).
  - Heuristics: Identify deepest folder (Folder Depth Audit).
  - Integrity: List broken symlinks or unreachable paths.

### Sidebar UI (`diagnostics_sidebar.html`)
- **[MODIFY]** Add the STR tab to the master navigation bar.
- Add the `diag-pane-storage` viewport with high-density storage telemetry cards.

### Controller (`sidebar_controller.js`)
- **[MODIFY]** Implement `runStorageAudit()` to fetch and render the new storage telemetry data.
- Update the tab-switching logic to handle the STR domain.

---

## Open Questions
- Should we include an "Analyze Extensions" block (e.g., Pie chart of .mp4 vs .mkv)? (Recommendation: Add as a forensic summary for v1.37.30).

---

## Verification Plan

### Automated Tests
- Confirm `get_storage_forensics` correctly identifies files in the ./media directory.
- Verify that file size calculations match OS-level reporting (`du -sh`).

### Manual Verification
- Navigate to the STR (Storage) tab → Verify the real-time storage telemetry renders correctly.
- Check the SENTINEL trace for the environmental audit entry.
- Verify that the "Top 10 Largest Files" list accurately reflects the actual files in your ./media folder.

---

## Implementation Checklist
- [ ] Implement get_storage_forensics() Eel bridge in main.py
- [ ] Add STR tab and viewport to diagnostics_sidebar.html
- [ ] Render storage telemetry cards and file/folder stats
- [ ] Implement runStorageAudit() in sidebar_controller.js
- [ ] Integrate SENTINEL trace logging for all storage audits

---

"Nur ergänzen und nichts entfernen" — Rebuilding the technical heartbeat now. (Continue / "weiter")
