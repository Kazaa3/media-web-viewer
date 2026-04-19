# Implementation Plan: Ultimate Forensic Steering Matrix (v1.46.052)

## Context
Dieses Update modernisiert die Orchestrierungs-Hierarchie, indem es die alten Flags für physische Medien durch eine einheitliche, granulare Steering-Matrix ersetzt, die Auflösung, Frequenz und Interlacing berücksichtigt.

---

## User Review Required

### WARNING: Legacy Removal
- Die folgenden Keys werden aus `config_master.py` entfernt:
    - dvd_ntsc_routing
    - dvd_pal_routing
    - bd_standard_routing
    - bd_3d_routing
    - bd_4k_routing
    - hevc_force_transcode_on_hd
- Sie werden durch die neue "Ultimate Steering Matrix" ersetzt.

---

## Proposed Changes

### [Core] Configuration & Routing
#### [MODIFY] `mode_router.py`
- **Audio Bypass:**
    - Früher Return für Audio-Dateien, damit diese immer `direct_play` nutzen und Video-Steering umgehen.
- **Refined Selection Logic:**
    - Dynamische Generierung von Auflösungs-Keys mit Scanning-Suffixen (p vs i).
    - Top-Down-Priorität:
        1. Safety (4K HEVC Hardware Guard)
        2. Special Format (3D Sonderfall)
        3. Frequency Master (PAL/NTSC Master Profiles)
        4. Manual Matrix (Granulare Resolution- & Codec-Steuerung)
        5. Heuristics (Bitratenbasierte Fallbacks)
- **Consolidation:**
    - Redundante Variablen und Legacy-Conditional-Blocks entfernen.

---

## Verification Plan

### Automated Tests
- `python3 src/core/main.py` (Config-Integrität prüfen)
- `smart_route`-Mapping für folgende Mock-Files prüfen:
    - DVD-PAL-I (sollte `pal_50hz` oder `720i` folgen)
    - 1080i H.264 (sollte `1080i`-Policy folgen)
    - 3D Blu-ray (sollte `3d`-Policy folgen)

### Manual Verification
- 1080i-Steering auf "mse" setzen
- 1080i-Datei abspielen
- Im Log prüfen: `Reason: Manual Resolution Steering (1080i -> mse)`

---

(See <attachments> above for file contents. You may not need to search or read the file again.)
