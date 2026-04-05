# Audio & Series Object Implementation (März 2026)

## 🆕 Features

### Audio Objects (Albums, Soundtracks, Podcasts)
- **Folder Logic:**
  - If tags are missing, parser extracts Artist, Album, and Year from parent folder (pattern: Artist - Album (Year)).
- **Soundtrack Detection:**
  - Keywords: o.s.t, soundtrack, ost.
- **Playlist Detection:**
  - m3u/m3u8 files now recognized as Playlists.

### Series Objects (TV Shows)
- **Series Detection:**
  - Regex for SxxExx, xx_xx, 1x01 episode patterns.
  - Folder keywords: Staffel, Season, Episode, Serien, Series.
- **Season/Episode Extraction:**
  - Displays Season/Episode info in UI for Series Objects.

## 🛠️ Implementation Details

### [Models]
- **models.py:**
  - Updated `detect_content_type` for Soundtrack, Playlist, and Series detection.
  - Enhanced Audio Object detection using parent folder heuristics.
  - Refined `to_dict` and `is_chrome_native` to check both extension and codec.

### [Parsers]
- **filename_parser.py:**
  - Added regex for series/episode extraction.
  - Implemented `extract_from_folder_structure` for parent directory metadata.
- **format_utils.py:**
  - Updated `is_chrome_native` to accept (ext, codec) and check for supported codecs (h264, avc1, vp8, vp9, av1, aac, mp4a, mp3, opus, vorbis, flac).

### [Frontend]
- **app.html:**
  - Added UI filters for 🎬 Series, 🎵 Soundtrack, 📻 Podcasts, 📀 Albums.
  - Updated `renderLibrary` to show Season/Episode for Series.
  - Synced `is_chrome_native` logic in JS with backend.

## ✅ Verification Plan
- **Automated:**
  - Ran `verify_streaming_matrix.py` (no regressions).
  - Created `verify_content_types.py` to test Series/Album detection with mock paths.
- **Manual:**
  - Tested with folders like `Pink Floyd - The Dark Side of the Moon (1973)/01 Speak to Me.mp3`.
  - Tested with series files like `Breaking Bad S01E01.mkv`.

---

**Result:**
The application now robustly detects and categorizes Audio and Series Objects, with improved metadata extraction, UI filtering, and Chrome Native compatibility checks.
