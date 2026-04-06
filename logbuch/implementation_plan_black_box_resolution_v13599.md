# Implementation Plan — The 'Black Box' Resolution (v1.35.99)

This plan achieves the dual goal of resolving the persistent "0 items" library bug while finalizing the UI and de-cluttering the footer. By moving detailed parity metrics into the Sidebar Diagnostics, we provide a professional "cockpit" view for troubleshooting.

## User Review Required

**IMPORTANT**

- **Footer Simplification:** The footer is being "flattened". The detailed `[FS | DB | GUI]` indicator is moving into the Diagnostics Sidebar. The footer will now only show a minimal "Sync Status" light.

**TIP**

- **Logic Audit: Why 0 Items?**
    - Adding a `dropped_reasons` audit to the backend. This will definitively tell us if items are being dropped due to:
        - Category Mismatch (e.g., 'Film' vs 'video').
        - Extension Whitelist (e.g., unsupported format).
        - Search/Genre Conflicts.

## Proposed Changes

### Phase 1: Logic Audit Enhancement (`main.py`)
- **[MODIFY] main.py**
    - Update `_apply_library_filters` to return a `dropped_reasons` dictionary in the audit metadata.
    - Integrate categorization auto-fixes if obvious mismatches are detected (e.g., lowercase vs uppercase).

### Phase 2: UI Consolidation (`app.html` & `diagnostics_helpers.js`)
- **[MODIFY] app.html**
    - Relocate the `footer-sync-anchor` DIV into the `sidebar-view-diagnostics` container.
    - Update Footer: Simplify to a minimal "System Pulse" status.
    - Add `dropped-reasons-viewport` to the Diagnostics sidebar.
- **[MODIFY] diagnostics_helpers.js**
    - Update `updateSyncAnchor()` to target the new sidebar ID.
    - Update `auditSwitchStage()` to display the backend `dropped_reasons` in the sidebar mini-logs.

### Phase 3: Category SSOT Validation (`models.py`)
- **[MODIFY] models.py**
    - Audit `MASTER_CAT_MAP` for missing common labels that might cause drops (e.g., ensuring "Video", "Film", "Movie" all map to the canonical "multimedia").

## Open Questions
- **Final Footer View:** Do you want the footer to show any text (e.g., "Ready"), or just a clean icon cluster?

## Verification Plan

### Automated Tests
- `python3 scripts/verify_audit_flow.py`: Verify that `dropped_reasons` are correctly passed through Eel.

### Manual Verification
- **Check Sidebar:** Toggle "Diagnostics" → Do you see the `[FS | DB | GUI]` parity?
- **Trigger Audit Stage 3:** Does the sidebar tell you exactly why items are dropped?
- **Apply RAW BYPASS:** Confirm items appear to verify the pipeline is healthy.
