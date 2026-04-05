# Multimedia-Test-Suite: Ebenen & Beispiele

**Ziel:**
Eine systematische Test-Suite für deinen Video-Player, die Routing, Transportwege und UI-Ende-zu-Ende abdeckt.

---

## 1. Backend-Routing-Tests (ohne echte Wiedergabe)

- Prüft, ob `get_play_plan()` und Analyse-Logik korrekt arbeiten.
- Beispiele:
  - Kompatible MP4: `mode == "direct"`, URL zeigt auf `/direct/...`
  - MKV mit H.264/AAC: Remux (`ensure_mp4_remux`), dann `mode == "direct"`
  - HEVC 4K mit TrueHD/PGS: `mode == "hls"` oder `mode == "vlc-file"` (Policy)
  - ISO/BD: Erst `extract_main_from_iso`, dann kein Direct-Play, nur HLS oder VLC
- Umsetzung: Python-Unit-Tests, ffprobe-Ergebnisse mocken, Routing-Funktion prüfen

---

## 2. Media-Pfad-Tests (ohne UI)

- Prüft, ob jeder Transportweg technisch funktioniert:
  - **Direct-Play:**
    - `GET /direct/test.mp4` mit `Range`-Header → Status 206, korrekte Header
    - Datei laden, Hash/Länge vergleichen
  - **HLS:**
    - `ensure_hls()` erzeugt Playlist + Segmente
    - `GET /hls/<hash>/index.m3u8` → gültig, Segmente erreichbar
  - **VLC/RTSP (MediaMTX):**
    - FFmpeg-Publish → RTSP
    - ffprobe/ffplay liest 3–5 s RTSP → Returncode 0
  - **VLC/pyVLC:**
    - pyVLC kann Media setzen, `play()` aufrufen, `is_playing()` schlägt nicht direkt fehl

---

## 3. Player-Integrationstests (mit UI / End-to-End)

- Prüft, ob der Video-Tab aus Nutzersicht korrekt funktioniert:

1. **Direct-Play-Fall**
   - MP4/H.264/AAC anklicken →
     - `get_play_plan` liefert `mode=direct`
     - video.js bekommt MP4-URL
     - Playback startet, Seekbar funktioniert
2. **HLS-Fall**
   - Schweres MKV →
     - Plan: `mode=hls`
     - video.js bekommt m3u8-URL
     - Segmente werden geladen, Seek/Skip gehen
3. **VLC-Fall**
   - ISO/BD-Item →
     - Plan: `mode=vlc-bluray`
     - Klick auf „VLC-Modus“ → Eel startet `vlc bluray:///...`
     - (Manuell Menüs/Boni prüfen)
4. **Fehler/Fallback**
   - Defekte Datei →
     - Test-Suite: `direct_play_browser = false`
     - Play im Browser zeigt Fehler, bietet „in VLC öffnen“ an

---

## 4. Test-Suite-Struktur (Empfehlung)

- `analyze_media()` – reine Analyse / ffprobe
- `get_play_plan()` – Routing
- `test_media_paths()` – Direct/HLS/RTSP-Smoke-Tests
- `ui_play_scenarios()` – End-to-End-Szenarien (manuell/automatisiert, z.B. Playwright/Selenium)

---

**Fazit:**
- Verifiziert Backend-Logik
- Checkt alle Transportwege
- Testet das UI-Verhalten deines Players
- Ermöglicht robuste, nachvollziehbare Multimedia-Workflows
