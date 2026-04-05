# Implementation Plan: Perfect Video Player – Overhaul 6 & GUI Fixes

**Datum:** 27.03.2026

## Target
Refine the media player with Stage 6 features: comprehensive subtitle/audio track support, advanced filtering, and GUI stability fixes (dynamic loading verification).

## Proposed Changes

### [Component] Backend: Overhaul 6 & Logic
- [MODIFY] main.py
  - Implement advanced filtering logic (genre, year, quality).
  - Enhance `get_library` to support server-side pagination or dynamic loading stats.
- [MODIFY] streams/mse_stream.py & hls_stream.py
  - Ensure all audio/subtitle tracks are correctly mapped and available for switching.

### [Component] Frontend: Overhaul 6 UI
- [MODIFY] app.html
  - **Filter Bar Expansion:**
    - Add a year filter (dropdown) and genre filter (dropdown) next to the subcategory filter.
    - Add a global search input for the library tab.
    - Update `renderLibrary` to support these new filter states.
  - **Video.js Settings Overhaul:**
    - Expand the audio/subtitle track selection to show language labels (e.g., "English", "Deutsch") and codec info.
    - Ensure track switching is seamless and triggers the /video-remux-stream reload with the correct track index.
  - **Refined Stats:**
    - Integrate the new audio_tracks and subtitle_tracks metadata into the "Stats for Nerds" overlay.

### [Component] Testing: Non-Selenium GUI Tests
- [NEW] tests/gui/test_dynamic_loading.py
  - Test scenario using browser_subagent to verify item rendering without Selenium overhead.
  - Verify "No Media" fallback → Data Arrival → Card Rendering cycle.

## Verification Plan

### Automated Tests
- `python3 tests/gui/test_dynamic_loading.py` (via subagent wrapper)
- `PYTHONPATH=. pytest tests/test_mode_router.py`

### Manual Verification
- Test track switching (Audio/Subs) for 4K MKV files.
- Verify advanced filters in the library tab.
- Check "Stats for Nerds" for Intel Arc / NVIDIA GPU utilization sync.
- Verify 0% CPU for H.264/MP4 (Direct Play).

**Perfect!**
