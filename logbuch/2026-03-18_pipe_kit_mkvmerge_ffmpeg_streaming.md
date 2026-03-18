
# Logbuch: PIPE-KIT mkvmerge → ffmpeg Streaming – Bewertung & Alternativen

## Stand März 2026

### Bewertung der Pipe-Kette mkvmerge → ffmpeg
- Die Kombination mkvmerge → ffmpeg zu FragMP4 ist für Media-Library-Streaming nicht optimal:
  - Unnötig komplex (zwei Prozesse, CPU/IO-Overhead).
  - Langsamer als direkter FFmpeg-Remux.
  - Kompatibilitätsrisiko bei Subs/Multi-Audio.
  - FragMP4 ist für DASH nützlich, aber für HTML5-Player meist Overkill – Browser erwarten seekbare MP4s.

### Bessere Alternativen
1. **Reiner FFmpeg-Remux (empfohlen):**
   - Lossless, blitzschnell, Web-optimiert (moov-Atom vorne).
   - Beispiel:
     ```python
     def remux_to_mp4(input_file, output_file):
         cmd = [
             'ffmpeg', '-i', input_file,
             '-c', 'copy',           # lossless copy aller Streams
             '-map', '0',            # alle Tracks übernehmen
             '-movflags', '+faststart',  # Web-optimiert (moov-Atom vorne)
             output_file
         ]
         subprocess.run(cmd, check=True)
     ```
   - Perfekt für Jellyfin/Plex-ähnliche Streaming-Setups.
   - Funktioniert bei 99% MKV (auch Subs, HDR).

2. **HLS-Segmentierung für echtes Streaming:**
   - Dynamisch oder statisch, ideal für `<video src="playlist.m3u8">`.
   - Beispiel:
     ```python
     def generate_hls(input_file, output_dir):
         os.makedirs(output_dir, exist_ok=True)
         cmd = [
             'ffmpeg', '-i', input_file,
             '-c:v', 'libx264', '-preset', 'veryfast',
             '-c:a', 'aac',
             '-f', 'hls', '-hls_time', '10', '-hls_list_size', '0',
             '-hls_segment_filename', f'{output_dir}/segment_%03d.ts',
             f'{output_dir}/playlist.m3u8'
         ]
         subprocess.run(cmd, check=True)
     ```
   - On-Demand: Backend generiert HLS dynamisch, kein Pre-Processing nötig.

3. **Smart Routing im Frontend:**
   - Native Chrome: MP4/HLS.
   - VLC/FFplay: RTSP/HLS direkt aus MKV (kein Remux nötig).

### Performance-Vergleich
| Methode            | Lossless? | Geschwindigkeit | Browser? | Komplexität |
|--------------------|-----------|-----------------|----------|-------------|
| FFmpeg copy MP4    | Ja        | Sehr hoch       | Perfekt  | Niedrig     |
| mkvmerge→FFmpeg    | Ja        | Mittel          | Gut      | Hoch        |
| HLS-Segments       | Optional  | Mittel          | Optimal  | Mittel      |
| Dynam. Transcode   | Nein      | Niedrig         | Perfekt  | Niedrig     |

### Empfehlungen & ToDo
- Batch: Vor Remux prüfen, ob MP4 schon vorhanden/kompatibel (ffprobe).
- Für Docker: FFmpeg/MKVToolNix in einem Container.
- UI-Feedback und Statusanzeige für Streaming ergänzen.
- Testfälle für alle Routing-Varianten.

### Hinweis zu Codecs
Typische Codecs in MKV (H.264/AV1, Subs) entscheiden, ob `-c copy` reicht oder leichte Re-Encode nötig ist.

---
Dieses Logbuch dokumentiert die Bewertung der PIPE-KIT Streaming-Architektur und gibt Empfehlungen für effizientes, browserfreundliches Video-Streaming.
