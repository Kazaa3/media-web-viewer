## Phase 11: Systematische Umstrukturierung
**Datum:** 12. März 2026

- Die Projektdateien werden in logische Bereiche unterteilt, um einen sauberen Root-Folder und bessere Wartbarkeit zu gewährleisten.

### Neue Struktur
- src/core/: Hauptlogik (main.py, models.py, db.py etc.)
- src/parsers/: Alle Parser-Module
- infra/: Docker, Build-Scripts und Paketierung
- docs/: Alle Markdown-Dokumente und Logbücher
- scripts/: Utility-Scripts und Launcher
- data/: Datenbank (database.db) und Logs

### Ergänzende Details & Verifikationsplan

**Proposed Directory Layout:**
| Directory      | Content / Purpose |
|---------------|------------------|
| src/core/     | Core logic: main.py, models.py, db.py, env_handler.py, logger.py, media_format.py |
| src/parsers/  | Moved from root parsers/ |
| web/          | Frontend assets and app_bottle.py |
| infra/        | Build scripts: build.py, build_system.py, build_deb.sh, build_exe.sh, packaging/, Dockerfile*, docker-compose* |
| docs/         | Documentation: *.md (except README), logbuch/, Screens/ |
| scripts/      | Utility scripts: update_version.py, create_mocks.py, check_environment.py, setup_venvs.sh, reinstall_deb.sh, run.sh |
| tests/        | Test suites |
| data/         | Database and logs: database.db, logs/ |

**Proposed Changes:**
- [NEW] [DIRECTORY] src/core, infra, docs, scripts, data: Create the high-level hierarchy and move relevant files.
- [MODIFY] media_parser.py: Update absolute/relative imports for the new src/ structure.
- [MODIFY] main.py: Refactor path constants to point to new web/ and data/ locations.
- [MODIFY] .gitignore: Clean up patterns to target entire directories (e.g., data/logs/) instead of many root-level file patterns.

**Verifikationsplan:**
- Automatisierte Tests: pytest ausführen, um sicherzustellen, dass alle Imports nach der Umstrukturierung weiterhin funktionieren.
- Build-Skripte (build.py) prüfen, ob alle notwendigen Dateien gefunden werden.
- Manuelle Verifikation: App starten und Datenbank-/Web-Asset-Konnektivität prüfen.
- Sicherstellen, dass das Root-Verzeichnis nur noch essentielle Projektdateien enthält (README, .gitignore, src folder).

*Entry created: 12. März 2026*
---