# [PLAN] Hydration Parity Report: Four-Stage Audit (v1.37.22)

## Objective
Implement a professional-grade parity report that audits media counts across the entire application data flow (DB → Backend Cache → Frontend Hydration → DOM).

---

## User Review Required
**NOTE:**
- **Technical Transparency:** This report will identify exactly how many items are currently indexed in your database versus how many are visually rendered in your browser. Discrepancies will be highlighted with forensic alerts.

---

## Proposed Changes

### Backend (`main.py`)
- **[MODIFY]** Implement `get_hydration_stats()` Eel bridge.
- Return raw counts from the SQLite index and the current backend id_map/list cache.

### Sidebar UI (`diagnostics_sidebar.html`)
- **[MODIFY]** Update the HYD (Hydration) results pane to support the new "Parity Matrix" layout.
- Include a high-density status header for immediate overview.

### Controller (`sidebar_controller.js`)
- **[MODIFY]** Implement the refined `runHydrationAuditProbe()` logic.
- Perform the Four-Stage comparison: DB vs Backend Cache vs Frontend Memory vs DOM Node Count.

---

## Open Questions
Implement a professional-grade parity report that audits media counts across the entire application data flow (DB Index → Backend Cache → Frontend Memory → DOM Projection).

---
**IMPORTANT:**
- **Technical Transparency:** This upgrade provides a data-driven overview of your media library's health. It will identify if items are being filtered out by the backend or failing to render in the frontend.

### Automated Tests
- **[MODIFY]** Implement `get_hydration_stats()` Eel bridge.
- Logic: Resolve total records in the media table and current length of the backend library list.

### Manual Verification
- **[MODIFY]** Update the HYD (Hydration) tab header to include a [SCAN PARITY] trigger.
- Add a high-density viewport for the Four-Stage Parity Matrix.
- Ensure any "Drop-off" in the pipeline is visually identified with red forensic markers.
- Inspect the SENTINEL trace for the parity audit results.
- **[MODIFY]** Implement `runHydrationParityAudit()`: handles the four-layer handshake.
- Perform the comparison: DB (Backend) → CACHE (Backend) → MEMORY (Frontend) → DOM (Browser).
- Integrate with SENTINEL for persistent forensic logging.

## Implementation Notes
- Should the report distinguish between Filtered Items and Missing Items? (Recommendation: Add a "REASON" column to the matrix later, keeping the current version strictly numerical for clarity).
- All parity report executions will be logged in the SENTINEL trace for auditability.
- Chromatic alerts will highlight any discrepancies in the pipeline.

---

## Status
- [ ] Backend Eel bridge implemented
- [ ] Parity Matrix UI designed
- [ ] Four-Stage comparison logic complete
- [ ] SENTINEL trace integration complete
- [ ] Verification steps passed

---

## Implementation Checklist

- [ ] Implement get_hydration_stats() Eel bridge in main.py
- [ ] Update HYD tab header in diagnostics_sidebar.html with [SCAN PARITY] trigger
- [ ] Add high-density viewport for Four-Stage Parity Matrix in diagnostics_sidebar.html
- [ ] Implement runHydrationParityAudit() in sidebar_controller.js
- [ ] Integrate SENTINEL trace logging for all parity report actions

---

"Nur ergänzen und nichts entfernen" — Rebuilding the technical heartbeat now. (Continue / "weiter")
