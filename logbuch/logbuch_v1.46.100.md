# Logbuch: Backend Robustness & Config Centralization (v1.46.099)

## Date: 2026-04-19

---

## Implementation Plan

### Phase 1: Scan Settings & Robustness
#### 1. Centralization in config_master.py
- Added a dedicated `scan_settings` block to `GLOBAL_CONFIG`:
  ```python
  "scan_settings": {
      "max_files": 50000,
      "max_depth": 12,
      "batch_commit_size": 250,
      "log_unsupported_extensions": True
  }
  ```
- All scan-related variables are now centrally managed.

#### 2. Robustness & Logging in main.py
- Replaced hardcoded scan limits in `_scan_media_execution` with values from `GLOBAL_CONFIG["scan_settings"]`.
- Wrapped path-depth and file indexing blocks in try-except structures:
  - Logs exceptions with `log.error()` and includes filename and exception details (`exc_info=True`).
  - Replaced silent `pass` with fallback mechanisms or forensic skipping logs.

#### Open Question
- Soll das erweiterte Traceback-Logging (`exc_info=True`) für alle Scanner-Exceptions aktiviert werden, um den Stacktrace in der Log-Datei zu sehen, oder reicht eine saubere Error-Nachricht ohne Stacktrace?

#### Verification Plan
- **Automated:**
  - Scanner über `main.py` ausführen, Exception provozieren, Log auf detaillierte Fehlermeldung prüfen.
  - Scanner Audit: Prüfen, dass Skip-Flags respektiert werden und keine Abstürze bei korrupten Dateien auftreten.
  - Reporting Audit: Sicherstellen, dass das Storage Forensic Report mit den Scanner-Exklusionen übereinstimmt.

---

### Phase 2: Reporting & Process Robustness (Planned)
#### 1. Centralization Stage 2
- Added `forensic_settings` block to `GLOBAL_CONFIG`:
  ```python
  "forensic_settings": {
      "browser_process_names": ["chrome", "chromium", "electron", "brave", "opera", "msedge"],
      "stream_worker_names": ["ffmpeg", "mkvmerge", "ffprobe"],
      "max_largest_files_report": 15
  }
  ```
#### 2. Alignment & Robustness in api_reporting.py
- Integrated `scan_settings` skip logic into `get_storage_forensics`.
- Improved logging: Replaced `except: pass` with `log.debug` or `log.warning` for unreachable paths.
#### 3. Startup Optimization in main.py
- Refactored `get_startup_info` to use centralized `browser_process_names`.
- Improved error handling in `FRONTEND_PROCESS_ID` resolution.

---

### Phase 3: Parser Robustness & Metadata Limits (Planned)
#### 1. Centralization Stage 3
- Added `parser_limits` block to `GLOBAL_CONFIG`:
  ```python
  "parser_limits": {
      "max_tag_length": 1024,
      "max_chapters": 500,
      "heavy_parser_skip_size_mb": 500,
      "enable_semantic_validation": True
  }
  ```
#### 2. Refactoring media_parser.py
- Fixed undefined constants by pulling from centralized config.
- Replaced hardcoded ISO skip size with `heavy_parser_skip_size_mb`.
- Replaced silent failures with explicit error logging in `get_file_magic` and helpers.
- Added `log.warning` when metadata is truncated or dropped due to limits.

---

## Status
- [x] Phase 1: Scan settings and robustness complete
- [ ] Phase 2: Reporting & process robustness planned
- [ ] Phase 3: Parser robustness & metadata limits planned
- [ ] Entscheidung zu Traceback-Logging offen

---

## Notes
- Diese Maßnahmen erhöhen die Wartbarkeit, Nachvollziehbarkeit und Robustheit des gesamten Backends.
- Rückmeldung zur Traceback-Logging-Strategie erforderlich.
