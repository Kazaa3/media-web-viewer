# Logbuch Meilenstein: Infrastructure Centralization (v1.35.68)

## Ziel
Vollständige Zentralisierung der Media Viewer-Infrastruktur. Die Anwendung ist jetzt vollständig datengetrieben, portabel und für robuste Deployments vorbereitet.

---

## Umsetzung & Details

### 1. Universal Configuration Hub (config_master.py)
- **Parser & Extension Registry:** Jede Extension explizit im globalen Registry gemappt
- **Streaming Capability Matrix:** 7-Engine-Matrix (Chrome Native, MediaMTX, VLC, mkvmerge, ffplay, swyh-rs, PyPlayer) zentralisiert
- **Normalization Hub:** codec_map, container_map, tag_type_map zentralisiert; alle Standardisierungen laufen über eine Quelle
- **PIP Package Discovery:** Bootzeit-Registry für installierte Python-Pakete
- **Hardware & Versioning:** Automatische Erkennung von SSD/HDD, GPU-Accelerators, Toolchain-Versionen (FFmpeg, VLC, MPV)

### 2. Storage & Library Centralization
- **Storage Registry:** Absolute Pfade für /data/ und /media/ zentralisiert, volle Docker/Linux-Portabilität
- **db.py:** Alle DB- und Legacy-Pfade (get_legacy_db_candidates) aus Registry
- **format_utils.py:** Nutzt globale Normalisierungsmaps, Spezialhandler für Ambiguitäten erhalten
- **main.py:** Exportiert Capability- und Package-Registry via Eel

### 3. Build System Synchronization
- **build_config.py:** Single Source für VERSION, PACKAGE_NAME, RSYNC_EXCLUDES
- **Zero-Leak Pipeline:** Build Test Gate & Distribution-Excludes zentralisiert für saubere Releases

---

## Final Verification Result
- [x] Metadata Parity: Alle Parser matchen Extension-Map
- [x] Path Integrity: /data/ und /media/ werden überall korrekt aufgelöst
- [x] Version Sync: App identifiziert sich überall als v1.35.68

---

## Ergebnis
Die Media Viewer App ist jetzt vollständig datengetrieben, von Hardcodings entkoppelt und bereit für produktive Deployments.

---

**Meilenstein abgeschlossen: Infrastructure Centralization (v1.35.68)**
