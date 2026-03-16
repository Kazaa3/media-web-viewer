# Logbuch: Aktueller Stand Videoplayer – März 2026

## Übersicht
Der Videoplayer unterstützt jetzt alle modernen Streaming- und Wiedergabemodi, ist vollständig modular und für maximale Kompatibilität und Performance optimiert.

---

## Unterstützte Modi & Features
- **Direct Play:** Native Wiedergabe von MP4/WebM (H.264/AAC/VP9) ohne Transcoding, HTTP Range, <1% CPU.
- **MediaMTX (HLS/WebRTC):**
  - HLS: Perfektes Seeking, breite Browser-Kompatibilität, native <video>-Unterstützung.
  - WebRTC (WHEP): Ultra-low-latency (<100ms), ideal für Live und Instant-Playback.
  - Beide Streams parallel, Browser/Frontend wählt optimal.
- **ffmpeg FragMP4:** On-the-fly MP4-Streaming mit HTTP Range, Seeking, 100% browserkompatibel.
- **ffmpeg HLS:** Segmentiertes HLS-Streaming, kompatibel mit allen Browsern.
- **mkvmerge Direct/Pipe:** Schnelles Remux zu MP4 oder On-Demand-Streaming.
- **DVD/ISO-Handler:** Spezial-Playback via VLC (dvd://), inkl. User-Experience-Flags.
- **Drag & Drop Playlist:** Intuitive Verwaltung und Wiedergabe von Medien.
- **Kontextmenü:** Glassmorphism-UI, direkter Moduswechsel pro Item.
- **Automatische Kompatibilitätsprüfung:** ffprobe-Integration, intelligentes Fallback (Direct Play → MediaMTX → Remux).
- **Port Discovery & Logging:** Dynamische Port-Allokation, persistente Speicherung für Verifikation.

---

## Architektur & Integration
- **Backend:** Modular (Eel/Bottle), alle Streaming-Engines (ffmpeg, mkvmerge, MediaMTX) integriert.
- **Frontend:** Moderne UI, Statusanzeigen, Toasts, Kontextmenü, Auto-Select für Streams.
- **Docker-Setup:** MediaMTX als Dual-Stream-Server (HLS/WebRTC), Synology-ready.

---

## Verifikation & Benchmarking
- Alle Modi getestet (CPU, Startzeit, Seeking, Kompatibilität, Stabilität).
- MediaMTX HLS/WebRTC als Default für maximale Flexibilität.
- Direct Play spart bis zu 90% CPU bei kompatiblen Dateien.

---

## Fazit
Der Videoplayer ist universell, performant und flexibel – alle modernen Wiedergabemodi sind abgedeckt, Fallbacks und Kompatibilitätschecks sind automatisiert. Die Architektur ist bereit für weitere Erweiterungen und professionelle Nutzung.

---

*Siehe Logbuch-Einträge für Details zu einzelnen Modi, Benchmarks und Setup.*
