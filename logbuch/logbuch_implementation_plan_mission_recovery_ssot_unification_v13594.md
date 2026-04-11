# 🚀 Final Consolidation Details (v1.35.95)

The final cleanup of the Media Viewer v1.35.95 architecture is complete. All core systems—from the scanning engine to the smart router and diagnostic hubs—are now fully synchronized and driven by the centralized Single Source of Truth (SSOT).

## Final Consolidation Details

- **Purged Legacy Categories:** Completed a full audit of `main.py`, transitioning all remaining logic from legacy identifiers (`Abbild`, `Film`, `images`) to the canonical names: `disk_images`, `multimedia`, and `pictures`.
- **Smart Router Hardening:** Updated the intelligent routing logic (line 4967) to correctly prioritize `vlc_embedded` for the new `disk_images` category, ensuring seamless DVD and ISO playback.
- **Refined Pipe-Kit Engine:** Verified and finalized the performance-driven remuxing pipeline (Pipe-Kit), integrating centralized buffer configurations for both `mkvmerge` and `ffmpeg`.
- **Diagnostic Consistency:** Updated the Routing Suite and Capability Matrix diagnostics (line 8018+) to ensure diagnostic ratings perfectly align with the actual player routing logic.

## ✅ Recovery Status

- **'0 Item' Bug:** FIXED (Categories are now perfectly synced).
- **Hardcoded Values:** PURGED (All core logic now consumes `GLOBAL_CONFIG`).
- **Stats Overlay:** LIVE (Real-time tracking of bitrate, codec, and latency).
- **App Data Cleanup:** SSOT-DRIVEN (Uses the canonical `storage_registry`).

Your environment is now stable, hydrated, and fully config-driven. Please perform an Atomic Sync in the Diagnostic Hub to refresh the UI with the final canonical metadata. Refer to the updated `walkthrough` for full implementation details.
# 🛡️ Mission Recovery Highlights (v1.35.94)

The architectural foundation for Media Viewer v1.35.94 is now fully established. All hardcoded parameters have been centralized into the Single Source of Truth (SSOT), and the critical filtering regression has been resolved.

## Highlights

- **Resolved '0 Item' Bug:** Synchronized the backend filtering logic in `_apply_library_filters` with the new canonical category names (`pictures`, `disk_images`). Indexed media is once again visible in the UI.
- **Hydrated Stats Overlay:** Replaced mocked diagnostic data in `get_playback_stats` with real-time metrics. The Stats Overlay (Alt+S) now tracks live session data, including codecs, bitrates, and RTT, pushed directly from the active streaming pipelines.
- **SSOT Integration:** Refactored `main.py` to eliminate hardcoded values for:
    - **Transcoding & Remuxing:** FFmpeg and mkvmerge now consume global profiles from `config_master.py`.
    - **Performance Buffers:** Streaming and pipe-kit buffer sizes are now managed via `perf_settings`.
    - **Scanning Limits:** Max depth and file count are now driven by `scan_settings`.
    - **Hardware Priority:** Encoder detection now uses the centralized hardware priority registry.
- **Category Expansion:** Formally integrated `unbekannt` (Unknown) as a canonical category in both `models.py` and the SSOT registries to ensure no media is lost during indexing.

## 🔬 Next Steps for Verification

To confirm the recovery and verify the new diagnostic capabilities:

1. Navigate to the Diagnostic Hub in the Options panel.
2. Trigger a Direct Scan or Atomic Sync to re-hydrate the library using the new category filters.
3. Start a video stream and verify the live metrics in the Stats Overlay.

Please refer to the updated `walkthrough.md` for a detailed summary of the architectural changes.
# Implementation Plan: Mission Recovery & SSOT Unification (v1.35.94)

We have identified a critical category mismatch that is causing a "0 item" black hole in the media library. Multiple hardcoded blocks in main.py also violate our Single Source of Truth (SSOT) architecture. This plan outlines the restoration of full library visibility and the final hydration of the Diagnostic Stats overlay.

## User Review Required

**IMPORTANT**

- **Category Migration Consistency:** All media labeled `images` in old versions will now be canonicalized as `pictures`. All `abbild` (ISO) items will be `disk_images`. This is necessary to align with the backend database standards.

- **Playback Stats Hydration:** Real bitrate/codec stats will be pulled from active HLS/VLC sessions. If no active session is found, it will return "N/A" instead of mock values to ensure technical accuracy.

## Proposed Changes

### [Component] Core Configuration (SSOT)
- Centralize all newly identified hardcoded values into `src/core/config_master.py`.

#### [MODIFY] config_master.py
- **Categories:** Update `displayed_categories` and `indexed_categories` to use `pictures` and `disk_images` (resolves "0 item" bug).
- **Scan Settings:** Add `scan_settings` registry:
    - `max_depth: 12`, `max_files: 50000`.
- **Player Settings:** Add `player_settings` registry:
    - `video_extensions` (moved from main.py).
    - `force_native_audio: True`.
    - `media_prefixes: ["/media/", "media/"]`.
    - `playback_mode_mapping`.
- **Transcoding & Remuxing Profiles (SSOT v1.35.94):**
    - `audio_transcode`: `codec: aac`, `bitrate: 192k`, `movflags: ...`.
    - `video_transcode`: `preset: veryfast`, `crf: 23`, `bitrate_a: 128k`.
    - `lossless_remux`: `flags: ["-c", "copy", "-f", "mp4", "-movflags", "..."]`.
- **Performance Tracking:** Add `perf_settings` registry:
    - `streaming_buffer_size: 1048576`, `mkvmerge_bufsize: 1048576`.
- **Storage Registry:** Add `config_dir` and move hardcoded cleanup paths.
- **Hardware Registry:** Standardize encoder priorities (`nvenc`, `vaapi`, `qsv`).

### [Component] Main Application Logic
- Refactor `main.py` to consume the expanded SSOT.

#### [MODIFY] main.py
- **Playback Stats:** Hydrate `get_playback_stats` with real session data.
- **Library Filtering:** Update `_apply_library_filters` to use synchronized category names.
- **Playback Routing:** Refactor `play_media` and `resolve_media_path` to consume `player_settings`.
- **Streaming Engine:** Refactor `ffmpeg_stream` and `mkvmerge` logic to consume centralized Transcoder profiles, `perf_settings`, and `player_settings`.
- **Cleanup & Reset:** Refactor `reset_app_data` to use `storage_registry` and unify deleted tracking.
- **Scanning Engine:** Update scan functions to consume `scan_settings`.
- **Hardware Detection:** Refactor `get_best_hw_encoder` to use centralized priorities.

### [Component] Library Models
- Finalize category standardizations.

#### [MODIFY] models.py
- Ensure all helper functions like `get_allowed_internal_cats` are fully synchronized with the updated `config_master.py`.

## Open Questions
- **Bitrate Polling:** Should `get_playback_stats` perform a real-time check on the current stream's bitrate (more accurate, higher load) or return the target bitrate from the transcoder profile?
- **Cleanup Policy:** Should `reset_app_data` also clear the `cache/` directory by default?

## Verification Plan

### Automated Tests
- Run the application and verify that the "Library" tab shows the expected items (proving fix of "0 item" bug).
- Verify `get_playback_stats` returns real data during active HLS playback.
- Verify that `reset_app_data` returns the correct centralized paths in the deleted list.

### Manual Verification
- Confirm that the "Stats" overlay visually reflects real GPU usage and codec information.
- Perform a sample "Direct Scan" to ensure scanning depth limits are correctly applied from the SSOT.
