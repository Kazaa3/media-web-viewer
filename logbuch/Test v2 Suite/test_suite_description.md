# Finalizing Perfect Video Player (Overhaul 6)

## Audio Player & GUI Stability
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

## Video Player "Pimping" (Cinema Overhaul)
- **Advanced Filters:** Implement "Premium Cinema" visual filters.
- **Multi-Language Tracks:** Seamless switching for Audio/Subtitles (HLS/MSE).
- **Audio Excellence:** Display Bitstream/Atmos Core metadata in Stats.
- **Modern UI:** Enhance Video.js 8 with new "Glass" or "Carbon" theme tweaks.

## Verification
- **Test Bed:** Implement `window.runDiagnostic()` in `app.html` for self-reporting.
# 7 Object Test Suite: Media Player Overhaul 6

This test suite is designed to verify the application's integrity across 7 progressive levels of abstraction, without the overhead and instability of Selenium.

---

## Level 1: Memory & Data Structure (The "Dict" Level)
- Verifies that metadata dictionaries (JSON/Dict) are correctly structured before any processing.
- **Checked:** `MediaItem.to_dict()` and `ffprobe_analyzer` raw outputs.

## Level 2: Database Persistence
- Verifies that the SQLite database correctly stores and retrieves all Stage 6 fields (`full_tags`, `tracks`, `filters`).
- **Checked:** `db.insert_media` and `db.get_all_media`.

## Level 3: Mode Router & Logic
- Verifies that `smart_route` picks the correct playback mode and returns valid metadata for various file types.
- **Checked:** `src.core.mode_router.smart_route`.

## Level 4: HTML Template Integrity
- Verifies that `app.html` contains the required DOM elements for the Stage 6 UI (Filter Bar, Settings Panel).
- **Checked:** Static analysis of `app.html` using BeautifulSoup.

## Level 5: Dynamic JS State & Test Bed
- Verifies that the JS application correctly handles dynamic data arrival and state changes.
- **Implementation:** A built-in `window.runDiagnostic()` function in `app.html` that self-tests the UI state (e.g., "Are 10 items rendered in the right split?").

## Level 6: Mock File End-to-End
- Verifies the full pipeline using mock media files in a controlled environment.
- **Checked:** Faking file existence and verifying stream URL generation.

## Level 7: Real Media Verification
- Verifies the application with real media files from the user's library.
- **Constraint:** No filenames or identifying metadata are leaked in logs (anonymization).
- **Checked:** Real FFmpeg remuxing/transcoding stability.
