---

## Finalizing Perfect Video Player (Overhaul 6)

### Audio Player & GUI Stability
- **Tab Split Test (Non-Selenium):** Verify Audio Player right-split populates correctly.
- **Dynamic GUI Loading:** Ensure JS structure is solid and handles database arrivals.
- **7 OBJECT TEST SUITE:** Multi-level verification (Dict → ...):
  - Level 1: Dictionary structures
  - Level 2: SQLite database consistency
  - Level 3: Mode Router logic (Mocked FFprobe)
  - Level 4: Static HTML integrity
  - Level 5: Dynamic JS Diagnostic (Eel Bridge)
  - Level 6: Mock Backend End-to-End
  - Level 7: Real Media Path Verification

### Video Player "Pimping" (Cinema Overhaul)
- **Advanced Filters:** Implement "Premium Cinema" visual filters.
- **Atmos/Bitstream Stats:** Display advanced audio metadata in overlay.
- **Track Switching:** Finalize FFmpeg-based audio/sub switching for Audio/Subtitles (HLS/MSE).
- **Audio Excellence:** Display Bitstream/Atmos Core metadata in Stats.
- **Modern UI:** Enhance Video.js 8 with new "Glass" or "Carbon" theme tweaks.

### Verification
- **Test Bed:** Implement `window.runDiagnostic()` in `app.html` for self-reporting.
- **Documentation:** Create `test_suite_description.md` for the user.
---

## Finalizing Perfect Video Player (Overhaul 6)

### Audio Player & GUI Stability
- **Tab Split Test (Non-Selenium):** Verify Audio Player right-split populates correctly.
- **Dynamic GUI Loading:** Ensure JS structure is solid and handles database arrivals.
- **7 OBJECT TEST SUITE:** Multi-level verification (Dict → ...):
  - Level 1: Dictionary structures
  - Level 2: SQLite database consistency
  - Level 3: Mode Router logic (Mocked FFprobe)
  - Level 4: Static HTML integrity
  - Level 5: Dynamic JS Diagnostic (Eel Bridge)
  - Level 6: Mock Backend End-to-End
  - Level 7: Real Media Path Verification

### Video Player "Pimping" (Cinema Overhaul)
- **Advanced Filters:** Implement "Premium Cinema" visual filters.
- **Atmos/Bitstream Stats:** Display advanced audio metadata in overlay.
- **Track Switching:** Finalize FFmpeg-based audio/sub switching for Audio/Subtitles (HLS/MSE).
- **Audio Excellence:** Display Bitstream/Atmos Core metadata in Stats.
- **Modern UI:** Enhance Video.js 8 with new "Glass" or "Carbon" theme tweaks.

### Verification
- **Test Bed:** Implement `window.runDiagnostic()` in `app.html` for self-reporting.
- **Documentation:** Create `test_suite_description.md` for the user.

# Implementation Plan: Perfect Video Player - Overhaul 6 & GUI Fixes

**Datum:** 27.03.2026

## Target
Refine the media player with Stage 6 features: comprehensive subtitle/audio track support, advanced filtering, and GUI stability fixes (dynamic loading verification).

---

## Proposed Changes

### [Component] Backend: Overhaul 6 & Logic
- **[MODIFY] main.py**
  - Implement advanced filtering logic (genre, year, quality).
  - Enhance `get_library` to support server-side pagination or dynamic loading stats.
- **[MODIFY] streams/mse_stream.py & hls_stream.py**
  - Ensure all audio/subtitle tracks are correctly mapped and available for switching.

### [Component] Testing: 7 Object Test Suite (Non-Selenium)
- **[NEW] tests/test_suite_7_objects.py**
  - Implement a Python test suite that verifies the 7 levels of abstraction (Dict, DB, Router, Static HTML, Dynamic JS State).
  - Use BeautifulSoup for HTML static analysis (Level 4).
  - Invoke `window.runDiagnostic()` via Eel to verify JS state (Level 5).

### [Component] Video Player: Cinema Overhaul
- **[MODIFY] app.html**
  - Premium Filters: Update `setVideoFilter` with "HDR Cinema" (contrast/saturate blend).
  - Audio Engine Info: Display Bitstream/Dolby Atmos Core potential in the Stats Overlay.
  - Layout Split Test: Ensure right-split in Audio player is populated and verified by the test bed.

---

## Verification Plan

### Automated Tests
- `python3 tests/gui/test_dynamic_loading.py` (via subagent wrapper)
- `PYTHONPATH=. pytest tests/test_mode_router.py`

### Manual Verification
- Test track switching (Audio/Subs) for 4K MKV files.
- Verify advanced filters in the library tab.
- Check "Stats for Nerds" for Intel Arc / NVIDIA GPU utilization sync.
- Verify VLC Bridge or MPV.js WASM.
- Verify 0% CPU for H.264/MP4 (Direct Play).
