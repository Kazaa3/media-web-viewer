# Logbuch: Dedicated Playlist Module (v1.45.120)

## Overview
This release extracts all playlist-related state and logic into a new, standalone module (playlists.js), following the project's modularization principles and elevating the media queue to a first-class component of the forensic workstation.

---

## Key Changes

### 1. Unified Playlist Module
- **playlists.js:**
  - Defines `window.currentPlaylist = []` and `window.playlistIndex = -1`.
  - Implements `syncQueueWithLibrary()` (moved from app_core.js).
  - Implements manipulation functions (moved from audioplayer.js):
    - `clearQueue()`
    - `addToQueue(item)`
    - `removeItem(index)`
    - `moveItemUp(index)`
    - `moveItemDown(index)`
    - `addAndPlayNow(el, item)`
    - `resetAllFilters()`
  - Implements `startAtomicHydrationWatcher()` (moved from audioplayer.js).

### 2. app_core.js Cleanup
- Removed `window.currentPlaylist` and `window.playlistIndex` definitions.
- Removed `syncQueueWithLibrary()`.

### 3. audioplayer.js Cleanup
- Removed all manipulation and watcher functions listed above.
- Ensured all calls to these functions remain operational (they are still global).

### 4. HTML Integration
- **shell_master.html:** Added `<script src="js/playlists.js?v=1.45.110"></script>` before app_core.js.
- **app.html:** Ensured the same script inclusion if applicable.

---

## Open Questions
- Should player-specific rendering calls (`renderAudioQueue`, `renderVideoQueue`) be moved into playlists.js as observers, or should the trigger remain in `syncQueueWithLibrary`?
- Should playlists.js also include logic for saving/loading named playlists from the backend? (Recommended: Yes, for better encapsulation.)

---

## Verification Plan

### Automated Tests
- Verify that `window.currentPlaylist` is correctly initialized via playlists.js.
- Verify that `syncQueueWithLibrary` correctly triggers rendering in both players.
- Check console for any ReferenceError during bootstrap.

### Manual Verification
- Test "Clear Queue", "Remove Item", and "Move Up/Down" in the Audio Player UI.
- Test "Add to Queue" from the library grid (both players).
- Verify hydration pulse between players.

---

**This modularization ensures robust, maintainable, and testable playlist management for all forensic workstation flavors.**
