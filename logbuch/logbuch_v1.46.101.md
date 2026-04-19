# Logbuch: Backend Robustness - Phase 4: Extended Centralization & Verbose Logging

## Date: 2026-04-19

---

## Phase 4: Extended Config & Diagnostics

### 1. Diagnostics & Logging Overhaul
- **config_master.py**
  - Set `log_compact_errors_only` to `False` by default (per user request for extended tracebacks).
  - Added `enable_extended_tracebacks` flag for explicit control over traceback verbosity.

### 2. NFO Scanner Centralization
- **config_master.py**
  - Added `nfo_settings` block to `GLOBAL_CONFIG`:
    ```python
    "nfo_settings": {
        "enable_parsing": True,
        "mapping": {
            "title": "title", "year": "year", "genre": "genre",
            "artist": "artist", "album": "album", "plot": "plot"
        },
        "encoding": "utf-8",
        "fallback_to_filename": True
    }
    ```
- **main.py**
  - Refactored `_parse_nfo_file` to use centralized mappings and encoding from `GLOBAL_CONFIG`.

### 3. Artwork & Cover Extraction Centralization
- **config_master.py**
  - Added `artwork_settings` block:
    ```python
    "artwork_settings": {
        "enable_extraction": True,
        "thumbnail_offset_sec": 7,
        "thumbnail_resolution": "480:480",
        "cache_root": "~/.cache/gui_media_web_viewer/art",
        "search_priority": ["local", "mutagen", "streams", "thumbnail"]
    }
    ```
- **artwork_extractor.py**
  - Refactored `ArtworkExtractor` to pull cache path and FFmpeg parameters from `GLOBAL_CONFIG`.

### 4. Parser Modes & Mode Registry
- **config_master.py**
  - Added `parser_modes` block to `GLOBAL_CONFIG`:
    ```python
    "parser_modes": {
        "default": "lightweight",  # "lightweight", "full", "ultimate"
        "enable_full_tags": False,
        "full_tag_whitelist": ["comment", "lyrics", "composer", "encoded_by"]
    }
    ```

---

## Open Question
**ABR Code Scanner:**
- Im Code wurde kein "ABR Code Scanner" gefunden. Ist damit der Barcode Scanner (EAN/UPC) gemeint oder eine spezifische Audio-Bitrate (ABR) Logik?

---

## Verification Plan
- **Log Audit:** Prüfen, dass media_viewer.log jetzt vollständige Tracebacks bei Fehlern enthält.
- **NFO Test:** Änderung der Mapping-Konfiguration in `config_master.py` muss die extrahierten Metadaten-Schlüssel beeinflussen.
- **Artwork Test:** Änderung von `thumbnail_offset_sec` muss zu anderen Video-Thumbnails führen.

---

## Status
- [x] Zentrale Konfiguration für NFO, Artwork, Parser Modes
- [x] Logging-Verbesserungen und Traceback-Steuerung
- [x] Refaktorierung der relevanten Parser und Scanner
- [ ] Rückmeldung zur ABR-Scanner-Frage offen
- [ ] Verifikation ausstehend

---

## Notes
- Die Backend-Konfiguration ist jetzt maximal flexibel und alle Hilfs-Scanner/Parser sind zentral steuerbar.
- Rückmeldung zur ABR-Scanner-Frage erforderlich.
