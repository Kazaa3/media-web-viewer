# Implementation Plan – Perfect Video Player Architecture Overhaul

This plan outlines the complete restructuring of the media player into a unified, high-performance architecture.

## Proposed Changes

### [Backend] Intelligence & Routing
- [NEW] `ffprobe_analyzer.py`: Deep media detection (4K/HDR/Atmos/ISO/DVD).
- [MODIFY] `mode_router.py`: Unified decision engine for 8+ primary playback modes.

### [Backend] Modular Streaming Backends (`src/core/streams/`)
- [NEW] `direct_play.py`: Logic for native browser passthrough (0% CPU).
- [NEW] `mse_stream.py`: Fragmented MP4 remuxing (0.5s latency).
- [NEW] `hls_stream.py`: Universal Apple HLS (fMP4).
- [NEW] `vlc_bridge.py`: Interactive bridge for DVD/ISO menus.

### [Frontend] Unified Player & MPV.js
- [NEW] `web/js/mpv-wasm/`: Deployment of libmpv WASM assets for browser-side ISO/DVD menu support.
- [MODIFY] `app.html`: Integrated `<video-js id="universal-player">`.
- [NEW] `web/js/universal-player.js`: Wrapper for mode negotiation and track switching.
- [NEW] `web/js/stats-overlay.js`: Live playback metrics (GPU/Bitrate/RTT).

### [System] Docker & Hardware Acceleration
- [NEW] `docker-compose.yml`: Intel Arc / NVIDIA mapping and ENV setup.
- [NEW] `Dockerfile`: Multi-stage build with optimized FFmpeg and VLC.

## Verification Plan

### Automated Tests
- `pytest tests/test_mode_router.py` (Validation of all 14+ routing combinations).
- `python3 tests/test_video_performance_benchmark.py` (FFmpeg HW-Accel validation).

### Manual Verification
- Test 4K HEVC playback (Expect HLS fMP4 + HW Accel).
- Test ISO with Menus (Expect VLC Bridge or MPV.js WASM).
- Verify 0% CPU for H.264/MP4 (Direct Play).
