# Reporting System - Components Menu

Select a reporting component to view detailed status and performance metrics.

---

## 📺 Video Streaming Reporting
- **Performance**: Throughput (Mbps), FPS, Framedrops.
- **Latency**: End-to-end delay (ms), Buffer status.
- **Transcoding**: Real-time FFmpeg logs, codec efficiency.
- **Status**: Live / Ready / Error / Re-buffering.

## 🎵 Audio Streaming Reporting
- **Quality**: Bitrate (kbps), Sample Rate (kHz), Dynamic Range.
- **Playback**: Synchronization (AV-Sync), Buffer status.
- **Processing**: Transcoding status for non-native formats (FLAC/ALAC to Opus).

## 🌐 General Streaming Reporting
- **Protocols**: HLS Segment health, WebRTC ICE connection status.
- **Infrastructure**: MediaMTX path availability, CPU/RAM usage of streamers.
- **Connectivity**: Client count, bandwidth utilization.

## 🧠 Metadata Parser Reporting
- **Timing metrics**: Seconds per file (Filename vs. Mutagen vs. FFmpeg).
- **Coverage**: Percentage of fields correctly identified.
- **Failure Rates**: Logs of unrecognized containers or corrupted metadata.
- **Queue Status**: Multi-parser pipeline progress in full/ultimate mode.

---

[Back to Documentation Hub](../DOCUMENTATION.md) | [Back to Architecture Overlook](../ARCHITEKTUR.md)
