# Logbuch – Navigation Restoration & Library Restructuring (v1.34)

## Datum
1. April 2026

## Ziel
Wiederherstellung zentraler Management- und System-Tabs in der v1.34-Navigation sowie Umstrukturierung von `File` und `Item` in eine Sub-Navigation innerhalb des Library-Bereichs.

## User Review Required
**IMPORTANT**

- **Sidebar Expansion:** Vier primäre Tabs werden in der Sidebar wiederhergestellt: `Edit`, `Reporting`, `Debug`, `Testing`.
- **Library Sub-Tabs:** `Library` wird zum Domain-Container mit horizontaler Sub-Navigation für `Mediathek`, `Dateibrowser` und `Inventar / Datenbank`.
- **Logging & Diagnostics:** Frontend-Trace-Events und GUI-Interaktionen werden für Phase 4 zusätzlich protokolliert.

## Proposed Changes

### [Frontend] UI Shell & Navigation
**[MODIFY]** `app.html`

- Sidebar Restoration:
  - Add `Edit` (Icon: `icon-edit`) to the Management section.
  - Add `Reporting` (Icon: `icon-stats`) to the Management section.
  - Add `Testing` (Icon: `icon-test`) and `Debug` (Icon: `icon-debug`) to the System section.
- Library Layout Refactor:
  - Add a `.sub-nav-bar` container at the top of `#main-content-area` or within the Library fragment.

### [Frontend] Modular Logic
**[MODIFY]** `ui_nav_helpers.js`

- Update `switchTab()` to load and reveal the restored tabs correctly.
- Add orchestration for Library sub-tab state so `File` and `Item` render inside the `Library` context.
- Inject `mwv_trace` calls for navigation and state debugging.

**[MODIFY]** `library_explorer.html`

- Add a sub-navigation header for:
  - `Mediathek`
  - `Dateibrowser`
  - `Inventar / Datenbank`

**[MODIFY]** `main.py`

- Expose `log_gui_event` for frontend traces.
- Add file-backed logging for GUI interaction events.
- Support inspection of backend GUI traces via `/tmp/mwv_backend.log`.

### Logging & Diagnostics (New Phase)
- Frontend Tracing: Inject `mwv_trace` into `ui_nav_helpers.js` and `bibliothek.js`.
- DOM/Playwright Logs: Forward browser console logs into the test runner output.
- Log Retrieval: Inspect `/tmp/mwv_backend.log` during debugging.
- Phase 4 activity includes logging-based debugging as a primary validation method.

## [Testing] Verification
**[NEW]** `navigation_verify.py`

A Playwright-based script to verify:
- existence and clickability of the 4 restored sidebar buttons
- successful fragment loading for `Edit`, `Reporting`, and `Testing`
- correct operation of the Library sub-tab navigation

## Open Questions
- Should `File` and `Item` completely disappear from the main sidebar once they become Library sub-tabs?  
  _Current assumption: Yes, to reduce clutter._
- Do we need a unified `Master Search` across `Mediathek`, `Dateibrowser`, and `Inventar`?

## Verification Plan

### Automated Tests
- Run `tests/ui/navigation_verify.py` to ensure restored tabs route correctly and DOM state updates as expected.

### Manual Verification
- Visual inspection of sidebar icon alignment and responsive behavior.
- Smooth transition check between `Mediathek` and `Dateibrowser` within the Library view.
- Confirm frontend trace events and backend GUI logs are written as expected.

## Recommended Defaults
- Remove `File` and `Item` from the main sidebar after Library sub-tabs are active.
- Defer unified `Master Search` until the new Library domain flow is stable.
