# Walkthrough: Video Player & Media Handling Overhaul (März 2026)

## Zusammenfassung
Das "Big Video Player Update" ist abgeschlossen. Mit dem neuen "mkvmerge PIPE KIT" wird MKV-Playback direkt im Chrome-Browser ermöglicht – ohne VLC, mit maximaler Performance und neuen Premium-Controls im UI.

---

## 🚀 mkvmerge PIPE KIT (Backend)
- **Neuer Streaming-Pipeline:**
    - `mkvmerge -o - file.mkv | ffmpeg -i pipe:0 -c copy -f mp4 -movflags frag_keyframe+empty_moov -`
    - Fragmented MP4 (FragMP4) wird direkt an Chrome gestreamt (schneller als klassisches Transcoding).
- **Routing:**
    - chrome_remux und chrome_fragmp4 nutzen jetzt diese Pipeline.
    - Auto-Detection: PIPE KIT wird für MKV genutzt, wenn mkvtoolnix verfügbar ist, sonst Fallback auf reines ffmpeg-Remuxing.

## 📺 Big Video Player Update (Frontend)
- **Playlist-Integration:**
    - Video.js springt automatisch zum nächsten Item (Shuffle/Repeat werden beachtet).
- **Advanced Controls:**
    - 🔀 Shuffle: Zufallswiedergabe umschaltbar
    - 🔁 Repeat: Off, Repeat One, Repeat All
    - ⏱️ Speed Control: 0.5x, 1x, 1.25x, 1.5x, 2x
    - ⏪/⏩ Seeking: 10s vor/zurück
    - 🖼️ Picture-in-Picture: Vollständig integriert
    - 🎚️ Equalizer: Platzhalter für DSP
- **UI-Refinement:**
    - Premium-Panel für alle Controls
    - Lokalisierte Labels und Toasts (z.B. "🚀 mkvmerge PIPE KIT (Direct FragMP4)")

## 🛠️ Verification & Stability
- Selenium E2E-Test-Isolation refixed (keine Regressionsgefahr mehr)
- chrome_remux liefert korrektes video/mp4 für Chrome
- Fallback auf ffmpeg-only, falls mkvmerge fehlt

---

**Status:** Alle Kernziele des Overhauls sind erreicht. Die Wiedergabe ist jetzt hochperformant, direkt im Browser und mit modernen Controls.

**Datum:** 18. März 2026  
**Autor:** GitHub Copilot
