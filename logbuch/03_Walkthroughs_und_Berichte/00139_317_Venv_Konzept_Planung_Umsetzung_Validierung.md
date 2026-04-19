# 4-Venv Konzept – Planung, Umsetzung & Validierung

## Ziel
Dieser Logbuch-Eintrag dokumentiert die Recherche, Planung, Implementierung und Validierung des 4-Venv-Konzepts im Media Web Viewer Projekt. Die Infrastruktur ist nun architekturell sauber getrennt und bereit für professionelle Workflows.

---

### Schritte & Fortschritt
1. **Recherche und Planung**
   - Analyse der Anforderungen für Core, Testbed, Dev und Build.
   - Definition der Aufgaben und Abhängigkeiten pro Umgebung.

2. **Implementierungsplan**
   - Initialisierung der vier Umgebungen: `.venv_core`, `.venv_testbed`, `.venv_dev`, `.venv_build`.
   - Installation der spezialisierten Abhängigkeiten in den jeweiligen venvs.
   - Saubere Neuerstellung zur Vermeidung von Pfadkonflikten.

3. **Skript-Anpassungen**
   - `run.sh`, `main.py`: Nutzen `.venv_core`.
   - `tests/run_gui_tests.py`: Nutzt `.venv_testbed`.
   - `run_all_tests.sh`: Nutzt `.venv_dev` für Backend-Tests.
   - `build_deb.sh`: Schließt alle venvs im finalen Paket aus.
   - `.gitignore`: Deckt alle venv-Pfade ab.

4. **Validierung**
   - 4-Venv Setup erfolgreich getestet.
   - Automatische Fallbacks in den Skripten.
   - Infrastruktur sauber getrennt.

---

### Struktur & Zweck der Umgebungen
- `.venv_core`: Schlanke App-Laufzeit (Standard für run.sh)
- `.venv_testbed`: Testpipeline für Backend- und Integrationstests
- `.venv_dev`: Für Backend-Tests und Entwicklungstools (pytest, linting, black)
- `.venv_build`: Für Packaging (pyinstaller)

---

### Vorteile
- Klare Trennung von Laufzeit, Test, Entwicklung und Build.
- Weniger Konflikte, bessere Wartbarkeit, professionelle Workflows.
- Automatisierte Checks und Fallbacks.

---

### ToDos
- Dokumentation des 4-Venv Setups in INSTALL.md, DOCUMENTATION.md und Walkthrough.
- Regelmäßige Überprüfung der venvs auf Aktualität.
- Automatisierte Checks für alle Umgebungen in CI/CD.

---

**Letzte Aktualisierung:** 12. März 2026

# Erweiterung: 6-Env-Konzept

Neben den vier Hauptumgebungen können weitere spezialisierte venvs sinnvoll sein:

- `.venv_selenium`: Separate Umgebung für Selenium/UI-Tests (falls nicht in testbed integriert)
- `.venv_ci`: Spezielle Umgebung für CI/CD-Jobs (z.B. GitHub Actions)
- `.venv_docs`: Umgebung für Dokumentations- und Sphinx-Builds

Damit ergibt sich ein flexibles 6-Env-Modell:

| Umgebung       | Zweck                                  |
|---------------|----------------------------------------|
| .venv_core    | App-Laufzeit (run.sh, main.py)         |
| .venv_testbed | Testpipeline für Backend- und Integrationstests |
| .venv_dev     | Backend-Tests, Linting, Entwicklung    |
| .venv_build   | Packaging (pyinstaller)                |
| .venv_selenium| Separate Umgebung für Selenium/UI-Tests         |
| .venv_ci      | CI/CD-Jobs, Automatisierung            |
| .venv_docs    | Dokumentations-Builds (optional)       |

Vorteile:
- Maximale Isolation und Flexibilität für alle Workflows
- Weniger Konflikte, bessere Wartbarkeit
- Professionelle Infrastruktur für Entwicklung, Test, Build, CI und Doku

ToDos:
- Dokumentation des 6-Env-Modells in INSTALL.md, DOCUMENTATION.md und Walkthrough
- Automatisierte Checks für alle Umgebungen in CI/CD
- Regelmäßige Überprüfung und Pflege der venvs

---

# Zukunfts-Analyse: Sollte selenium aus .venv_testbed entfernt werden?
# Aktuell ist selenium sowohl in .venv_testbed als auch in .venv_selenium gelistet.
# Empfehlung: Für maximale Isolation und Klarheit sollte selenium nur in .venv_selenium installiert werden.
# .venv_testbed bleibt dann rein für Backend- und Integrationstests ohne UI.
# Dies verhindert Paketkonflikte und sorgt für saubere Testumgebungen.
# ToDo: Prüfen, ob Tests und Skripte entsprechend angepasst werden können und ob Abhängigkeiten getrennt werden müssen.

---

# Paketübersicht pro Umgebung

| Umgebung       | Typische Pakete/Tools                          |
|---------------|------------------------------------------------|
| .venv_core    | eel, bottle, sqlite, app-spezifische Pakete     |
| .venv_testbed | pytest, coverage, test-utils, mock, selenium    | Backend-Tests
| .venv_dev     | black, ruff, mypy, pytest, dev-tools            |
| .venv_build   | pyinstaller, setuptools, wheel, build-tools     | Packaging
| .venv_selenium| selenium, webdriver-manager, browser-driver     | UI-Tests
| .venv_ci      | ci-spezifische Tools (github-actions, tox, etc.)| 
| .venv_docs    | sphinx, mkdocs, docutils, doku-tools            |
| /venv         | ggf. legacy oder systemweite Umgebung           |

Hinweis:
- Es ist empfehlenswert, die venv frei zu lassen, falls jemand im Projekt arbeitet. Die jeweils aktive venv ist der Stand, der für App, Tests oder Build gewählt wird und sollte nicht von parallelen Prozessen blockiert werden.
- Die Trennung sorgt für saubere, reproduzierbare Workflows und verhindert Konflikte.

# Hinweis: Legacy-Module und six-Kompatibilität
- Einige komplexere Module (z.B. ältere Parser, spezielle Medienformate) sind nicht mit six kompatibel, da sie auf Python-Legacy-Code oder veraltete APIs setzen.
- Bei Migration auf reine Python-3-Umgebungen kann es zu Problemen kommen, wenn diese Module weiterhin Python-2-Kompatibilität oder six voraussetzen.
- Empfehlung: Legacy-Module identifizieren, Kompatibilität prüfen und ggf. refactoren oder ersetzen, um eine saubere Python-3-Basis zu gewährleisten.
- ToDo: Liste der betroffenen Module erstellen und Migrationsstrategie planen.

# Analyse: six-Paket für ISO-Support
- Das six-Paket wird für isoparser benötigt und ist aktuell in requirements.txt und DEPENDENCIES.md gelistet.
- six>=1.16.0 ist mit Python 3 kompatibel, wird aber primär für Python 2/3-Kompatibilität genutzt.
- Für reine Python-3-Umgebungen kann auf six verzichtet werden, sofern isoparser keine Abhängigkeit mehr hat.
- Empfehlung: ISO-Support (isoparser, pycdlib, six) ggf. in eigene env auslagern, um Paketkonflikte zu vermeiden.
- ToDo: Prüfen, ob isoparser ohne six funktioniert und ggf. auf reines Python 3 wechseln.

# Validierung der six-Kompatibilität
- Die Aussage ist teilweise korrekt: Das six-Paket ist für isoparser (ISO-Support) erforderlich und sorgt für Python 2/3-Kompatibilität. Die meisten modernen Module im Projekt sind mit six und Python 3 kompatibel.
- Es gibt keine Hinweise auf komplexe Parser oder Medienformate im aktuellen Code, die explizit nicht mit six kompatibel sind oder auf Python-Legacy-Code setzen. Die Legacy-Problematik betrifft vor allem sehr alte oder nicht gepflegte Module, die Python-2-APIs nutzen – solche sind im aktuellen Projekt nicht prominent vertreten.
- Empfehlung: Die Migration auf reine Python-3-Umgebungen ist möglich, solange alle Abhängigkeiten (insbesondere isoparser) mit Python 3 und six kompatibel sind. Legacy-Module sollten identifiziert und ggf. refactored werden, aber im aktuellen Code gibt es keine akuten Konflikte.

# Key Changes: 5-Venv Modell und Testarchitektur
1. Script Correction
- Das run_gui_tests.py-Skript wurde auf den korrekten .venv_selenium-Interpreter zurückgestellt. Browser-basierte Tests sind damit sauber von der allgemeinen Testpipeline isoliert.

2. Documentation Updates
- DOCUMENTATION.md: Aktualisiert, um das 5-Venv-Konzept und Snapshots zu dokumentieren.
- TEST_DOCUMENTATION.md: Architektur-Tabelle erweitert, um die Trennung Selenium/Testbed zu zeigen.
- implementation_plan.md: Das 5-Venv-Modell als Projektstandard formalisiert.

3. Verification of Internal Tests
- Untersuchung des integrierten "Test"-Tabs (main.py):
  - Allgemeine Tests werden mit sys.executable ausgeführt (meist .venv_core).
  - Der interne GUI-Test-Trigger ist aktuell ein Platzhalter und verweist auf externe Automatisierung.

Summary of Completed Tasks
- Environment Refinement: 5-Venv Model implemented.
- Selenium Automation isolated to .venv_selenium.
- Testbed consistency ensured.
- All relevant documentation synchronized.
- Das System ist jetzt robust isoliert und ermöglicht saubere Entwicklung und automatisierte Verifikation.

# Konzept: Mehrere venvs und Python-Instanzen
- Wenn mehrere venvs existieren, kann jede Umgebung einen eigenen Python-Interpreter und eigene Paketbasis haben – sie sind wirklich getrennt.
- Die Isolation ist vollständig, solange jede venv separat aktiviert und genutzt wird.
- Mehrere venvs ermöglichen parallele Python-Instanzen mit unterschiedlichen Abhängigkeiten.
- Man kann mehrere Python-Prozesse gleichzeitig laufen lassen, z.B. für App, Tests, Build, Doku – jeder nutzt seine eigene venv.
- Das sorgt für maximale Flexibilität und verhindert Konflikte zwischen Paketen und Versionen.
- Die Trennung ist echt, nicht nur „mehrmals Python laufen lassen“, sondern wirklich separate Umgebungen und Interpreter.

# Hinweis: UI-Trace-Logs in VS Code
- Die UI-Trace-Logs erscheinen in VS Code, weil das Backend (main.py) und die App im aktuellen Workspace laufen und ihre Log-Ausgaben (z.B. Tab-Wechsel, Sichtbarkeitsänderungen, Events) direkt ins Logfile oder die Konsole schreiben.
- VS Code zeigt diese Logs entweder im Terminal, Output-Panel oder über eine Logdatei an.
- Aktionen des Copilot-Agents (z.B. Patch, Recherche, Test) starten keine eigenen Python-Prozesse – es wird direkt mit den Dateien und der Umgebung gearbeitet, die bereitgestellt wird.
- Die Logs stammen von der laufenden App, nicht von internen Prozessen des Agents.

