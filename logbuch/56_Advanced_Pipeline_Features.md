# Logbuch-Eintrag: Advanced Pipeline Features & Branch-Specific Config

## Ziel
Erweiterte Pipeline-Features und branch-spezifische Konfiguration für stabile, reproduzierbare Builds und Releases.

## Konzept
- Automatisierte Bereitstellung von branch-spezifischen JSON-Konfigurationsdateien (main vs. develop).
- Hang Protection: Builds/Tests werden bei Hängern oder Zeitüberschreitungen automatisch gestoppt.
- Datenbank-Persistenz: Unterschiedliche Policies für Entwicklungs- und Release-Builds.
- Vollständige Anforderungs-/Testzuordnung für CI/CD.

## Umsetzung
- [MODIFY] `infra/build_system.py`: Branch-Erkennung und Auswahl der passenden Konfigurationsdatei (`web/config.dev.json` vs. `web/config.prod.json`).
- [MODIFY] `monitor_utils.py`, `build_system.py`: Integration von StatusBar und run_monitored für Hang Detection und Fortschrittsanzeige.
- **Database Persistence Policy:**
  - Dev-Builds: Bestehende `data/media_library.db` bleibt erhalten.
  - Release-Builds: Datenbank wird gesäubert oder migriert (je nach Version/Flag).
- **Requirement Mapping:**
  - R1: FFmpeg Reliability → `tests/integration/category/tech/ffmpeg/`
  - R2: UI Stability → `tests/integration/category/ui/test_ui_session_stability.py`
  - R3: Git Integrity → `tests/integration/category/git/test_git_guard.py`
  - R4: Install/Uninstall Hygiene → `tests/e2e/install/test_reinstall_deb.py`
  - R5: Performance Benchmarks → `tests/integration/performance/`
  - R6: Test Suite Reliability → Standardisiertes Root-Path-Discovery (parents[4]), robustere UI-Assertions.

## Status
Abgeschlossen – Pipeline ist branch-spezifisch, robust gegen Hänger und erfüllt alle Zuordnungen.

## Stand
13. März 2026
