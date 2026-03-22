# Logbuch-Eintrag: Implementation Plan - Logbook File Manager

## Ziel
Ein Python-basiertes Utility zur Verwaltung, Auflistung und Validierung von Einträgen im logbuch/-Verzeichnis.

## Konzept
- Einhaltung der bestehenden Struktur (Ziel, Konzept, Umsetzung, Status, Stand) für neue Einträge.
- Automatisierte und interaktive Verwaltung der Logbuch-Einträge.
- Unterstützung für Index-Lücken, Dual-Header-Standard und CI/CD-Integration.

## Umsetzung
### Scripts
**[MODIFY] logbook_manager.py**
- CLI-Tool mit folgenden Funktionen:
  - **list**: Zeigt alle Logbücher, sortiert nach Präfix oder Datum. Unterstützt --search.
  - **create**: Interaktive oder argumentbasierte Erstellung eines neuen Eintrags mit Standard-Template.
  - **lint**: Validiert, dass Dateien die korrekten Abschnitte und ein aktuelles Datum haben.
  - **next-index**: Schlägt den nächsten numerischen Index basierend auf bestehenden Dateien vor.
  - **reorganize**: [NEU] Behebt automatisch Index-Lücken und benennt nicht indizierte Dateien nach dem XX_Subject.md-Muster um.
- Das Skript hält sich an den Dual-Header-Standard.

**[NEW] logbook_watchdog.py**
- Hintergrunddienst, der:
  - Das logbuch/-Verzeichnis auf neue .md-Dateien überwacht (auch manuelle Erstellung/Pushes).
  - Git-Aktivität (letzte Commits) überwacht.
  - System-Health (CPU, Disk) überwacht.
  - Automatisch "Anchor"-Updates in logbuch/Watchdog_Live_Log.md anhängt.
  - --poll-interval (Standard 60s) unterstützt.
  - Dual-Header-Standard einhält.

### Git History Alignment & Cleanup
**Ziel:**
Push nach GitHub ermöglichen, indem Dateien >100MB entfernt und die Repo-Größe reduziert wird (~2.3GB).

**Vorgeschlagene Änderungen:**
- Große Blobs identifizieren: git rev-list und git cat-file zur Auflistung der größten Objekte.
- Binärmüll entfernen: git filter-branch zum Entfernen von media/, dist/ und *.deb aus der gesamten Historie von main und milestone1-pre-release.
- Repository optimieren: git gc --prune=now --aggressive.
- Push zum Remote: milestone1-pre-release nach GitHub pushen.

**Automatisierte Verifikation:**
- git rev-list --objects --all | git cat-file --batch-check | sort -nr -k 3 | head -n 5 (prüfen, dass keine Datei >100MB)
- git push origin milestone1-pre-release (finaler Erfolg)

**Warnung:**
Dies überschreibt die Git-Historie und ändert Commit-Hashes. Da die lokalen Branches noch nicht gepusht wurden, ist dies der einzige Weg, den Push zu ermöglichen.

### Verification Plan
**Automatisierte Tests:**
- Watchdog-Start: python3 scripts/logbook_watchdog.py start --once und prüfen, dass logbuch/Watchdog_Live_Log.md erzeugt/aktualisiert wird.
- Pfadprüfung: Korrekte Erkennung von Projekt-Root und logbuch/-Ordner.
- Graceful Exit: Ctrl+C Handling testen.

**Manuelle Verifikation:**
- Watchdog starten und Dummy-Commit machen; prüfen, ob Logbuch die Änderung widerspiegelt.
- Formatierung des generierten Logbuch-Eintrags prüfen (sauberes Markdown).

### Pipeline & Test Readiness Synchronization
**Ziel:**
Sicherstellen, dass die CI/CD-Pipeline die neuen Testkategorien korrekt orchestriert und gegen Regressionen im Build/Release-Prozess schützt.

**Build System & CI**
- [MODIFY] build_system.py: tests/integration/category/git/test_git_guard.py zu BUILD_TEST_GATE hinzufügen. Pfade für Performance-Benchmarks in run_performance_benchmarks aktualisieren.
- [MODIFY] release.yml: Testpfade auf das neue tests/integration/category/-Schema umstellen. Selenium-Testpfad auf tests/e2e/selenium/ korrigieren.
- [MODIFY] ci-main.yml: Konsistente Testabdeckung via build_system.py --test all sicherstellen.

**Advanced Pipeline Features**
- Branch-spezifische Konfiguration: build_system.py erkennt aktuellen Branch und wählt das passende .json-Template (z.B. web/config.dev.json vs web/config.prod.json).
- Hang Protection & Monitoring: monitor_utils.py und build_system.py mit StatusBar und run_monitored für Hang-Detection erweitern.
- Database Persistence Policy: Entwicklungs-Builds behalten bestehende Datenbank, Release-Builds säubern/migrieren je nach Version.

**Requirement Mapping (Requirement -> Test)**
- R1: FFmpeg Reliability -> tests/integration/category/tech/ffmpeg/
- R2: UI Stability -> tests/integration/category/ui/test_ui_session_stability.py
- R3: Git Integrity -> tests/integration/category/git/test_git_guard.py
- R4: Install/Uninstall Hygiene -> tests/e2e/install/test_reinstall_deb.py
- R5: Performance Benchmarks -> tests/integration/performance/

---

*Letzte Aktualisierung: 13. März 2026*
