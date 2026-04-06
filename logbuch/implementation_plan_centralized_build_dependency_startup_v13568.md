# Implementation Plan: Centralized Build, Dependency & Startup Orchestration (v1.35.68)

## Ziel
Vollständige Zentralisierung und Formalisierung aller Build-, Dependency- und Startup-Prozesse. Sicherstellung, dass alle Komponenten aus einer einzigen, konsistenten Quelle konfiguriert werden.

---

## Maßnahmen & Architektur

### 1. Environment & Packages
- **.env-Support formalisiert:**
  - python-dotenv als Core-Dependency aufgenommen
  - .env-Overrides werden systematisch geladen und dokumentiert

### 2. Unified Startup
- **run.sh gehärtet:**
  - Erkennt und lädt Umgebungsvariablen aus .env
  - Startet die App immer im korrekten Environment (Conda, Venv, ...)
  - Fallback-Logik für fehlende .env oder nicht gesetzte Variablen

### 3. Build Centralization
- **src/core/build_config.py** neu:
  - Enthält Package-Metadaten (Name, Version, Arch, ...)
  - build_deb.sh und die App selbst lesen aus derselben Quelle
  - Keine Redundanz mehr zwischen Build-Skripten und App-Code

### 4. Bootstrap Logging
- **main.py:**
  - Loggt beim Start, aus welchem Environment und mit welchen Dependency-Quellen (Conda, Venv, .env) die App läuft
  - Transparenz für Debugging und Deployment

---

## Review & Nächste Schritte
- Plan reviewen
- Nach Freigabe: Umsetzung der Maßnahmen in den genannten Modulen/Skripten

---

**Plan bereit zur Ausführung: Centralized Build, Dependency & Startup Orchestration (v1.35.68)**
