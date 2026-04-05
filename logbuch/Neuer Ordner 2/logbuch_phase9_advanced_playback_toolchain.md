# Logbuch: Phase 9 – Advanced Playback & Toolchain Integration

## Status: In Progress

---

### Backend
- SWYH-RS CLI Bridge in main.py: Implementierung zur Steuerung und Überwachung des swyh-rs-cli-Prozesses.
- MKVcleaver-Style Batch Extraction: Logik für parallele Extraktion von Streams aus mehreren MKV-Dateien mit mkvextract.

### Mode Router
- Erweiterung von mode_router.py um 10+ Playback-Modes (DASH, webtorrent, hls_native, native_chrome, mpv_native, vlc_native, etc.).

### Frontend
- Integration von MPV (WASM/Native) in die Playback-UI für maximale Kompatibilität und Performance.
- Hinzufügen von UI-Controls für SWYH-RS (Audio-Streaming) und Batch Extract (Subtitle/Track Extraction).

---

*Dieses Logbuch dokumentiert die laufende Umsetzung der Advanced Playback & Toolchain Integration in Phase 9.*
