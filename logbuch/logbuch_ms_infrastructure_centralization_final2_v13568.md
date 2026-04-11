# Logbuch Meilenstein: Infrastructure Centralization – Final (v1.35.68)

## Ziel
Vollständige Zentralisierung der Media Viewer-Infrastruktur, Kategorisierung, Storage und Toolchain. Die Anwendung ist jetzt vollständig datengetrieben, portabel und für moderne Deployments vorbereitet.

---

## Umsetzung & Details

### 1. Universal Categorization & Routing Hub
- **config_master.py:** MASTER_CAT_MAP, TECH_MARKERS, BRANCH_MAP zentralisiert; alle Routing- und UI-Branching-Regeln sind datengetrieben
- **category_master.py:** Nur noch funktionale Schicht, die Regeln aus dem Registry löst

### 2. Streaming & Environment Stability
- **Capability Matrix:** 7-Engine-Streaming-Matrix zentralisiert, UI kann Feature-Set direkt abfragen
- **PIP Registry:** Bootzeit-Discovery aller installierten Python-Pakete, via Eel für Remote-Diagnose
- **Normalization Hub:** Codec-, Container- und Tag-Maps zentralisiert, konsistente Benennung in der gesamten Indexing-Chain

### 3. Storage & Path Portability
- **Storage Registry:** Absolute Pfade für /data/ (DB, Logs) und /media/ (Library) zentralisiert, volle Docker-Kompatibilität
- **db.py:** Nutzt konfigurierbare legacy_db_candidates-Liste für DB-Cleanup

### 4. Automated Hardware & Toolchain Observation
- **Dynamic Discovery:** SSD/HDD und GPU-Transcoding (VAAPI, NVENC, QSV) werden bei jedem Boot erkannt
- **Binary Parity:** Versionstracking für VLC, MPV, FFmpeg, MKVTools im globalen Config-Objekt

---

## Final Verification Result
- [x] Category Sync: Routing erfolgt über zentrale Registry
- [x] Storage Sync: DB- und Media-Pfade entsprechen lokalen Overrides
- [x] Metadata Sync: Parser nutzen zentrale Magic-Byte-Signaturen
- [x] Version Sync: App identifiziert sich überall als v1.35.68

---

## Ergebnis
Die Media Viewer Suite ist jetzt vollständig portabel, datengetrieben und mit modernster Infrastruktur ausgestattet.

---

**Meilenstein abgeschlossen: Infrastructure Centralization – Final (v1.35.68)**
