# Plan – Video Player Overhaul & MP4 Playback Fix

**Datum:** 17. März 2026

## Ziel
Systematische Behebung des MP4-Black-Screen-Problems, Integration eines flexiblen Video-Players mit mehreren Modi und kontextabhängige Menüs.

---

## Proposed Changes

### [Frontend] app.html
- **MP4 Playback Fix:**
  - `startEmbeddedVideo` so anpassen, dass Video.js korrekt initialisiert und sichtbar ist.
  - Kein direktes `style.display = 'block'` auf dem Video-Element bei Video.js; stattdessen Sichtbarkeit des Video.js-Containers steuern.
- **Global Playback:**
  - `playMediaObject` in allen relevanten Item-Tab-Views korrekt verdrahten und in Library (Coverflow/Grid/Details) sowie File (Browser) testen.
- **Dynamic Context Menu:**
  - `showContextMenu` prüft Dateiendung und generiert Menü dynamisch (z.B. ISO → "Open with VLC ISO", MKV → "MediaMTX HLS").
- **Systematic Player Integration:**
  - `orchestrateVideoPlaybackMode` und `playVideo` refaktorieren für:
    - chrome_native (Direct MP4)
    - videojs_hls (HLS via MediaMTX)
    - ffmpeg_fragmp4 (Transmuxed stream)
    - vlc_embedded (VLC im Browser)
    - pyplayer_native (Standalone Player)

### [Backend] main.py & app_bottle.py
- **Transcoding & Streaming:**
  - `stream_video` (FragMP4) auf Range-Requests prüfen und ggf. für Seeking robust machen.
  - `serve_media` in `app_bottle.py` stellt korrekten Content-Type für alle Extensions sicher.
- **Eel API:**
  - Methoden für neue Player-Modi ergänzen/aktualisieren.

---

## Verification Plan

### Automated Tests
- **Selenium Tests:**
  - `tests/e2e/selenium/test_video_modes.py`: MP4-Playback (video.currentTime > 0), HLS-Modus, Kontextmenü für .mp4/.iso.
- **Unit Tests:**
  - `tests/unit/test_categories.py` ggf. aktualisieren.
  - `tests/unit/test_media_serving.py`: Bottle-Requests mocken, MIME-Typen prüfen.

### Manual Verification
- Mit echten Dateien testen: clip.mp4, .mkv, .iso.
- "Öffnen mit"-Funktionalität im Player-Tab prüfen.

---

**Kommentar:**
Alle geplanten Änderungen und Tests sind im walkthrough.md dokumentiert. (Ctrl+Alt+M)
