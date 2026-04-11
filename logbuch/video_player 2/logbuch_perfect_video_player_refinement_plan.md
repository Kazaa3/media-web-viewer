# Implementation Plan: Perfect Video Player Refinement (March 2026)

## Goal
Refine the media player for better MKV seeking, track switching, and universal GPU monitoring (Intel Arc/AMD/NVIDIA).

## Proposed Changes
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
