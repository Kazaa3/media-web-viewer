# Media Item Audit Track (Journey) Suite – v1.37.08

## Motivation
To permanently resolve the "Black Hole" and other item-dropping bugs, a new diagnostics feature called the "Item Track" (Journey) Suite is being implemented. This suite allows tracing any media item's journey from the database to the UI, identifying exactly where and why it is dropped or modified.

## Feature Overview
- **Journey Tracking:**
  - Visualizes the full path of a media item:
    1. **DB Status:** Presence in SQLite.
    2. **SSOT Status:** Category assignment in models.py.
    3. **Backend Filter:** Pass/fail in main.py, with rejection reason.
    4. **Frontend Model:** Presence in JS allLibraryItems.
    5. **Display Filter:** Pass/fail in bibliothek.js (search/category/genre).
    6. **DOM Render:** Existence of the grid-item in the browser.
- **UI:**
  - New "ITEM TRACK" tab in the diagnostics sidebar.
  - Search/select input for manual audit, plus a "Track This" button in the item context menu.
  - Vertical timeline visualizer for the item's journey.

## Implementation Plan
1. **Backend Audit Engine (main.py):**
   - Add `audit_specific_item(query)`, Eel-exposed, returns a JSON object with the item's state at every backend stage.
2. **Frontend Journey Visualizer (diagnostics_helpers.js):**
   - Add `renderItemTrackTab()` for the sidebar tab UI.
   - Add `performJourneyAudit(item)` to coordinate backend and frontend checks, building the timeline.
3. **System UI (app.html):**
   - Add "ITEM TRACK" button/tab and result viewport to the diagnostics sidebar.

## Open Questions
- **Trigger:** Should the audit run automatically on item click, or only via manual search? (Suggested: Both.)

## Verification Plan
- **Parity Test:** Track an item present in Stage 1 but dropped in Stage 3; UI must show the correct rejection point.
- **Black Hole Simulation:** Track an item that passes all filters but is hidden by CSS; DOM Auditor must flag it.

---

**Date:** 2026-04-06
**Author:** GitHub Copilot
