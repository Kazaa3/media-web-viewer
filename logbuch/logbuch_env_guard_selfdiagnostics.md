# logbuch_env_guard_selfdiagnostics.md

## Environment Guard & Self-Diagnostics Refactor

**Datum:** 29. März 2026

---

### Zielsetzung

- Behebt das Problem `ModuleNotFoundError: psutil` beim Start außerhalb der venv.
- Stellt sicher, dass die Anwendung IMMER im richtigen (unified) .venv oder .venv_run läuft, bevor Third-Party-Module geladen werden.
- Fügt eine Self-Diagnostics-Routine hinzu, die bei Umgebungsfehlern sofort Klarheit über Python-Version, Executable und venv-Status gibt.

---

### Wichtige Anpassungen

#### 1. Sofortiger Environment Guard
- Die Funktion `ensure_stable_environment()` steht jetzt ganz oben in `main.py` (direkt nach den Basis-Imports).
- Vor jedem Import von Drittanbieter-Bibliotheken prüft und erzwingt der Guard die Ausführung in `.venv` (bevorzugt) oder `.venv_run`.
- Bei Abweichung wird automatisch re-executed oder ein Fehler ausgegeben.

#### 2. Self-Diagnostics
- Die neue Funktion `log_self_diagnostics()` gibt im Fehlerfall sofort folgende Infos aus:
  - Python-Version
  - Executable-Pfad
  - sys.prefix
  - Projekt-Root & Arbeitsverzeichnis
- Wird bei jedem Guard-Fehlschlag oder Re-Exec-Problem aufgerufen.

#### 3. Import-Isolation
- Alle Imports von Modulen wie `psutil`, `eel`, `gevent` etc. erfolgen erst NACH erfolgreichem Environment-Check.
- Dadurch werden Import-Fehler und inkonsistente Zustände vermieden.

---

### Verifikationsplan

- **Automatisiert:**
  - Syntax-Check für `main.py`.
  - Start mit `/usr/bin/python3 src/core/main.py` prüft, ob korrekt in `.venv` gewechselt wird.
- **Manuell:**
  - Sicherstellen, dass der `psutil`-Fehler verschwindet, wenn aus einer Nicht-venv gestartet wird.
  - Terminalausgabe "STDOUT: [Guard] Switching Environment..." erscheint bei Re-Execution.

---

**Fazit:**

Mit dieser Umstrukturierung ist die Anwendung robust gegen Umgebungsfehler und liefert im Problemfall sofort verwertbare Diagnosedaten. Die Imports sind sauber isoliert und die venv-Nutzung ist garantiert.

*Letzte Änderung: 29.03.2026*
