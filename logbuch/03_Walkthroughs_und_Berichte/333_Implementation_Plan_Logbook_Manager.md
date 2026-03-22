# Logbuch-Eintrag: Implementation Plan - Logbook File Manager & Git History Cleanup

## Ziel
Python-Utility zur Verwaltung, Auflistung und Validierung von Logbuch-Einträgen sowie nachhaltige Bereinigung der Git-Historie.

## Konzept
- CLI-Tool für das Management von logbuch/-Einträgen (Listen, Erstellen, Linting, Index-Vorschlag, Reorganisation).
- Watchdog-Service zur Überwachung neuer Einträge, Git-Aktivität und System-Health.
- Automatisierte Einhaltung des Dual-Header-Standards.
- Git-History-Bereinigung zur Einhaltung der GitHub-Limits und Reduktion der Repository-Größe.

## Umsetzung
### Scripts
- [MODIFY] `logbook_manager.py`: CLI mit `list`, `create`, `lint`, `next-index`, `reorganize` (Index-Lücken fixen, unbenannte Dateien umbenennen).
- [NEW] `logbook_watchdog.py`: Hintergrunddienst, der neue .md-Dateien, Git-Commits und Systemmetriken überwacht und in `logbuch/Watchdog_Live_Log.md` protokolliert. Unterstützt `--poll-interval` (Standard 60s).
- Beide Skripte setzen den Dual-Header-Standard durch.

### Git History Alignment & Cleanup
- Ziel: Push nach GitHub ermöglichen, indem Dateien >100MB entfernt und die Repo-Größe reduziert wird (~2.3GB → <100MB pro Datei).
- Schritte:
  - Große Blobs identifizieren: `git rev-list` + `git cat-file`.
  - Binärmüll entfernen: `git filter-branch` für media/, dist/, *.deb.
  - Optimieren: `git gc --prune=now --aggressive`.
  - Push: milestone1-pre-release nach GitHub.
- **Warnung:** Historie wird überschrieben, Commit-Hashes ändern sich. Nur möglich, solange Branches noch nicht gepusht wurden.

### Verification Plan
- Automatisierte Tests: Watchdog-Start, Pfadprüfung, Graceful Exit.
- Manuelle Verifikation: Watchdog-Logbuch-Eintrag nach Dummy-Commit prüfen, Markdown-Formatierung kontrollieren.
- Git: `git rev-list --objects --all | git cat-file --batch-check | sort -nr -k 3 | head -n 5` (keine Datei >100MB), `git push origin milestone1-pre-release`.

## Status
In Review – Umsetzung und Cleanup-Strategie dokumentiert, Review durch User erforderlich.

## Stand
13. März 2026
