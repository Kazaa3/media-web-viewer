# Implementation Plan: Advanced Playback & Log Refinement

## Datum
16. März 2026

---

## Ziel
- Log-Level-Visibility verbessern
- MediaMTX-Streaming um WebRTC erweitern
- Fehlende Playback-Varianten (mkvmerge, cvlc solo) ergänzen
- "Öffnen mit"-Funktion für manuelle Moduswahl implementieren

---

## Proposed Changes

### Backend (main.py)
- [MODIFY] set_log_level: Logge Level-Wechsel vor Update, damit Bestätigung immer sichtbar. CRITICAL explizit unterstützen.
- [NEW] open_video(file_path: str, mode: str): Eel-exposed, triggert Playback mit Modus-Override. Unterstützt MediaMTX (HLS/WebRTC), ffmpeg/mkvmerge mit cvlc, etc.
- [MODIFY] stream_to_vlc(file_path, engine="ffmpeg"): mkvmerge als Remux-Engine für VLC-Pipe, cvlc solo (nur Datei öffnen).
- [MODIFY] stream_to_mediamtx(file_path, protocol="hls"): WebRTC (WHEP) Pfade unterstützen.

### Frontend (app.html)
- [MODIFY] UI-Komponenten: "MediaMTX (WebRTC)", "mkvmerge mit cvlc", "cvlc solo" im Playback-Selector ergänzen.
- [MODIFY] "Öffnen mit"-Button neben Selector, openWith() ruft eel.open_video.

### Localization (i18n.json)
- Neue Einträge für Playback-Modi und "Öffnen mit"-Button.

---

## Verification Plan

### Automated Tests
- tests/debug/test_log_levels.py: Prüft, ob alle 5 Log-Levels im UI-Logbuffer erscheinen.
- tests/debug/test_db_console_writer.py: Prüft DB-Status und Console-Output Logging.

### Manual Verification
- "Öffnen mit"-Button für jeden Modus testen.
- MediaMTX WebRTC Playback testen (sofern Umgebung unterstützt).
- Logs auf allen Leveln (DEBUG bis CRITICAL) prüfen.

---

## Kommentar
Ctrl+Alt+M

---

*Siehe logbuch/2026-03-16_gui_bandwidth_desktopmode.md für GUI-Status und Empfehlungen.*
