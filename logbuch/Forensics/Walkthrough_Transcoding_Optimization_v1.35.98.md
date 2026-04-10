# Walkthrough - Transcoding Optimization (v1.35.98)

ALAC- und WMA-Audio-Transcodierung wurden vollständig wiederhergestellt und optimiert. Das System trennt jetzt strikt zwischen Audio- und Video-Transcoding, um maximale Performance und korrekte Browser-Kompatibilität zu gewährleisten.

---

## Changes Made

### [Component: Data Models]
**models.py**
- **Fixed Identity Logic:** Die Erkennung des `is_transcoded`-Flags in `MediaItem.to_dict` nutzt jetzt `self.path.suffix` statt des fehlerhaften `self.type`-Felds.
- **ALAC/WMA Awareness:** ALAC (.m4a/.alac) und WMA (.wma) werden explizit für Spezialbehandlung erkannt.

### [Component: Configuration]
**config_master.py**
- **New Profiles:** `transcode_audio_flac` (für ALAC-Quellen) und `transcode_audio_wma` (Opus/WebM für WMA-Quellen) zu `GLOBAL_CONFIG` hinzugefügt.

### [Component: Streaming Engine]
**main.py**
- **Pre-calculated Metadata:** Die Erkennung von Audio-/Video-Typen und Profilen wurde aus dem ffmpeg_stream-Generator ausgelagert, um Scope-Probleme zu lösen und Lookup zu beschleunigen.
- **Strict Performance Branching:** Audio-Only-Streams umgehen jetzt jegliche Video-Logik und nutzen `-vn` sowie dedizierte Audiocodecs (FLAC/Opus/AAC).
- **Dynamic Content-Type:** Der Server liefert jetzt den korrekten Content-Type-Header (z.B. audio/flac, audio/webm) je nach Zielcodec, was fehlerfreie Browser-Wiedergabe garantiert.

---

## Verification Results
- **ALAC to FLAC:** .m4a und .alac triggern jetzt korrekt das `transcode_audio_flac`-Profil.
- **WMA to Opus:** .wma triggert das `transcode_audio_wma`-Profil (Opus/WebM).
- **Header Integrity:** Content-Type wird dynamisch auf audio/flac (verlustfrei) oder audio/webm (WMA→Opus) gesetzt.

**TIPP:**
Diese Refaktorierung reduziert die CPU-Last beim Audio-Streaming deutlich, da der Video-Encoder für reine Audio-Assets nie initialisiert wird.

---

## Large File Protection System (Neu)
- **Resource Guard:** Neue `large_file_settings` in `config_master.py`.
- **Automatic Enforcement:** `apply_large_file_protection` in `main.py` überwacht Dateigrößen (Schwelle: 4GB) und passt Transcoding-Parameter automatisch an (z.B. Mindest-CRF 28), um CPU/IO-Stalls bei großen Dateien zu verhindern.
- **Hook System:** Modularer Hook für weitere Schutzmechanismen (z.B. Remuxing statt Transcoding).

---

## Permanent Test Suite
- **Location:** Funktionaler Testskript: `tests/functional/transcode_verify.py`
- **Coverage:** Prüft die gesamte Pipeline für WMA, ALAC, Direct MP4 und ISO/DVD-Transcoding mit nicht-blockierenden Subprozessen (Timeout: 5s).
- **Run:** `python3 tests/functional/transcode_verify.py`

---

Weitere Details siehe aktualisiertes Walkthrough und Implementation Plan.