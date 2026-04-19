# Implementation Plan – v1.41.09 Cross-Effect Remediation

This plan eliminates "Kreuzwirkungen" (cross-effects) by unifying the mapping of the "STATUS" category and cleaning up hardcoded layout conflicts.

---

## User Review Required
**CAUTION**
- **Registry Mismatch:** I found that the "STATUS" button triggers the category `status`, but the internal JS registry was expecting `diagnostics`. This mismatch caused the "Black Screen" because the system didn't know which tab to open for status.

**IMPORTANT**
- **Class Purge:** I will remove all hardcoded `active` classes from `app.html`. The UI will start in a clean state and let the JS Orchestrator (`MWV_UI`) decide what to show based on your last session.

---

## Proposed Changes

### Navigation Registry (JS)
- **[MODIFY] ui_nav_helpers.js**
  - **Status Mapping:** Add `'status': 'debug'` (or the correct diagnostic container) to the `categoryDefaults` map.
  - **Switch Consolidation:** Ensure `switchMainCategory('status')` triggers the correct sub-view population.

### Layout Cleanup (HTML)
- **[MODIFY] app.html**
  - **Remove Hardcoded Active:** Strip the `active` class from `#player-panel-container` and others.
  - **Fragment Guard:** Ensure the "Lade..." overlays are hidden by default and only shown during active loading.

### Orchestration Logic (JS)
- **[MODIFY] ui_core.js**
  - **Safe State:** Ensure that if a category mapping is missing, it falls back to a visible "Player" view instead of a black screen.

---

## Open Questions
None.

---

## Verification Plan

### Manual Verification
- **Status Click:** Click "STATUS" and verify the diagnostics pane opens immediately.
- **Player Switch:** Click "Player" and verify the video/audio interface returns.
- **No Ghosts:** Verify only ONE tab has the `active` class in the DOM at any time.
