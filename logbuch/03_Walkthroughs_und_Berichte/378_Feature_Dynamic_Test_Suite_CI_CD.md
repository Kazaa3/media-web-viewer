# Projekt: Media-Web-Viewer
# Logbuch-Eintrag: Dynamic Test Suite, CI/CD und Testabdeckung

**Datum:** 13.03.2026  
**Autor:** Copilot

## Kontext
Die Teststrategie des Media Web Viewer wurde auf eine dynamische, automatisierte Test Suite und eine vollständige CI/CD-Integration ausgebaut. Ziel ist die kontinuierliche Sicherstellung der Kernfunktionalität und die Vermeidung von Regressionsfehlern bei allen Updates und Releases.

## Features & Workflows
- **Dynamic Test Suite:**
  - Umfassende Tests für Session Management, Environment, Backend, VLC, Launcher, Parser, DB, Transcoding
  - Pytest + Unittest, >100 Tests, Ausführung <5s
  - Tests laufen lokal und in CI/CD
- **CI/CD Automation:**
  - Zwei GitHub Actions Workflows: ci-artifacts.yml (main), release.yml (tagged release)
  - Automatisierte Builds: Linux Executable, Debian-Paket, Windows Executable
  - Artifacts werden als GitHub Actions-Artefakte bzw. Release-Assets bereitgestellt
- **Lokale & Repo-Cleanup-Strategie:**
  - scripts/cleanup_build_artifacts.sh für lokale Artefaktbereinigung
  - .gitignore schützt vor versehentlichem Tracking generierter Artefakte
  - Einmaliges Entfernen bereits getrackter Artefakte per git rm --cached

## Testkategorien & Abdeckung
- **Session Management:**
  - Dynamische Portvergabe, parallele Instanzen, Logging, Konfliktvermeidung
- **Environment & Dependencies:**
  - Python-Version, venv, System- und Python-Abhängigkeiten
- **Backend Integration:**
  - Eel-API, Datenserialisierung, Responsiveness
- **VLC Integration:**
  - M3U8, Metadaten, Fehlerfälle
- **Launcher System:**
  - Script-Validierung, Permissions, Testmode
- **Parser, DB, Transcoding:**
  - Parserpipeline, Tag-Extraktion, Bitdepth, Kapitel, DB-Operationen, Transcoding

## Testausführung & Best Practices
- pytest tests/ -v (alle Tests)
- pytest tests/ -k <pattern> (selektiv)
- pytest tests/ --cov=. --cov-report=html (Coverage)
- Test-Template mit Arrange-Act-Assert, Mocking, unabhängige Tests
- Docstrings mit @test und @details

## CI/CD-Workflows
- **ci-artifacts.yml:**
  - Trigger: push main, manuell
  - Builds: Linux Executable, Debian-Paket
  - Upload als Actions-Artefakt
- **release.yml:**
  - Trigger: Tag v*, manuell
  - Builds: Linux, Debian, Windows
  - Automatisches Release mit Binaries

## Testabdeckung
- Aktuell: ~75%, Ziel: >80%
- Starke Abdeckung: Session, Environment, VLC, Launcher
- Verbesserungsbedarf: Parserpipeline, DB, Transcoding

## Fazit
**Parser-Tab Hinweis:**
Aktuell sind im Parser-Tab nur die Modi "Lightweight" und "Full" verfügbar. Der "Ultimate"-Modus ist noch nicht implementiert.
Die dynamische Test Suite und die automatisierte CI/CD-Pipeline gewährleisten eine hohe Softwarequalität und schnelle Releasezyklen. Die Testabdeckung wird kontinuierlich ausgebaut, um alle Kernbereiche und kritische Pfade abzudecken.

**Hinweis:** Für Version 1.34 ist eine erneute Analyse der Testabdeckung und ggf. ein Update der Testkategorien und Dokumentation erforderlich.
