# Logbuch: Library Recovery & Diagnostic Integrity (v1.46.097)

## Date: 2026-04-19

---

## Implementation Plan

### 1. Diagnostic Labeling Fix
- **forensic_hydration_bridge.js**
  - Restored `is_mock: true` for `RecoveryManager` items.
  - Explicitly set `is_diag: true` for these samples to allow UI differentiation.
- **bibliothek.js**
  - Updated item badge logic:
    - `is_mock && is_diag` → [D] (Diagnostic)
    - `is_mock && !is_diag` → [M] (Mock/Pulsar)
    - `!is_mock` → [R] (Real/Forensic)

### 2. Implementation of Auto-Scan Recovery
- **api_library.py**
  - In `get_library`, enhanced audit metadata.
  - If `db_count == 0`, return a `triggered_auto_scan: True` flag to notify the UI that restoration is in progress.
- **main.py**
  - Added a safety check in the startup sequence: if `db.get_media_count() == 0`, trigger a background `scan_media` call to rebuild the library from the filesystem.

### 3. Log Expansion (Backend)
- **main.py**
  - Added detailed `[Scan-Trace]` logs to `_scan_media_execution` to show exactly which files are being indexed and why they might be skipped.

---

## Verification Plan
- **Automated Tests:**
  - Query the database via `sqlite3` after startup to verify the media table count is > 0.
- **Manual Verification:**
  - **HUD Audit:** Verify the HUD shows `DB: 541` (or the actual file count) after the auto-scan completes.
  - **Badge Audit:** Verify that if the DB is empty, the fallback items show [D] instead of [R].
  - **Playback Audit:** Verify that items scanned from the physical `./media` folder can be played in the respective players.

---

## Status
- [x] Diagnostic labeling logic fixed
- [x] Auto-scan recovery implemented
- [x] Backend scan trace logs expanded
- [ ] Automated/manual verification pending

---

## Notes
- These changes ensure clear differentiation between diagnostic and real items, and provide automatic recovery if the database is empty.
- Awaiting user review and verification.
