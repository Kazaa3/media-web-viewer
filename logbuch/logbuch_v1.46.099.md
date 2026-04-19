# Logbuch: Backend Robustness & Config Centralization

## Date: 2026-04-19

---

## Implementation Plan

### 1. Centralization in config_master.py
- Defined a dedicated `scan_settings` core dictionary block inside `GLOBAL_CONFIG`:
  ```python
  "scan_settings": {
      "max_files": 50000,
      "max_depth": 12,
      "batch_commit_size": 250,
      "log_unsupported_extensions": True
  }
  ```
- All scan-related variables are now adjustable from a single location in the backend config.

### 2. Robustness & Logging in main.py
- Replaced hardcoded limits in `_scan_media_execution` with values from `GLOBAL_CONFIG["scan_settings"]`.
- Wrapped the path-depth calculation block in a try-except structure that explicitly catches and logs `Exception as e` using `log.error()`.
- Wrapped the file indexing block (which populates `collected_items`) in an explicit try-except block that logs the exact filename and exception message using `log.error("[Scan-Error] Failed to index {filename}: {e}", exc_info=True)`.
- Replaced silent `pass` statements with fallback mechanisms or forensic skipping logs.

---

## Open Question
**Soll das erweiterte Traceback-Logging (`exc_info=True`) für alle Scanner-Exceptions aktiviert werden, um den genauen Stacktrace in der Log-Datei zu sehen, oder reicht eine saubere Error-Nachricht ohne Stacktrace, um die Logs kleiner zu halten?**

---

## Verification Plan
- **Automated Tests:**
  - Führe den Scanner über `main.py` aus.
  - Provoziere eine Scanner-Exception (z.B. Berechtigungsfehler auf einem Ordner) und überprüfe die `media_viewer.log` auf die detaillierte Fehlermeldung.
- **Manual Verification:**
  - Sicherstellen, dass im UI der Scan weiterhin makellos funktioniert und bei kaputten Dateien der Scan-Prozess nicht mehr stumm stirbt, sondern die Datei sauber überspringt und loggt.

---

## Status
- [x] Scan-Settings zentralisiert
- [x] Robuste Fehlerbehandlung und Logging implementiert
- [ ] Entscheidung zu Traceback-Logging offen
- [ ] Verifikation ausstehend

---

## Notes
- Diese Änderungen erhöhen die Wartbarkeit und Nachvollziehbarkeit des Scan-Prozesses erheblich.
- Rückmeldung zur Traceback-Logging-Strategie erforderlich.
