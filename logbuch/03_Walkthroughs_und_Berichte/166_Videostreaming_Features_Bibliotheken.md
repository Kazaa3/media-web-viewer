<!-- Category: streaming -->
<!-- Title_DE: Videostreaming-Features und Bibliotheken für MediaWebViewer -->
<!-- Title_EN: Video Streaming Features and Libraries for MediaWebViewer -->
<!-- Summary_DE: Erweiterung der App um robustes Videostreaming, Transcoding, Subtitles, Playlists und moderne Player-Bibliotheken. -->
<!-- Summary_EN: Extending the app with robust video streaming, transcoding, subtitles, playlists, and modern player libraries. -->
<!-- Status: in-progress -->
<!-- Date: 2026-03-10 -->

# Videostreaming-Features und Bibliotheken für MediaWebViewer

## Kern-Features
- **Transcoding/Streaming:** FFmpeg für On-the-Fly-Konvertierung von MKV/ISO zu HTML5-kompatiblen Formaten (HLS/DASH).
- **Subtitles/Chapters:** Automatische SRT-Extraktion und WebVTT-Rendering.
- **Playlists/Queue:** JSON-basierte Playlists mit Shuffle/Repeat.

## Empfohlene Libraries
| Library         | Zweck                                 | Vorteil für MediaWebViewer                |
|-----------------|---------------------------------------|-------------------------------------------|
| python-vlc      | Vollständiger Player-Backend (MKV/ISO/Audio/Blu-ray) | Embedde VLC in Eel-HTML5-Player; unterstützt alles ohne Transcode |
| GStreamer (gi)  | Streaming/Pipelines (RTSP/WebRTC)     | Für Synology-NAS-Streaming; kombiniere mit ffprobe |
| shaka-player (JS)| Adaptive Streaming (HLS/DASH)         | Integriere in Vue/Eel für Browser-Playback von großen Dateien |
| SQLAlchemy/SQLite| Medien-Datenbank                     | Indexiere ffprobe-Daten (Tracks, Posters); suche/filtern |

## Code-Beispiel: FFmpeg-Streaming-Endpoint
```python
import bottle
from pathlib import Path

@bottle.route('/stream/<filename:path>')
def stream(filename):
    path = Path(f"./media/{filename}")
    if not path.exists(): return bottle.abort(404)
    
    cmd = [
        "ffmpeg", "-i", str(path),
        "-c:v", "libx264", "-preset", "fast",
        "-f", "hls", "-hls_time", "10",
        "-hls_list_size", "6", "-y", f"{filename}.m3u8"
    ]
    subprocess.run(cmd)  # Oder async mit asyncio
    
    return bottle.static_file(f"{filename}.m3u8", root="./")
```

## Integration in Eel/JS
- Verwende video.js oder shaka-player für HLS-Playback im Browser.
- Subtitles als WebVTT/SRT einbinden.

## Praxis-Empfehlung
- Für maximale Kompatibilität: python-vlc als Backend, FFmpeg für Transcoding, shaka-player für Browser.
- Medien-Datenbank mit SQLAlchemy/SQLite für Suche und Index.

