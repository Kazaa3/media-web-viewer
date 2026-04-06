# Implementation Plan: Centralized Build Orchestration & Version Hardening (v1.35.68)

## Ziel
Zentralisierung des Build-Test-Gates und Synchronisierung des Projekt-Versionsstandes, damit Tests und Packaging immer die aktuellen Metadaten aus dem Core nutzen.

---

## Maßnahmen & Architektur

### 1. Centralized Test Orchestration
- **build_config.py:**
  - BUILD_GATE_TESTS-Liste als Single Source für Pre-Build-Checks
  - RSYNC_EXCLUDES für "Zero-Leak Mode" zentralisiert
- **infra/build_system.py:**
  - BUILD_TEST_GATE und _read_version importieren Konstanten aus build_config.py
- **infra/build_deb.sh:**
  - rsync-Excludes und pytest-Loop lesen aus build_config.py

### 2. Version Hardening
- **infra/VERSION_SYNC.json:**
  - Basisversion auf 1.35.68 aktualisiert
  - sync_locations für v1.35-Struktur geprüft
- **scripts/update_version.py:**
  - Liest Zielversion aus zentraler VERSION-Datei, falls kein Argument

### 3. Startup & Build Trigger
- **scripts/fast_build_deb.sh:**
  - Ruft update_version.py explizit vor dem Build auf, damit alle Metadaten (Desktop, control) aktuell sind

---

## Offene Frage
- Sollen MWV_WIDTH/MWV_HEIGHT-Defaults auch in DEBIAN/postinst zentralisiert werden oder rein env-gesteuert bleiben?

---

## Verifikation
- **Automatisiert:**
  - python3 scripts/update_version.py --new-version 1.35.69 --dry-run prüft alle Sync-Locations
  - infra/build_deb.sh nutzt zentralisierte Testliste
- **Manuell:**
  - ./build.sh ausführen
  - .deb-Metadaten prüfen (dpkg-deb -I ...) auf Version-Parität

---

**Plan bereit zur Ausführung: Centralized Build Orchestration & Version Hardening (v1.35.68)**
