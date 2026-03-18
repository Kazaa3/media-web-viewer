# Video Streaming & DVD/Film Reporting Expansion (März 2026)

## 📝 Overview
This update expands the application's reporting capabilities to provide a comprehensive overview of all supported Players, Streaming Modes, and File Format support, while maintaining rich metadata for "DVD Objects" and "Film Objects".

## 🛠️ Implementation Details

### [Parsers]
- **filename_parser.py**: Added/verified regex to extract years (19xx/20xx) from filenames. Extracted title excluding the year and stored both in tags.
- **isoparser_parser.py**: Added support for .bin and .img extensions. Extracted volume_id as fallback title. Searched for year patterns in volume_id or filename and stored in tags.

### [Models]
- **models.py**: Enhanced `detect_content_type` to identify:
  - DVD Object: .iso, .bin, .img, or VIDEO_TS folder.
  - Film Object: Folder containing an ISO/movie with title/year metadata.
  - Content Labels: "PAL DVD", "NTSC DVD", "Data DVD", "Mixed Media".
- Ensured year and film_title are stored in tags.
- Updated `extract_artwork` to look for local poster.jpg, cover.png, etc., in parent folders.

### [Backend]
- **main.py**:
  - Added `@eel.expose def get_streaming_capability_matrix()`: Returns a static/dynamic map of supported Engines (VLC, Chrome, MTX, PyPlayer) and their supported Protocols/Formats.
  - Refined `open_video_smart` to include .bin and .img in disc image detection logic and prioritize VLC for items with category='Film' or 'Abbild'.

### [Frontend]
- **app.html**:
  - Shows "Chrome Native" support flags for MP4 files.
  - Added a Streaming Capability Matrix table showing Players, Protocols (HLS, WebRTC, Direct), and File Format support (ISO, MKV, MP4).
  - Added a Film filter button to the library's coverflow view.

## ✅ Verification Plan
- **Automated:** Created `/tmp/verify_dvd_film_objects.py` to mock filename parsing with years, ISO/BIN metadata extraction, and DVD folder classification.
- **Manual:** Populated the library with a test DVD folder and an ISO. Verified the "Video Streaming" tab in Reporting for accurate object details and Chrome Native status.

---

**Result:**
The reporting dashboard now provides a complete technical baseline for all streaming operations, with rich metadata and format support for DVD and Film objects.
