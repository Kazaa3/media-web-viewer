# Implementation Plan: Media Viewer UI De-Monolith Phase 2

We will continue splitting the massive logic blocks in app.html into specialized JavaScript modules. This phase targets the Logbook, Test Suite, System Sync, and Core Navigation components.

## User Review Required
**IMPORTANT**

- **Namespace Collisions:** Several functions in app.html (like `renderLogbuchList`) overlap with existing logic in `js/logbook_helpers.js`. The more feature-rich versions from app.html will be prioritized during the merge.

**WARNING**

- **Dependency Order:** The new `test_helpers.js` will depend on `video.js` and `reporting_helpers.js`. The import order in app.html will be managed to prevent "undefined" errors.

## Proposed Changes

### [Logbook & Documentation Component]
- **[MODIFY] logbook_helpers.js**
  - Import and merge `renderLogbuchList` and `loadLogbuchContent` from app.html.
  - Move `loadFeatureStatus`, `renderFeatureSection`, `toggleFeatureStatus`, and `openLogbook` into this file.
  - Clean up redundant or legacy implementations of these functions within the file.

### [Test Suite & Diagnostics Component]
- **[NEW] test_helpers.js**
  - Extract the entire Test Suite logic (approx. 2000 lines).
  - Includes: `loadTestSuites`, `runSelectedTests`, `runVideoPlayerTest`, `monitorVjsPlayback`, and `updateTestResultsTable`.
  - Includes specialized triggers: `runMtxValidation`, `runFfmpegPipelineSuite`, `runCodecMatrix`.

### [System & Environment Component]
- **[MODIFY] system_helpers.js**
  - Move `syncVersionInfo` and `checkConnection` (Sync Status heartbeat) into this file.
  - Ensure the sync-indicator UI updates correctly from the external module.

### [Navigation & Main View Component]
- **[MODIFY] ui_nav_helpers.js**
  - Move `switchMainCategory` and `update_progress` (Eel progress bar) into this file.
  - Move media support utility `isUnsupportedMediaError`.

### [Main View Cleanup]
- **[MODIFY] app.html**
  - Remove extracted script blocks from `<head>` and `<body>`.
  - Add import for the new `js/test_helpers.js`.
  - Retain only the minimal initialization logic and DOM event listeners.

## Open Questions
- Should the large context-menu HTML/JS logic (~100 lines) also be extracted? (Recommendation: Yes, into `js/ui_nav_helpers.js`.)

## Verification Plan

### Automated Tests
- Run `runUiIntegrityCheck()` in the console to verify DOM node presence and event listener attachment.
- Verify `frontend_errors.log` remains empty after navigation.

### Manual Verification
- Test Logbuch tab filtering and entry loading.
- Test Diagnostics tab test suite execution (run a small Python test).
- Verify Video Player engine switching still updates the playback history.
- Check the Sync Dot (bottom bar) for green "Synchronized" status.
