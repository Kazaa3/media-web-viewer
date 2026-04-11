# ⚙️ Modular Tool Registry (SSOT Integration) — v1.35.95

Every tool in the pipeline—FFmpeg, mkvmerge, VLC—is now fully decoupled from the core business logic and consumes its own specific, globally linked configuration profile.

## Key Enhancements

- **Tool-Specific Flags:** Engine flags (e.g., `-loglevel error`, `-hide_banner`) are now managed in `GLOBAL_CONFIG["transcoding_profiles"]`. This enables global adjustment of tool behavior (such as adding a mapping argument to all mkvmerge remuxing tasks) without modifying streaming logic in `main.py`.
- **Linked Pipeline Configs:**
    - **Pipe-Kit (mkvmerge + FFmpeg):** Orchestration flags are now pulled from `lossless_remux` and `perf_settings` registries.
    - **MSE Engine (FFmpeg Transcode):** Pulls from `audio_transcode` and `video_transcode` profiles.
    - **HLS Engine (VLC):** Consumes the `vlc_hls_settings` block.
- **Global Testability:** All tools are globally linked through `config_master.py`, allowing easy swapping of presets or buffer sizes for automated tests by simply editing the centralized registry.

## ✅ Verification in main.py

Streaming functions such as `ffmpeg_stream` and `play_video_remux` now strictly query the config for execution parameters. For example:

```python
lossless_flags = lossless_cfg.get("flags", [...])
stream_buf = perf_cfg.get("streaming_buffer_size", ...)
```

This modular architecture is the foundation for robust testing, the "0 item" fix, and live stats hydration. The system is now robustly decoupled and ready for deployment.
# Walkthrough - Mission Recovery & SSOT Consolidation (v1.35.94)

We have successfully stabilized the Media Viewer architecture by centralizing all hardcoded logic into a Single Source of Truth (SSOT) and resolving the critical '0 item' library bug.

## 🛠️ Key Improvements

### 1. Architectural SSOT Unification
- Expanded `src/core/config_master.py` to manage all performance, transcoding, and player routing parameters.
    - **Transcoding Profiles:** FFmpeg and mkvmerge now consume global profiles for audio, video, and lossless remuxing.
    - **Performance Buffers:** Streaming and pipe-kit buffer sizes are now managed via `perf_settings`.
    - **Player Routing:** Standardized file extensions, media prefixes, and hardware encoder priorities.

### 2. '0 Item' Library Fix
- The library regression was caused by a mismatch in category naming between the backend and legacy filtering logic.
    - Synchronized category names: `images` → `pictures`, `abbild` → `disk_images`.
    - Added `unbekannt` (Unknown) as a canonical category to ensure unclassified media is correctly indexed.
    - Updated `_apply_library_filters` in `main.py` to consume these new canonical names.

### 3. Hydrated Stats Overlay
- The Playback Diagnostic Hub now displays real-time metrics instead of mocked values.
    - **Session Tracking:** Implemented a global session tracker (`GLOBAL_ACTIVE_STREAMS`) in `main.py`.
    - **Live Metrics:** Codec, engine, bitrate, and ultra-low latency RTT stats are now pushed directly from the active streaming pipelines.

## 🔬 Validation Results

### Automated Verification
- **Config Integration:** Verified that `main.py` correctly reads from `GLOBAL_CONFIG`.
- **Filtering Sync:** Confirmed that `allowed_internal_cats` matches the new indexed categories.

### Manual Verification Required
**IMPORTANT**

To fully verify the fix, please perform the following actions in the UI:

1. Open the Diagnostic Hub.
2. Trigger a Direct Scan or Atomic Sync.
3. Verify that the library now displays your media files correctly.
4. Start a video and check the Stats Overlay (Alt+S) for live metrics.

## 📂 Modified Files
- `config_master.py`: Expanded registries.
- `models.py`: Synced category maps.
- `main.py`: Refactored core business logic and hydrated stats.

Architectural integrity restored. The system is now primed for high-performance, config-driven operation.
