# Finalisierung: Zentrale Verzeichnis-Konfiguration & Build-System-Integration

**Datum:** 15.03.2026

## Centralized Directory Management
- **Neue Konfigurationsschlüssel:** Die Anwendung verwaltet jetzt zentral `browse_default_dir`, `library_dir` und `additional_library_dirs` in `src/parsers/format_utils.py` und dem `config.json`-System.
- **Migrationslogik:** Das Backend synchronisiert automatisch bestehende `scan_dirs` mit den neuen Feldern, um einen reibungslosen Übergang zu gewährleisten.
- **Saubere Defaults:**
  - `config.main.json`: Enthält produktive Standardwerte.
  - `config.develop.json`: Vorkonfiguriert mit 4 gewünschten Index-Verzeichnissen (1 primär, 3 zusätzlich) für die Entwicklung.

## Build System Integration
- **CLI-Overrides:** Die Verzeichnispfade können beim Build/Deployment übergeben werden:
  ```bash
  python infra/build_system.py --deploy-config --browse-dir /path/to/browse --library-dir /path/to/lib --additional-library-dirs /path/a,/path/b
  ```
- **Branch-Aware Deployment:** Die Branch-Erkennung erkennt jetzt korrekt "meilenstein"-Branches und verwendet die Entwicklungs-Konfiguration als Basis.

## Frontend UI Enhancements
- **Options-Tab:**
  - Eigene Eingabefelder für `browse_dir` und `library_dir`.
  - Multi-Line-Textfeld für `additional_library_dirs` zur komfortablen Verwaltung mehrerer Scan-Roots.
- Die UI bleibt synchron mit dem globalen `config.json`-State.

---

**Ergebnis:**
- Saubere, zentrale Konfiguration von Verzeichnissen – von Build-Argumenten über branch-spezifische Templates bis zur Live-Anwendung.
- Technische Details sind in `config_enhancements_summary.md` dokumentiert.
