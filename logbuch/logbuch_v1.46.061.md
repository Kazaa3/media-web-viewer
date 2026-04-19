# Logbuch: Forensic DOM Audit & Centralized Timeout (v1.46.061)

## Date: 2026-04-18

### Context
- To further improve reliability and forensic traceability, the 2-second database timeout is now centralized, and the UI's DOM state is periodically logged for backend verification.

---

## Implementation Plan

### Backend Core
- **config_master.py**
  - Enforced SSOT: Added `db_timeout: 2` to `forensic_hydration_registry`, making it the single source of truth for all database wait-times (Library, Search, Playlists).

- **db.py**
  - Dynamic Connectivity: Updated `init_db`, `get_all_media_items`, and `get_db_stats` to use the timeout value from `GLOBAL_CONFIG` instead of hardcoded values.

### Frontend Orchestration
- **common_helpers.js**
  - DOM Pulse (DOM Auditor): Enhanced `updateSyncAnchor` to, every 20 iterations, perform a "Surgical DOM Count" of all `.media-item` elements and check the visibility of the player container. This data is sent to the backend via `eel.ui_trace` for forensic logging.

---

## Verification Plan
- **Log Audit:** Use `grep` for `[JS-NAV] [DOM-AUDIT]` in `media_viewer.log` to confirm backend receipt of real-time DOM state.
- **Timeout Verification:** Ensure all database connections use the 2.0s timeout from the centralized config.

---

## User Review Required
- **Centralized Timeout:** All database interactions now governed by a single config value.
- **DOM Integrity Audit:** Real-time DOM state is logged for forensic verification, ensuring frontend and backend parity.

---

## Status
- [x] Backend and frontend changes implemented
- [x] Manual verification completed
- [ ] Awaiting user review

---

## Notes
- These changes further strengthen forensic traceability and operational consistency across the stack.
- Additional audit hooks can be added as needed for deeper verification.
