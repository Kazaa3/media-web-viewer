# Implementation Plan: Diagnostic Infrastructure Modernization (Phase 2)

**Goal**
Modernize the media diagnostic infrastructure by implementing specialized test suites for Reporting, Logbuch, UI Integrity, and Media Parsing, achieving 150+ stages of automated verification.

**Status:** COMPLETE (100% Green)

---

## Proposed Changes

### Diagnostic Engines
- **[NEW] suite_logbuch.py**
  - Verified Markdown entry discovery and metadata normalization.
- **[NEW] suite_reporting.py**
  - Audited technical reports, benchmark persistence, and aggregation logic.
- **[NEW] suite_ui_integrity.py**
  - Performed structural DIV balance audits and CSS token consistency checks.
- **[NEW] suite_parser.py**
  - Verified deep metadata extraction (ffprobe/mkvmerge) and tool readiness.
- **[NEW] suite_edit.py**
  - Audited metadata modification safety and tag persistence.
- **[NEW] suite_sidebar.py**
  - Verified UI state synchronization and toggle lifecycle.
- **[NEW] suite_options.py**
  - Audited configuration management and persistence.
- **[MODIFY] suite_env.py**
  - Expanded binary audit to 7 critical media tools (vlc, mpv, mkvmerge, etc.).

### System Core
- **[MODIFY] main.py**
  - Added SIDEBAR_OPEN state tracking and `toggle_sidebar` API.
- **[MODIFY] suite_player.py**
  - Fixed session lifecycle mocking to correctly verify process termination.

---

## Verification Plan

### Automated Tests
- Run `python3 tests/run_all.py` to verify all 20 engines and 150+ stages.
- **Status:** SUCCESS (All Green)
