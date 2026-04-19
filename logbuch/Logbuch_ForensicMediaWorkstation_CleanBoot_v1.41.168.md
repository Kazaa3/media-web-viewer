# Logbuch: Forensic Media Workstation – Clean Boot & Architektur-Realignment (v1.41.168)

## Zusammenfassung der Stabilisierung und Verbesserungen

### 1. Branch Strategy & CI/CD Optimization
- **Aktiver Branch:** feature/forensic-realignment
- Entwicklung von main entkoppelt, CI-E-Mail-Spam durch Zwischenstände gestoppt.
- **CI Pipeline (ci-main.yml):**
    - Geckodriver-Setup jetzt über browser-actions/setup-geckodriver@latest
    - secrets.GITHUB_TOKEN integriert (kein Rate-Limiting)
    - Ubuntu-latest (22.04/24.04) wird zuverlässig unterstützt

### 2. Bootstrapping & Path Integrity
- **Circular Import Resolution:** sys.path-Injektion vor allen src-Imports in main.py, ModuleNotFoundError gelöst
- **Build System Pathing:** infra/build_system.py erkennt Projekt-Root korrekt, Tests/Packaging laufen aus jedem Verzeichnis
- **Environment Guard:** ensure_stable_environment prüft und erzwingt .venv-Ausführung

### 3. Semantic Code Repairs
- **Undefined Name Resolution:**
    - transcode_mgr, SubtitleProcessor, find_free_port(), index_file, requests & extensions: Alle kritischen NameError/Import-Probleme gelöst
- **Import Error Mitigation:**
    - ImportError: cannot import name 'AUDIO_EXTENSIONS' aus 'src.core.models' gelöst, alle Parser/Core-Module nutzen jetzt SSOT-Registry aus config_master.py
- **Refactored Imports:**
    - Dutzende ungenutzte oder doppelte Imports entfernt

### 4. Forensic Category Realignment
- **Selective UI Architecture:** library_category_map in config_master.py nutzt jetzt Content-Labels statt technischer Branch-IDs
- **Neue Kategorien:**
    - HÖRBÜCHER (Audiobooks)
    - SAMPLER / MIXES (Kompilationserkennung in models.py integriert)
    - DVD / ISO IMAGES
- **Branch-Aware Filtering:**
    - audio branch: Nur Audio/Hörbuch-Content
    - multimedia branch: Inkl. Video und Disk Images
    - extended branch: Volle Sichtbarkeit auf alle Medientypen

---

**Status:**
- Codebase ist im "Clean Boot"-Zustand. ModuleNotFoundError gelöst, Environment Detection und Dependency-Checks funktionieren.

**Tipp:**
- Weiterentwicklung sollte auf dem feature/ Branch bleiben, um CI-Stille auf main zu gewährleisten.
