# Logbuch Meilenstein: Multi-Tool Configuration & Diagnostics Hub (v1.35.68)

## Ziel
Vollständige Zentralisierung aller Projekt-Tools, Hardware-Diagnostik und Session-Konfigurationen. Die gesamte Infrastruktur ist jetzt aus einer einzigen, environment-aware Registry steuerbar und vollständig beobachtbar.

---

## Umsetzung & Details

### 1. Universal Toolchain Centralization
- **config_master.py:** Registry für alle Spezialtools (mkvmerge, mkvextract, MediaMTX, pyvidplayer2, ...)
- **main.py:** Alle Backend-Funktionen (inkl. fmp4frag, spezialisierte Player) nutzen zentrale Binary-Pfade

### 2. Hardware-Aware Intelligence & Transcoding
- **SSD/HDD Discovery:** Automatische Erkennung des Library-Speichers (NVMe/SSD/HDD) beim Boot
- **GPU Detection:** Sub-Sekunden-Erkennung von NVENC, QSV, VAAPI; automatische Auswahl des besten Hardware-Encoders
- **FragMP4 Settings:** Fragmentierungsdauer für HLS/fMP4 zentralisiert (MWV_FMP4_FRAG)

### 3. App Version & Session Observability
- **Tool Version Tracking:** Automatische Versionserkennung für FFmpeg, VLC, MKVTools; UI zeigt Toolchain-Health
- **Port Synchronization:** Port 8345 nicht mehr hardcodiert; alle Endpunkte und Fehlermeldungen nutzen Registry-Port

### 4. Docker & Linux Storage Parity
- **docker_mode:** Environment-aware db_filename für lokale und Container-Deployments

---

## Zusammenfassung der zentralen Registry
```python
"hardware_info": { "disk_type": "SSD", "pcie_gen": "PCIe 3", "gpu_type": "VAAPI-Generic", ... },
"app_versions":  { "ffmpeg": "5.1.2", "vlc": "3.0.18", "python": "3.12.7", ... },
"transcoding_settings": { "ffmpeg_preset": "veryfast", "hwaccel": "auto", "fmp4_frag": 5000 },
"mediamtx_settings":    { "hls_port": 8888, "webrtc_port": 8889, ... }
```

---

## Ergebnis
Die Infrastruktur ist jetzt vollständig beobachtbar, environment-aware und hochgradig konfigurierbar – alles aus einer einzigen Registry.

---

**Meilenstein abgeschlossen: Multi-Tool Configuration & Diagnostics Hub (v1.35.68)**
