# Task List: JavaScript Logic Modularization & UI Refinement

## Infrastructure Cleanup
- [ ] Attempt to terminate zombie processes (python3 -c ...)

## Module: Common Helpers
- [ ] Create `web/js/common_helpers.js`
- [ ] Extract `appendUiTrace`, `showToast`, `update_progress`, and DOM utils
- [ ] Link in app.html

## Module: System & Diagnostics
- [ ] Create `web/js/system_helpers.js`
- [ ] Extract RTT tests, stress tests, and environment loading
- [ ] Link in app.html

## Module: Options Logic
- [ ] Create `web/js/options_helpers.js`
- [ ] Extract startup config saving/loading, playback modes, and bandwidth limits
- [ ] Link in app.html

## Module: Edit (Metadata) Logic
- [ ] Create `web/js/edit_helpers.js`
- [ ] Extract tag saving, ISBN scanning, and file-renaming
- [ ] Link in app.html

## Refinement: Edit Tab UI
- [ ] Standardize `edit-split-container` labels and icons
- [ ] Ensure consistent "Split-to-Right" proportions

## Final Cleanup
- [ ] Delete redundant inline scripts from app.html (~5000+ lines)
- [ ] Verify functionality via `suite_ui_integrity.py`
