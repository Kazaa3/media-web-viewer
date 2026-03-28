# Eel Exposed Function Audit

## Übersicht

Diese Reporting-Ansicht dokumentiert alle mit `@eel.expose` versehenen Funktionen in der Anwendung und gibt einen Überblick über die API-Struktur, Redundanzen und Optimierungsempfehlungen.

---

## Gesamtzahl der @eel.expose-Funktionen in src/core/main.py

**169**

---

## Functional Overview

Die Anwendung stellt eine umfangreiche API für Medienverwaltung, Wiedergabe und Systemdiagnostik bereit.

### Key Categories

- **Playback Control:**
  - play_media, open_video, vlc_seek, vlc_ts_mode, next_in_playlist, prev_in_playlist
- **Library Management:**
  - scan_media, get_library, add_file_to_library, delete_media, rename_media
- **Configuration:**
  - get_startup_config, update_startup_config, set_language, set_app_mode
- **Diagnostics:**
  - check_ui_integrity, run_tests, get_system_stats_static, rtt_ping
- **MKV/ISO Tools:**
  - mkv_batch_extract, remux_mkv_batch, extract_main_from_iso

---

## Detected Redundancies/Duplicates

| Function Name   | Location         | Issue                                      |
|----------------|------------------|--------------------------------------------|
| analyse_media  | main.py#4353     | Legacy synchronous analysis mode.          |
| analyze_media  | main.py#7739     | Modern asynchronous routing-focused analysis. |
| getTabButton   | app.html#2662 / #8611 | Duplicated JS definition. (To be removed). |

---

## Recommendation

- Konsolidiere `analyse_media` in den modernen Handler `analyze_media`.
- Entferne die doppelte Definition von `getTabButton` an Zeile 8611 in app.html.

---

*Diese Ansicht dient als Referenz für API- und Code-Audits sowie für die weitere Optimierung der Eel-Exposed-Funktionen.*
