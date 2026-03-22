# Logbuch Eintrag 55: CI/CD Integration und Build Watchdog (v1.34)

**Datum:** 13. März 2026  
**Status:** Abgeschlossen ✅  
**Thema:** Automatisierung der Build-Pipeline und Absicherung gegen Prozess-Hänger.

## 1. Problemstellung
Mit dem Anwachsen des Projekts und der Komplexität der Build-Schritte (PyInstaller, Debian Packaging) kam es vermehrt zu:
- **Silent Hangs**: Prozesse blieben ohne Fehlermeldung hängen (z.B. bei fehlenden Berechtigungen oder rekursiven Dateisystem-Operationen).
- **Inkonsistenz**: Lokale Builds unterschieden sich von CI-Builds auf GitHub durch unterschiedliche Skripte (`build_deb.sh` vs. `build_exe.sh`).
- **Manueller Aufwand**: Die Verteilung der Artefakte (Binary, DEB) war nicht vollständig automatisiert.

## 2. Die Lösung: Build Watchdog & Unified Pipeline
Es wurde ein zentrales Monitoring-System (`monitor_utils.py`) implementiert, das nun in `infra/build_system.py` integriert ist.

### Key Features:
- **Watchdog-Monitoring**: Jeder kritische Build-Schritt wird von einem Watchdog überwacht. Erfolgt über einen Zeitraum von X Sekunden keine Ausgabe, wird der Prozessbaum automatisch beendet (Kill-Switch).
- **Unified Build Interface**: Statt vieler Einzelskalepte wird nun alles über `./.venv_build/bin/python infra/build_system.py --build all --monitor` gesteuert.
- **Environment Propagation**: Automatische Weitergabe von `PYTHONPATH` und anderen Variablen an alle Sub-Prozesse, um `ModuleNotFoundError` in Tests und Benchmarks zu verhindern.

## 3. GitHub Actions Integration
Die Workflows wurden modernisiert:
- **`ci-artifacts.yml`**: Baut bei jedem Push auf `main` automatisch linux-binaries und .deb Pakete und lädt sie als Artefakte hoch.
- **`release.yml`**: Erstellt bei einem Versions-Tag automatisch ein GitHub Release mit allen Binaries (Linux EXE, Windows EXE, Debian Package).

## 4. Validierung
Die Pipeline wurde erfolgreich lokal und in der Cloud validiert:
- **Transcoding Benchmarks**: 11/11 Tests bestanden.
- **Build-Stabilität**: Erfolgreiche Erstellung von `MediaWebViewer-1.34` unter 48MB.
- **Auto-Install**: Der `--install` Flag im Build-System sorgt für eine sofortige Aktualisierung des Systems nach erfolgreichem Build.

---
**Nächste Schritte:** 
- Erweiterung des Release-Prozesses um automatische Changelog-Generierung.
- Integration von Docker-Builds für isolierte Testumgebungen.
