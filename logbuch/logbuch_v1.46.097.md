# Logbuch: Category Orthogonality & Playback Repair (v1.46.096)

## Date: 2026-04-19

---

## Implementation Plan

### 1. Hardened Media Detection
- **common_helpers.js**
  - Fixed `isAudioItem`: Now uses a strict check against `window.CONFIG.audio_extensions` instead of a generic extension match.
  - Implemented `isImageItem`: New helper uses the centralized image extension registry from the backend.
  - Hardened `isVideoItem`: Explicitly excludes images from video classification to prevent "multimedia" overlap.

### 2. Library Filter Integrity
- **bibliothek.js**
  - Removed Mock Bypass: Mocks (`is_mock` items) no longer skip category checks in the filtering loop.
  - Mocks now respect "Audio", "Films", and "Series" sub-filters.

### 3. Playback Routing & Log Expansion
- **app_core.js**
  - Hardened `playMediaObject`: Added explicit triage for Images/Photos.
  - Added detailed routing decision logs: `[Play-Routing] Type: Video | Ext: .mp4 | Target: player`.
  - Expanded logs with detailed trace points throughout the routing chain.

### 4. Backend Log Level
- **config_master.py**
  - (Optional) Set `enable_ui_console` to `True` for maximum forensic traceability.

---

## Verification Plan
- **Automated Tests:**
  - `node -c web/js/*.js`: Ensure no syntax regressions in detection helpers.
- **Manual Verification:**
  - **Category Check:** Select "Audio" in the sidebar and verify that NO .jpg or .mp4 items are visible.
  - **Mock Audit:** Verify that Stress Mocks are correctly distributed across their respective categories (e.g., "Stress Probe [audio]" only in the Audio tab).
  - **Playback Audit:**
    - Play an .mp4: Verify Video tab triggers.
    - Play an .mp3: Verify Audio tab direct-fire.
    - Click a .jpg: Verify no crash/routing failure occurs.

---

## Status
- [x] Media detection logic hardened
- [x] Library filter integrity enforced
- [x] Playback routing and logging expanded
- [x] Backend log level set (optional)
- [ ] Manual/automated verification pending

---

## Notes
- These changes resolve category leakage, playback blackouts, and ensure mocks are filtered consistently with real data.
- Awaiting user review and verification.
