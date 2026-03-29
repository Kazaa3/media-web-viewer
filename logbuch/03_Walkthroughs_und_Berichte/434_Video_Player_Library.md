<!-- Category: Feature -->
<!-- Status: ACTIVE -->
<!-- Title_DE: Video Player & Bibliothek -->
<!-- Title_EN: Video Player & Library -->
<!-- Summary_DE: HTML5-basierter Video Player mit Bibliotheks-Integration für MP4, MKV, WebM und erweiterte Codec-Unterstützung -->
<!-- Summary_EN: HTML5-based video player with library integration for MP4, MKV, WebM and extended codec support -->

# Video Player & Bibliothek

**Version:** 1.3.1  
**Datum:** 8. März 2026  
**Status:** 🎬 ACTIVE

## Übersicht

Vollständig integrierter HTML5 Video Player mit nahtloser Bibliotheks-Anbindung. Unterstützt gängige Video-Formate (MP4, WebM) sowie erweiterte Container-Formate (MKV) für professionelles Media-Management.

## Features

### 🎥 Video Player
- **Native HTML5 <video> Element:** Hardware-beschleunigte Wiedergabe im Browser
- **Format-Unterstützung:**
  - ✅ MP4 (H.264/AAC) - Vollständig unterstützt
  - ✅ WebM (VP8/VP9/Opus) - Vollständig unterstützt
  - ⚠️ MKV (Matroska) - Abhängig von Browser-Codecs
- **Player-Steuerung:** Play/Pause, Seek, Volume, Fullscreen
- **Tastenkombinationen:** Space (Play/Pause), Arrow Keys (Seek), F (Fullscreen)

### 📚 Bibliotheks-Integration
- **Video-Erkennung:** Automatische Indexierung von Video-Dateien im Media-Ordner
- **Metadaten-Extraktion:** 
  - FFmpeg-Parser für technische Details (Resolution, Bitrate, Codec)
  - Container-Parser für MKV/MP4 Strukturanalyse
  - Mutagen/pymediainfo für erweiterte Metadaten
- **Thumbnail-Generierung:** Automatische Vorschaubilder aus erstem Frame
- **Filter & Suche:** Filterung nach Format, Auflösung, Codec

### 🎨 UI/UX
- **Responsive Design:** Fluid Player-Layout mit automatischer Skalierung
- **Sidebar-Info:** Technische Details (Codec, Auflösung, Bitrate, FPS)
- **Playlist-Support:** Sequenzielle Wiedergabe aus Bibliothek
- **Fortschritts-Speicherung:** Resume-Funktion für unterbrochene Wiedergabe

## Technische Implementierung

### Unterstützte Formate

| Format | Container | Video Codec | Audio Codec | Support |
|--------|-----------|-------------|-------------|---------|
| MP4 | MPEG-4 | H.264, H.265 | AAC, MP3 | ✅ Native |
| WebM | WebM | VP8, VP9, AV1 | Opus, Vorbis | ✅ Native |
| MKV | Matroska | H.264, VP9 | AAC, Opus | ⚠️ Limited |
| AVI | AVI | MPEG-4, Xvid | MP3, AC3 | ❌ No Support |

**Hinweis zu MKV:** Matroska-Container werden vom Browser nicht nativ unterstützt. 
- **Workaround 1:** Codec-Prüfung via `canPlayType()` vor Wiedergabe
- **Workaround 2:** Externe VLC-Integration (siehe [43_VLC_Integration.md](43_VLC_Integration.md))
- **Workaround 3:** Server-side Transcoding (geplant)

### Parser-System

**Video-Metadaten werden über 3 Parser extrahiert:**

1. **FFmpeg Parser** (`parsers/ffmpeg_parser.py`)
   - Technische Analyse: Resolution, Bitrate, Codec-Names
   - Stream-Erkennung: Video/Audio-Tracks, Untertitel
   - Container-Validierung

2. **Container Parser** (`parsers/container_parser.py`)
   - MKV-Struktur: EBML Header, Segment Info, Cluster
   - MP4-Struktur: ftyp, moov, mdat Atoms
   - Codec-Extraktion aus Container-Metadaten

3. **Mutagen/pymediainfo Parser** (`parsers/mutagen_parser.py`, `parsers/pymediainfo_parser.py`)
   - Erweiterte Tags: Titel, Autor, Beschreibung
   - Embedded Cover Art
   - Chapter-Informationen

### Frontend (HTML5 Video)

**Video Player Element:**
```html
<video id="video-player" controls>
  <source id="video-source" src="" type="">
  Your browser does not support HTML5 video.
</video>
```

**JavaScript Steuerung:**
```javascript
function playVideo(mediaItem) {
    const videoPlayer = document.getElementById('video-player');
    const videoSource = document.getElementById('video-source');
    
    // Set source and type
    videoSource.src = `/media/${mediaItem.filename}`;
    videoSource.type = mediaItem.mime_type;
    
    // Load and play
    videoPlayer.load();
    videoPlayer.play();
}
```

**MIME-Type Mapping:**
```javascript
const VIDEO_MIMETYPES = {
    'mp4': 'video/mp4',
    'webm': 'video/webm',
    'mkv': 'video/x-matroska',  // Limited browser support
    'avi': 'video/x-msvideo'     // No browser support
};
```

### Backend (Python/Eel)

**API-Funktionen:**
```python
@eel.expose
def get_video_metadata(filename: str) -> dict:
    """Extract video metadata using ffmpeg/mediainfo"""
    # Returns: {resolution, bitrate, codec, duration, fps}

@eel.expose
def get_video_thumbnail(filename: str) -> str:
    """Generate thumbnail from video file"""
    # Returns: base64-encoded image

@eel.expose
def check_video_codec_support(filename: str) -> dict:
    """Check browser compatibility for video codecs"""
    # Returns: {playable, codec, browser_support}
```

## Herausforderungen & Lösungen

### Problem 1: MKV-Browser-Support
**Issue:** Chromium unterstützt Matroska-Container nur eingeschränkt.

**Lösung:**
- Runtime-Codec-Check via `HTMLMediaElement.canPlayType()`
- Fallback auf VLC-Integration für nicht unterstützte Codecs
- User-Hinweis bei inkompatiblen Dateien

### Problem 2: Große Video-Dateien
**Issue:** 4K-Videos > 10 GB können den Browser überlasten.

**Lösung:**
- HTTP Range Requests für chunked streaming
- Progressive Download statt kompletter Pufferung
- Proxy-Endpoint mit Chunk-Forwarding

### Problem 3: Codec-Vielfalt
**Issue:** Nutzer haben Videos in verschiedenen Codecs (H.264, H.265, VP9, AV1)

**Lösung:**
- Multi-Parser-Ansatz für robuste Metadaten-Extraktion
- Format-Anzeige in Bibliothek (mit Kompatibilitäts-Hinweisen)
- Transcoding-Preview für nicht-native Formate (geplant)

## Testing

### Browser-Kompatibilität
✅ **Chromium 90+:** MP4 (H.264/AAC), WebM (VP8/VP9/Opus)  
✅ **Firefox 88+:** MP4 (H.264/AAC), WebM (VP8/VP9/Opus)  
⚠️ **Safari:** MP4 (H.264/AAC) only, kein WebM-Support  

### Test-Dateien
```bash
media/
├── sample_h264.mp4      # ✅ Tested
├── sample_vp9.webm      # ✅ Tested
├── sample_mkv_h264.mkv  # ⚠️ Limited (depends on browser)
└── sample_avi_xvid.avi  # ❌ Not supported
```

### Test-Suite
```bash
# Run video parser tests
python tests/test_video_parsers.py

# Test video player metadata extraction
python tests/check_video_metadata.py
```

## Verwandte Einträge

- [28_Premium_Sidebar_Info.md](28_Premium_Sidebar_Info.md) - Technische Details-Anzeige
- [43_VLC_Integration.md](43_VLC_Integration.md) - VLC-Fallback für MKV-Dateien
- [01_Features.md](01_Features.md) - Ursprüngliche Video-Support-Planung

## Nächste Schritte

1. ⏳ **Server-side Transcoding:** FFmpeg-basiertes On-the-fly Transcoding für inkompatible Formate
2. ⏳ **Untertitel-Support:** WebVTT-Integration für eingebettete Subtitles
3. ⏳ **Playlist-Management:** Dedicated Video-Playlisten mit Shuffle/Repeat
4. ⏳ **Chromecast-Support:** Cast-API für TV-Wiedergabe

---

<!-- lang-split -->

# Video Player & Library

**Version:** 1.3.1  
**Date:** March 8, 2026  
**Status:** 🎬 ACTIVE

## Overview

Fully integrated HTML5 video player with seamless library integration. Supports common video formats (MP4, WebM) as well as extended container formats (MKV) for professional media management.

## Features

### 🎥 Video Player
- **Native HTML5 <video> Element:** Hardware-accelerated playback in browser
- **Format Support:**
  - ✅ MP4 (H.264/AAC) - Fully supported
  - ✅ WebM (VP8/VP9/Opus) - Fully supported
  - ⚠️ MKV (Matroska) - Depends on browser codecs
- **Player Controls:** Play/Pause, Seek, Volume, Fullscreen
- **Keyboard Shortcuts:** Space (Play/Pause), Arrow Keys (Seek), F (Fullscreen)

### 📚 Library Integration
- **Video Detection:** Automatic indexing of video files in media folder
- **Metadata Extraction:** 
  - FFmpeg parser for technical details (Resolution, Bitrate, Codec)
  - Container parser for MKV/MP4 structure analysis
  - Mutagen/pymediainfo for extended metadata
- **Thumbnail Generation:** Automatic preview images from first frame
- **Filter & Search:** Filtering by format, resolution, codec

### 🎨 UI/UX
- **Responsive Design:** Fluid player layout with automatic scaling
- **Sidebar Info:** Technical details (Codec, Resolution, Bitrate, FPS)
- **Playlist Support:** Sequential playback from library
- **Progress Saving:** Resume function for interrupted playback

## Technical Implementation

### Supported Formats

| Format | Container | Video Codec | Audio Codec | Support |
|--------|-----------|-------------|-------------|---------|
| MP4 | MPEG-4 | H.264, H.265 | AAC, MP3 | ✅ Native |
| WebM | WebM | VP8, VP9, AV1 | Opus, Vorbis | ✅ Native |
| MKV | Matroska | H.264, VP9 | AAC, Opus | ⚠️ Limited |
| AVI | AVI | MPEG-4, Xvid | MP3, AC3 | ❌ No Support |

**Note on MKV:** Matroska containers are not natively supported by the browser.
- **Workaround 1:** Codec check via `canPlayType()` before playback
- **Workaround 2:** External VLC integration (see [43_VLC_Integration.md](43_VLC_Integration.md))
- **Workaround 3:** Server-side transcoding (planned)

### Parser System

**Video metadata is extracted via 3 parsers:**

1. **FFmpeg Parser** (`parsers/ffmpeg_parser.py`)
   - Technical analysis: Resolution, Bitrate, Codec names
   - Stream detection: Video/Audio tracks, Subtitles
   - Container validation

2. **Container Parser** (`parsers/container_parser.py`)
   - MKV structure: EBML header, Segment info, Cluster
   - MP4 structure: ftyp, moov, mdat atoms
   - Codec extraction from container metadata

3. **Mutagen/pymediainfo Parser** (`parsers/mutagen_parser.py`, `parsers/pymediainfo_parser.py`)
   - Extended tags: Title, Author, Description
   - Embedded cover art
   - Chapter information

### Frontend (HTML5 Video)

**Video Player Element:**
```html
<video id="video-player" controls>
  <source id="video-source" src="" type="">
  Your browser does not support HTML5 video.
</video>
```

**JavaScript Control:**
```javascript
function playVideo(mediaItem) {
    const videoPlayer = document.getElementById('video-player');
    const videoSource = document.getElementById('video-source');
    
    // Set source and type
    videoSource.src = `/media/${mediaItem.filename}`;
    videoSource.type = mediaItem.mime_type;
    
    // Load and play
    videoPlayer.load();
    videoPlayer.play();
}
```

**MIME-Type Mapping:**
```javascript
const VIDEO_MIMETYPES = {
    'mp4': 'video/mp4',
    'webm': 'video/webm',
    'mkv': 'video/x-matroska',  // Limited browser support
    'avi': 'video/x-msvideo'     // No browser support
};
```

### Backend (Python/Eel)

**API Functions:**
```python
@eel.expose
def get_video_metadata(filename: str) -> dict:
    """Extract video metadata using ffmpeg/mediainfo"""
    # Returns: {resolution, bitrate, codec, duration, fps}

@eel.expose
def get_video_thumbnail(filename: str) -> str:
    """Generate thumbnail from video file"""
    # Returns: base64-encoded image

@eel.expose
def check_video_codec_support(filename: str) -> dict:
    """Check browser compatibility for video codecs"""
    # Returns: {playable, codec, browser_support}
```

## Challenges & Solutions

### Problem 1: MKV Browser Support
**Issue:** Chromium supports Matroska containers only partially.

**Solution:**
- Runtime codec check via `HTMLMediaElement.canPlayType()`
- Fallback to VLC integration for unsupported codecs
- User notification for incompatible files

### Problem 2: Large Video Files
**Issue:** 4K videos > 10 GB can overwhelm the browser.

**Solution:**
- HTTP Range Requests for chunked streaming
- Progressive download instead of complete buffering
- Proxy endpoint with chunk forwarding

### Problem 3: Codec Diversity
**Issue:** Users have videos in various codecs (H.264, H.265, VP9, AV1)

**Solution:**
- Multi-parser approach for robust metadata extraction
- Format display in library (with compatibility notes)
- Transcoding preview for non-native formats (planned)

## Testing

### Browser Compatibility
✅ **Chromium 90+:** MP4 (H.264/AAC), WebM (VP8/VP9/Opus)  
✅ **Firefox 88+:** MP4 (H.264/AAC), WebM (VP8/VP9/Opus)  
⚠️ **Safari:** MP4 (H.264/AAC) only, no WebM support  

### Test Files
```bash
media/
├── sample_h264.mp4      # ✅ Tested
├── sample_vp9.webm      # ✅ Tested
├── sample_mkv_h264.mkv  # ⚠️ Limited (depends on browser)
└── sample_avi_xvid.avi  # ❌ Not supported
```

### Test Suite
```bash
# Run video parser tests
python tests/test_video_parsers.py

# Test video player metadata extraction
python tests/check_video_metadata.py
```

## Related Entries

- [28_Premium_Sidebar_Info.md](28_Premium_Sidebar_Info.md) - Technical details display
- [43_VLC_Integration.md](43_VLC_Integration.md) - VLC fallback for MKV files
- [01_Features.md](01_Features.md) - Original video support planning

## Next Steps

1. ⏳ **Server-side Transcoding:** FFmpeg-based on-the-fly transcoding for incompatible formats
2. ⏳ **Subtitle Support:** WebVTT integration for embedded subtitles
3. ⏳ **Playlist Management:** Dedicated video playlists with shuffle/repeat
4. ⏳ **Chromecast Support:** Cast API for TV playback
