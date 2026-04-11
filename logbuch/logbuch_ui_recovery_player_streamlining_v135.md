# UI Recovery & Player Streamlining (v1.35)

## Changes Overview

### 1. Library Content Restoration
- **Issue:** Blank Library tab due to uninitialized `librarySubTab` state.
- **Fix:**
  - Initialized `librarySubTab = 'coverflow'` in bibliothek.js.
  - Added a safety check in `renderLibrary` to ensure a default view is always rendered.

### 2. Player Tab Streamlining (Mediengalerie Removal)
- **Action:** Mediengalerie has been fully retired; focus is now on the Queue.
  - **HTML:** Removed Mediengalerie button and container from player_queue.html.
  - **JS:** Deleted `renderItemGallery` and `setGallerySource` logic from audioplayer.js.
  - **Defaults:** Queue is now the active default view upon fragment load.

### 3. Navigation Lock Hardening
- **Goal:** Prevent UI freezing during rapid clicking.
  - **Lock Release:** Updated `finishSwitchTab` in ui_nav_helpers.js to explicitly reset `isNavigating` to false and restore the default mouse cursor.
  - **Sync:** Updated `initActions['player']` to trigger a clean `renderPlaylist()` call.

---

## Verification Results

### Render Trace Audit
- Backend logs confirm rendering engines are firing correctly:
  - `[DOM-UI] RENDER-LIBRARY (3 items detected)`
  - `[NAV] FINISH-SWITCH (Successful lock release)`

### File Integrity
- No references to `renderItemGallery` remain in the codebase.
- player_queue.html script now correctly defaults to warteschlange.

**NOTE:**
All media items should now be visible in both the Library (as Coverflow/Grid) and the Player (as the Queue).
