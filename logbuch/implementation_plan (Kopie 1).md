# Implementation Plan: Modularization of Core Logic

The goal is to further reduce the complexity of the 3300+ line app_core.js by splitting its logic into three primary domain-specific modules: audioplayer.js, edit.js, and browse.js. This will improve maintainability, reduce line-number drift during edits, and clarify the separation of concerns between media playback, library browsing, and metadata management.

---

## Proposed Changes

### 1. Audioplayer Module [NEW]
**audioplayer.js**
- **State Management:** Consolidate global playback state (currentPlaylist, playlistIndex, isShuffle, volume).
- **Playback Control:** Extract play(), playAudio(), playNext(), playPrev(), and renderPlaylist().
- **UI Integration:** Move updateMediaSidebar() for metadata display and jumpToChapter() for audiobook navigation.
- **Media Session:** Call into media_session_helpers.js for OS-level integration.

### 2. Browse Module [NEW]
**browse.js**
- **State Management:** Consolidate library filtering state (libraryFilter, librarySearch, CATEGORY_MAP).
- **Grid & Coverflow:** Move renderLibrary(), updateCoverflowDisplay(), renderGridView(), and renderDatabaseView().
- **Filter Logic:** Extract setLibraryFilter(), handleLibrarySearch(), and updateFilterOptions().
- **Domain Views:** Move renderAlbumView() and renderFollowingView().

### 3. Edit Module [RENAME/MERGE]
**edit_helpers.js → edit.js**
- **Rename** edit_helpers.js to edit.js for consistency with the new naming scheme.
- **Move** openEditForm() and openMetaEditor() from app_core.js into this module.
- **Consolidate** all metadata CRUD logic (Save, Rename, Delete, ISBN Scan).

### 4. Application Orchestration
**app_core.js**
- Transition into a lean Orchestrator.
- Retain routing logic like playMediaObject() and isVideoItem() which decide which player (Audio or Video) to engage.
- Act as the primary entry point for cross-module interactions.

**app.html**
- Update <head> imports to include the new script tags in the correct dependency order.

---

## Dependencies & Order of Execution
- Extract Browse Logic: High volume of code, clear boundaries.
- Extract Edit Logic: Merging existing helper with remaining app_core.js logic.
- Extract Audio Logic: Requires careful management of the currentPlaylist global shared with the video player.
- Syntax Verification: Run node --check after each extraction to ensure no truncated blocks.

---

## Open Questions
**State Visibility:**
- Should these modules expose functions via a global MWV object, or remain global for now to maintain compatibility with existing onclick handlers in app.html?
- Recommendation: Stay global for now and progressively namespace in a later phase.

**Video Player:**
- video.js already exists. Should some of the "current track" state move to a shared player_state.js or remain duplicated if logic differs?

---

## Verification Plan

### Automated Checks
- `node --check web/js/*.js` to ensure script integrity.
- Grep for orphaned functions in app_core.js.

### Manual Verification
- Test Library Filtering & Searching.
- Verify Audio Playlist progression and Sidebar updates.
- Test the Metadata Editor from the context menu.
