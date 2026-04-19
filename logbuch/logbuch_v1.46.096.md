# Logbuch: Stress Mock Centralization (v1.46.095)

## Date: 2026-04-19

---

## Implementation Plan

### 1. Backend Stress Registry (`config_master.py`)
- Imported `random` for availability simulation.
- Located the hydration block under `technical_orchestrator`.
- Added `stress_mocks` list:
  - **Count:** 100 items by default.
  - **Categories:** Rotated through `['audio', 'video', 'album', 'podcast', 'series', 'bilder']`.
  - **Metadata:** Artist set to "Chaos Monkey Engine", album to "Hydration Stress v1.46.019".
  - **Path Template:** `/stress/test/forensic_media_file_{i}_hd.mp4`.
  - **Availability:** `available` status randomized (e.g., `random.random() > 0.1`), fixed per session but randomized on each launch.

### 2. Frontend Consumption (`forensic_hydration_bridge.js`)
- Refactored `injectStressSet(count)`:
  - Removed the local categories array and for loop.
  - Reads `stress_mocks` from `window.CONFIG.technical_orchestrator.hydration.stress_mocks`.
  - Slices the array if the requested count is smaller than the pre-generated set.
  - Maintains UI rendering and toast notifications.

---

## Verification Plan
- **Automated Tests:**
  - `node -c web/js/forensic_hydration_bridge.js`: Verify syntax remains intact after refactoring.
  - Python check: Ensure `GLOBAL_CONFIG` contains the `stress_mocks` array.
- **Manual Verification:**
  - **Stress Trigger:** Call `ForensicHydrationBridge.injectStressSet(50)` in the browser console.
  - **Data Integrity:** Verify that items in the library have the "Chaos Monkey Engine" artist and correctly rotated categories.
  - **Availability Check:** Scroll through the list and verify that ~10% of items appear offline (if the UI handles `available: false`).

---

## Status
- [x] Backend stress mock registry implemented
- [x] Frontend consumption refactored
- [ ] Automated/manual verification pending

---

## Notes
- This change ensures stress test data is fully configurable from the backend, improving consistency and maintainability.
- Awaiting user review and verification.
