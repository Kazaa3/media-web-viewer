# Task List: UI Navigation & Library Sub-tab Repair

## Backend Telemetry Integration
- [ ] Add `log_ui_event` to src/core/main.py

## Frontend Navigation Instrumentation
- [ ] Create `traceUiNav` in web/app.html
- [ ] Update `switchTab` for unified tracing
- [ ] Update `switchLibrarySubTab`
- [ ] Update `setLibraryFilter`
- [ ] Update view-switching helpers (`switchOptionsView`, `switchParserView`, etc.)
- [ ] Update `toggleModal`

## Library Sub-tab Repair
- [ ] Fix categorical filter buttons (active state / onclick)
- [ ] Verify `renderLibrary` correctly filters by category

## Diagnostic Suite Expansion
- [ ] Add `level_16_navigation_coverage_audit` to suite_ui_integrity.py
- [ ] Add `level_17_modal_structural_audit`

## Verification
- [ ] Run full diagnostic suite
- [ ] Manually verify library sub-tab transitions
