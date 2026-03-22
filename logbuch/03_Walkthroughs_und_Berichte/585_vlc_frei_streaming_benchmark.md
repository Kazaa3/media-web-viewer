# Logbuch: VLC-freie Streaming-Modi & Benchmarking-Plan

## Datum
16. März 2026

---

## Übersicht: VLC-freie Streaming-Modi
- **ffmpeg FragMP4**: On-the-fly MP4-Streaming mit HTTP Range, Seeking, 100% browserkompatibel.
- **ffmpeg HLS**: Segmentiertes HLS-Streaming, kompatibel mit allen Browsern (über .m3u8).
- **mkvmerge Direct**: Schnelles Remux zu MP4, dann Direct Play via /direct/.
- **mkvmerge Pipe**: On-Demand-Remux, Streaming als MP4 (Batch-Tool, weniger für Live).

---

## Neuer Workflow
- "Öffnen mit"-Menü bietet alle Modi (FragMP4, HLS, mkvmerge Direct, mkvmerge Pipe, MediaMTX, Direct Play).
- Keine VLC-Abhängigkeit mehr nötig – alle Streams laufen über ffmpeg/mkvmerge.
- Fallback-Logik: Direct Play → FragMP4 → HLS → MediaMTX.

---

## Benchmarking-Plan
- **Ziel:** Alle Modi (FragMP4, HLS, mkvmerge Direct/Pipe, MediaMTX, Direct Play) auf CPU-Last, Startzeit, Seeking, Kompatibilität testen.
- **Metriken:**
  - CPU-Auslastung (Server/Client)
  - Startzeit (bis erster Frame)
  - Seek-Latenz (100MB/1GB File)
  - Kompatibilität (Chrome, Firefox, Edge)
  - Stabilität bei langen Streams
- **Testfälle:**
  - MP4 (H.264/AAC), MKV (H.264/AAC), ISO (DVD), WebM (VP9/Opus)
  - Netzwerk (SMB/NFS) vs. lokale SSD/HDD

---

## Empfehlung
- Alle Modi parallel anbieten und im Benchmark vergleichen.
- Ergebnisse im Logbuch dokumentieren, um den optimalen Default-Modus zu bestimmen.

---

## Kommentar
Ctrl+Alt+M

---

*Siehe vorherige Logbuch-Einträge für Details zu Direct Play und Streaming-Architektur.*
