# Logbuch: Port Discovery, DVD/ISO Handler & Streaming Route

## Datum
16. März 2026

---

## Backend Enhancements
- **Port Discovery:**
  - Dynamische Port-Allokation mit find_free_port.
  - Persistenz: Port wird beim Startup in port.json gespeichert.
  - Logging: Port-Info wird im Startup-Log ausgegeben.
  - Ermöglicht automatisierte und manuelle Verifikation.

- **DVD/ISO Handler:**
  - Spezial-Handler für ISO/DVD: Nutzt dvd://-Protokoll mit VLC.
  - Zusätzliche Flags (--fullscreen, --no-video-title-show) für bessere User Experience.
  - Fehlerhandling und Logging für ISO-Playback.

- **High-Performance Streaming Route:**
  - mkvmerge und ffmpeg als Remux-Engines für VLC-Pipe.
  - MediaMTX-Streaming mit HLS und WebRTC (WHEP).
  - Logging der Streaming-URL für Debugging und Verifikation.

---

## Verification Plan
- Port im Startup loggen und in port.json persistieren.
- DVD/ISO-Playback separat testen (VLC-GUI, Muxing).
- Streaming-URL im Log prüfen (MediaMTX, VLC-Pipe).

---

## Kommentar
Ctrl+Alt+M

---

*Siehe vorherige Logbuch-Einträge für Kontext und Workflow.*
