# FFmpeg Capabilities: libx264 & Fragmented MP4
  - Verified that libx264 is installed and accessible for H.264 encoding.
  - Enables high-quality, low-latency video encoding for media processing and streaming.

- **ISO-Dateien und Player-Logik**

- **ISO-Dateien:**
  - ISO-Images dürfen nicht mit dem internen Player verknüpft werden.
  - Ein Klick auf ein ISO-Item muss zur Videoengine im Videoplayer-Reiter führen.
  - Chrome und andere Chromium-Browser können keine ISOs abspielen und werden dies auch zukünftig nicht unterstützen.

- **Spezialfall Ordner-Erkennung:**
  - Es gibt verschiedene Typen:
    - ISO-Dateien
    - Entpackte ISO-Ordner
    - Filmordner-Objekte mit Metadatenstruktur
    - MKV-transkodierte Videos
  - Die Erkennung und Behandlung dieser Typen ist für die Medienverwaltung und das UI entscheidend.
  - Filmordner und entpackte ISOs enthalten oft zusätzliche Metadaten und Strukturen, die für die Anzeige und Navigation genutzt werden.

- **Fragmented MP4 Support:**
  - Confirmed use of FFmpeg options: `-movflags frag_keyframe+empty_moov`.
  - Ensures MP4 files are streamable in Chromium-based browsers (Chrome, Edge, etc.).
  - Allows playback to start before the file is fully downloaded, improving user experience.

- **Integration Notes:**
  - Media Web Viewer leverages these capabilities for optimal video handling.
  - Streamability and encoding quality are validated as part of the environment check.

---

*Entry created: 12. März 2026*

---

## Transkodierung (Transcoding)

- **Definition:** Transkodierung bezeichnet die Umwandlung von Mediendateien von einem Format oder Codec in ein anderes.
- **FFmpeg-Einsatz:**
  - FFmpeg wird verwendet, um Videos mit libx264 neu zu kodieren und dabei Fragmented MP4 zu erzeugen.
  - Typische Anwendung: Anpassung von Bitrate, Auflösung oder Codec für Streaming-Kompatibilität und Speicheroptimierung.
- **Workflow:**
  - Eingabedatei wird analysiert und mit den gewünschten Parametern (z.B. H.264, frag_keyframe, empty_moov) neu kodiert.
  - Ergebnis: Streambare, browserkompatible MP4-Dateien mit optimaler Qualität und niedriger Latenz.

---
