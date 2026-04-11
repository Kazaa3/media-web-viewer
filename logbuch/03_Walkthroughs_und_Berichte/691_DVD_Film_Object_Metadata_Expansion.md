# DVD & Film Object Expansion: Rich Metadata & Reporting (März 2026)

## 🚀 Overview
This entry documents the expansion of the application's ability to handle complex "DVD Objects" and "Film Objects" with rich metadata extraction and detailed reporting in the Video Streaming tab.

## 🛠️ Implementation Steps
- **Parsers**
  - *filename_parser.py*: Enhanced regex and logic to extract year (19xx/20xx) from filenames and store both year and title in tags.
  - *isoparser_parser.py*: Added support for .bin and .img extensions, extraction of volume_id as fallback title, and year detection in volume_id or filename.
- **Models**
  - *models.py*: Improved `detect_content_type` to identify DVD Objects (.iso, .bin, .img, VIDEO_TS) and Film Objects (folders with ISO/movie and title/year). Added content labels ("PAL DVD", "NTSC DVD", etc.) and ensured year/film_title are stored in tags. Updated `extract_artwork` to search for poster/cover images in parent folders.
- **Backend**
  - *main.py*: Implemented `@eel.expose def get_multimedia_analysis()` to scan the DB for DVD/Film objects, check MP4s for Chrome-native codecs, and return structured data for the reporting UI.
- **Frontend**
  - *app.html*: Updated `reporting-video-streaming-view` to render a table of DVD/Film Objects with metadata and Chrome Native support flags for MP4 files.

## ✅ Verification Plan
- **Automated**: Created `/tmp/verify_dvd_film_objects.py` to mock filename parsing, ISO/BIN metadata extraction, and DVD folder classification.
- **Manual**: Populated the library with test DVD folders and ISOs. Verified the Video Streaming tab in Reporting for accurate object details and Chrome Native status.

## 📈 Result
- The application now robustly identifies and reports on DVD and Film Objects, extracting years, titles, and artwork, and providing detailed analysis in the reporting UI. Chrome Native support for MP4s is clearly indicated.

---

This logbuch entry serves as the authoritative record for the DVD/Film Object metadata and reporting expansion.
