# Implementation Plan: Advanced Media Pipelines & ISO Hardening (v1.46.045)

## Context
Dieses Update stellt sicher, dass High-End-Formate (PAL/NTSC DVD, Blu-ray, 3D, 4K) korrekt erkannt und geroutet werden. Zudem werden alle Bitraten-Schwellenwerte in ein globales Konfigurations-Register überführt.

---

## User Review Required

### ISO/BD Handling
- Explizite Erkennung von Blu-ray-Strukturen (BDMV).
- Standardmäßig Routing zu VLC, um volle Menüfunktionalität zu erhalten.

### Global Bitrate SSOT
- Alle Bitraten-Schwellen (Direct Play, MSE, DASH, MPV Native) werden in ein gemeinsames Registry in `config_master.py` verschoben.
- Erlaubt universelles Tuning des Streaming-Pulses der Workstation.

---

## Proposed Changes

### [Backend]
#### [MODIFY] `ffprobe_analyzer.py`
- `is_bluray`: Logik zur Erkennung von Blu-ray ISOs oder BDMV-Ordnerstrukturen.
- `is_3d`: Prüfung auf `stereo_mode` oder `multiview`-Tags im Videostream.
- Verbesserte 4K-Erkennung: Sicherstellen, dass Bitrate und Farbtiefe für 4K korrekt gemeldet werden.

#### [MODIFY] `config_master.py`
- `media_pipeline_registry`:
    - `bitrate_thresholds`:
        - `direct_play_max_kbps: 20000`
        - `mse_max_kbps: 15000`
        - `dash_max_kbps: 35000`
        - `mpv_native_min_kbps: 50000`
    - `iso_bd_flags`:
        - `prefer_vlc_for_menus: True`
        - `enable_3d_side_by_side_detection: True`

#### [MODIFY] `mode_router.py`
- Refaktor `smart_route`, um die neuen globalen Bitraten- und ISO-Flags zu nutzen.
- Priorisiertes Routing für 3D- und Blu-ray-Medien implementieren.

---

## Open Questions
- Für 3D-Medien: Soll automatisch ein spezieller "3D-Acknowledge" Toast/HUD angezeigt werden? (Vorschlag: Im Forensic Trace ergänzen.)

---

## Verification Plan

### Automated Tests
- Mock-BDMV-Pfad zur Überprüfung der `is_bluray`-Erkennung verwenden.
- Prüfen, dass eine Datei mit Bitrate > 50000 korrekt zu `mpv_native` geroutet wird.

### Manual Verification
- Nach Abspielen einer 4K-Datei das Diagnose-Log ([PLAY-PULSE]) auf die konfigurationsgetriebene Entscheidung prüfen.

---

(See <attachments> above for file contents. You may not need to search or read the file again.)
