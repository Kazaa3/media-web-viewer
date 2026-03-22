# Logbuch-Eintrag 51: Refined Conda Dependency Resolution & Build 1.3.1

## Status
**Datum:** 2026-03-08  
**Version:** 1.3.1  
**Status:** ✅ Abgeschlossen  

## Änderungen

### 1. Drei-Listen-Abhängigkeitserkennung
- Refactor von `env_handler.py` zur Rückgabe von drei Listen: `missing_pip`, `missing_apt` und `missing_conda`.
- Implementierung eines intelligenten Name-Mappings für Conda (z.B. `libgdk-pixbuf2.0-0` -> `gdk-pixbuf`).
- Unterstützung für den `--list-missing-conda` Flag in `check_environment.py`.

### 2. Conda-optimiertes Setup (`run.sh`)
- Das Setup-Skript `run.sh` erkennt nun aktive Conda-Umgebungen.
- Alle fehlenden Abhängigkeiten werden in einem einzigen `conda install -y -c conda-forge` Befehl installiert, was die Konsistenz der Umgebung erhöht.
- Automatische Übersetzung von System-Binary-Namen in Conda-Package-Namen.

### 3. Build & Release v1.3.1
- Update der Version auf **1.3.1** in allen relevanten Dateien (`VERSION`, `main.py`, `control`, `DOCUMENTATION.md`).
- Erfolgreicher Build des Debian-Pakets: `media-web-viewer_1.3.1_amd64.deb`.
- Verifizierung der Build-Integrität (Meta-Tests).

## Bekannte Probleme / Ausblick
- Build-Integritäts-Tests schlagen lokal fehl, wenn die Test-Umgebung selbst nicht alle Abhängigkeiten (`m3u8`, `python-vlc`, etc.) installiert hat. Dies ist bei einer sauberen Neuinstallation durch `run.sh` jedoch behoben.
- Nächster Fokus: Weitere UI-Optimierungen für die Anzeige der nachinstallierten Abhängigkeiten.
