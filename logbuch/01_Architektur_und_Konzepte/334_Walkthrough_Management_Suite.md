# Walkthrough - Management Suite

## Überblick
Das Projekt enthält jetzt leistungsstarke Wartungs- und Dokumentations-Tools für effiziente Entwicklung, Qualitätssicherung und Repository-Pflege.

---

### 1. Project Garbage Collector (`scripts/project_garbage_collector.py`)
Automatisiert Workspace-Cleanup und Git-Maintenance.
- **Features:** Fortschrittsbalken, Heartbeat-Indikator, Git-Kontext (ahead/behind).
- **Usage:**
  ```bash
  python3 scripts/project_garbage_collector.py --status  # Vorschau
  python3 scripts/project_garbage_collector.py --force   # Cleanup
  ```

---

### 2. Logbook File Manager & Watchdog
Verwaltet das `logbuch/`-Verzeichnis und überwacht es im Hintergrund.
- **Logbook Manager (`scripts/logbook_manager.py`):**
  - `list`: Zeigt alle Einträge mit Titeln (unterstützt --search).
  - `create`: Erstellt neuen Eintrag mit korrektem Index und bilingualem Template.
  - `lint`: Validiert erforderliche Abschnitte.
- **Logbook Watchdog (`scripts/logbook_watchdog.py`):**
  - Hintergrunddienst, der auf neue Dateien (auch manuell) prüft.
  - Loggt Git-Status (Commits, Branch) und Systemmetriken (CPU, RAM, Disk).
  - Pflegt `logbuch/Watchdog_Live_Log.md` als Audit-Trail.
- **Usage:**
  ```bash
  python3 scripts/logbook_manager.py list
  python3 scripts/logbook_watchdog.py start  # Startet Hintergrundüberwachung
  ```

---

### 3. Git Management & Guards
Hält das Repository gesund und gibt visuelles Feedback.
- **Git Guard (`scripts/git_guard.py`):**
  - Prüft gestagte Dateien auf Größe vor Commit (Warnung ab 50MB, Limit 100MB).
- **Status Bar Utilities (`scripts/status_bar_utils.py`):**
  - Wiederverwendbarer CLI-Fortschrittsbalken für lange Skripte (bereits in logbook_manager integriert).
- **History Cleanup:**
  - Repository von 2.3 GB auf 155 MB reduziert.
  - Große Binärdateien aus Git-Historie entfernt (GitHub-Sync möglich).
- **Usage:**
  ```bash
  python3 scripts/git_guard.py
  # logbook_manager nutzt Status Bars automatisch
  ```
- **Tests:**
  - `tests/integration/category/git/test_git_guard.py` prüft die Einhaltung der Dateigrößen.

---

### 4. Header Compliance Tool (`scripts/check_test_headers.py`)
- Unterstützt gezielte Scans einzelner Dateien/Skripte.
- **Usage:**
  ```bash
  python3 scripts/check_test_headers.py scripts/logbook_manager.py
  ```
- Alle neuen Skripte folgen dem Dual-Header-Standard.
- Size Guards und Progress Bars sind Standard.
- History Cleanup dokumentiert in Logbuch 25.
- Repository-Bloat reduziert, Developer Experience verbessert.
- Advanced Pipeline Stabilization integriert.

---

### 5. Advanced Build Pipeline & Stabilization
Letzter Feinschliff für stabile Releases und Entwicklung.
- **Branch-Aware Deployments:**
  - Automatische Erkennung von `main` vs. `develop`.
  - Deployment spezialisierter config.json-Templates je nach Branch.
- **Reporting Infrastructure:**
  - Standardisierte `build/management_reports` für alle Testergebnisse.
  - Automatisierte JUnit-XML-Generierung für das 24-Test-Build-Gate.
- **Test Suite Haerdening:**
  - Fix für parents[3] vs. parents[4] bei tief verschachtelten Tests.
  - UI-Assertions gegen Browser-Formatierungsänderungen gehärtet.
- **Database Persistence Policy:**
  - `postrm` prüft `.build_metadata`, um `data/` für Dev-Builds zu erhalten, aber für Releases zu löschen.
- **Usage:**
  ```bash
  python3 infra/build_system.py --test-gate  # 100% Pass verified
  ```

---

*Letzte Aktualisierung: 13. März 2026*
