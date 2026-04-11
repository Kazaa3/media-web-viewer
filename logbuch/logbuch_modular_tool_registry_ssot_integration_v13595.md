# Logbuch: Modular Tool Registry & SSOT Integration (v1.35.95)

## Overview

The Media Viewer architecture has reached a new milestone with the full integration of a modular tool registry, driven by the Single Source of Truth (SSOT). All core tools—FFmpeg, mkvmerge, and VLC—are now decoupled from business logic and consume globally linked configuration profiles.

## Key Achievements

- **Tool-Specific Flags:** All engine flags (e.g., `-loglevel error`, `-hide_banner`) are now managed in `GLOBAL_CONFIG["transcoding_profiles"]`. This enables global adjustments for tool behavior without modifying streaming logic in `main.py`.
- **Linked Pipeline Configs:**
    - **Pipe-Kit (mkvmerge + FFmpeg):** Orchestration flags are pulled from `lossless_remux` and `perf_settings`.
    - **MSE Engine (FFmpeg Transcode):** Uses `audio_transcode` and `video_transcode` profiles.
    - **HLS Engine (VLC):** Consumes the `vlc_hls_settings` block.
- **Global Testability:** All tools are globally linked through `config_master.py`, allowing easy swapping of presets or buffer sizes for automated tests by editing the centralized registry.

## Verification

- Streaming functions (`ffmpeg_stream`, `play_video_remux`) now strictly query the config for execution parameters, e.g.:

    lossless_flags = lossless_cfg.get("flags", [...])
    stream_buf = perf_cfg.get("streaming_buffer_size", ...)

- The modular architecture is the foundation for robust testing, the "0 item" fix, and live stats hydration.

## Status

- The system is robustly decoupled, test-ready, and fully config-driven.
- All core logic now consumes `GLOBAL_CONFIG`.
- Ready for deployment and further automated testing.
