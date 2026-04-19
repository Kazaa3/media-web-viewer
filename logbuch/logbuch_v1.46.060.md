# Logbuch: Forensic Throughput Hardening (v1.46.060)

## Date: 2026-04-18

### Context
- After implementing the "Fail Fast" logic, the HUD occasionally still reported `DB: 12` due to a hidden 500-second timeout in the statistics query.
- The goal is to ensure the HUD always displays the correct item count (579), even during active scans or database contention.

---

## Implementation Plan

### Backend Core
- **db.py**
  - Universal Timeout: All database read-paths now use a 2-second timeout (specifically, `timeout=2` in `sqlite3.connect` within `get_db_stats`).
  - Error Recovery: `get_db_stats` now returns 0 or cached values if the database is locked, instead of crashing.

- **api_library.py**
  - Metrics Pulsing: On `db_busy`, an independent shallow query is attempted to retrieve the total record count (579), stabilizing the HUD display.

---

## Verification Plan
- **HUD Stabilization:** Confirm the HUD consistently reports `DB: 579`, even when the "R (Real)" button is clicked during a background scan.
- **Visual Parity:** Ensure the DB box remains Yellow/Pulsing until all 579 items are fully loaded for the list view.

---

## User Review Required
- **Parity Enforcement:** Standardized all database read-paths to a 2-second timeout for immediate and consistent HUD updates.
- **Busy-Mode Metrics:** System now reports `DB: 579 (Busy)` to the HUD if the database is locked, preventing fallback to mock data.

---

## Status
- [x] Backend changes implemented
- [x] Manual verification completed
- [ ] Awaiting user review

---

## Notes
- These changes further harden startup and runtime feedback, ensuring accurate and stable HUD metrics regardless of database state.
- Additional monitoring may be required to confirm long-term stability under heavy load.
