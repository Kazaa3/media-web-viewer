# Streaming Capability Matrix: Full Engine & Mode Coverage (März 2026)

## 🛠️ Matrix Expansion & Corrections
This update finalizes the Streaming Capability Matrix, ensuring all engines, modes, and technical features are accurately represented.

## 🗂️ Engine & Mode Table

| Engine                | Modes                  | Formats                        | Codecs                        | Features                                 | Notes                                                        |
|-----------------------|------------------------|-------------------------------|-------------------------------|------------------------------------------|--------------------------------------------------------------|
| Chrome Native         | Integrated, Direct     | MP4, WebM, OGG                | H.264, VP8, VP9, AV1          | HW Accel, Low Latency, Browser Native    | Best for web-compatible MP4 files. Zero transcoding required. |
| MediaMTX (mmts)       | HLS, WebRTC, RTSP      | MP4, MKV (via FFmpeg)         | H.264, AAC                    | Multi-device, Zero client install, HTTP  | Ideal for streaming to multiple devices via FFmpeg remux.     |
| VLC (Universal)       | External, VLC.js       | ISO, BIN, IMG, MKV, AVI, DVD, VIDEO_TS | All (H.265, AC3, DTS, etc.)  | DVD Menus, Subtitles, Post-processing    | Universal player for all file types, disc images, legacy.     |
| mkvmerge              | Remux, Batch           | MKV (Output), All (Input)      | Container Shift                | Sub-track preservation, Fast remux, ISO→MKV | Used for converting incompatible containers.                 |
| ffmpeg-mp4frag        | Fragmented MP4 (HLS)   | MP4 (frag), All (Input)        | H.264, AAC, etc.              | Live HLS, Fragmented MP4, Browser Seek   | Enables live/seekable MP4 streaming for browsers.             |
| ffplay                | CLI Preview            | All                            | All (FFmpeg-based)            | Low latency, Raw decoding, Debug view    | Technical fallback for quick local playback.                  |
| swyh-rs (suw)         | Audio HTTP, DLNA       | WAV, FLAC, LPCM                | Lossless PCM                  | System Audio Capture, Network Audio      | Specialized for lossless audio streaming (Stream What You Hear).|
| PyPlayer (Integrated) | Direct Python          | All (FFmpeg compatible)         | All                           | Zero external dependencies, Native control| Python-based fallback/simple playback engine.                 |

## 🔍 Notable Additions
- **ffmpeg-mp4frag:** Now included for live/fragmented MP4 streaming (HLS, browser seeking).
- **All engines/modes:** Matrix now covers every supported tool, protocol, and technical feature.
- **PyPlayer:** Fully documented as an integrated fallback engine.

## ✅ Verification
- Matrix reviewed for completeness and technical accuracy.
- All engines, modes, and features now visible in the reporting dashboard.

---

**Result:**
The Streaming Capability Matrix now provides a complete, accurate technical baseline for all playback and streaming operations, supporting advanced workflows and troubleshooting.
