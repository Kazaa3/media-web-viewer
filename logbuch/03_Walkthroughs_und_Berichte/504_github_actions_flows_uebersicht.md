# Übersicht der aktuell definierten GitHub Actions Workflows

## 1. ci-artifacts.yml
- **Zweck:** Baut und paketiert Linux-Artefakte (z.B. PyInstaller-Binary) für den Hauptbranch (main).
- **Trigger:**
  - Push auf main
  - Manuell via workflow_dispatch
- **Ablauf:**
  1. Checkout Code
  2. Python 3.11 Setup
  3. Systemabhängigkeiten (ffmpeg, mediainfo) installieren
  4. Python-Abhängigkeiten & PyInstaller installieren
  5. Build & Packaging via `infra/build_system.py`
  6. Upload des Linux-Binaries als Artifact

## 2. ci-develop.yml
- **Zweck:** Testet den Entwicklungsbranch (develop) mit Unit- und Integrationstests, baut ein Debian-Paket zur Validierung.
- **Trigger:**
  - Push oder Pull Request auf develop
- **Ablauf:**
  1. Checkout Code
  2. Python 3.11 Setup
  3. Systemabhängigkeiten installieren
  4. Python-Abhängigkeiten installieren
  5. Ausführung von Unit-Tests (Tier 1)
  6. Ausführung von Integrationstests (Tier 2)
  7. Build eines Debian-Pakets (Validierung)

## 3. ci-main.yml
- **Zweck:** Vollständige Validierung und Release-Gate für main-Branch (inkl. Selenium/Xvfb).
- **Trigger:**
  - Push oder Pull Request auf main
- **Ablauf:**
  1. Checkout Code
  2. Python 3.11 Setup
  3. Systemabhängigkeiten (ffmpeg, mediainfo, xvfb) installieren (mit Retry-Logik)
  4. Geckodriver-Prüfung
  5. Python-Abhängigkeiten (build, test, selenium) installieren
  6. (Weitere Schritte im vollständigen Workflow definiert)

## 4. release.yml
- **Zweck:** Validierung, Build und Release bei neuen Tags (z.B. v1.33).
- **Trigger:**
  - Push auf Tags, die mit "v" beginnen (z.B. v1.33)
  - Manuell via workflow_dispatch
- **Ablauf:**
  1. Checkout Code
  2. Python 3.11 Setup
  3. Systemabhängigkeiten (ffmpeg, mediainfo, xvfb) installieren
  4. Python-Abhängigkeiten (core, test, selenium) installieren
  5. Ausführung von Tech- und Basic-Integrationstests
  6. Ausführung von UI-Tests (Headless, Selenium)
  7. (Weitere Schritte: Build, Release, Upload)

---

**Hinweis:**
Alle Workflows sind im Verzeichnis `.github/workflows/` definiert. Sie decken die wichtigsten CI/CD-Szenarien ab: Entwicklung, Hauptbranch, Artefakt-Build und Release.

**Siehe auch:**
- Logbuch: Build-Pipeline Beschreibung
- Logbuch: GitHub Actions Beschreibung
- [README.md](../README.md)
