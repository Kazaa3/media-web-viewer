# Global Diagnostic Integration & Real Audio Restoration (v1.35)

## Problem
- The "Atomic Recovery" logic for diagnostics and UI hardening was temporary and not centrally managed.
- Audio playback with real media files was not reliably restored after recovery or empty state events.

## Solution & Proposed Changes

### 1. Core Orchestration
- **app.html**: Registers `web/js/mwv_diagnostics.js` and adds a hidden diagnostic toolbar (`#diagnostic-toolbar`) that appears only when diagnostics are enabled.
- **app_core.js**: Initializes the DiagnosticSuite during the `mwv_finalize_boot` phase for consistent startup behavior.

### 2. Diagnostic Suite [NEW]
- **mwv_diagnostics.js**:
  - **Visibility Lock**: MutationObserver prevents hiding the player viewport, ensuring persistent UI integrity (lime borders).
  - **Atomic Hydration**: Function injects real tracks (e.g., `media/sample_audio.mp3`) into `allLibraryItems` and `currentPlaylist`.
  - **UI Toggle**: `Diagnostics.toggleBorders()` and `Diagnostics.toggleHeader()` allow toggling of diagnostic overlays via UI or console.

### 3. Audio Lifecycle
- **audioplayer.js**:
  - Synchronizes `currentPlaylist` with `allLibraryItems` on demand.
  - Ensures `renderPlaylist()` handles transitions from 'Empty' to 'Hydrated' state, restoring playback functionality.

### 4. Auto-Sync
- Implements an auto-sync that fills the player queue with library items if it remains empty for more than 5 seconds.

## Verification Plan

### Automated Tests
- **DOM Persistence Audit**: Verifies that lime borders remain visible after tab switches.
- **Hydration Audit**: Triggers `Diagnostics.hydrate()` and checks that the "Warteschlange leer" message disappears.

### Manual Verification
- Confirm that clicking "Play" on a hydrated track plays the `./media/sample_audio.mp3` file.

## Outcome
- **Restored:** Permanent, toggleable diagnostic suite and reliable real audio playback.
- **Verified:** UI and playback integrity through both automated and manual tests.
- **Status:** Awaiting user review for full integration into the v1.35 Diagnostic Suite.
