# Logbuch: MediaMTX Integration & "Öffnen mit"-Konzept

## Datum
16. März 2026

## Übersicht
Dieser Logbuch-Eintrag dokumentiert die Integration von MediaMTX als neue Video-Option und die Umsetzung des "Öffnen mit"-Konzepts im Eel/Bottle-Frontend.

---

## Umsetzung

### 1. Modus-Implementierung (Frontend)
- Video-Tab mit Modus-Auswahl (inkl. MediaMTX (HLS)).
- Button "Öffnen mit" ruft openWith() auf.
- Video wird im gewählten Modus geladen (Chrome Native, ffmpeg mit cvlc, mkvmerge mit cvlc, cvlc solo, Direct Play, Embedded VLC, VLC extern, Drag & Drop, Playlist, MediaMTX (HLS)).
- Player-Switch und Placeholder-Handling.

### 2. Backend (Python/Bottle)
- open_video(file_path, mode): Startet MediaMTX-Docker, setzt Player-Source je nach Modus.
- MediaMTX (HLS): Trigger via API, Stream-URL generiert.
- ffmpeg mit cvlc: Stream via cvlc und HTTP.
- Weitere Modi analog.
- /video/<fname> Route für MP4-Streaming.

### 3. Docker-Compose & mediamtx.yml
- MediaMTX als Service, autostart via Docker Compose.
- Pfad-Konfiguration für ffmpeg-Loop und RTSP.

---

## Tests
- Modus-Wechsel: Player-Switch funktioniert sofort.
- "Öffnen mit": Kontextmenü und Modus-Auswahl laden Video korrekt.
- Chrome: HLS/Seeking voll unterstützt.
- Fallback: ISO → Auto-Remux via ffmpeg in MediaMTX.

---

## Kommentar
Ctrl+Alt+M

---

*Siehe walkthrough.md für vollständige Details und Proof of Work.*
