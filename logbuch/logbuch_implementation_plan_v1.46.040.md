# Implementation Plan: Advanced Queue Steering & Hybrid Sync (v1.46.040)

## Context
This plan implements specialized forensic flags in `config_master.py` to govern the `syncQueueWithLibrary` behavior. It addresses the "Black Hole" issue where real items were dropped during diagnostic pulses and introduces a resilient emergency fallback.

---

## User Review Required

### Hybrid Sync
- When `hybrid_sync_enabled` is True, the queue will prioritize real media while keeping forensic mock items visible, regardless of the active hydration mode (M/R).

### Emergency Bypass
- If filtering results in 0 items but the library has data, the system will automatically bypass all filters (Category/Branch/Mode) to prevent a "Black Screen" state.

---

## Proposed Changes

### [Backend]
#### [MODIFY] `config_master.py`
- Expand `queue_orchestration` registry:
    - `hybrid_sync_enabled: True`
    - `emergency_bypass_enabled: True`
    - `block_real_in_diagnostic: False`
    - `diagnostic_highlighting: True`

### [Frontend]
#### [MODIFY] `playlists.js`
- `syncQueueWithLibrary`:
    - Integrate the new config flags.
    - Implement the "Emergency Bypass" logic block at the end of the filtration stage.
    - Implement "Hybrid Sync" override in the hydration mode filter (allowing real items to pass even in mock mode if the flag is enabled).
- **UI Rescue:**
    - Add a console warning with a suggested rescue command (`resetAllFilters()`) if the bypass is triggered.

---

## Open Questions
- Should the "Emergency Bypass" show a UI toast/notification to inform the user that filters were ignored? (Proposed: Yes, for transparency).

---

## Verification Plan

### Automated Tests
- Update `test_api.py` (or a JS equivalent) to mock an empty filter result and verify the bypass triggers.

### Manual Verification
- Set `activeQueueFilter` to a non-existent category and verify that real items appear anyway via the bypass (if confirmed in logic).
- Verify that real items remain visible when switching to Mock mode if `hybrid_sync_enabled` is True.

---

(See <attachments> above for file contents. You may not need to search or read the file again.)
