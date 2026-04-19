# Logbuch: Mock Centralization (v1.46.094)

## Date: 2026-04-19

---

## Implementation Plan

### 1. Centralized Configuration
- Expanded the `technical_orchestrator.hydration` section in `config_master.py`.
- Added `emergency_mock_template`:
  - `name_pattern`: EX-PULSE-{index}_DATA_STREAM.wav
  - `path_prefix`: media/test_files/
  - `metadata`: artist, album, category, etc.

### 2. Dynamic Hydration Handshake
- Updated `forceEmergencyHydration()` in `forensic_hydration_bridge.js`:
  - Checks for `window.CONFIG.technical_orchestrator.hydration.emergency_mock_template`.
  - Uses the pattern and metadata from the config to generate the `emergencyMocks` array.
  - Falls back to legacy hardcoded values only if the config is missing.

---

## Verification Plan
- **Automated Tests:**
  - `node -c web/js/*.js`: Ensure no syntax errors in the template resolution logic.
  - Config Audit: Verify `get_global_config` returns the new template via Eel.
- **Manual Verification:**
  - Cold Boot: Wipe localStorage and refresh. Verify that the 12 Pulsar items appear in the queue with the exact metadata defined in `config_master.py`.
  - Metadata Update: Change the "Artist" in `config_master.py` and verify it reflects in the UI after a refresh.

---

## Status
- [x] Emergency mock template centralized in config
- [x] Hydration bridge updated for dynamic generation
- [ ] Automated/manual verification pending

---

## Notes
- This change ensures a single source of truth for proof-of-life media assets and simplifies future updates.
- Awaiting user review and verification.
