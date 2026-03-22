# Implementation Plan: Transcoding & Auto-Detection System (März 2026)

## Ziel
Robustes, automatisches Transcoding- und Auto-Detection-System für performantes Media-Playback aller Formate in der Media-Library-App.

---

## 1. Core Backend (src/core/main.py)
- **[MODIFY] main.py**
    - **FFprobe-Integration:**
        - Hilfsfunktion für ffprobe-Calls (Live-Detection, JSON-Parsing)
    - **Auto-Routing-Logik:**
        - `open_video` nutzt ffprobe-Metadaten
        - Routing:
            - codec == 'h264' & container == 'mp4' → chrome_direct
            - codec == 'hevc' oder container == 'matroska' → chrome_fragmp4 (Transcode)
            - ISO/DVD → vlc_iso
    - **MediaMTX-Verbesserung:**
        - `stream_to_mediamtx` prüft und setzt HW-Acceleration-Flags (falls verfügbar)
    - **MPV Standalone:**
        - mpv-Execution mit sinnvollen Default-Flags (z.B. --fullscreen)

---

## 2. Parser (src/parsers/ffprobe_parser.py)
- **[MODIFY] ffprobe_parser.py**
    - Sicherstellen, dass Video-Stream-Metadaten (Codec, Auflösung) immer extrahiert werden (Library-Scan)

---

## 3. Frontend UI (web/app.html)
- **[MODIFY] app.html**
    - "Auto-Detect"-Option im Player-Dropdown ergänzen
    - UI zeigt aktiven Transcoding-Modus an (z.B. "Live Transcode: H-HLS")

---

## 4. Verification Plan
- **Automatisierte Tests:**
    - Unit-Test für Auto-Routing: `tests/unit/test_auto_routing.py` (ffprobe-Output mocken, open_video-Routing prüfen)
    - Integrationstest für FragMP4: Headless-Test, `/video-stream/`-Route liefert gültigen Stream-Header
- **Manuelle Verifikation:**
    - ISO-Playback: Rechtsklick auf ISO, "Auto-Detect" → VLC-Start prüfen
    - MKV-Playback: MKV-Datei triggert FragMP4-Transmuxing
    - HW-Acceleration: Log-Ausgabe prüft -hwaccel-Flag bei Transcode

---

**Datum:** 17. März 2026  
**Autor:** GitHub Copilot
