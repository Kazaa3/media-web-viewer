# Implementation Plan: Forensic Media Orchestration & Granular Logging (v1.46.047-REV1)

## Context
Dieses Update erweitert die Orchestrierungs-Engine des Media Viewers um granulare Steuerung für physische Medien (DVD/Blu-ray) und High-End-Formate (4K/HEVC). Das Logging-System wird für eine lückenlose Audit-Trail-Transparenz ausgebaut.

---

## User Review Required

### Decision Steering
- Separate Flags für "Menu" vs. "Transcode"-Modi für DVD (NTSC/PAL) und Blu-ray (3D/4K) in `config_master.py`.
- Ermöglicht gezieltes Routing: z.B. VLC (Menu) für PAL, MSE (Transcode) für NTSC.

### 4K HEVC Policy
- Neues Flag: `hevc_force_transcode_on_4k`.
- Wenn aktiviert, werden 4K HEVC-Dateien immer transkodiert, auch wenn die Bitrate Direct Play zulassen würde – für forensische Zuverlässigkeit auf schwacher Hardware.

---

## Proposed Changes

### [Component] Core Configuration
#### [MODIFY] `config_master.py`
- `media_pipeline_registry` um folgende Flags erweitern:
    - `dvd_ntsc_routing`: "menu" | "transcode"
    - `dvd_pal_routing`: "menu" | "transcode"
    - `bd_standard_routing`: "menu" | "transcode"
    - `bd_3d_routing`: "menu" | "transcode"
    - `bd_4k_routing`: "menu" | "transcode"
    - `hevc_force_transcode_on_4k`: True | False

### [Component] Media Analysis
#### [MODIFY] `ffprobe_analyzer.py`
- Erweiterte Forensik:
    - `is_hevc`-Flag
    - `is_4k_bd`-Erkennung
    - `is_interlaced`-Erkennung
    - Explizite `media_subtype`-Tags (z.B. DVD-NTSC, BD-3D)
    - `[Analyzer-Pulse]`-Logging für alle Erkennungsergebnisse

### [Component] Playback Orchestration
#### [MODIFY] `mode_router.py`
- Granulare Steuerlogik:
    - Berücksichtigt die neuen NTSC/PAL- und BD-Typ-Flags
    - Erklärt die Entscheidungslogik im `[PLAY-PULSE]`-Log
    - Beispiel: `[PLAY-PULSE] Route: vlc_bridge | Reason: NTSC-DVD detected and dvd_ntsc_routing is set to menu.`

### [Component] Forensic Logging
#### [MODIFY] `db.py`
- `[BD-AUDIT]`-Logging für Media-Insert/Update um neue Forensik-Tags (Subtype/FPS/Codec/FieldOrder) erweitern

#### [MODIFY] `main.py`
- Alle Streaming-Routen (`/stream/via/...`) loggen den finalen forensischen Subtyp

---

## Open Questions
- Soll zwischen Interlaced (i) und Progressive (p) für PAL/NTSC-DVDs unterschieden werden? (Vorschlag: Ja, da dies die Transcoding-Qualität beeinflusst)

---

## Verification Plan

### Automated Tests
- `analyze_media` auf NTSC- und PAL-ISOs laufen lassen und `media_subtype` sowie `is_interlaced` prüfen
- Sicherstellen, dass `smart_route` das korrekte Engine-Routing gemäß den neuen Flags auswählt

### Manual Verification
- Im `media_viewer.log` den erweiterten `[PLAY-PULSE]`-Audit-Trail bei 4K HEVC-Playback prüfen

---

(See <attachments> above for file contents. You may not need to search or read the file again.)
