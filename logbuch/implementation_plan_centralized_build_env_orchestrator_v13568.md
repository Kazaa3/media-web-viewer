# Implementation Plan: Centralized Build & Environment Orchestrator (v1.35.68)

## Ziel
Erweiterung des zentralen Konfigurationssystems auf Build-Prozess, Dependency-Management (PIP) und Startup-Orchestrierung. Sicherstellung, dass alle Komponenten und Skripte aus einer einzigen, konsistenten Quelle konfiguriert werden.

---

## Maßnahmen & Architektur

### 1. Environment & Dependencies
- **requirements-core.txt:** python-dotenv>=1.0.0 als Core-Dependency
- **requirements-test.txt:** playwright>=1.42.0, selenium>=4.18.0, pytest-playwright
- **config_master.py:**
  - dotenv.load_dotenv() integriert
  - test_engine-Flag (playwright, selenium, chrome-headless)
  - headless_mode-Toggle (Env: MWV_HEADLESS=true)
- **.env.example:** Template für lokale Anpassungen

### 2. Build Process Orchestration
- **build_config.py:**
  - Zentrale Build-Metadaten (Name, Arch, Version aus VERSION-File)
- **infra/build_deb.sh:**
  - Nutzt build_config.py (via Python-Call) statt harter Strings
  - Build-Skript passt sich automatisch an zentrale Metadaten an

### 3. Startup & Bootstrap
- **run.sh:**
  - Dependency-Check prüft gezielt auf python-dotenv
  - Korrektes PYTHONPATH-Handling für Venv/Conda
- **main.py:**
  - Loggt beim Start die Environment-Quelle ([Config] Loaded from .env: True)

---

## Offene Frage
- Soll pyproject.toml in die Zentralisierung aufgenommen werden oder als separate Metadatenquelle für statische Tools bestehen bleiben?

---

## Verifikation
- **Automatisiert:**
  - tests/integration/env/test_dotenv_overrides.py: .env überschreibt Defaults
  - scripts/verify_build_metadata.py: build_deb.sh-Target entspricht build_config.py
- **Manuell:**
  - .env mit MWV_PORT=9999 → ./run.sh → App startet auf Port 9999
  - ./build.sh → .deb enthält korrekten Namen/Version

---

**Plan bereit zur Ausführung: Centralized Build & Environment Orchestrator (v1.35.68)**
