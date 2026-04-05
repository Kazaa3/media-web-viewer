# Implementation Plan: Subtitle UI & Advanced Media Toolchain (Phases 7 & 8)

## Goal
Complete the frontend integration for subtitle management and expand the application's core toolchain to support professional-grade media operations (MKVToolNix, HandBrake, advanced diagnostics).

---

## User Review Required
**IMPORTANT:**
- **System Dependencies:** MKVToolNix and HandBrakeCLI must be installed (`sudo apt install mkvtoolnix handbrake-cli`).
- **SWYH-RS:** This component is currently missing and will be flagged as a diagnostic warning until installed.

---

## Proposed Changes

### [Phase 7] Subtitle Management UI
- **[MODIFY] app.html**
  - SubtitleControlCenter: Inject a glassmorphism panel below the video player.
  - Track Interaction: Buttons for extraction (ffmpeg) and timing (pysubs2/srt).
  - External Load: Button to load .srt/.ass files from local disk.
- **[MODIFY] index.css (or style block)**
  - Add premium styles for subtitle track lists and sync controls.

### [Phase 8] Expanded Toolchain & Advanced Diagnostics
- **[NEW] mkv_tool_wrapper.py**
  - Wrapper for mkvmerge (muxing), mkvextract (streams), mkvinfo (details), mkvpropedit (tags).
- **[NEW] batch_processor.py**
  - Support for HandBrakeCLI batch encoding with GPU acceleration (VAAPI/QSV).
- **[NEW] suite_toolchain.py**
  - Diagnostic suite for all external binaries (FFplay, FFprobe, MKVToolNix, HandBrake).
- **[MODIFY] main.py**
  - Expose new toolchain APIs to the frontend.
  - Integrate pymediainfo and enzyme into the metadata pipeline.
- **[MODIFY] suite_routing.py**
  - Enhance routing tests for complex HW-accelerated paths.

---

## Verification Plan

### Automated Tests
- `python3 tests/run_all.py`
- Expect 240+ stages to pass.
- Verification of mkvmerge, HandBrakeCLI, and ffplay presence.

### Manual Verification
- **Subtitle Extraction:** Click "Extract" on a track and verify the .srt is created and loaded.
- **Timing Sync:** Adjust offset by +500ms and verify the shift in playback.
- **Media Routing:** Open the Reporting tab and verify the "Routing Drill-down" shows the correct logic (e.g., MSE vs Direct).
