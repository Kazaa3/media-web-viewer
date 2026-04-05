# Implementation Plan — Scanner Restoration (v1.35.47)

## Overview
The Database Discovery (v1.35.46) confirmed the database file exists but is empty. Analysis of `main.py` suggests the Scanner may be skipping files due to a configuration mismatch in the "Extension Filter."

## 🛠️ Key Goals
- **Audit indexed_categories:**
  - Ensure the scanner is configured to look for "audio" and "video". If `PARSER_CONFIG` is empty, force robust defaults.
- **Verify AUDIO_EXTENSIONS:**
  - Confirm that `.mp3`, `.ogg`, `.flac`, and `.m4a` are included in the backend's `format_utils.py` extension lists.
- **Discovery Log:**
  - Add a log entry for every file discovered by the scanner, even if not indexed: `[DISCOVERED] path/to/file.mp3 (Category: ???)`.
- **Config Resilience:**
  - Add a safety catch in `main.py` so that if no categories are enabled, it defaults to `["audio", "video"]`.

## 📂 Files to Audit/Modify
- `src/core/main.py`: Add discovery logs and category defaults.
- `src/parsers/format_utils.py`: Verify extension white-lists.
- `config/settings.json` (if exists): Check for restrictive scan filters.

## 🧪 Expected Outcome
- On next boot, the DATA-HUD will show "SCANNING" and logs will list discovered files.
- Once extensions are mapped, real items will populate the BACKEND DB count.

---

*This plan will restore scanner functionality and ensure robust, transparent file discovery for all supported media types.*
