# Logbuch Meilenstein: Infrastructure Centralization (v1.35.68)

## Ziel
Vollständige Zentralisierung der Infrastruktur, Parser-Engine und Storage-Management. Die Media Viewer-Architektur ist jetzt vollständig datengetrieben, environment-aware und für robuste Deployments vorbereitet.

---

## Umsetzung & Details

### 1. Universal Configuration Hub (config_master.py)
- **Streaming Capability Matrix:** Engine-Level-Matrix (Chrome, MediaMTX, VLC, ...) zentralisiert und via eel.get_streaming_capability_matrix() ans Frontend exportiert
- **PIP Package Registry:** Automatische Discovery aller installierten Python-Pakete, API: eel.get_installed_packages()
- **Normalization Maps:** codec_map, container_map, tag_type_map zentralisiert; alle Format-Standardisierungen laufen über eine Quelle

### 2. Storage & Library Centralization
- **Storage Registry:** Absolute Pfade für /data/ und /media/ zentralisiert
- **db.py:** nutzt zentrale db_path und data_dir
- **format_utils.py:** get_default_scan_dir() zeigt auf zentrales media_dir

### 3. Parser & Extension Engine
- **Full Parser Mapping:** Jede Extension ist explizit im globalen Config gemappt
- **Ambiguity Handling:** Spezialhandler für matroska/webm und id3/wav-Fallbacks erhalten, Primärmappings im Registry
- **Hardware Discovery:** SSD/HDD und GPU-Info beim Boot in global config integriert

### 4. Project-Wide Parity
- **Port 8345:** Vollständig zentralisiert in allen Diagnosen und Services
- **build_config.py:** (v1.35.68) synchron mit Runtime-Umgebung

---

## Verification Matrix
- [x] Config Integrity: Alle Maps (codec, container, tag) korrekt befüllt
- [x] API Coverage: Eel-Endpunkte für Capabilities & Packages aktiv
- [x] Path Consistency: DB- & Media-Pfade entsprechen User-Overrides
- [x] Toolchain Versioning: MPV, FFmpeg, VLC werden dynamisch getrackt

---

## Ergebnis
Die Media Viewer App ist jetzt vollständig datengetrieben, zentral konfigurierbar und bereit für den produktiven Einsatz in Linux- und Docker-Umgebungen.

---

**Meilenstein abgeschlossen: Infrastructure Centralization (v1.35.68)**
