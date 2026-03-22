---
Build & Test Artifacts: Centralization Strategy

Ziel: Alle Build- und Test-Artefakte entstehen nur an einem zentralen Ort (z.B. build/), um Übersicht, Cleanup und CI-Integration zu erleichtern.

Empfohlene Orte für Artefakte:
- build/: Alle Build-Outputs (Debian-Pakete, Executables, Wheel/Sdist, etc.)
- build/test-reports/: Test-Reports (JUnit XML, HTML, Coverage)
- build/logs/: Build- und Test-Logs
- build/screenshots/: E2E/Selenium Screenshots

Best Practices:
- Keine Artefakte im Projekt-Root, src/, scripts/ oder tests/ ablegen.
- Alle temporären und finalen Artefakte werden in build/ und Unterordnern erzeugt.
- CI/CD und Cleanup-Skripte greifen nur auf build/ zu.

Dokumentation:
- walkthrough.md und TEST_SUITE_SUMMARY.md beschreiben die Artefakt-Orte und Cleanup-Strategie.
- E2E/Selenium-Screenshots werden in build/screenshots/ abgelegt und im Test-Report referenziert.
- Logs und Reports werden zentral in build/logs/ und build/test-reports/ gespeichert.

Tipp:
- Für neue Artefakte immer build/ als Ziel wählen und in der Doku vermerken.

---

Automated Code Quality Cleanup & Test Finalization

- Tests wurden in die Tier-Struktur konsolidiert und das tests/-Verzeichnis bereinigt.
- Lint-Audit durchgeführt: 323 Fehler in src/core/main.py und infra/build_system.py identifiziert.
- autopep8 eingesetzt, um 300+ Formatierungs- und Whitespace-Probleme automatisch zu beheben.
- Fokus auf verbleibende High-Impact-Lint-Fehler: fehlende Imports, Typ-Mismatches, redundante Imports.
- monitor_utils-Import in infra/build_system.py bereinigt (nur noch lokal in _run_command).
- _extract_key_from_obj-Helper in src/core/main.py implementiert.
- Finales Linting und PEP8-Compliance für Milestone 7 erreicht.
- install_latest_deb.sh-Skript hinzugefügt für schnelle Installation des neuesten Debian-Pakets.
- Ziel: Clean, robust, und PEP8-konformer Code für alle Kernmodule.
