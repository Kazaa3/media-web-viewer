# Implementation Plan: Advanced Playback Modes & Hardware Detection

## Date
16. März 2026

## Overview
Abschluss der Implementierung: Advanced Playback, Hardware Detection & Scan-Optimierung

Wesentliche Ergebnisse:
- Hardware Detection: Echtzeit-Erkennung von SSD/HDD, PCIe-Generationen und Netzwerk-Mounts (SMB/NFS).
- Playback Modes: UI-Integration für Chrome Native, FFmpeg, VLC, mkvmerge und Direct Play.
- Scan-Optimierung: Automatischer Lightweight-Mode für Netzwerkpfade, intelligentes Skip-Parsen.
- Analyse/Write Modes: Konfigurierbare Feature Flags für Deep Metadata Extraction.
- Verifikation: Backend-Logik mit neuer Integrationstest-Suite validiert.

Siehe walkthrough.md für vollständige Details und Proof of Work.
Walkthrough: Advanced Playback & Hardware Detection
Die folgenden Features wurden erfolgreich implementiert:

Backend Implementation:
- hardware_detector.py erkennt SSD vs. HDD, PCIe Generation (NVMe), und Netzwerk-Mounts (SMB/NFS/CIFS).
- play_media in main.py unterstützt chrome_native (Audio/Video), ffmpeg (Transcoding via VLC pipe), cvlc (Fallback), mkvmerge (Remux), direct (VLC extern).
- Scan-Optimierung: Netzwerkpfade triggern Lightweight Mode, bereits indexierte Medien werden übersprungen.
- Analyse & Write Modes: Feature Flags für Deep Analysis und Metadaten-Schreiben.

Frontend Integration:
- Optionen-Tab mit Playback- und Hardware-Einstellungen.
- Dropdown für Wiedergabe-Modus, numerisches Bandbreiten-Limit.
- Echtzeit-Anzeige Hardware-Informationen (Disk, PCIe, Netzwerk).
- i18n.json aktualisiert, Warnungen behoben.

Verification Results:
- Hardware-Logik: test_hardware_detector.py (alle Tests bestanden)
- Playback-Switching: test_playback_modes.py (alle Tests bestanden)
- Manuelle Verifikation: Optionen-Tab, Hardware-Info, Modus-Wechsel, Feature Flags.

Hinweis: Netzwerk-Mounts (SMB/NFS) triggern jetzt automatisch schnelles Scanning, um langsame I/O zu vermeiden.
MediaMTX (ehemals rtsp-simple-server) – Feature- und Integrationsübersicht:
- Zero-Dependency Media-Router für RTSP/WebRTC/HLS/RTMP, ideal für headless Streaming von lokalen Dateien (MKV/ISO/MP4) zu Browsern.
- Streaming: Liest lokale Dateien/ISO/MKV und streamt via HLS/WebRTC/RTSP zu <video> im Browser (automatisch kompatibel).
- Seeking: Perfekt über HLS/fMP4-Chunks oder WebRTC, mit Range-Support und niedriger Latenz (<100ms).
- Features: Kein Transcoding nötig (Direct Play), Recording, Proxy, API-Control, Docker-ready (Synology/NAS).
Docker-Setup (Synology/NAS):
version: '3.8'
services:
  mediamtx:
    image: bluenviron/mediamtx:latest
    container_name: mediamtx
    network_mode: host
    volumes:
      - /path/to/your/media:/media
      - ./mediamtx.yml:/mediamtx.yml
    restart: unless-stopped
mediamtx.yml (Config für Dateien):
paths:
  all:
    runOnInit: ffmpeg -re -stream_loop -1 -i /media/$MTX_PATH -c copy -f rtsp rtsp://localhost:8554/$MTX_PATH
    runOnDemand: ffmpeg -re -stream_loop -1 -i /media/$MTX_PATH -c copy -f rtsp rtsp://localhost:8554/$MTX_PATH
Integration in Bottle/Eel/Chrome:
<video id="player" controls width="800">
  <source src="http://nas-ip:8888/movie.mkv/index.m3u8" type="application/x-mpegURL">
</video>
Python/Bottle (API zum Starten):
import subprocess
from bottle import route
@route('/start/<path>')
def start_stream(path):
    subprocess.run(['curl', '-X', 'POST', f'http://localhost:9997/paths/{path}'])
    return {'url': f'http://localhost:8888/{path}/index.m3u8'}
Vorteile: ISO/DVD/MKV direkt streambar, Seeking via HLS, kein Custom-Remux nötig, Docker-ready, WebRTC für <1s Latency.
Performance-Vergleich (LAN, Seeking):
| Tool         | On-Fly Seeking | Latency | CPU (Direct Play) | Docker/NAS |
|--------------|---------------|---------|-------------------|------------|
| MediaMTX     | Exzellent     | <100ms  | Minimal           | Ja         |
| Jellyfin     | Sehr gut      | 1–2s    | Minimal           | Ja         |
| Plex         | Gut           | 1–3s    | Minimal           | Ja         |
| ffmpeg Frag  | Gut           | 2–5s    | Niedrig           | -          |
| cvlc         | Mittel        | 3–10s   | Mittel            | Ja         |
Für Bottle/Eel-Setup: MediaMTX als Docker-Sidecar starten, Eel ruft http://localhost:8888/stream/iso auf – nahtloses <video>.
MediaMTX ist der Game-Changer für low-CPU, ms-Seeking ohne Custom-Skripte.
Fazit: MediaMTX (rtsp-simple-server) ist die bevorzugte Lösung für on-the-fly Streaming und Seeking von ISO/MKV im NAS/Bottle/Eel-Setup. Es bietet exzellentes Seeking (<100ms), browserfreundliche Formate und Docker-Kompatibilität ohne Transcoding.
Alternativen zu cvlc/ffmpeg für on-the-fly Streaming und Seeking:
- MediaMTX (rtsp-simple-server): Streams RTSP/HTTP/WebRTC aus ISO/MKV ohne Transcoding, on-the-fly Remux zu browser-freundlichen Formaten, exzellentes Seeking (<100ms), Docker-kompatibel.
- Jellyfin: Open-Source Plex-Alternative, Direct Play für MKV/ISO, perfektes Seeking/Caching, Web-UI oder App, Docker-ready.
- Plex: Kommerziell, Direct Stream/Remux, Browser-Client mit Seeking, Server lizenzpflichtig bei >5 Usern.
- MP4Box/Fragmented MP4: On-the-fly Remux zu fMP4 (DASH), besseres Seeking als HLS.

Empfehlung: MediaMTX als Docker-Sidecar für ultra-low-latency Streaming, Jellyfin für No-Code Direct Play, beide optimal für NAS/Bottle/Eel-Integration.
Benchmarking für on-the-fly Seeking und Streaming:
- Teste progressive Download + Range Requests, on-the-fly Remux (ffmpeg/VLC), HLS/DASH Chunked Streaming.
- Metriken: Seek-Latenz, CPU-Last, Stabilität, Browser-Kompatibilität.
Vergleichstabelle:
| Methode           | Seeking während Open | Latenz | CPU-Last |
|-------------------|---------------------|--------|----------|
| ffmpeg FragMP4    | Ja (Ranges)         | <2s    | Niedrig  |
| VLC TS-Stream     | Ja (Ranges)         | 1–3s   | Niedrig  |
| HLS Chunks        | Ja (perfekt)        | 5–10s  | Mittel   |
| Raw ISO/MKV       | Nein (Browser nein) | N/A    | -        |
Fazit: On-the-fly ist machbar und seek-fähig, aber Remux zu MP4 mit faststart bleibt stabiler/langfristiger. Für dein Setup: ffmpeg FragMP4 oder VLC TS als Bridge zu Eel.
Strategie für große m2ts-Dateien (Blu-ray):
- Direktes Streaming: m2ts-Datei als progressive Download mit Range-Support ausliefern, falls Browser/Player kompatibel.
- Remux: m2ts per ffmpeg -c copy in MP4 oder TS umcontainerisieren, um Browser-Kompatibilität und schnelles Seek zu ermöglichen.
- Chunked Streaming: ffmpeg HLS oder DASH nutzen, um m2ts in kleine .ts-Chunks zu splitten, für nahtloses Seeking und adaptive Bitrate.
Empfohlene ffmpeg-Befehle:
ffmpeg -i input.m2ts -c copy -movflags +faststart output.mp4
ffmpeg -i input.m2ts -c copy -f hls -hls_time 4 -hls_list_size 0 playlist.m3u8
Bei sehr großen Dateien: SSD/NAS für schnellen Zugriff, Range-Requests und Caching aktivieren.
On-the-fly Seeking während ISO/MKV geöffnet ist:
- Progressive Download + Range Requests: Browser fordert Bytes via HTTP 206, Server liest direkt aus ISO/MKV und liefert. Seeking = neuer Range-Request.
- On-the-fly Remux: ffmpeg/VLC remuxen MKV/ISO-Inhalt zu MP4/HLS-Chunks während des Streams (Codec-Copy), Browser cached Chunks für schnelles Seek.
- HLS/DASH: ISO/MKV → kleine .ts-Chunks (4–10s), Browser lädt nur gesuchte Chunks – perfektes Seeking, aber 5–10s Latenz.
Einschränkungen:
- ISO: VLC kann ISO direkt streamen, aber Browser versteht ISO nicht – Remux zu TS/MP4 nötig.
- MKV: H.264/AAC remuxbar zu MP4, sonst Buffering beim Seek.
Praktische ffmpeg/VLC-Befehle:
ffmpeg -re -i input.iso -c copy -f mp4 -movflags frag_keyframe+empty_moov -listen 1 http://0.0.0.0:8080/stream.mp4
cvlc input.iso --sout '#transcode{vcodec=h264}:std{access=http,mux=ts,dst=:8080/}' --no-sout-all --sout-keep
ffmpeg -i input.mkv -c copy -f hls -hls_time 4 -hls_list_size 0 -hls_flags delete_segments playlist.m3u8
Vergleich Seeking-Performance:
ffmpeg FragMP4: <2s Latenz, niedrig CPU
VLC TS-Stream: 1–3s Latenz, niedrig CPU
HLS Chunks: 5–10s Latenz, mittel CPU
Raw ISO/MKV: nicht browserfähig
Fazit: On-the-fly ist machbar und seek-fähig, aber Remux zu MP4 mit faststart bleibt stabiler/langfristiger.
Remuxing (z.B. mit mkvmerge/ffmpeg) ermöglicht perfektes Caching auf Browser-, Server- und NAS-Ebene:
- Nach Remux in MP4 mit korrektem MOOV-Atom (ffmpeg -movflags faststart) speichert Chrome Chunks und ermöglicht schnelles Seek.
- HTTP Range Requests: Browser fordert nur gesuchte Bytes an, Server liefert Chunks mit ETag/Cache-Control.
- Keine Re-Encoding-Last: Einmal remuxen, dann I/O-only Streaming.
Empfohlene ffmpeg/mkvmerge-Befehle:
ffmpeg -i input.mkv -c copy -movflags +faststart output.mp4
mkvmerge -o out.mp4 input.mkv + qt-faststart out.mp4
Empfohlene Bottle-Route für Streaming und Caching:
@route('/video/<fname>')
def video(fname):
  resp = static_file(fname, root='/path/to/remuxed', mimetype='video/mp4')
  resp.set_header('Cache-Control', 'public, max-age=3600')
  resp.set_header('Accept-Ranges', 'bytes')
  return resp
NAS/Server: Remuxte MP4s auf SSD/Fast-Disk legen, OS/Dateisystem cached Zugriffe.
Nach Remux immer ffprobe output.mp4 checken – Duration/SeekPoints müssen korrekt sein.
Vergleich der Headless-Streaming-Optionen für Python/Bottle/Eel/NAS:
1. mkvmerge: Schnellstes Remux, ideal für Batch-Konvertierung (MKV/ISO → MP4), dann als statische Datei im Bottle-Server ausliefern.
2. ffmpeg Remux: Flexibel, auch für HLS, sehr schnell (Codec-Copy), direkt oder als HLS streambar.
3. VLC Pipe: Video über stdin/stdout zu Browser streamen, unterstützt ISO/MKV direkt, aber Container nicht immer browser-freundlich.
4. ffmpeg HLS: On-the-fly Chunked-Playlist (.m3u8 + .ts), gut für Live-Streaming, etwas Latenz.
5. mpv: Headless, weniger streaming-fokussiert.
6. HFS: HTTP File Server, nur für kompatible MP4, kein Remux.
Empfehlung: Batch-Remux mit mkvmerge/ffmpeg, dann direktes Bottle-Streaming für schnellste und ressourcenschonendste Lösung.
Empfohlene Streaming-Strategie für LAN/Bottle/Eel/Chrome:
- Direkter HTTP-Stream: MP4/H.264 oder WebM als statische Datei mit Content-Type ausliefern, Browser spielt sofort, keine CPU-Last.
- Remux: MKV mit H.264/AAC per ffmpeg -c copy in MP4/WebM umcontainerisieren, CPU-Kosten gering, ideal als Batch-Konvertierung.
- On-the-fly Remux: Server liest z.B. MKV und liefert währenddessen MP4/HLS mit Codec-Copy, spart Speicherplatz, benötigt aber laufenden ffmpeg/cvlc-Prozess pro Stream.
- Vollständiges Transcoding: Nur nötig bei inkompatiblen Codecs, höchste CPU-Last, vermeiden wenn möglich.
Praxisnahe Reihenfolge:
1. Bibliothek einmalig konvertieren: ISO → MKV → MP4/H.264 (oder direkt MP4).
2. MKV (H.264/AAC) → ffmpeg -i in.mkv -c copy out.mp4 (Remux).
3. Bottle-Route als File-Server mit Range-Support und Content-Type.
4. Browser <video src="/video/..."> nutzen, Chrome übernimmt Playback.
Zusätzliche Hinweise:
- cvlc ist VLC ohne GUI, alle VLC-Optionen funktionieren auch mit cvlc (CLI, RC/HTTP-Interface).
- ISO/MKV können nicht direkt im Browser gestreamt werden; sie müssen serverseitig in MP4/WebM umgewandelt oder transkodiert werden.
- Typischer Workflow: ISO → MKV/MP4 umwandeln, MKV ggf. umcontainerisieren oder transkodieren, HTTP-Endpoint in Bottle/Eel bereitstellen, im <video>-Tag im Chrome-Frontend einbinden.
- Browser spielt MP4 (H.264) fast überall, WebM (VP9) modern, MKV nur eingeschränkt, ISO gar nicht.
- Für Streaming/Transcoding mit cvlc: cvlc input --sout '#transcode{...}:standard{access=http,mux=ts,dst=:8080/}'
Zusätzlich wird HLS (HTTP Live Streaming) als weiterer Playback-Modus unterstützt. HLS kann für Live-Streaming und adaptive Bitrate genutzt werden und wird als Option in die Playback-Mode-Auswahl integriert.
Die Implementierung umfasst:
- VLC piped Mode: cvlc kann als Pipe für Playback genutzt werden, insbesondere als Fallback wenn Chrome Native nicht unterstützt wird oder für ffmpeg/mkvmerge.
- Playback Mode Auswahl: set_playback_mode(mode) erlaubt Umschalten zwischen chrome_native, ffmpeg, cvlc, mkvmerge, direct.
- Bandwidth-Limit: set_bandwidth_limit(limit_mbps) setzt die Bandbreite (z.B. 20MB/s).
- Analyse- und Schreib-Modus: analyse_media(path) und write_media_tags(path, tags) mit Schutzmechanismen und Feature-Flags.
- Hardware-Erkennung: get_hardware_info() liefert SSD/HDD/PCIe-Infos für Desktop-Mode.
- Playlist: Drag & Drop und Playlist-Handling werden als API und UI-Feature integriert.
This entry documents the planned implementation for advanced playback modes, hardware detection ("Desktop-Mode"), low bandwidth optimization, playlist enhancements, and benchmarking in the Media Web Viewer project.
Der Implementierungsplan wurde mit den neuen Anforderungen verfeinert:

- Audio: Immer Chrome Native als Standard.
- VLC: Als zweiter, eingebetteter Player integriert.
- Scan-Optimierung: Erkennt SMB/NFS-Pfade automatisch (Lightweight-Mode) und prüft, ob Pfade bereits in der DB sind (< 1 Sekunde für MP3/FLAC).
- Modi: Neuer Analyse- und Schreib-Modus (mit Schutzmechanismen).
- Hardware: Erkennung von HDD/SSD und PCIe 3/4 für den Desktop-Modus.

Alle geplanten Playback-Modi werden integriert:
  - ffmpeg (transcoding/streaming)
  - cvlc (VLC dummy/embedded player, auch als piped Mode für Playback nutzbar)
  - vlc mit gui
  - mkvmerge (direct remux to MKV)
  - direct play (file access)
  - chrome native (MP4 playback, codec check)
  - analyse (deep ffprobe analysis)
  - write (tag editing)
  - low bandwidth mode (20MB/s)
  - Desktop-Mode (detect HDD, SSD, PCIe3, PCIe4)
  - Drag & Drop playlist
Chrome Native mode spielt MP4-Dateien, wenn der Codec unterstützt wird.
Benchmarking wird durchgeführt, um alle Varianten zu vergleichen und die bevorzugte auszuwählen.

---

## Proposed Changes


### Backend

#### [NEW] hardware_detector.py

#### [MODIFY] main.py
  - Check if path exists in DB before re-parsing.
  - Automatic "Lightweight" mode for SMB/NFS paths.
  - Speed target: < 1s for MP3/FLAC.
  - Analyse: Deep ffprobe/analysis.
  - Write: Tag writing, with safeguards for ISO/MKV parser blocking.
  - Bandwidth: Implement "Low Bandwidth" optimization (20MB/s).
  - ffmpeg: Transcoding/streaming.
  - cvlc: VLC dummy interface.
  - mkvmerge: Direct remux to MKV.
  - direct_play: Direct file access.
  - chrome_native: Browser-native playback for MP4.
  - Caching: For large files, implement caching mechanism to optimize playback. If SSD is available, enable SSD storage mode for fast access.
  - Remux Capability: If remuxing is supported, enable live streaming mode for compatible formats.

#### [MODIFY] models.py

---

### Frontend

#### [MODIFY] app.html
- UI for Mode Selection (ffmpeg, cvlc, mkvmerge, direct, native).
- "Low Bandwidth" toggle (20MB/s).
- "Desktop Info" section (HDD/SSD, PCIe).
- Drag & Drop area for playlists.

#### [MODIFY] script.js
- Drag & Drop playlist handlers.
- Update UI with hardware info from backend.
- Hook up new playback modes to backend.

---

## Verification Plan


### Automated Tests
- Playback Modes: pytest tests/test_video_modes_extended.py (new, covers all modes).
- Hardware Detection: pytest tests/test_hardware_detection.py (mocked, covers HDD/SSD/PCIe detection).
- Performance: pytest tests/benchmark_playback.py (startup and playback speed for all modes).

### Manual Verification
- Test Drag & Drop playlist in the UI.
- Verify "Low Bandwidth" mode affects FFmpeg command (bitrate/remuxing).
- Check "Desktop-Mode" display for correct hardware info.
- Verify "Chrome Native" plays MP4s and audio if codec is supported.
- Test SMB/NFS auto-lightweight detection.
- Compare playback modes via benchmarking and select preferred variant.

---

## Comment
Ctrl+Alt+M

---

*See attachments for referenced files and project conventions.*
