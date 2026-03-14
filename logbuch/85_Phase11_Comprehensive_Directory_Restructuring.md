# Phase 11: Comprehensive Directory Restructuring

**Datum:** 13.03.2026
**Autor:** Copilot

## Ziel
Das Root-Verzeichnis wird durch eine logische Hierarchie aufgeräumt. Dies verbessert die Wartbarkeit und ermöglicht eine effektivere Anwendung der `.gitignore`-Regeln.

## Vorgeschlagenes Verzeichnis-Layout
| Verzeichnis     | Inhalt / Zweck                                                        |
|----------------|-----------------------------------------------------------------------|
| src/core/      | Core-Logik: main.py, models.py, db.py, env_handler.py, logger.py, media_format.py |
| src/parsers/   | Modularisierte Parser (aus root/parsers/ verschoben)                  |
| web/           | Frontend-Assets, app_bottle.py                                        |
| infra/         | Build-Skripte: build.py, build_system.py, build_deb.sh, build_exe.sh, packaging/, Dockerfile*, docker-compose* |
| docs/          | Dokumentation: *.md (außer README), logbuch/, Screens/                |
| scripts/       | Utility-Skripte: update_version.py, create_mocks.py, check_environment.py, setup_venvs.sh, reinstall_deb.sh, run.sh |
| tests/         | Test-Suiten                                                           |
| data/          | Datenbank und Logs: database.db, logs/                                |

## Geplante Änderungen
- [NEW] [DIRECTORY] src/core, infra, docs, scripts, data: Hierarchie anlegen, relevante Dateien verschieben
- [MODIFY] media_parser.py: Absolute/relative Imports für neue src/-Struktur anpassen
- [MODIFY] main.py: Pfad-Konstanten auf neue web/ und data/ Locations refaktorisieren
- [MODIFY] .gitignore: Patterns auf ganze Verzeichnisse (z.B. data/logs/) umstellen

## Verification Plan
**Automatisierte Tests:**
- pytest ausführen, um Import-Fehler nach Umstrukturierung zu erkennen
- Build-Skripte (build.py) testen, ob alle Dateien gefunden werden

**Manuelle Prüfung:**
- App starten, Datenbank-Konnektivität und Web-Asset-Loading prüfen
- Sicherstellen, dass im Root nur essentielle Projektdateien (README, .gitignore, src/) liegen

---

**Fazit:**
Die umfassende Verzeichnis-Umstrukturierung schafft eine klare, wartbare Projektbasis und erleichtert die Pflege und Weiterentwicklung des Media Web Viewer.
