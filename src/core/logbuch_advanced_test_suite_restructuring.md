# Advanced Test Suite Restructuring & Expansion

## Goal
Finalize the transformation of the testing environment into a professional, hierarchical structure and fill the remaining "Level 1-26" gaps with high-value functional tests.

---

## Proposed Changes

### [Directory Restructuring]
- **Move Suites:** Relocate `suite_*.py` and `test_base.py` to `tests/engines/`.
- **Functional Tests:** Move standalone scripts like `test_environment_deploy.py` to `tests/functional/`.
- **Core Orchestration:** Keep `run_all.py` in `tests/` root as the main entry point.
- **Resource Management:** Consolidate `mockfiles/`, `assets/`, and `data/` under `tests/resources/`.

### [Advanced Test Implementation]
- **MediaItem Property Mocks (Items L08-L10):**
  - Verify ALAC/WMA transcoding triggers in `MediaItem.to_dict()`.
  - Validate duration H:M:S formatting for long files.
  - Audit category -> type_token mapping for "Hörbuch" and "Film".
- **Multi-Track Metadata (Items L11):**
  - Mock ffprobe output with 5+ streams to verify count accuracy.
- **Transcoding Stress (Ultimate L29):**
  - Implement a real load test for the transcoder module.
- **Database Concurrency (Ultimate L27):**
  - Already implemented, will refine if needed.
- **Corrupt Media Recovery (Ultimate L28):**
  - Already implemented.

### [E2E & Automation Diagnostic]
- **PyAutoGUI Desktop Metrics (Automation L01):**
  - Verify screen size and mouse access.
- **PyAutoGUI Interaction Smoke (Automation L02):**
  - Perform safe relative mouse movement and back.
- **Structural Integrity Audit (Automation L03):**
  - Port `gui_validator.py` logic to verify DIV/BRACE balance in `app.html`.

### [Casting & External Bridge Diagnostic]
- **Chromecast Discovery (Casting L01):**
  - Verify MDNS discovery status and pychromecast integration.
- **Spotify librespot Bridge (Casting L02):**
  - Audit binary availability and bridge process spawning logic.
- **swyh-rs Stream Toggling (Casting L03):**
  - Validate state persistence and system audio capture triggers.

### [Audioplayer & Playback Lifecycle]
- **Playback State Sync (Audioplayer L01):**
  - Verify consistency between `CURRENT_INDEX` and frontend state.
- **Volume & Mute Propagation (Audioplayer L02):**
  - Audit volume level clamping and mute state persistence.
- **Track Transition Logic (Audioplayer L03):**
  - Test `next_in_playlist` and `prev_in_playlist` boundary conditions.

### [Playlist & Queue Management]
- **Import/Export Reliability (Playlist L01):**
  - Verify M3U export/import via `export_playlist_to_vlc`.
- **Shuffle & Reorder Integrity (Playlist L02):**
  - Audit index shifting during `move_item_up` and `remove_playlist_item`.
- **Persistence & Recovery (Playlist L03):**
  - Validate playlist restoration from `media-web-viewer.json`.

---

## Verification Plan

### Automated Tests
- Run `python3 tests/run_all.py` and verify all 26 stages in Ultimate (and others) are green.
- Execute new functional tests in `tests/functional/` to ensure path resolution remains correct after move.
