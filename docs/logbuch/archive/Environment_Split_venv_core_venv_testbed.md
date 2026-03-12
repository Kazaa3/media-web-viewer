# Environment Split – .venv_core & .venv_testbed

## Ziel
Dieser Logbuch-Eintrag dokumentiert die Umstellung und Validierung des Dual-Venv-Setups im Media Web Viewer Projekt. Die Trennung von Haupt- und Testumgebung ist nun funktional und architekturell sauber umgesetzt.

---

### Umsetzung & Fortschritt
1. **Umstellung der Hauptanwendung auf .venv_core**
   - .venv_core ist jetzt die Standardumgebung für die App.
   - .venv_testbed bleibt für Tests erhalten.

2. **Skript-Anpassungen**
   - `run.sh`, `main.py`: Standardmäßig .venv_core.
   - `tests/run_gui_tests.py`: Nutzt weiterhin .venv_testbed.
   - `build.py`, `build_deb.sh`: Berücksichtigen beide Umgebungen.
   - `.gitignore`: Deckt beide Venvs ab.
   - `env_handler.py`, `check_environment.py`: Validieren gegen .venv_core.

3. **Validierung**
   - Dual-Venv Setup erfolgreich getestet.
   - Trennung von Produktions- und Testumgebung gewährleistet.
   - App kann wie gewohnt über `./run.sh` gestartet werden.
      - Zusätzlich existiert `venv_selenium` als separate Umgebung für automatisierte UI-Tests mit Selenium. Diese isoliert Testabhängigkeiten und verhindert Konflikte mit der Haupt- und Testumgebung.
      - Aktuell laufen keine Prozesse in einer venv-Umgebung (Prüfung mit `ps aux | grep venv`).
         - Die venv ist somit frei und kann problemlos von anderen Programmen oder IDE-Prozessen im Projekt genutzt werden.

---

### Vorteile
- Klare Trennung von Produktions- und Testumgebung.
- Saubere Architektur, weniger Konflikte bei Paketinstallationen.
- Einfachere Wartung und Debugging.

---

### ToDos
- Regelmäßige Überprüfung der Venvs auf Aktualität.
- Dokumentation der Dual-Venv-Strategie in INSTALL.md und DOCUMENTATION.md.
- Automatisierte Checks für beide Umgebungen in CI/CD.

---

**Letzte Aktualisierung:** 12. März 2026
