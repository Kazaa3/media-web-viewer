# Current Implementation State: Forensic Media Workstation (v1.41.168)

## 1. Branch Strategy & CI/CD Optimization
- **Active Branch:** feature/forensic-realignment
    - Entwicklung von main entkoppelt, kein CI-E-Mail-Spam mehr bei Zwischenständen.
- **CI Pipeline (ci-main.yml):**
    - Manuelle Geckodriver-Installation durch browser-actions/setup-geckodriver@latest ersetzt.
    - secrets.GITHUB_TOKEN integriert, um Rate-Limiting beim Treiber-Download zu vermeiden.
    - Ubuntu-latest (22.04/24.04) wird zuverlässig unterstützt.

## 2. Bootstrapping & Path Integrity
- **Circular Import Resolution:**
    - ModuleNotFoundError: No module named 'src' durch Vorziehen der sys.path-Injektion in main.py gelöst.
- **Build System Pathing:**
    - infra/build_system.py erkennt jetzt das Projekt-Root korrekt, Tests und Packaging laufen aus jedem Verzeichnis.
- **Environment Guard:**
    - ensure_stable_environment prüft und erzwingt .venv-Ausführung zuverlässig.

## 3. Semantic Code Repairs
- **Undefined Name Resolution:**
    - transcode_mgr, SubtitleProcessor, find_free_port(), index_file, requests & extensions: Alle kritischen NameError/Import-Probleme in main.py und models.py gelöst.
- **Refactored Imports:**
    - Dutzende ungenutzte oder doppelte Imports entfernt (z.B. socket, is_mkvtoolnix_available).

## 4. Forensic Category Realignment
- **Selective UI Architecture:**
    - library_category_map in config_master.py nutzt jetzt Content-Labels statt technischer Branch-IDs.
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
