# [PLAN] Database Forensic Overview: Statistical Audit (v1.37.24)

## Objective
Implement a high-density statistical dashboard for the Database Overview (DBI) tab to provide professional-grade library observability.

---

## User Review Required
**NOTE:**
- **Data Observability:** This upgrade provides an instant technical breakdown of your media library, identifying exactly how many files of each category and format are currently indexed in your database.

---

## Proposed Changes

### Backend (`main.py`)
- **[MODIFY]** Implement/Upgrade `get_debug_stats()` Eel bridge.
- **Logic:** Perform technical grouping by category and file extension; Calculate total indexed media size.

### Sidebar UI (`diagnostics_sidebar.html`)
- **[MODIFY]** Ensure total compatibility with the technical statistical dashboard via the existing `debug-db-overview-content` viewport.

### Controller (`sidebar_controller.js`)
- **[MODIFY]** Implement/Enhance `renderDebugDatabase()`.
- Bridge the frontend with the backend `get_debug_stats` suite.
- Render high-density bar-charts or technical lists for category and format distribution.

---

## Open Questions
- Should we include a "Duplicate Path" audit in this overview? (Recommendation: Add a simple "DUPLICATES" counter to identify potential SQLite index bloat).

---

## Verification Plan

### Automated Tests
- Confirm `get_debug_stats` returns logically grouped data for categories and formats.
- Verify total counts match the master hydration parity report.

### Manual Verification
- Navigate to the DBI tab → Verify the Statistical Audit Dashboard appears instantly.
- Cross-reference category counts with the main library view to ensure 100% data fidelity.
- Inspect the SENTINEL trace for the database audit completion.

---

## Implementation Checklist
- [ ] Implement/Upgrade get_debug_stats() Eel bridge in main.py
- [ ] Ensure debug-db-overview-content viewport in diagnostics_sidebar.html supports dashboard
- [ ] Implement/Enhance renderDebugDatabase() in sidebar_controller.js
- [ ] Render bar-charts or technical lists for category/format distribution
- [ ] Integrate SENTINEL trace logging for all database audits

---

"Nur ergänzen und nichts entfernen" — Rebuilding the technical heartbeat now. (Continue / "weiter")
