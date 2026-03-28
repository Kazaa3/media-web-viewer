# Implementation Plan - Extended Diagnostic Modernization

This plan outlines the implementation of several new specialized diagnostic suites to ensure 100% health coverage across reporting, logging, UI structural integrity, and advanced media parsing.

---

## Proposed Changes

### Diagnostic Infrastructure
- **[NEW] tests/engines/suite_reporting.py:** Verifies automated report generation (PDF/JSON/HTML) and data consistency between backend and UI reporting tabs.
- **[NEW] tests/engines/suite_logbuch.py:** Audits logbook entry creation, category filtering, and persistence in the SQLite database.
- **[NEW] tests/engines/suite_ui_integrity.py:** Performs deep DOM audits, CSS variable verification, and balance checks (DIV/BRACE) to prevent scaling issues.
- **[NEW] tests/engines/suite_parser.py:** Extends media parsing diagnostics to include mkvmerge, ffprobe advanced streams, and format-specific metadata edge cases.
- **[NEW] tests/engines/suite_edit.py:** Verifies the safety and persistence of metadata editing (tags, covers, rename operations).
- **[NEW] tests/engines/suite_sidebar.py:** Checks sidebar state management and synchronization with the main playlist view.
- **[MOD] tests/engines/suite_env.py:** Expand CLI tool discovery to include mpv, mkvmerge, and vlc (CLI interface).

### Master Integration
- **[MOD] tests/run_all.py:** Register all new engines for the unified health report.

---

## Verification Plan

### Automated Tests
- Run `python3 tests/run_all.py` to verify the total count of passing diagnostics reaches 150+.
- Perform targeted manual verification of the Reporting UI to ensure the new tests align with visual state.
