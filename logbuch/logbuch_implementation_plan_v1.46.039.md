# Implementation Plan: Restoring Forensic Integrity & Hydration (v1.46.039)

## Context
The migration to `shell_master.html` (the v1.46 Atomic Shell) caused a "logic blackout" due to omission of critical JavaScript utilities. A new steering flag for the Media Queue is also required to govern the hydration pulse. This plan restores the mission-critical forensic stack and introduces the requested configuration controls.

---

## User Review Required

### Script Sequencing
- Scripts are restored in a specific order to avoid `ReferenceError` dependencies.
- `common_helpers.js` must precede `bibliothek.js`.

### Queue Flag
- Adding a `queue_orchestration` registry to `config_master.py`.
- Default: `auto_hydration_enabled = True` to resolve "Black Hole" issues.

### Performance Impact
- Adding ~15 scripts will slightly increase initial load time (~200ms).
- This is mandatory for "Forensic Elite" features (Hydration, HUD, Monitoring).

---

## [Backend]
### [MODIFY] `config_master.py`
- [NEW] Add `queue_orchestration` registry to `GLOBAL_CONFIG`.
- Target flag: `auto_hydration_enabled: True`.

## [Frontend]
### [MODIFY] `shell_master.html`
- Inject missing core scripts:
    - `js/common_helpers.js` (Restores `setHydrationMode`)
    - `js/diagnostics_helpers.js` (Restores HUD & Pulse monitoring)
    - `js/forensic_hydration_bridge.js` (Restores Stage 0->1 handshake)
    - `js/forensic_recovery_engine.js` / `js/nuclear_recovery_pulse.js`
- Correct the loading order: `common_helpers.js` MUST be loaded before `bibliothek.js`.

---

## Open Questions
- Should legacy `app.html` be removed entirely once stability is confirmed to avoid future confusion?

---

## Verification Plan

### Automated Tests
- Refresh the browser or verify via logs that `HYD-CHANGE` events now trigger `loadLibrary()`.
- Run `test_api.py` to confirm backend is still responding correctly.

### Manual Verification
- User should verify that clicking "B" on the footer HUD now correctly hydrates the library with real items.
- Verify that the LOGS button correctly opens the diagnostics overlay.

---

(See <attachments> above for file contents. You may not need to search or read the file again.)
