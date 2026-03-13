#dict - Desktop Media Player and Library Manager v1.34

## Management Suite - Walkthrough & Features

Dieses Dokument beschreibt die neuen Maintenance- und Dokumentations-Tools im Media Web Viewer Projekt.

---

### 1. Project Garbage Collector
**Datei:** scripts/project_garbage_collector.py
- Automatisiert Workspace-Cleanup und Git-Pflege.
- Features: Fortschrittsbalken, Heartbeat-Indikator, Git-Kontext (ahead/behind).
- Usage:
  ```bash
  python3 scripts/project_garbage_collector.py --status  # Preview
  python3 scripts/project_garbage_collector.py --force   # Cleanup
  ```

---


### 2. Logbook File Manager & Watchdog
- **Logbook Manager (scripts/logbook_manager.py):**
  - list: Zeigt alle Einträge mit Titeln und Dateigröße (unterstützt --search).
  - create: Erstellt neuen Eintrag mit korrektem Index und bilingualem Template.
  - lint: Prüft auf erforderliche Abschnitte.
- **Logbook Watchdog (scripts/logbook_watchdog.py):**
  - Hintergrunddienst, der das logbuch/ Verzeichnis auf neue Dateien überwacht (auch bei manueller Erstellung).
  - Loggt Git-Status (Commits, Branch) und Systemmetriken (CPU, RAM, Disk).
  - Pflegt logbuch/Watchdog_Live_Log.md als fortlaufendes Audit-Log.
- Usage:
  ```bash
  python3 scripts/logbook_manager.py list
  python3 scripts/logbook_watchdog.py start
  ```

---


### 3. Git Management & Guards
- **Git Guard (scripts/git_guard.py):**
  - Prüft gestagte Dateien auf Größe vor dem Commit (Warnung ab 50MB, Limit 100MB).
- **Status Bar Utilities (scripts/status_bar_utils.py):**
  - Wiederverwendbare CLI-Fortschrittsanzeige für lange Skripte (in logbook_manager integriert).
- **History Cleanup:**
  - Reduzierte Repository-Größe von 2.3 GB auf 155 MB.
  - Entfernte große Binärdateien aus der Git-Historie für GitHub-Kompatibilität.
- Usage:
  ```bash
  python3 scripts/git_guard.py
  # logbook_manager nutzt Status Bar automatisch
  ```

### 4. Header Compliance Tool (scripts/check_test_headers.py)
- Unterstützt gezielte Scans auf Header-Konformität.
- Usage:
  ```bash
  python3 scripts/check_test_headers.py scripts/logbook_manager.py
  ```

---

### Accomplishments
- Automatisierte Garbage Collection implementiert.
- Zentralen Logbook Manager erstellt.
- Dual-Header Standard für neue Scripts.
- Repository-Bloat reduziert, Developer Experience verbessert.

---

**Kommentar:**
Die Management Suite sorgt für effiziente Wartung, Dokumentation und Standardisierung im Projekt.

*Letzte Aktualisierung: 13. März 2026*
