# Implementation Plan — Global Diagnostic Integration & Real Audio Restoration (v1.35 Diagnostic Suite)

## Objective
Formalize the "Atomic Recovery" logic into a permanent Diagnostic Suite and restore robust audio playback using real media files from the workspace.

---

## Core Orchestration
- **app.html**
  - Register `web/js/mwv_diagnostics.js`.
  - Add a hidden diagnostic toolbar (`#diagnostic-toolbar`) that appears only when diagnostics are enabled.
- **app_core.js**
  - Initialize the `DiagnosticSuite` during the `mwv_finalize_boot` phase.

---

## Diagnostic Suite (NEW: mwv_diagnostics.js)
- **Visibility Lock:**
  - Use a `MutationObserver` to prevent hiding of the player viewport (lime borders always visible).
- **Atomic Hydration:**
  - Provide a function to inject real tracks (e.g., `media/sample_audio.mp3`) into `allLibraryItems` and `currentPlaylist`.
- **UI Toggle:**
  - Implement `Diagnostics.toggleBorders()` and `Diagnostics.toggleHeader()` for runtime control via UI or console.
- **Auto-Sync:**
  - Automatically fill the player queue with library items if it remains empty for more than 5 seconds.

---

## Audio Lifecycle
- **audioplayer.js**
  - Synchronize `currentPlaylist` with `allLibraryItems` on demand.
  - Ensure `renderPlaylist()` correctly transitions from 'Empty' to 'Hydrated'.

---

## Verification Plan
- **Automated Tests:**
  - *DOM Persistence Audit:* Verify lime borders remain visible after tab switches.
  - *Hydration Audit:* Trigger `Diagnostics.hydrate()` and confirm the "Warteschlange leer" message disappears.
- **Manual Verification:**
  - Click "Play" on a hydrated track and confirm playback of `./media/sample_audio.mp3`.

---

## Notes
- All diagnostic features are now modular, toggleable, and persistent across UI states.
- This suite ensures both developer diagnostics and real user playback are robust and reliable.

---

*Ready for user review and implementation as described above.*
