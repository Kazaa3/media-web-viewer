# Logbuch: Chrome Direct Play – Kompatibilität & Fallback

## Datum
16. März 2026

---

## Chrome Direct Play: Kompatibilitätsmatrix (2026)
| Container | Codecs (Video/Audio)   | Direct Play? | Hinweis         |
|-----------|-----------------------|--------------|-----------------|
| MP4       | H.264 + AAC           | ✅ Voll      | Beste Wahl      |
| WebM      | VP9/AV1 + Opus/Vorbis | ✅ Voll      | Modern, klein   |
| MKV       | H.264 + AAC           | ⚠️ Oft      | Inkonsistent    |
| ISO       | MPEG-2/AC3            | ❌ Nein      | Browser ignoriert|
| TS        | H.264 + AAC           | ⚠️ Mit JS   | HLS/video.js nötig|

- Realität: ~80% der MKV-Library (H.264/AAC) funktionieren, exotische Audio (DTS, TrueHD) oder HEVC scheitern.

---

## Intelligenter Modus: Direct Play Pre-Check
- **Python (ffprobe):**
  - Prüft Container & Codecs
  - "direct_play_perfect": MP4/H.264/AAC → Direct Play
  - "direct_play_maybe": MKV/H.264/AAC → Test, evtl. Buffering
  - "needs_remux": Nicht kompatibel → Remux/Transcode nötig
- **Eel-API:**
  - open_video_smart prüft Kompatibilität und gibt passende URL zurück
  - Fallback zu MediaMTX (HLS) bei Inkompatibilität
- **Frontend:**
  - Zeigt Status "Direct Play ✓" oder "MediaMTX Fallback (kompatibel)"

---

## Fazit & Empfehlung
- Direct Play spart bis zu 90% CPU bei kompatiblen Files
- Pre-Check mit ffprobe automatisiert die Moduswahl
- Default-Fallback: MediaMTX (HLS) für maximale Kompatibilität
- Test-Kommando: ffprobe -v quiet -print_format json -show_streams movie.mkv | jq '.streams[0].codec_name' → "h264"? → Direct Play möglich!

---

## Kommentar
Ctrl+Alt+M

---

*Siehe vorherige Logbuch-Einträge für Details zu Direct Play, Fallback und Streaming-Architektur.*
