# Global Diagnostic Integration & Real Audio Restoration (v1.35 Diagnostic Suite)

## Summary
This milestone formalizes the temporary "Atomic Recovery" logic into a permanent diagnostic system and restores full audio playback functionality using real media files from the workspace. Diagnostics are now modular, UI-togglable, and support both automated and manual verification of the player pipeline.

---

## Key Changes

### 1. Diagnostic Suite Modularization
- **New File:** `web/js/mwv_diagnostics.js` now contains all diagnostic logic (lime borders, MutationObservers, hydration, toolbar UI).
- **UI Integration:** A hidden diagnostic toolbar (`#diagnostic-toolbar`) is registered in `app.html` and can be toggled via the UI or console.
- **Auto-Sync:** If the player queue is empty for more than 5 seconds, it is automatically filled with available library items.

### 2. Audio Pipeline Restoration
- **Hydration:** Diagnostics can inject a real audio track (`media/sample_audio.mp3`) into both `allLibraryItems` and `currentPlaylist`.
- **Playback:** The player queue and playlist rendering now handle transitions from 'Empty' to 'Hydrated' state, ensuring the UI and playback engine recover gracefully.

### 3. DOM & UI Persistence
- **MutationObserver:** Prevents the player viewport from being hidden by UI transitions or tab switches.
- **Lime Borders:** Visual diagnostic borders can be toggled for persistent DOM audit.

---

## Verification Plan

### Automated
- **DOM Persistence Audit:** Confirm lime borders remain visible after tab switches.
- **Hydration Audit:** Trigger `Diagnostics.hydrate()` and verify the "Warteschlange leer" message disappears.

### Manual
- Open the app and enable diagnostics.
- Click "Hydrate Audio" in the toolbar.
- Confirm that clicking "Play" on the hydrated track plays `./media/sample_audio.mp3`.

---

## Artifact Metadata
- **ArtifactType:** implementation_plan
- **RequestFeedback:** true
- **Summary:** Diagnostic suite integration and audio pipeline restoration for robust recovery and testability.
