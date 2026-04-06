# 🛡️ Mission Recovery & SSOT Unification (v1.35.95)

The architectural restoration and SSOT unification for Media Viewer v1.35.95 is complete. The system is now fully config-driven, with granular profiles for all streaming and transcoding operations.

## Key Improvements

- **Granular Transcoding Profiles:**
    - Transcoding settings are now split into codec-specific blocks in `config_master.py`: AAC, Opus, and FLAC.
    - The FFmpeg streaming pipeline dynamically selects the optimized profile (e.g., `libopus` for `.opus` files), defaulting to AAC for browser compatibility.
- **Content-Aware HLS Logic:**
    - The VLC HLS engine now distinguishes between PAL DVD (SD) and HD content.
    - Automatically applies a 2000kbps vb for PAL/DVD sources and 4500kbps for HD sources, optimizing quality-to-bandwidth ratios.
- **'0 Item' Bug Resolved:**
    - Synchronized all category mappings across `models.py`, `config_master.py`, and `main.py`.
    - Canonical categories (`pictures`, `disk_images`, `unbekannt`) are now consistently indexed and filtered, restoring full library visibility.
- **Live Stats Hydration:**
    - All mocked playback metrics replaced with a real-time session tracker (`GLOBAL_ACTIVE_STREAMS`).
    - The diagnostic overlay now displays live codec, bitrate, and ultra-low latency RTT diagnostics for active HLS and MSE sessions.
- **Decoupled Tool Configs:**
    - Every transfer path (VLC, Pipe-Kit, SSE) is now decoupled and consumes its own globally linked config block, allowing for precise adjustments and automated testing.

## ✅ Verification

- The Routing Suite and Capability Matrix now correctly reflect the new canonical registries.
- No legacy hardcoded constants remain in the core streaming or scanning logic.

Refer to the updated walkthrough for a summary of the technical implementation. The architecture is now stabilized and ready for high-performance operation.
