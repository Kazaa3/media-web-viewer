# Walkthrough: Advanced ISO & Bitrate Orchestration (v1.46.045)

Die Forensic Media Workstation bietet jetzt gehärtete Unterstützung für High-End-Formate (ISO, Blu-ray, 3D, 4K) und eine globalisierte, konfigurationsgetriebene Bitraten-Logik.

---

## ✅ Was umgesetzt wurde

### Advanced Media Detection
- **Blu-ray:** Der ffprobe_analyzer erkennt Blu-ray-Strukturen (BDMV-Ordner oder ISOs > 20GB) automatisch.
- **3D (Stereo):** Dateien mit 3D-Metadaten (`stereo_mode`, Frame-Packing) werden explizit identifiziert (`is_3d`).
- **PAL/NTSC:** Verfeinerte Frameraten-Erkennung für klassische DVDs.

### Global Bitrate Switches
- Alle Schwellenwerte wurden in das neue Register `bitrate_thresholds_kbps` in der `config_master.py` verschoben:
    - `direct_play_max_kbps: 20.000`
    - `mse_max_kbps: 15.000`
    - `dash_max_kbps: 35.000`
    - `mpv_native_min_kbps: 50.000`
- Jede Anpassung ist nun zentral und ohne Codeänderung möglich.

### Gezieltes Orchestration-Routing
- **VLC-Priorität:** Blu-ray und DVD ISOs werden an die VLC-Engine (`vlc_bridge`) geroutet, um volle Menü-Funktionalität zu erhalten.
- **3D-Routing:** 3D-Medien triggern spezialisierte Orchestrierung für korrekte Darstellung.
- **High-Bitrate 4K:** Assets > 50 Mbps werden automatisch via MPV Native abgespielt.

---

## 🔍 Überprüfung
- **Blu-ray Detection Test:**
    - Input: BDMV-Ordner oder große ISO
    - Trace: `[PLAY-PULSE] smart_route decision: vlc_bridge | Path: ... (v1.46.045)`
    - Status: VLC-Handler korrekt getriggert
- **Global Bitrate Test:**
    - Aktion: `direct_play_max_kbps` auf 10.000 gesenkt
    - Ergebnis: 15 Mbps File wird korrekt zu `mse` oder `hls_fmp4` geroutet
- **4K-Test:**
    - 4K-Asset > 50 Mbps wird automatisch via MPV Native abgespielt
- **Audit-Log:**
    - Jede Routing-Entscheidung zeigt Bitraten und Auflösung im `[PLAY-PULSE]`-Log

---

## Hinweise
- **media_pipeline_registry** ist jetzt die maßgebliche Quelle für alle Orchestrierungs-Flags physischer Medien.
- **Tipp:** Mit dem "PROBE"-Button kann geprüft werden, ob eine Datei als 3D oder Blu-ray erkannt wurde.

---

Weitere Details im Walkthrough v1.46.045. Die Workstation ist nun optimal für High-End-Medien-Forensik gerüstet.
