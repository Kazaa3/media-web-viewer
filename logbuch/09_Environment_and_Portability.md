<!-- Category: Deployment -->
<!-- Title_DE: 08 Environment & Portabilität: Die "Exklusiv"-Strategie -->
<!-- Title_EN: 08 Environment & Portability: The "Exclusive" Strategy -->
<!-- Summary_DE: Sicherstellung der Stabilität durch strikte Umgebungs-Validierung (Venv/Conda). -->
<!-- Summary_EN: Ensuring stability through strict environment validation (Venv/Conda). -->
<!-- Status: COMPLETED -->

<!-- Anchor: 09_Environment_and_Portability -->
<!-- Redundancy: Section covers environment hygiene, venv/conda validation, auto-fix, binaries. -->

# 08 Environment & Portabilität: Die "Exklusiv"-Strategie

Python-Anwendungen leiden oft unter dem "Works on my machine"-Syndrom. Um dies zu verhindern, verfolgt der *Media Web Viewer* eine strikte Strategie der **Umgebungs-Hygiene**.

### Die "Exklusiv"-Philosophie
Die Anwendung erkennt automatisch, in welcher Umgebung sie läuft (Venv, Conda oder System-Python). 
1. **Isolation:** Wenn die App fälschlicherweise in der Systemumgebung gestartet wird, warnt sie den Nutzer oder verweigert den Dienst, um Paketkonflikte zu vermeiden.
2. **Auto-Fix:** Das `run.sh` Skript kann fehlende Abhängigkeiten in Venvs oder Conda-Umgebungen automatisch nachinstallieren.
3. **Binaries:** Nicht nur Python-Pakete werden geprüft. Auch systemrelevante Tools wie FFmpeg und MediaInfo werden an bekannten Pfaden gesucht, um eine "Out-of-the-box"-Lauffähigkeit zu garantieren.

### Warum ist das komplex?
Die Unterstützung für **Conda** und deren spezifische Paket-Namenskonventionen (z. B. `libgdk-pixbuf2.0-0` zu `gdk-pixbuf`) erforderte eine intelligente Mapping-Logik. Diese "Hygiene" sorgt dafür, dass die App auch in komplexen wissenschaftlichen Umgebungen oder auf frischen Linux-Installationen gleichermaßen stabil läuft.

<!-- lang-split -->

# 08 Environment & Portability: The "Exclusive" Strategy

Python applications often suffer from the "Works on my machine" syndrome. To prevent this, the *Media Web Viewer* follows a strict strategy of **environment hygiene**.

### The "Exclusive" Philosophy
The application automatically detects the environment it is running in (Venv, Conda, or system Python). 
1. **Isolation:** If the app is erroneously started in the system environment, it warns the user or refuses service to avoid package conflicts.
2. **Auto-Fix:** The `run.sh` script can automatically install missing dependencies in Venvs or Conda environments.
3. **Binaries:** Not just Python packages are checked. System-relevant tools like FFmpeg and MediaInfo are also searched for in known paths to guarantee "out-of-the-box" functionality.

### Why is this complex?
Support for **Conda** and its specific package naming conventions (e.g., `libgdk-pixbuf2.0-0` to `gdk-pixbuf`) required intelligent mapping logic. This "hygiene" ensures that the app runs equally stable in complex scientific environments or on fresh Linux installations.
