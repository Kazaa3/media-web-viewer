# 7. Test-Ordnerstruktur & Test-Artefakte

Die Teststruktur wird klar gegliedert, um Übersichtlichkeit und Wartbarkeit zu gewährleisten.

**Empfohlene Ordnerstruktur:**
- `tests/unit/` – Unit-Tests für einzelne Module/Funktionen
- `tests/integration/` – Integrationstests für das Zusammenspiel mehrerer Komponenten
- `tests/e2e/` – End-to-End-Tests (UI, Workflows, Selenium etc.)
- `tests/performance/` – Performance- und Lasttests
- `tests/mocks/` – Testdaten, Mock-Objekte, Fixtures
- `tests/artifacts/` – Testartefakte wie Logfiles, Screenshots, Coverage-Reports

**Test-Artefakte:**
- Logfiles (z.B. `logs/test_run.log`)
- Screenshots von fehlgeschlagenen UI-Tests (z.B. `artifacts/screenshots/`)
- Coverage-Reports (z.B. `artifacts/coverage/`)
- Test-Reports im JUnit- oder HTML-Format (z.B. für CI/CD)

**Vorteile:**
- Klare Trennung der Testarten und Artefakte
- Schnellere Fehleranalyse und Nachvollziehbarkeit
- Bessere Integration in CI/CD und automatisierte Auswertung

**ToDo:**
- Testordner nach Testart und Artefakt-Typ strukturieren
- Artefakt-Ordner in .gitignore aufnehmen (wo sinnvoll)
- Dokumentation der Teststruktur im Logbuch und README

---

# 8. Beispiel: Aktuelle Test-Artefakte im Projekt

Im Ordner `tests/artifacts/reports/` liegt z.B. das Artefakt `performance_audit_results.json`.

**Inhalt dieses Artefakts:**
- Audit-Metadaten (Zeitstempel, Parser-Konfiguration, Scan-Verzeichnisse)
- Detaillierte Statistiken zu getesteten Medienformaten (z.B. .ogg, .flac, .wav, .wma, .m4a)
- Für jedes Format: Anzahl, Erfolgsrate, durchschnittliche und Gesamtdauer, verwendete Parser

**Nutzen:**
- Dokumentiert die Performance- und Erfolgsstatistik der Medienparser
- Grundlage für Analyse und Optimierung der Medienunterstützung

**Hinweis:**
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
