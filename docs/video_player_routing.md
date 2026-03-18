# Video Player Routing (open_video_smart)

This document describes the core routing logic for video playback, centered around the `open_video_smart` function.

## Overview

The `open_video_smart` function in `src/core/main.py` is the primary orchestrator for choosing the correct playback method (Direct Play, Remux, or Streaming).

## Routing Logic

### 1. Direct Play (Chrome Native)
- **Criteria**: H.264 in MP4/MOV or VP8/VP9 in WebM/MKV.
- **Action**: Returns a direct `/media/` path.
- **Mode**: `chrome_direct`.

### 2. MediaMTX (HLS/WebRTC)
- **Status**: **MOCKED**.
- **Action**: Currently returns hardcoded `localhost:8888` (HLS) and `localhost:8889` (WebRTC) URLs.
- **Note**: The actual triggering of MediaMTX paths via FFmpeg is currently commented out in the backend.

### 3. ffmpeg FragMP4 / Remux
- **Criteria**: Formats requiring on-the-fly container correction (like MKVs not suitable for direct play).
- **Action**: Routes through `/video-remux-stream/<item_id>`.
- **Mode**: `chrome_fragmp4`.

### 4. Fallback (open_video)
- Handles external players (VLC, FFplay) and legacy modes.

## Implementation Details

- **Anchor**: [`src/core/main.py:3273`](file:///home/xc/#Coding/gui_media_web_viewer/src/core/main.py#L3273)
- **Metadata Source**: `get_video_metadata(file_path)`

## Knowledge Maintenance (KI)

- **MediaMTX Update**: Once a running MediaMTX instance is available, the commented-out `requests.post` block in `open_video_smart` must be reactivated.
- **UI Indicators**: The frontend currently lacks status/feedback for streaming modes. This is a known gap and should be addressed in the next UI iteration.
