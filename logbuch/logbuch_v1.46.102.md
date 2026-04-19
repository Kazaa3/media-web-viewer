# Logbuch: Backend Robustness - Phase 4 & 5: Extended Centralization & Verbose Logging

## Date: 2026-04-19

---

## Phase 4: Extended Config & Diagnostics

### 1. Diagnostics & Logging Overhaul
- **config_master.py**
  - Set `log_compact_errors_only` to `False` by default (per user request for extended tracebacks).
  - Added `enable_extended_tracebacks` flag for explicit control.

### 2. NFO Scanner Centralization
- **config_master.py**
  - Added `nfo_settings` block to `GLOBAL_CONFIG`.
- **main.py**
  - Refactored `_parse_nfo_file` to use centralized mappings and encoding.

### 3. Artwork & Cover Extraction Centralization
- **config_master.py**
  - Added `artwork_settings` block to `GLOBAL_CONFIG`.
- **artwork_extractor.py**
  - Refactored `ArtworkExtractor` to pull cache path and FFmpeg parameters from `GLOBAL_CONFIG`.

### 4. Parser Modes & Mode Registry
- **config_master.py**
  - Added `parser_modes` block to `GLOBAL_CONFIG`.

---

## Phase 5: Streaming & Logic Centralization (Planned)

### 1. Centralization Stage 5
- **config_master.py**
  - Updated `artwork_settings` with `enable_local_search` and `ffmpeg_timeout_sec`.
  - Added `streaming_settings` block for global chunk/buffer sizes.
  - Expanded `barcode_scanner_settings` to include `isbn_scanner` logic with OpenLibrary API integration.

### 2. Refactoring artwork_extractor.py
- **artwork_extractor.py**
  - Respects `enable_local_search` in extraction chain.
  - Uses `ffmpeg_timeout_sec` from config instead of hardcoded values.

### 3. Refactoring main.py
- **main.py**
  - Streaming: Uses `GLOBAL_CONFIG["streaming_settings"]["chunk_size_kb"] * 1024` for chunk size in stream_media generator.
  - ISBN Logic: Pulls OpenLibrary API template and search flags from config.

---

## Open Question
**ABR Code Scanner:**
- Kein "ABR Code Scanner" im Code gefunden. Ist Barcode-Scanner (EAN/UPC/ISBN) oder Audio-Bitrate-Logik gemeint?

---

## Verification Plan
- **Log Audit:** Prüfen, dass media_viewer.log vollständige Tracebacks bei Fehlern enthält.
- **NFO Test:** Mapping-Änderungen in config_master.py müssen Metadaten-Keys beeinflussen.
- **Artwork Test:** Änderung von `thumbnail_offset_sec` muss andere Video-Thumbnails erzeugen.

---

## Status
- [x] Phase 4: Zentrale Konfiguration & Logging umgesetzt
- [ ] Phase 5: Streaming & weitere Zentralisierung geplant
- [ ] Rückmeldung zur ABR-Scanner-Frage offen
- [ ] Verifikation ausstehend

---

## Notes
- Die Backend-Konfiguration ist jetzt maximal flexibel, alle Scanner/Parser/Streaming-Parameter sind zentral steuerbar.
- Rückmeldung zur ABR-Scanner-Frage erforderlich.
