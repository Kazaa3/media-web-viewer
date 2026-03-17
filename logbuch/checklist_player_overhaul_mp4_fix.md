# Task Checklist: Video Player Overhaul & MP4 Fix (März 2026)

## 1. Research & Debugging
- [ ] Investigate current `playMedia` and `startEmbeddedVideo` logic
- [ ] Identify cause of MP4 black screen (audio works, video doesn't)
- [ ] Research Video.js integration and CSS constraints
- [ ] Map out file-type specific context menu requirements

## 2. Implementation: Player Overhaul
- [ ] Fix MP4 Playback: resolve black screen in `app.html` via `trigger('resize')`
- [ ] Ensure Video.js container correctly receives visibility
- [ ] Global Playback Integration: enable playback from Library, Item, and File views
- [ ] Dynamic Context Menu: implement file-type dependent context menu (DVD options for ISOs, etc.)
- [ ] VLC/cvlc CLI Refinement: prioritize `cvlc` over `vlc`, correct ISO handling (direct path, no protocols)
- [ ] Robust Path Resolution: implement `resolve_media_path` with decoding and prefix stripping
- [ ] Multi-Mode Support:
    - [ ] MediaMTX (HLS/WebRTC)
    - [ ] ffmpeg FragMP4 (via `/video-stream/` route)
    - [ ] Standalone Desktop (VLC, mpv, pyvidplayer2)
- [ ] Comprehensive Testing:
    - [ ] Unit/Integration tests for ISO/DVD playback (`test_dvd_iso.py`)
    - [ ] Unit tests for path resolution (`test_path_resolution.py`)
    - [ ] Selenium tests for PiP and player UI

## 3. UI/UX Refinement
- [ ] Improve Video Player tab layout for all modes
- [ ] Ensure proper responsive behavior for the video viewport

## 4. Transcoding & Auto-Detection
- [ ] FFprobe Auto-Detect: implement `get_video_metadata` using ffprobe
- [ ] Add logic to route based on codec (H.264 → Direct, HEVC → Transcode)
- [ ] Add "Auto-Detect" option to `app.html` player settings
- [ ] Kern-Transcoding Modes:
    - [ ] ffmpeg FragMP4 (On-the-fly)
    - [ ] MediaMTX HW-Transcode integration
    - [ ] pymkv + mkvmerge Remuxing
- [ ] Advanced Optimization:
    - [ ] pyhandbrake Batch Encoding integration
    - [ ] towebm (VP9/WebM) conversion
    - [ ] ffplay testing fallback
- [ ] Fix VLC Stream Errors: debug and fix fd://0 and mjpeg demux errors

## 5. Verification & Testing
- [ ] Unit Tests: test media serving logic with mocks, test backend mode detection logic
- [ ] Selenium Tests: verify MP4 playback (non-black screen), verify multi-mode switching (HLS vs Native), test context menu sensitivity to file types
- [ ] Manual Verification: test with real MP4/MKV/ISO files from the library

---

**Datum:** 17. März 2026  
**Autor:** GitHub Copilot
