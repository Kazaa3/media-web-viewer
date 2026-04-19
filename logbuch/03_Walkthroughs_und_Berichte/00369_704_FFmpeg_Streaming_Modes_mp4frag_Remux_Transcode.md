# FFmpeg Streaming Modes: mp4frag, Remux, Transcode (März 2026)

## 🛠️ Overview of FFmpeg Streaming Modes
This entry documents the three primary FFmpeg-based streaming modes now supported for advanced playback and transcoding of MKV, ISO, and other formats.

## 1. mp4frag (Fragmented MP4 for HLS/Browser)
- **Purpose:** Enables live, seekable streaming of MP4 content using fragmented MP4 (fMP4) segments.
- **Use Case:** Best for browser-based playback (HLS, MediaSource), allowing instant seeking and adaptive streaming.
- **Supported Inputs:** MP4, MKV, ISO (via remux/transcode).
- **Features:**
  - Live HLS/fMP4 segment generation
  - Browser-native seeking
  - Low latency

## 2. Remux (Container Shift, No Transcode)
- **Purpose:** Fast, lossless conversion of containers (e.g., MKV→MP4, ISO→MKV) without re-encoding streams.
- **Use Case:** When input codecs are already browser-compatible (H.264, AAC, etc.).
- **Supported Inputs:** MKV, ISO, MP4, AVI, etc.
- **Features:**
  - No quality loss
  - Sub-track preservation
  - Fast processing

## 3. Transcode (Full Codec Conversion)
- **Purpose:** Converts any input (MKV, ISO, DVD, etc.) to browser-friendly codecs (H.264/AAC) for maximum compatibility.
- **Use Case:** Required for legacy or incompatible formats (e.g., MPEG-2, AC3, DTS, DVD ISOs).
- **Supported Inputs:** MKV, ISO, DVD, AVI, etc.
- **Features:**
  - Full video/audio re-encoding
  - Customizable bitrate, resolution, and audio options
  - Ensures playback on all devices

## 🔄 Mode Selection Logic
- **mp4frag:** Used when input is already H.264/AAC and browser supports fMP4.
- **Remux:** Used when only container change is needed (no codec change).
- **Transcode:** Used for all other cases (legacy codecs, DVD images, etc.).

## ✅ Verification
- All three modes tested with MP4, MKV, and ISO sources.
- Verified browser playback, seeking, and compatibility for each mode.

---

**Result:**
The application now supports mp4frag, remux, and full transcode streaming modes via FFmpeg, providing robust, adaptive playback for all major media formats.
