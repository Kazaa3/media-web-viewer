# Task List: Management Tabs Split-Layout Refactor

## Item (Inventory) Split Refactor
- [ ] Create `item-split-container` wrapper
- [ ] Add `item-sidebar-left` with category chips
- [ ] Add `item-splitter`
- [ ] Move grid into `item-main-content-pane`

## Options Tab Overhaul
- [ ] Create `options-split-container` wrapper
- [ ] Add `options-header-tabs` sub-navigation bar
- [ ] Group settings into `options-general-view`
- [ ] Group settings into `options-appearance-view`
- [ ] Group settings into `options-indexing-view`
- [ ] Group settings into `options-transcoding-view`
- [ ] Create `options-debug-view` (Debug & Flags)

## Navigation & Tracing
- [ ] Implement/Update `switchOptionsView(viewId)` (Currently in app.html)
- [ ] Ensure all sub-tab switches are logged via `traceUiNav`

## Navigation Modularization (JS Helpers)
- [ ] Create `web/js/ui_nav_helpers.js`
- [ ] Extract `switchOptionsView`, `switchEditView`, `switchReportingView`, `switchTestView`, and `switchLibrarySubTab` from app.html
- [ ] Link `ui_nav_helpers.js` in app.html

## Verification & Validation
- [ ] Run `tests/engines/suite_ui_integrity.py` and verify all new IDs
- [ ] Manually verify split-resizing and view persistence
