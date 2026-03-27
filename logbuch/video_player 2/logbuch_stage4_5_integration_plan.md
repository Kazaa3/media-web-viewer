# Implementation Plan – Stage 4 & 5 Integration and JS Fixes

This plan outlines the steps to implement Stages 4 and 5 of the test suite, fix a common JS error on right-click, address broken video selection, and introduce a JS-based automated test suite for videos.

## Proposed Changes

### [Component Name] web/app.html
- [MODIFY] app.html
  - Define `groupHeaders` in `showContextMenu` to fix the ReferenceError.
  - Ensure `startEmbeddedVideo` correctly handles potential empty `type` or `path` to avoid "Kein Video ausgewählt" error.
  - Add a trigger for the new JS-based video test suite.

### [Component Name] src/core/main.py
- [MODIFY] main.py
  - Update streaming routes to use `/via/` segment (e.g., `/direct/via/<path>`, `/transcode/via/<path>`) as requested.
  - Update `get_universal_stream_url` to return the new `/via/` URLs.
  - Remove redundant `test_pyautogui` function as it will be moved to a proper test file.

### [Component Name] tests/
- [NEW] test_pyautogui_automation_stage4.py
  - Dedicated test for PyAutoGUI automation.
- [NEW] test_subprocess_safety_stage5.py
  - Dedicated test for sub-process safety and management.

### [Component Name] web/js/
- [NEW] video_test_suite.js
  - JS-based automated test suite that programmatically interacts with the video player and verifies playback.

## Verification Plan

### Automated Tests
- Run Stage 4 tests: `./tests/run_all_tests.sh --stage 4`
- Run Stage 5 tests: `./tests/run_all_tests.sh --stage 5`
- Run the new JS test suite via the browser (manual trigger in Reporting tab).

### Manual Verification
- Right-click on a media item and verify no JS error occurs in the console.
- Verify that videos play correctly with the new `/via/` routing URLs.
- Check the "Stats for Nerds" overlay to ensure the correct protocol and engine are displayed.
- Verify that the "Kein Video ausgewählt" error is resolved.
