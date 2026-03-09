<!-- Category: Deployment -->
<!-- Title_DE: Deployment & Environment-Hygiene -->
<!-- Title_EN: Deployment & Environment Hygiene -->
<!-- Summary_DE: Konzepte für saubere Installationen und Umgebungsvalidierung. -->
<!-- Summary_EN: Concepts for clean installations and environment validation. -->
<!-- Status: COMPLETED -->

# Deployment & Environment-Hygiene

Ein häufiges Problem bei Python-Anwendungen ist die Abhängigkeit von der lokalen Systemumgebung ("It works on my machine"). Der *Media Web Viewer* adressiert dies durch eine strikte **Environment-Hygiene**.

### Native Packaging (DEB)
Statt komplexer Setup-Anleitungen setzt das Projekt auf native Debian-Pakete (`.deb`). Dies ermöglicht:
- Automatische Auflösung von System-Abhängigkeiten (FFmpeg, MediaInfo).
- Standardisierte Pfade für Binaries und Konfigurationsdateien.
- Nahtlose Integration in das Linux-Startmenü.

### Umgebungsvalidierung (venv & Conda)
Die Anwendung erkennt beim Start automatisch, in welcher Umgebung sie läuft. Ein dedizierter `EnvironmentManager` prüft:
1. **Python-Module:** Sind alle Pakete aus `requirements.txt` in der richtigen Version vorhanden?
2. **System-Binaries:** Sind FFmpeg, MediaInfo und ein kompatibler Browser (Chrome/Chromium) im Pfad oder an bekannten Orten installiert?
3. **Isolations-Check:** Läuft die App fälschlicherweise im System-Python statt in einer virtuellen Umgebung?

### Automatisches Self-Healing
Dank des `run.sh` Skripts und der Logik in `env_handler.py` kann die App fehlende Abhängigkeiten oft selbstständig nachinstallieren (via `pip`, `apt` oder `conda`), bevor der eigentliche Server startet.

Diese Philosophie reduziert Support-Aufwand und sorgt für eine extrem hohe "Out-of-the-box"-Stabilität beim Endnutzer.

<!-- lang-split -->

# Deployment & Environment Hygiene

A common problem with Python applications is dependency on the local system environment ("It works on my machine"). The *Media Web Viewer* addresses this through strict **environment hygiene**.

### Native Packaging (DEB)
Instead of complex setup instructions, the project relies on native Debian packages (`.deb`). This enables:
- Automatic resolution of system dependencies (FFmpeg, MediaInfo).
- Standardized paths for binaries and configuration files.
- Seamless integration into the Linux start menu.

### Environment Validation (venv & Conda)
Upon startup, the application automatically detects the environment in which it is running. A dedicated `EnvironmentManager` checks:
1. **Python Modules:** Are all packages from `requirements.txt` present in the correct version?
2. **System Binaries:** Are FFmpeg, MediaInfo, and a compatible browser (Chrome/Chromium) installed in the path or at known locations?
3. **Isolation Check:** Is the app erroneously running in system Python instead of a virtual environment?

### Automatic Self-Healing
Thanks to the `run.sh` script and the logic in `env_handler.py`, the app can often independently install missing dependencies (via `pip`, `apt`, or `conda`) before the actual server starts.

This philosophy reduces support effort and ensures extremely high "out-of-the-box" stability for the end user.
