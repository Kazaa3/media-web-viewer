# Streaming Capability Matrix & Reporting Expansion (März 2026)

## 📊 Streaming Engine & Format Matrix
A comprehensive matrix has been added to the reporting dashboard, providing a technical baseline for all playback and streaming capabilities.

| Engine        | Modes / Protocols         | Formats                | Key Features                                 |
|--------------|---------------------------|------------------------|----------------------------------------------|
| Chrome Native| Integrated, Direct        | MP4, WebM, OGG         | HW Accel, Low Latency, Browser Native        |
| VLC (Native) | External, Integrated      | ISO, BIN, MKV, AVI, DVD| DVD Menus, Subtitles, Universal support      |
| MediaMTX     | HLS, WebRTC, RTSP         | MP4, MKV (FFmpeg)      | Network Streaming, Zero-client install       |
| PyPlayer     | PyVidPlayer2              | MP4, MKV, AVI          | Python-embedded, Custom Overlays             |

- **Engine Comparison:** Side-by-side view of Chrome Native, VLC, MediaMTX, and PyPlayer.
- **Mode & Protocol Visibility:** Integrated vs External, HLS/WebRTC support.
- **Format Support Matrix:** Which engines handle ISO, BIN, MKV, MP4, etc.
- **Feature Highlights:** HW Acceleration, DVD Menus, Zero-client install, etc.

## 👁️ Visual Verification
- **Player Controls:** Cohesive, scalable SVGs in the main control bar.
- **Navigation Sidebar:** Unified SVG design for navigation and file browser utilities.

## 🚀 MediaMTX Dynamic Push Engine
- **Automatic FFmpeg Push:** Backend spawns managed FFmpeg process for MTX modes.
- **Remuxing & Transcoding:** Zero-copy for MKV/M4V, H.264 for DVDs.
- **Concurrent Streams:** Unique path slugs for multiple streams.
- **Low Latency:** Optimized for WebRTC (WHEP) and HLS.

## 🧪 Verification & Testing
- **Integration Tests:** All core video tests PASSED.
- **Mock Verification:** `verify_mtx_streaming.py` confirmed correct FFmpeg command generation for all formats.

## ✅ Status
- COMPLETED — Video Player Overhaul, Reporting Expansion & MediaMTX Integration finalized.

---

Combined with the Multimedia Library Analysis, the dashboard now provides a complete overview of your library's health and the technical baseline for all streaming operations.

See the updated walkthrough.md for the full feature list and verification results!
