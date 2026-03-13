---
Logbuch-Eintrag: Foolproof Build & Fragment Management – Milestone 4

Datum: 13. März 2026

Status & Maßnahmen:
- venv-Transition für main.py und Kernmodule abgeschlossen.
- Fokus auf Build-Hygiene im develop-Branch: Verhindern von Build-Fragmenten im Git-Repo.
- .gitignore und build_deb.sh auf Fragment-Leaks geprüft und Regeln verschärft; alle Build-Artefakte inkl. root-level .deb und Debian-Staging werden jetzt abgedeckt.
- infra/build_system.py mit robuster clean-Logik erweitert, die sämtliche Build-Fragmente entfernt und vor jedem Build einen sauberen Zustand sicherstellt.
- implementation_plan.md aktualisiert, um die neue Housekeeping-Strategie zu dokumentieren.
- Cleanup durch Build-Tests verifiziert: Keine Residual-Fragmente nach Build.
- Nächste Schritte: Automatisierte Fragment-Prüfung im CI, Dokumentation der Fragment-Strategie, Monitoring für neue Artefakttypen.

---
Milestone 3: Python Environment Transition (venv focus)

Wir haben die primäre Projektumgebung erfolgreich von Conda auf Python's native venv umgestellt. Dies sorgt für mehr Stabilität, bessere Versionskontrolle und Unabhängigkeit von externen Environment-Managern.

Key Changes
1. Backend Recommendation Logic
main.py gibt jetzt eine strukturierte Empfehlung für venv_core zurück.

Alt: Empfahl Conda "p14".
Neu: Empfiehlt venv_core mit Python 3.14.2 für maximale Stabilität.

json
{
    "recommended_environment": {
        "name": "venv_core",
        "type": "venv",
        "python_version": "3.14.2",
        "reason": "Eigene venv für main.py empfohlen"
    }
}

2. Startup Validation & Warnings
env_handler.py erkennt jetzt Conda-Umgebungen und gibt eine Warnung aus:

WARNING
Conda-Umgebung erkannt. Wechsel zu 'venv_core' wird für maximale Stabilität und Unabhängigkeit empfohlen.

3. Automated Management Scripts
manage_venvs.py: Markiert .venv_core im Status-Überblick mit einem ⭐ RECOMMENDED-Tag.
run.sh: Priorisiert system python3.14 für Environment-Erstellung, nutzt Conda p14 nur als Legacy-Fallback.

4. Documentation Overhaul
README.md: "From Source" nach oben verschoben und als ⭐ EMPFOHLEN markiert.
INSTALL.md: Installationsmethoden neu organisiert, Venv-basierte Einrichtung hervorgehoben und Conda als "Alternative/Legacy" markiert.

---
Milestone 4: "Foolproof" Build & Fragment Management

Wir haben eine "Zero-Leak" Build-Strategie implementiert, um sicherzustellen, dass der Entwicklungsbaum sauber bleibt und Build-Artefakte nie das Source-Verzeichnis kontaminieren.

1. Isolated Build Isolation
build_deb.sh staged jetzt alle Dateien in einem temporären /tmp-Verzeichnis und nutzt präzise rsync-Exclusions, um Junk aus dem Paket zu halten.

Zero-Leak: Schließt .git, .github, .venv und alle Test-Ordner vom finalen Produktionspaket aus.
Zentralisiertes Staging: Alle finalen .deb-Artefakte werden jetzt ins root build/-Verzeichnis exportiert, nicht mehr ins Projekt-Root.

2. Centralized Cleanup
build_system.py bietet jetzt einen umfassenden Cleanup-Befehl:

python infra/build_system.py --clean: Schnelles Clean von Cache und pycache.
python infra/build_system.py --clean-all: Tiefenreinigung inkl. build/, dist/ und alten .deb/.exe-Artefakten.

3. Continuous Integration für develop
Der Develop CI-Workflow wurde erweitert:

- Führt alle Unit- und Integrationstests aus.
- Validiert den Build-Prozess durch einen Test-Build des Debian-Pakets.
- Räumt automatisch auf, um die CI-Umgebung konsistent zu halten.

4. Refined .gitignore
.gitignore mit spezifischen Regeln für Build-Fragmente aktualisiert:

text
packaging/opt/*
infra/packaging/opt/*
**/pkg/
**/deb_staging/

Schützt jetzt kritische Scripts in infra/, ignoriert aber korrekt Legacy-Dateien im Root.

---
Test Suite & Automation Strategy Rethink (Ergänzung)

1. Test Classification
- Tier 1: Unit & Mock (Fast)
  - Ziel: Logik und interner Zustand prüfen.
  - Regeln: Keine externen Abhängigkeiten, Mocks verwenden.
  - Ausführung: python infra/build_system.py --test unit
  - CI-Trigger: Jeder Push.
  - Beispiele: tests/unit/test_performance_probes.py, tests/unit/test_bottle_health_latency.py

- Tier 2: Technology & Integration (Medium)
  - Ziel: Interaktion mit echten Systemtools (FFmpeg, VLC, SQLite).
  - Ausführung: python infra/build_system.py --test integration
  - CI-Trigger: Push auf develop und main, sowie PRs.
  - Beispiele: tests/integration/test_installed_packages_ui.py, tests/integration/test_environment_packages_fallback.py

- Tier 3: E2E & Release Validation (Heavy)
  - Ziel: Gesamtsystemvalidierung (GUI, Installation).
  - Ausführung: python infra/build_system.py --test e2e
  - CI-Trigger: PR auf main und Pushes auf main (Tags).
  - Beispiele: tests/e2e/test_ui_session_stability.py

2. Branching & CI/CD Strategy
- develop Branch: Aktive Entwicklung, führt Tier 1 & 2 Tests aus.
- main Branch: Stabile Releases, führt alle Tiers und validiert die gesamte Pipeline.
- PRs: Lösen Integration und E2E Tests aus.

3. Milestone 2: Modernization & Automation [DONE]
- tests/ refactored in unit, integration und e2e.
- build_system.py unterstützt Tier-basierte Testausführung.
- develop vs main Workflow-Trennung in GitHub Actions.
- .deb-Purge-Fragmente mit postrm und staged builds in /tmp gefixt.
- Testabdeckung und Testlaufzeiten im CI-Log dokumentiert.

4. Milestone 3: Python Environment Stability (venv transition)
- Ziel: Empfehlung von Conda auf venv umgestellt für mehr Stabilität und Unabhängigkeit.
- Startup-Logs zeigen venv-Empfehlung.
- manage_venvs.py prüft, ob venv-python verfügbar ist und bevorzugt diesen.
- env_handler.py loggt Warnung bei CONDA_PREFIX.
- README.md und INSTALL.md: venv als "EMPFOHLEN", Conda als "Alternative/Legacy".

5. Milestone 4: "Foolproof" Build & Fragment Management
- .gitignore deckt Build-Fragmente ab und schützt kritische Scripts in infra/.
- build_deb.sh staged alle Dateien in /tmp, nutzt präzise rsync-Exclusions.
- build_system.py bietet --clean und --clean-all für schnelle und tiefe Reinigung.
- CI-Workflow (ci-develop.yml) führt Unit- und Integrationstests aus, validiert Build und räumt nach Build automatisch auf.
- postrm-Skripte und staged builds verhindern .deb-Purge-Fragmente.
- Test- und Build-Logs werden zentral in build/logs/ gespeichert.
- Verifikation: python infra/build_system.py --clean sorgt für einen sauberen Tree; CI prüft, dass keine Fragmente im develop-Branch landen.

6. Milestone 5: Testing Maturity & Windows Build (Review Ergänzung)

- build_exe.sh refaktoriert: Windows-Executables werden ins root build/-Verzeichnis exportiert, Staging-Fragmente werden strikt im build/-Ordner isoliert und bereinigt.
- build_system.py unterstützt jetzt das --report-Flag für alle Test-Tiers:
  - JUnit XML: Standardisierte JUnit-XML-Dateien werden in build/test-reports/ erzeugt, CI-Integration vereinfacht.
  - Terminal Summary: Automatischer Parser gibt eine Zusammenfassung (Total, Passed, Failed, Duration) direkt im Terminal aus.
- TIERS.md erstellt: Klare Guidelines für Unit-, Integration- und E2E-Tests, sorgt für konsistente Klassifizierung und Entwicklerfokus.
- format_utils.py erweitert:
  - Audio: .ac3, .mka, .dts, .dtshd, .ra, .rm
  - Video: .vob, .dat, .divx, .xvid, .m2t, .mts, etc.
  - Disk Images: .toast, .ccd, .daa
- Test- und Build-Logs werden zentral in build/logs/ gespeichert.
- CI prüft, dass Windows-Builds und Testreports korrekt erzeugt und keine Fragmente im develop-Branch landen.

---
Milestone 7: Build Performance & Resilience

Goal: Professionelles Build-Monitoring und Zuverlässigkeit durch Performance-Messung und Hang-Prävention.

Proposed Changes
- Build System (infra/build_system.py):
  - Performance Tracking: Timer-Context-Manager misst die Dauer jeder Build-Phase.
  - Resilience: Timeout-Parameter (default 600s) für alle _run_command-Aufrufe, verhindert endlose Hänger.
  - Reporting: "Total Build Time" und Phase-Dauer werden im finalen Build-Summary ausgegeben.
- Build Scripts (infra/build_deb.sh, infra/build_exe.sh):
  - Interne Timestamp-Logs für detaillierte Performance-Daten auf Skript-Ebene.

Verification Plan
- Performance: Vollständigen Build ausführen und prüfen, dass "Build Time"-Summary erscheint.
- Resilience: Test-Build mit absichtlich langem sleep-Befehl ausführen und prüfen, dass Timeout korrekt greift.

---
Walkthrough Review (Ergänzung)

Milestone 3: Python Environment Transition (venv focus)
- Empfehlung für venv_core (Python 3.14.2) in main.py implementiert.
- env_handler.py erkennt Conda und gibt Warnung aus, empfiehlt venv_core.
- manage_venvs.py markiert .venv_core als ⭐ RECOMMENDED.
- run.sh priorisiert system python3.14, Conda nur als Legacy-Fallback.
- README.md und INSTALL.md: venv als "EMPFOHLEN", Conda als "Alternative/Legacy".
- Startup-Logs zeigen venv-Empfehlung.
- Automatisierte Tests prüfen, ob venv aktiv ist und Warnungen korrekt erscheinen.

Milestone 4: Foolproof Build & Fragment Management
- build_deb.sh staged alle Dateien in /tmp, nutzt präzise rsync-Exclusions (.git, .github, .venv, tests).
- Alle .deb-Artefakte werden ins build/-Verzeichnis exportiert, nicht ins Projekt-Root.
- build_system.py bietet --clean und --clean-all für schnelle und tiefe Reinigung.
- CI-Workflow (ci-develop.yml) führt Unit- und Integrationstests aus, validiert Build und räumt nach Build automatisch auf.
- .gitignore deckt Build-Fragmente ab und schützt kritische Scripts in infra/.
- postrm-Skripte und staged builds verhindern .deb-Purge-Fragmente.
- Test- und Build-Logs werden zentral in build/logs/ gespeichert.
- Verifikation: python infra/build_system.py --clean sorgt für einen sauberen Tree; CI prüft, dass keine Fragmente im develop-Branch landen.
