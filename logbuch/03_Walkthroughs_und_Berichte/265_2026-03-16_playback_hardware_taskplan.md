# Logbuch: Advanced Playback Modes & Hardware Detection – Taskplan & Umsetzung

## Datum
16. März 2026

## Taskplan

1. Research
   - Bestehende Playback-Implementierung analysiert
   - src/core/main.py auf stream_to_vlc und Routen untersucht
   - Hardware Detection-Integration vorbereitet

2. Design Implementation Plan
   - Integration der Playback-Modi: FFmpeg, CVLC, mkvmerge, Direct Play, Chrome Native
   - Low Bandwidth Mode und Hardware Detection geplant
   - Drag & Drop Playlist UI/UX entworfen
   - Analyse- und Write-Modi geplant
   - MediaMTX (rtsp-simple-server) als neuen Modus vorgesehen

3. Backend Changes
   - Erweiterte Hardware Detection (HDD, SSD, PCIe-Generationen) implementiert
   - Playback-Modi (ffmpeg, cvlc, mkvmerge, direct, native) integriert/refined
   - Analyse/Write-Mode-Logik umgesetzt
   - MediaMTX als Streaming-Option integriert

4. Frontend Changes
   - UI für Moduswahl hinzugefügt
   - Drag & Drop Playlist implementiert
   - Low Bandwidth Toggle und Hardware-Info-Anzeige integriert
   - MediaMTX in Playback-Optionen aufgenommen

5. Verification & Benchmarking
   - Tests für Playback-Modi erstellt/aktualisiert
   - Benchmarking-Suite implementiert
   - Drag & Drop Funktionalität verifiziert
   - MediaMTX Streaming und Seeking getestet

---

## Kommentar
Ctrl+Alt+M

---

*Siehe walkthrough.md für vollständige Details und Proof of Work.*
