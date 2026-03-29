# Implementation Plan – Stability & Component Modularization

This plan addresses the final stages of the Media Viewer's transition to a modular architecture, focusing on the Reporting and Video Player components, while also stabilizing the Python environment and enhancing diagnostic logging.

## User Review Required
**IMPORTANT**

- **Python Version Conflict:** The user reports issues between Python 3.12 and 3.14. A stricter environment guard will be implemented in `main.py` to explicitly check the major/minor version (3.14.2) and fail fast with a clear instruction if the wrong interpreter is used.
- **DOM 7 Debugging:** This suite will centralize all UI integrity checks (Div balance, script errors, event interception) into a single helper file.

## Proposed Changes

### 1. 🔥 Component Modularization
- **[NEW] `reporting_helpers.js`**
  - Extract all dashboard and analytics logic from `app.html`.
  - Functions: `switchReportingView`, `refreshReportingData`, `loadModelAnalysis`, `loadParserPerformance`.
- **[NEW] `video_helpers.js`**
  - Extract all media player orchestration logic.
  - Functions: `selectEngine`, `initVideoPlayer`, `runVideoPlayerTest`, `toggleMtxStream`.
- **[NEW] `debug_helpers.js`**
  - Extract "DOM 7" diagnostic suite and event interception.
  - Functions: `initUiTraceHooks`, `logDivBalancePerTab`, `appendUiTrace`, `runRoutingBenchmark`.
- **[MODIFY] `app.html`**
  - Remove thousands of lines of redundant JS.
  - Include the new script tags in the `<head>`.

### 2. 🛡️ System & Environment Guard
- **[MODIFY] `main.py`**
  - Stricter Env Guard: Modify `ensure_stable_environment()` to verify the exact Python version (3.14.2 recommended) and the active Virtual Environment path.
  - Structured Logging: Enhance `log_js_error` to write structured JSON logs to `logs/frontend_errors.log`.
- **[NEW] `.python-version`**
  - Explicitly set the python version to 3.14.2 to guide local development tools (pyenv, etc.).

### 3. 🔍 DOM 7 Diagnostics Concept
- **Stage 1:** Div Balance Verification.
- **Stage 2:** Global Variable Pollution Check.
- **Stage 3:** Script Loading Integrity.
- **Stage 4:** Event Listener Count Monitor.
- **Stage 5:** Backend Sync RTT Latency.
- **Stage 6:** Memory Leak / DOM Node Count.
- **Stage 7:** Frontend-Backend Log Synchronization.

## Open Questions
- **Python Version:** Is Python 3.14.2 the strictly required version, or should 3.12 be supported with fixes? (Assume 3.14.2 is the stable target for now.)
- **Reporting Charts:** Should the current chart rendering logic be kept, or simplified during modularization?

## Verification Plan

### Automated Tests
- Run `UiTestSuite.runAllTests()` from the Diagnostics panel.
- Execute `python src/core/main.py --test-env` to verify the environment guard (checking for 3.14.2).

### Manual Verification
- Confirm all sub-tabs in reporting (Dashboard, SQL, Audio, Parser) still populate correctly.
- Ensure switching between "Chrome Native" and "VLC Bridge" players is seamless.
