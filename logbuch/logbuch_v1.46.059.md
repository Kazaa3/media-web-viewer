# Logbuch: Forensic Throughput Stabilization (v1.46.059)

## Date: 2026-04-18

### Context
- The media-web-viewer library experienced severe startup bottlenecks due to the initial boot-scan (verifying 579 files) holding an exclusive database lock.
- The UI was blocked for up to 500 seconds, causing a "12 mocks only" display and a silent backend crash.

---

## Implementation Plan

### Backend Core
- **db.py**
  - Reduced `MAX_INIT_RETRIES` from 100 to 10 to avoid indefinite UI blocking.
  - Lowered timeout for non-critical library requests during boot-scan to improve connection fairness.

- **api_library.py**
  - Added scope protection: initialized empty placeholders before DB queries to prevent backend crashes affecting the HUD.
  - Ensured the HUD always receives the authoritative DB size (579), even if the DB is busy.

### Frontend Orchestration
- **bibliothek.js**
  - HUD now treats `db_count` from the backend as the single source of truth, even during the "yellow pulsing" warning phase.

---

## Verification Plan
- **Lock Survival:** HUD immediately displays `DB: 579 (Yellow)` on startup, reflecting the known DB size while the scan is running.
- **Recovery:** The 12 mock items are replaced by the 579 real items once the scan completes and the lock is released.

---

## User Review Required
- **Fail-Fast Policy:** UI wait time for DB lock reduced from 500s to 25s to prevent frozen UI.
- **Crash Protection:** Fixed backend NameError to ensure HUD updates even if DB is busy.

---

## Status
- [x] Backend and frontend changes implemented
- [x] Manual verification completed
- [ ] Awaiting user review

---

## Notes
- These changes improve startup resilience and user feedback during heavy DB operations.
- Further tuning may be required based on real-world usage and feedback.
