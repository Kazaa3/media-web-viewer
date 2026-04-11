## UI & Controller Integration Finalization
- Enable the PRUNE ORPHANS and PRUNE ALL ORPHANS buttons in `diagnostics_sidebar.html` for collection restoration.
- Implement `triggerPlaylistPruning()` and `triggerPlaylistPruningAll()` in `sidebar_controller.js` to bridge UI and backend repair logic.
- Update `runPlaylistAudit()` in `sidebar_controller.js` to display a professional integrity list for all collections.
- Ensure all repair/pruning actions are captured by the SENTINEL trace engine for persistent forensic documentation.
## Repair Suite Finalization
- Implement `prune_playlist_orphans(playlist_id)` bridge in `main.py` and `db.py` to surgically remove dead references from curated collections.
- Enable PRUNE ORPHANS button in `diagnostics_sidebar.html` for professional-grade repair tooling.
- Implement `triggerPlaylistPruning()` in `sidebar_controller.js` to bridge UI and backend repair logic.
- Ensure all repair/pruning actions are captured by the SENTINEL trace engine for persistent forensic documentation.
## Implementation Steps
- Implement `get_playlist_forensics()` in `main.py`
- Add reiter-playlist (PLY) to `diagnostics_sidebar.html`
- Add diag-pane-playlist viewport to `diagnostics_sidebar.html`
- Implement `runPlaylistAudit()` in `sidebar_controller.js`
- Update tab-switching mapping in `sidebar_controller.js`
- Verify orphaned track detection and duration summations
# v1.37.32 Playlist Forensic Audit: Integrity & Repair (PLANNED)

## User Review Required
**IMPORTANT**

**Collection Reliability:** This upgrade adds the "Curation Layer" to your workstation. You will have instant access to file-level integrity checks for your playlists, identifying "Dead Tracks" that no longer exist and repairing them with a single click.

---

## Proposed Changes
- **Backend (`main.py`):**
  - Implement `get_playlist_forensics()` Eel bridge.
  - Logic:
    - Scan the `./playlists` data directory.
    - Forensic Integrity Check: Map each track item in the playlist against the current SQLite index.
    - Metrics: Track Count, Broken Path Count, Total Duration Estimate.
- **Sidebar UI (`diagnostics_sidebar.html`):**
  - Add PLY as the 11th tab in the diagnostics master nav.
  - Add the high-density [PLAYLIST FORENSICS] viewport.
  - Render chromatic integrity markers (Green/Red).
- **Controller (`sidebar_controller.js`):**
  - Implement `runPlaylistAudit()` technical aggregator.
  - Logic:
    - Asynchronously fetch the playlist health report.
    - Render a matrix of playlists and their "Integrity Status".
    - Update the tab mapping to include the new domain.

---

## Open Questions
- Should we include Recursive Playlist Discovery (search for .m3u8)? (Recommendation: Focus on native JSON playlists for v1.37.32.)

---

## Verification Plan
- **Automated Tests:**
  - Verify that `get_playlist_forensics` correctly identifies orphaned track IDs.
  - Confirm total duration sums are numerically accurate based on metadata.
- **Manual Verification:**
  - Navigate to the PLY tab; verify that playlists appear with an "Integrity: OK" status.
  - Manually edit a playlist file to point to a non-existent ID; verify it is flagged.
  - Inspect the SENTINEL trace for the results.

---

## Status
- **PLANNED**
- Pending user approval for implementation.

---

*Next: Upon approval, proceed with backend and frontend implementation as described above.*
# v1.37.32 Playlist Forensic Audit: Integrity & Repair (PLANNED)

## Overview
This upgrade introduces the Playlist Forensic Audit, providing a professional-grade PLY (Playlist) tab in the diagnostics sidebar. The new dashboard delivers technical observability into curated collections, including Dead Track detection, Orphaned Track Identification, and Automated Repair triggers, ensuring total media collection awareness and integrity.

---

## Implementation Plan
- **Playlist Integrity Bridge (Backend):**
  - Implement a new backend bridge in `main.py` to audit playlist JSON files against the live SQLite database.
  - Identify Dead Tracks (referenced in playlists but missing from the database) and Orphaned Tracks (present in the database but not referenced by any playlist).
  - Provide endpoints for triggering automated repair actions.

- **High-Density PLY Dashboard (Frontend):**
  - Add the PLY tab to `diagnostics_sidebar.html` (11th tab).
  - Implement a professional-grade dashboard for playlist engineering, displaying:
    - Dead Track count and details
    - Orphaned Track identification
    - Automated Repair triggers and status

- **Controller Integration:**
  - Update `sidebar_controller.js` to support the PLY tab and orchestrate playlist audits and repairs.

- **SENTINEL Trace Integration:**
  - Capture every playlist audit and repair action in the sentinel engine, providing a persistent forensic record of the media collection's technical state.

---

## Verification Plan
- **Automated:**
  - Verify backend correctly identifies Dead and Orphaned Tracks.
  - Confirm repair actions update both playlists and database as expected.
- **Manual:**
  - Navigate to PLY tab; verify dashboard updates and repair triggers function.
  - Inspect SENTINEL trace for audit and repair logs.

---

## Status
- **PLANNED**
- Pending user approval for implementation.

---

*Next: Upon approval, proceed with backend and frontend implementation as described above.*
