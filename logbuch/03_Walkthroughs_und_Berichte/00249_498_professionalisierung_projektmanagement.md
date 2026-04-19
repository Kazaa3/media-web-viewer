# Logbuch: Professionalisierung & Projektmanagement (2026-03-15)

## 1. Zielsetzung
- Das Projekt wird durch gezielte Maßnahmen im Bereich Projektmanagement und Professionalisierung auf ein nachhaltiges, teamfähiges und wartbares Niveau gehoben.

## 2. Maßnahmen zur Professionalisierung
- Einführung klarer Rollen (z.B. Maintainer, Reviewer, QA, DevOps)
- Nutzung von Issue- und Feature-Templates für strukturierte Aufgabenverfolgung
- Regelmäßige Review- und Testzyklen (z.B. Pull-Request-Reviews, automatisierte Test-Gates)
- Dokumentationspflicht für alle relevanten Änderungen (Logbuch, Changelog, Architektur)
- CI/CD-Pipeline mit Build-, Test- und Release-Gates
- Definition von Coding-Standards und Styleguides
- Einführung von Release- und Milestone-Planung
- Nutzung von Projektmanagement-Tools (z.B. GitHub Projects, Kanban, Milestones)

## 3. Vorteile
- Höhere Codequalität und Nachvollziehbarkeit
- Schnellere Fehlererkennung und -behebung
- Bessere Zusammenarbeit im Team
- Klare Verantwortlichkeiten und strukturierte Abläufe
- Nachhaltige Weiterentwicklung und Skalierbarkeit

## 4. ToDo
- Projektmanagement-Tools und Templates einführen/aktualisieren
- Review- und Testprozesse dokumentieren und etablieren
- Regelmäßige Retrospektiven und Verbesserungszyklen
- Onboarding-Dokumentation für neue Teammitglieder erstellen
- Styleguides und Coding-Standards im Projekt verankern

## 5. ToDo (Detailiert)
- Projektmanagement-Tools (z.B. GitHub Projects, Kanban-Boards) einführen oder aktualisieren, um Aufgaben, Fortschritt und Verantwortlichkeiten transparent zu machen.
- Issue- und PR-Templates für Bugs, Features und Reviews im Repository anlegen und pflegen.
- Review- und Testprozesse klar dokumentieren (z.B. Review-Checklisten, Test-Gates, Definition of Done) und im Team etablieren.
- Regelmäßige Retrospektiven (z.B. monatlich) durchführen, um Prozesse und Zusammenarbeit kontinuierlich zu verbessern.
- Onboarding- und Prozessdokumentation für neue Teammitglieder bereitstellen.
- Styleguides und Coding-Standards verbindlich machen und regelmäßig überprüfen.

## 6. Ausblick
- Die Professionalisierung ist ein fortlaufender Prozess und wird regelmäßig evaluiert und angepasst.
- Ziel ist ein robustes, transparentes und kollaboratives Entwicklungsumfeld.

## 7. Test-Ordnerstruktur & Test-Artefakte
- Die Teststruktur wird klar gegliedert, um Übersichtlichkeit und Wartbarkeit zu gewährleisten.
- **Empfohlene Ordnerstruktur:**
  - `tests/unit/` – Unit-Tests für einzelne Module/Funktionen
  - `tests/integration/` – Integrationstests für das Zusammenspiel mehrerer Komponenten
  - `tests/e2e/` – End-to-End-Tests (UI, Workflows, Selenium etc.)
  - `tests/performance/` – Performance- und Lasttests
  - `tests/mocks/` – Testdaten, Mock-Objekte, Fixtures
  - `tests/artifacts/` – Testartefakte wie Logfiles, Screenshots, Coverage-Reports
- **Test-Artefakte:**
  - Logfiles (z.B. `logs/test_run.log`)
  - Screenshots von fehlgeschlagenen UI-Tests (z.B. `artifacts/screenshots/`)
  - Coverage-Reports (z.B. `artifacts/coverage/`)
  - Test-Reports im JUnit- oder HTML-Format (z.B. für CI/CD)
- **Vorteile:**
  - Klare Trennung der Testarten und Artefakte
  - Schnellere Fehleranalyse und Nachvollziehbarkeit
  - Bessere Integration in CI/CD und automatisierte Auswertung
- **ToDo:**
  - Testordner nach Testart und Artefakt-Typ strukturieren
  - Artefakt-Ordner in .gitignore aufnehmen (wo sinnvoll)
  - Dokumentation der Teststruktur im Logbuch und README

## 8. Beispiel: Aktuelle Test-Artefakte im Projekt
- Im Ordner `tests/artifacts/reports/` liegt z.B. das Artefakt `performance_audit_results.json`.
- **Inhalt dieses Artefakts:**
  - Audit-Metadaten (Zeitstempel, Parser-Konfiguration, Scan-Verzeichnisse)
  - Detaillierte Statistiken zu getesteten Medienformaten (z.B. .ogg, .flac, .wav, .wma, .m4a)
  - Für jedes Format: Anzahl, Erfolgsrate, durchschnittliche und Gesamtdauer, verwendete Parser
- **Nutzen:**
  - Dokumentiert die Performance- und Erfolgsstatistik der Medienparser
  - Grundlage für Analyse und Optimierung der Medienunterstützung
- **Hinweis:**
  - Weitere Artefakte (z.B. Screenshots, Coverage-Reports, Logfiles) können in anderen Unterordnern wie `screenshots/`, `coverage/` oder `logs/` liegen und werden analog verwaltet.

### Weitere aktuelle Test-Artefakte
- `tests/reference_screenshots/`: Enthält Referenz-Screenshots für UI- und Visual-Regression-Tests, z.B.:
  - test_abase_ref.png
  - test_bplayer_ref.png
  - test_debug_and_db_ref.png
  - test_library_ref.png
  - test_modals_ref.png
  - test_options_ref.png
  - test_playlist_ref.png
  - test_teststab_ref.png
  - test_videoplayer_ref.png
- `tests/artifacts/reports/performance_audit_results.json`: Performance- und Parserstatistiken (siehe oben)
- `tests/assets/screenshots/`, `tests/assets/logs/`, `tests/assets/reference/`: Platzhalter für weitere Artefakte (z.B. Screenshots, Logfiles, Referenzdaten)
- `.gitkeep`-Dateien sichern die Verzeichnisstruktur für Artefakte, auch wenn noch keine Dateien vorhanden sind.

Diese Artefakte dienen der Nachvollziehbarkeit, Fehleranalyse und Qualitätssicherung im Testprozess.

## 9. GitHub Actions: Firefox/Geckodriver Fehler & Fix

**Problem:**
- Bei GitHub Actions (Ubuntu 22.04/24.04) kommt es häufig zu Fehlern mit Firefox/Geckodriver:
  - Startprobleme/Hänger, wenn Firefox als Snap/Flatpak läuft (Standard auf Ubuntu)
  - Geckodriver/ASLR/Clang/ASAN-Crashes (z.B. Segfaults, Kernel-Inkompatibilität)

**Workarounds & Fixes:**
- **ASLR/Clang/ASAN-Fix:**
  - Vor dem Testlauf in der Workflow-Datei die Kernel-Entropie für Address Space Layout Randomization (ASLR) reduzieren:
    ```yaml
    - name: Fix kernel mmap rnd bits (ASLR workaround)
      run: sudo sysctl vm.mmap_rnd_bits=28
    ```
  - Hintergrund: Ältere LLVM/Clang-Versionen (z.B. in Ubuntu 22.04) sind nicht kompatibel mit der hohen ASLR-Entropie neuerer GitHub-Runner-Kernel. Siehe [actions/runner-images#9491](https://github.com/actions/runner-images/issues/9491).

- **Geckodriver-Version aktuell halten:**
  - Immer die neueste stabile Version verwenden, z.B. mit der Action:
    ```yaml
    - uses: browser-actions/setup-geckodriver@latest
      with:
        token: ${{ secrets.GITHUB_TOKEN }}
    ```

- **Firefox im Container (Snap/Flatpak):**
  - Setze `TMPDIR` auf ein Verzeichnis, das sowohl Firefox als auch Geckodriver beschreiben können:
    ```yaml
    - run: mkdir -p $HOME/tmp
    - run: export TMPDIR=$HOME/tmp
    ```
  - Oder nutze die Option `--profile-root` für Geckodriver.
  - Alternativ: Firefox als .deb von mozilla.org installieren und Snap/Flatpak vermeiden.

**Quellen & Details:**
- [actions/runner-images#9491](https://github.com/actions/runner-images/issues/9491)
- [Geckodriver Releases](https://github.com/mozilla/geckodriver/releases)
- [Geckodriver Usage: Container](https://firefox-source-docs.mozilla.org/testing/geckodriver/Usage.html#Running-Firefox-in-an-container-based-package)

**Empfehlung:**
- Diese Workarounds in der CI/CD-Pipeline dokumentieren und als Standard für Firefox/Geckodriver-Tests unter GitHub Actions übernehmen.
- Bei Änderungen an den GitHub-Runner-Images oder neuen Firefox/Geckodriver-Releases regelmäßig prüfen, ob die Workarounds noch nötig sind.
