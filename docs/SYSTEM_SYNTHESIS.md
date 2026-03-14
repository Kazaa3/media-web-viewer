# SYSTEM_SYNTHESIS.md


---

## Nachtrag: Venv/Requirements-Split in CI/CD & Technische Freigabe v1.34 (März 2026)

**CI/CD-Update:**
- Das Venv-Konzept wurde konsequent in die GitHub Actions Workflows (`ci-main.yml`, `release.yml`) übertragen.
- Die Anforderungen sind jetzt klar getrennt:
   - **Build-Phase:** nutzt `infra/requirements-build.txt` (Core + PyInstaller + Wheel)
   - **Test-Phase:** nutzt `infra/requirements-test.txt` (Core + Pytest + Coverage)
   - **Selenium-Phase:** nutzt `infra/requirements-selenium.txt`
- Die `infra/requirements.txt` im Root ist nur noch ein Redirect auf die Core-Abhängigkeiten (Abwärtskompatibilität).
- In den Workflows wurden generische requirements-Aufrufe durch die spezialisierten Files ersetzt.

**Status:**
- Änderungen sind gepusht, GitHub Actions laufen automatisch neu an.
- Sobald die Checks grün sind, kann der Merge nach `main` (siehe Schritt 1 im Tutorial) durchgeführt werden.
- Damit ist v1.34 technisch "sauber" und bereit, die stabile Basis für den Videoplayer in Meilenstein 1 zu bilden.
## System Infrastructure Consolidation & Synthesis (v1.34)

This document provides a high-level overview of the consolidated system architecture and infrastructure management for the Media Web Viewer project.

### 1. Configuration Management (Single Source of Truth)
- **Centralized Config**: All application settings are now consolidated in `parser_config.json`.
- **Media Categories**: Support for 10 distinct media categories (Audio, Video, Games, etc.) is deeply integrated.
- **Diagnostic Logging**: 20+ granular `debug_flags` are now managed directly via the central configuration.
- **Branch-Specific Profiles**: Reference configurations like `web/config.main.json` and `web/config.develop.json` serve as templates for different environments.

### 2. Environment Architecture (Multi-Venv Strategy)
- **Decoupled Environments**: The project uses specialized virtual environments to isolate core logic from development and testing tools:
  - `.venv_core`: Production/runtime dependencies.
  - `.venv_dev`: Development tools (formatting, documentation).
  - `.venv_run`: Lightweight execution environment for rapid testing.
- **Automated Setup**: Managed via `scripts/setup_venvs.sh` and `scripts/manage_venvs.py`.

### 3. Integrated Build & Packaging
- **Release Strategy**: 
  - **Prerelease**: `release/v1.34-purified` contains the squashed/purified source.
  - **Milestone 1**: `meilenstein-1-mediaplayer` is the staging branch for the v1.34 release.
  - **Main**: The `main` branch is protected and receives the final PR from M1.
- **Unified Packaging**: `infra/packaging/specs/MediaWebViewer.spec` provides a single point of truth for PyInstaller builds.
- **Version Synchronization**: Managed via `infra/VERSION_SYNC.json` across all source, packaging, and documentation files.

### 4. Quality Assurance & Reporting
- **Test Pipeline**: The `infra/build_system.py --pipeline` command executes 24 test gates, from unit tests to E2E Selenium flows.
- **Management Reporting**: All benchmark data, performance probes, and test results are consolidated in `build/management_reports/`.
- **Continuous Monitoring**: `scripts/monitor_utils.py` provides watchdog capabilities for long-running synchronization and scanning tasks.

### 5. Repository Purification (Git Purity)
- **Restrictive Gating**: The `.gitignore` uses a "Gated Purification" strategy (ignore-all by default) to ensure no binary residue or Selenium artifacts enter the version tree.
- **Root Discipline**: The repository root is kept clean; all infrastructure files are strictly organized in `infra/`, `scripts/`, or `docs/`.

## 6. Testdaten & Mockfiles
- Strukturierte Mockfiles in /tests/mockfiles/ und /media/ für Parser- und File-Tests
- README_mock_testfiles.md dokumentiert die Testdatenstrategie
- Reale, aber rechtlich unbedenkliche Mockfiles werden für fortgeschrittene Tests genutzt

## 7. Branch- und Tag-Historie
- main (alt) -> v1.33 (Tag) -> meilenstein-1-mediaplayer (v1.34 purified)
- M1 ist bereit, der neue main zu werden (PR auf GitHub)

## 8. Abschluss & Ausblick
- Debug-Flags konsolidiert, Datenbank für frischen Start vorbereitet
- Dokumentation ist vollständig und aktuell
- Repository ist frei von visuellen Altlasten und bereit für den Release

---

## Walkthrough: Final System Integration & Purification (v1.34)

### Key Accomplishments
1. **High-Level Repository Purification**
   - Root Cleanup: Alle Tool-Fragmente (.log, .png, .xml, .txt, .spec, .so) entfernt.
   - Legacy Migration: Root-Skripte nach infra/ oder scripts/ verschoben oder gelöscht.
   - Gated .gitignore: Restriktive "Gated Purification"-Strategie implementiert.
2. **Advanced Monitoring Infrastructure**
   - Progress Watchdogs: monitor_utils.py erkennt "silent hangs" via Logfile-Überwachung.
   - BuildSystem Integration: Automatischer Watchdog-Einsatz bei Benchmarks und Builds.
3. **Packaging Architecture & Purification**
   - Surgical Purge: packaging/-Verzeichnis und alte Spec-Files entfernt.
   - Template Consolidation: Alle Templates in infra/packaging/ isoliert.
   - Source vs. Artifacts: Nur Build-Logik im Repo, keine Artefakte.
   - Nuclear Index Refresh: git rm -r -f --cached . für sauberen Index.
   - Recursive Screenshot Purge: .gitignore fängt jetzt alle Screenshots ab.
4. **Integrated Pipeline Verification**
   - Vollständige Pipeline ausgeführt: Version Sync, Debian-Build, 24 Test Gates, Benchmarks, Management Reports.
5. **v1.34 Consolidation & v1.33 Archival**
   - v1.33 als Tag archiviert, v1.34 purified in M1 gemerged.
   - 565 Commits zu einem Clean Commit gesquasht.
   - DEBUG_FLAGS zentralisiert, DB für frischen Start bereinigt.

### Final Repository State

    .
    ├── src/            # Core logic (purified)
    ├── infra/          # Infrastructure, packaging templates, & version sync
    ├── scripts/        # Monitoring & utility scripts (watchdogs)
    ├── web/            # Frontend assets
    ├── docs/           # Centralized documentation
    ├── tests/          # Refactored test suite
    ├── logbuch/        # Project logbooks
    ├── data/           # Local data (gitignored)
    ├── main.py         # Entry point
    └── VERSION         # v1.34

### Validation Results
- **History & Archival:** main → v1.33 (Tag) → M1 (v1.34 purified) korrekt abgebildet.
- **Configuration & Data:** DEBUG_FLAGS-Propagation und frische DB-Schema-Generierung verifiziert.

---
Letzte Aktualisierung: 14.03.2026
