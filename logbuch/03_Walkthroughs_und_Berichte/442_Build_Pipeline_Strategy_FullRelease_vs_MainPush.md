# Projekt: Media-Web-Viewer
# Logbuch-Eintrag: Build Pipeline Strategy & Implementation Details

**Datum:** 13.03.2026
**Autor:** Copilot

## Kontext
Die Infrastruktur des Media Web Viewer wurde um eine differenzierte Build-Strategie erweitert. Ziel ist die Balance zwischen schneller CI-Validierung bei jedem Push und einer gründlichen Qualitätsprüfung vor jedem Release.

## Pipeline-Modi

### 1. Main Push / CI Mode (Minutely/Daily)
- **Frequenz**: Bei jedem Commit auf `main` oder `develop`.
- **Eigenschaften**: 
  - Schneller Durchlauf der Kern-Tests (Build Test Gate).
  - Validierung der Versionierung und Environment-Konsistenz.
  - Artefakte dienen nur zur kurzfristigen Überprüfung (Disposables).
- **Reporting**: Ergebnisse fließen in die `build/management_reports/` und werden als CI-Artefakte gesichert.

### 2. Full Release Mode (Version Tags)
- **Frequenz**: Bei Vergabe eines Release-Tags (z.B. v1.34).
- **Eigenschaften**:
  - Vollständige E2E-Tests inklusive Selenium-Suites.
  - Bau von Debian-Paketen (.deb) und Windows-Executables (.exe).
  - Destruktive Reinstallations-Tests zur Validierung des Upgrades.
- **Reporting**: Konsolidierte Benchmark-Daten und Test-Zertifikate werden dauerhaft im Release-Asset-Bereich gespeichert.

## Artifact & Fragment Management
Das System stellt sicher, dass temporäre Dateien (Selenium-Logs, Pytest-Caches) nach dem Build in git-ignorierten Verzeichnissen (`tests/debug_artifacts/`) verbleiben. Dies hält den Repository-Root sauber und vermeidet unsaubere Git-Historien.

## Testbed & Environment
Alle Umgebungen werden über `scripts/manage_venvs.py` synchronisiert. Das sogenannte "Testbed" (.venv_testbed) ist dabei die zentrale Instanz für die Ausführung der dynamischen Test-Suites, während .venv_selenium ausschließlich für Browser-Interaktionen genutzt wird.

## Status
Die Strategie ist vollständig im `Master Runner` (`infra/build_system.py`) implementiert und über GitHub Actions orchestriert.
